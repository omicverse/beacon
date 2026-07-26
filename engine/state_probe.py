"""The oracle: decide contract claims by execution, not by assertion.

Every ``requires`` / ``produces`` claim a synthesizer proposes is a statement
about what a call reads and writes. This module turns each such statement into
an experiment whose outcome can refute it.

Two asymmetric probes
---------------------
``produces`` is decided by **observation**: snapshot the state, run the call,
diff. A key that appears is produced.

``requires`` is decided by **removal**, not observation. A function may read a
key incidentally, or a key may merely happen to be present; neither
establishes dependence. The only evidence that ``f`` requires ``k`` is that
deleting ``k`` makes ``f`` fail. Observation over-admits; removal does not.

Both probes need a *fresh* subject per trial, because a probe mutates state.
The caller supplies ``make_subject`` rather than a subject, so every trial
starts from the same fixture.

State models are pluggable
--------------------------
"What state a call touches" is library-specific. AnnData threads one mutable
container through every call; ``pymatgen`` returns new objects; a DFT wrapper
writes files. An adapter declares snapshot and removal for its shape, and the
probes are written against the adapter rather than against AnnData. See
``STATE_MODELS.md``.
"""

from __future__ import annotations

import copy
import multiprocessing
import os
import signal
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Protocol

Snapshot = dict[str, set[str]]


# --------------------------------------------------------------------------
# Adapters
# --------------------------------------------------------------------------

class StateAdapter(Protocol):
    """How to observe, and how to remove, for one library shape."""

    name: str

    def snapshot(self, subject: Any) -> Snapshot:
        """Container -> set of keys currently present."""

    def strip(self, subject: Any, container: str, key: str) -> bool:
        """Remove ``key``; return False if it was not there to remove."""


class AnnDataAdapter:
    """The seven AnnData containers the decorator's maps are restricted to."""

    name = "anndata"
    CONTAINERS = ("layers", "obsm", "obsp", "uns", "var", "obs", "varm")

    def snapshot(self, subject: Any) -> Snapshot:
        out: Snapshot = {}
        for c in self.CONTAINERS:
            holder = getattr(subject, c, None)
            if holder is None:
                continue
            try:
                out[c] = set(map(str, holder.keys()))
            except Exception:
                # var/obs are DataFrames: columns are the keys
                try:
                    out[c] = set(map(str, holder.columns))
                except Exception:
                    out[c] = set()
        return out

    def strip(self, subject: Any, container: str, key: str) -> bool:
        holder = getattr(subject, container, None)
        if holder is None:
            return False
        try:
            if key in holder:
                del holder[key]
                return True
        except Exception:
            pass
        return False


class AttrsAdapter:
    """Object-centric libraries: pymatgen ``Structure``, RDKit ``Mol``, ASE ``Atoms``.

    There is no central mutable container, so "state" is the public attribute
    surface of the subject (and of the returned object, which the caller passes
    back in as the post-state). Removal is ``delattr``, which fails on slotted
    or read-only properties — those keys are reported unremovable rather than
    silently treated as not-required.
    """

    name = "attrs"

    def snapshot(self, subject: Any) -> Snapshot:
        names = {n for n in dir(subject)
                 if not n.startswith("_") and not callable(getattr(subject, n, None))}
        return {"attrs": names}

    def strip(self, subject: Any, container: str, key: str) -> bool:
        if container != "attrs":
            return False
        try:
            delattr(subject, key)
            return True
        except Exception:
            return False


class NamespaceAdapter:
    """Stateless / functional libraries: the subject is an exec namespace."""

    name = "namespace"

    def snapshot(self, subject: Any) -> Snapshot:
        return {"names": {k for k in dict(subject) if not k.startswith("_")}}

    def strip(self, subject: Any, container: str, key: str) -> bool:
        if container == "names" and key in subject:
            del subject[key]
            return True
        return False


class FilesystemAdapter:
    """Wrapper libraries whose effect is files (atomate2, VASP/QE drivers)."""

    name = "filesystem"

    def __init__(self, root: str):
        self.root = root

    def snapshot(self, subject: Any) -> Snapshot:
        found: set[str] = set()
        for dirpath, _dirs, files in os.walk(self.root):
            for f in files:
                found.add(os.path.relpath(os.path.join(dirpath, f), self.root))
        return {"files": found}

    def strip(self, subject: Any, container: str, key: str) -> bool:
        path = os.path.join(self.root, key)
        if container == "files" and os.path.exists(path):
            os.remove(path)
            return True
        return False


ADAPTERS: dict[str, Callable[..., StateAdapter]] = {
    "anndata": AnnDataAdapter,
    "attrs": AttrsAdapter,
    "namespace": NamespaceAdapter,
    "filesystem": FilesystemAdapter,
}


# --------------------------------------------------------------------------
# Probes
# --------------------------------------------------------------------------

@dataclass
class Trial:
    ok: bool
    error: str | None = None


@dataclass
class ProduceVerdict:
    observed: dict[str, set[str]] = field(default_factory=dict)
    claimed: dict[str, list[str]] = field(default_factory=dict)
    confirmed: list[tuple[str, str]] = field(default_factory=list)
    refuted: list[tuple[str, str]] = field(default_factory=list)
    unclaimed: list[tuple[str, str]] = field(default_factory=list)
    baseline_error: str | None = None


@dataclass
class RequireVerdict:
    confirmed: list[tuple[str, str]] = field(default_factory=list)
    refuted: list[tuple[str, str]] = field(default_factory=list)
    unremovable: list[tuple[str, str]] = field(default_factory=list)
    baseline_error: str | None = None


def _child(call, subject, adapter, q):
    """Runs in the forked child: execute, snapshot, report."""
    try:
        call(subject)
        q.put(("ok", adapter.snapshot(subject) if adapter is not None else None))
    except BaseException as exc:                  # noqa: BLE001 - probe boundary
        q.put(("err", f"{type(exc).__name__}: {exc}"))


def _run(
    call: Callable[[Any], Any],
    subject: Any,
    timeout_s: int,
    adapter: StateAdapter | None = None,
) -> tuple[Trial, Snapshot | None]:
    """Execute one trial in a forked child and return (verdict, post-snapshot).

    Isolation buys two things that an in-process ``signal.alarm`` cannot:

    **A timeout that actually fires.** ``SIGALRM`` is delivered to the Python
    interpreter loop, so a call that has descended into C — BLAS, a compiled
    solver, a native library's spin — never sees it. Probing a numerical
    library with an in-process alarm therefore hangs on exactly the functions
    most worth probing. ``SIGKILL`` on a child has no such blind spot.

    **No cross-trial contamination.** The child mutates its own copy-on-write
    memory, so the parent's subject is untouched no matter what the call does.
    The post-state must therefore be snapshotted *in the child* and shipped
    back, which is why this returns the snapshot rather than letting the
    caller take it afterwards.

    ``fork`` is required (Linux/macOS): it inherits the closure, so probes can
    stay ordinary Python callables instead of picklable specifications. Set
    ``OMP_NUM_THREADS=1`` before importing a threaded BLAS — forking a
    multi-threaded process is a documented deadlock risk, and the probe
    workload is single-call anyway.
    """
    try:
        ctx = multiprocessing.get_context("fork")
    except ValueError:                            # platform without fork
        return _run_inprocess(call, subject, timeout_s, adapter)

    q = ctx.Queue()
    proc = ctx.Process(target=_child, args=(call, subject, adapter, q), daemon=True)
    proc.start()
    proc.join(timeout_s)

    if proc.is_alive():
        proc.terminate()
        proc.join(5)
        if proc.is_alive():
            proc.kill()
            proc.join(5)
        return Trial(False, f"hard_timeout: exceeded {timeout_s}s"), None

    try:
        status, payload = q.get_nowait()
    except Exception:
        code = proc.exitcode
        return Trial(False, f"child_died: exitcode={code}"), None
    if status == "ok":
        return Trial(True), payload
    return Trial(False, str(payload)), None


def _run_inprocess(call, subject, timeout_s, adapter):
    """Fallback where fork is unavailable. Retains the C-level blind spot."""
    class _Timeout(Exception):
        pass

    def _alarm(signum, frame):
        raise _Timeout(f"probe exceeded {timeout_s}s")

    prev = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(timeout_s)
    try:
        call(subject)
        return Trial(True), (adapter.snapshot(subject) if adapter else None)
    except Exception as exc:                      # noqa: BLE001
        return Trial(False, f"{type(exc).__name__}: {exc}"), None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, prev)


def probe_produces(
    call: Callable[[Any], Any],
    make_subject: Callable[[], Any],
    adapter: StateAdapter,
    claimed: dict[str, list[str]] | None = None,
    timeout_s: int = 300,
) -> ProduceVerdict:
    """Snapshot, call, diff. Keys that appear are produced.

    Also reports keys that appeared but were *not* claimed — an
    under-declaration is as much a registry defect as a false claim, and it is
    the one a synthesizer is most likely to make.
    """
    claimed = claimed or {}
    v = ProduceVerdict(claimed=claimed)

    subject = make_subject()
    before = adapter.snapshot(subject)
    trial, after = _run(call, subject, timeout_s, adapter)
    if not trial.ok or after is None:
        v.baseline_error = trial.error or "child returned no snapshot"
        return v

    for container, keys in after.items():
        appeared = keys - before.get(container, set())
        if appeared:
            v.observed[container] = appeared

    claimed_pairs = {(c, k) for c, ks in claimed.items() for k in ks}
    observed_pairs = {(c, k) for c, ks in v.observed.items() for k in ks}
    v.confirmed = sorted(claimed_pairs & observed_pairs)
    v.refuted = sorted(claimed_pairs - observed_pairs)
    v.unclaimed = sorted(observed_pairs - claimed_pairs)
    return v


def probe_requires(
    call: Callable[[Any], Any],
    make_subject: Callable[[], Any],
    adapter: StateAdapter,
    claimed: dict[str, list[str]],
    timeout_s: int = 300,
) -> RequireVerdict:
    """Delete each claimed key and check the call now fails.

    A claim survives only if the baseline succeeds *and* the stripped run
    fails. If the baseline itself fails the probe is inconclusive and no claim
    is admitted — a failure that predates the removal proves nothing about it.
    """
    v = RequireVerdict()

    base, _ = _run(call, make_subject(), timeout_s)
    if not base.ok:
        v.baseline_error = base.error
        return v

    for container, keys in claimed.items():
        for key in keys:
            subject = make_subject()
            if not adapter.strip(subject, container, key):
                v.unremovable.append((container, key))
                continue
            trial, _ = _run(call, subject, timeout_s)
            (v.confirmed if not trial.ok else v.refuted).append((container, key))
    return v


def probe_prerequisites(
    steps: list[tuple[str, Callable[[Any], Any]]],
    make_subject: Callable[[], Any],
    target: str,
    timeout_s: int = 300,
    candidates: Iterable[str] | None = None,
    report: dict | None = None,
) -> dict[str, bool]:
    """Ablate each predecessor from a mined call sequence.

    ``steps`` is the tutorial-derived sequence ending at ``target``. Dropping a
    predecessor and re-running establishes whether the target genuinely
    depended on it, or merely followed it in the narrative. Tutorials encode
    habit as much as necessity; only the ablation separates the two.

    ``report``, if given, is filled with diagnostics — most importantly why an
    empty result is empty. An empty dict means *inconclusive*, and "the full
    sequence itself failed" is a different fact from "no candidate was under
    test"; folding both into ``{}`` loses the distinction the protocol insists
    on keeping.

    ``candidates`` restricts which predecessors are ablated. The sequence often
    has to carry steps that are *not* under test — the canonical prefix that
    makes the target runnable at all, or a pure renaming of an artefact under
    the name the example expects. Ablating those costs a full sequence re-run
    each and answers a question nobody asked. When ``candidates`` is None every
    predecessor is ablated, which is the original behaviour.
    """
    names = [n for n, _ in steps]
    if target not in names:
        raise ValueError(f"target {target!r} not in sequence {names}")
    cut = names.index(target)
    under_test = list(names[:cut]) if candidates is None else [
        n for n in names[:cut] if n in set(candidates)
    ]

    if report is not None:
        report.update(sequence=names, target=target, under_test=under_test)

    def run_sequence(skip: str | None) -> Trial:
        # One child for the whole sequence: with fork isolation each call would
        # otherwise mutate a copy that dies with the child, so step k+1 would
        # never see what step k produced and every sequence would "fail".
        def whole(subject):
            for name, fn in steps[: cut + 1]:
                if name == skip:
                    continue
                fn(subject)
        t, _ = _run(whole, make_subject(), timeout_s)
        return t

    base = run_sequence(None)
    if not base.ok:                     # full sequence broken: inconclusive
        if report is not None:
            report["baseline_error"] = base.error
        return {}
    if report is not None:
        report["baseline_error"] = None
        report["errors"] = {}
    out: dict[str, bool] = {}
    for name in under_test:
        t = run_sequence(name)
        out[name] = not t.ok
        if report is not None:
            report["errors"][name] = t.error
    return out


def get_adapter(spec: str | dict[str, Any]) -> StateAdapter:
    """``"anndata"`` or ``{"name": "filesystem", "root": "..."}``."""
    if isinstance(spec, str):
        return ADAPTERS[spec]()
    kwargs = dict(spec)
    return ADAPTERS[kwargs.pop("name")](**kwargs)


__all__ = [
    "AnnDataAdapter", "AttrsAdapter", "NamespaceAdapter", "FilesystemAdapter",
    "ADAPTERS", "get_adapter",
    "probe_produces", "probe_requires", "probe_prerequisites",
    "ProduceVerdict", "RequireVerdict",
]
