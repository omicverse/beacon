"""Auto-derived omicverse registry — generated, do not hand-edit.

Produced by awe-decoratr from tutorial mining plus execution probes. Contains
no hand-authored annotation: `requires` and `produces` hold only pairs a
state probe confirmed, `prerequisites` only predecessors a sequence ablation
confirmed, `auto_fix` is derived from that confirmed chain by policy, and the
remaining fields are unverified synthesis (see AUTO_PROVENANCE).

Usage
-----
    import omicverse as ov
    import decorations_auto
    decorations_auto.apply()            # register into ov's runtime registry
    ov.utils.registry_lookup("cluster the cells")

`apply()` overwrites any same-named runtime entry, so importing this module
after omicverse yields a registry whose contract fields are auto-derived —
which is the point: it makes the head-to-head against the hand registry a
substitution rather than a merge.
"""
from __future__ import annotations

import importlib
import json
from typing import Any

__all__ = ["AUTO_ENTRIES", "AUTO_PROVENANCE", "apply", "resolve", "coverage"]


def resolve(dotted: str, module: str = "", name: str = "") -> Any:
    """`ov.pp.pca` -> the callable.

    Attribute traversal from the package root misses anything behind a lazy
    submodule that a bare ``import omicverse`` never touches, which is most of
    the newer subpackages. So fall back to the defining module recorded at
    harvest time and import that directly.
    """
    root = importlib.import_module("omicverse")
    obj: Any = root
    for part in dotted.split(".")[1:]:
        obj = getattr(obj, part, None)
        if obj is None:
            break
    if obj is not None and obj is not root:
        return obj
    if module and name:
        try:
            return getattr(importlib.import_module(module), name, None)
        except Exception:
            return None
    return None


def apply(rebind: bool = False, verbose: bool = False) -> dict:
    """Register every auto entry whose callable resolves.

    Returns a report: registered / unresolved / rejected names. Nothing is
    silently dropped — a registry that hides its own coverage cannot be
    audited against the hand registry it is meant to replace.
    """
    from omicverse._registry import register_function

    report = {"registered": [], "unresolved": [], "rejected": {}}
    for dotted, entry in AUTO_ENTRIES.items():
        meta = {k: v for k, v in entry.items() if not k.startswith("_")}
        fn = resolve(dotted, entry.get("_module", ""), entry.get("_name", ""))
        if fn is None or not callable(fn):
            report["unresolved"].append(dotted)
            continue
        try:
            wrapped = register_function(**meta)(fn)
        except Exception as exc:                     # bad metadata, not a crash
            report["rejected"][dotted] = f"{type(exc).__name__}: {exc}"
            continue
        report["registered"].append(dotted)
        if rebind:
            parent = resolve(dotted.rsplit(".", 1)[0])
            if parent is not None:
                try:
                    setattr(parent, dotted.rsplit(".", 1)[1], wrapped)
                except Exception:
                    pass
    if verbose:
        print(f"registered {len(report['registered'])} / {len(AUTO_ENTRIES)}; "
              f"unresolved {len(report['unresolved'])}; "
              f"rejected {len(report['rejected'])}")
    return report


def coverage() -> dict:
    """How much of the emitted registry rests on a probe rather than a guess."""
    verified = [k for k, v in AUTO_ENTRIES.items()
                if v.get("requires") or v.get("produces")]
    prereq = [k for k, v in AUTO_ENTRIES.items() if v.get("prerequisites")]
    fix = [k for k, v in AUTO_ENTRIES.items()
           if v.get("auto_fix") in ("auto", "escalate")]
    ex = [k for k, v in AUTO_ENTRIES.items() if v.get("examples")]
    return {"functions": len(AUTO_ENTRIES),
            "probe_verified_contract": len(verified),
            "confirmed_prerequisites": len(prereq),
            "derived_auto_fix": len(fix),
            "with_example": len(ex)}


AUTO_ENTRIES: dict = json.loads(r"""
{
 "ov.bulk.Deconvolution": {
  "_module": "omicverse.bulk._decov",
  "_name": "Deconvolution",
  "aliases": [
   "Deconvolution",
   "ov.bulk.Deconvolution",
   "deconvolution"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Bulk RNA-seq deconvolution class for inferring cell-type fractions from single-cell references.",
  "examples": [
   "ov.bulk.Deconvolution(adata_bulk=bulk_ad, adata_single=single_ad_ref, max_single_cells=10000, celltype_key='cell.type.coarse', cellstate_key='cell.type.fine')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.plt.subplots",
   "ov.pl.cellproportion",
   "ov.plt.legend",
   "ov.plt.show"
  ]
 },
 "ov.bulk.Matrix_ID_mapping": {
  "_module": "omicverse.bulk._Deseq2",
  "_name": "Matrix_ID_mapping",
  "aliases": [
   "Matrix_ID_mapping",
   "ov.bulk.Matrix_ID_mapping",
   "matrix i d mapping",
   "id mapping"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Map gene IDs in the input data to gene symbols using a reference table.",
  "examples": [
   "ov.bulk.Matrix_ID_mapping(bulk, 'genesets/pair_GRCm39.tsv')"
  ],
  "related": [
   "ov.plot_set",
   "ov.utils.download_geneid_annotation_pair",
   "ov.bulk.pyDEG",
   "ov.utils.download_pathway_database",
   "ov.utils.geneset_prepare"
  ]
 },
 "ov.bulk.batch_correction": {
  "_module": "omicverse.bulk._combat",
  "_name": "batch_correction",
  "aliases": [
   "batch_correction",
   "ov.bulk.batch_correction",
   "batch correction"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Perform batch effect correction using ComBat algorithm.",
  "examples": [
   "ov.bulk.batch_correction(adata, batch_key='batch')"
  ],
  "related": [
   "ov.ov_plot_set",
   "ov.pp.pca",
   "ov.pl.embedding",
   "ov.metabol.drift_correct",
   "ov.metabol.serrf"
  ]
 },
 "ov.bulk.geneset_enrichment": {
  "_module": "omicverse.bulk._Enrichment",
  "_name": "geneset_enrichment",
  "aliases": [
   "geneset_enrichment",
   "ov.bulk.geneset_enrichment",
   "geneset enrichment",
   "multi pathway enrichment",
   "多通路富集",
   "除了对单个数据库",
   "通路富集外",
   "OmicVerse还支持",
   "对多个通路",
   "富集",
   "可视化"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Perform pathway enrichment analysis using Enrichr-compatible gene-set libraries.",
  "examples": [
   "ov.bulk.geneset_enrichment(gene_list=deg_genes, pathways_dict=pathway_dict, pvalue_type='auto', organism='mouse')"
  ],
  "related": [
   "ov.bulk.pyDEG",
   "ov.bulk.geneset_plot",
   "ov.utils.download_pathway_database",
   "ov.utils.geneset_prepare"
  ]
 },
 "ov.bulk.geneset_plot": {
  "_module": "omicverse.bulk._Enrichment",
  "_name": "geneset_plot",
  "aliases": [
   "geneset_plot",
   "ov.bulk.geneset_plot",
   "geneset plot"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Plot enrichment results as a bubble plot.",
  "examples": [
   "ov.bulk.geneset_plot(enr, figsize=(2, 5), fig_title='Wiki Pathway enrichment', cax_loc=[2, 0.45, 0.5, 0.02], bbox_to_anchor_used=(-0.25, -13), node_diameter=10, custom_ticks=[5, 7], text_knock=3, cmap='Reds')"
  ],
  "related": [
   "ov.bulk.geneset_enrichment",
   "ov.utils.download_pathway_database",
   "ov.utils.geneset_prepare"
  ]
 },
 "ov.bulk.geneset_plot_multi": {
  "_module": "omicverse.bulk._Enrichment",
  "_name": "geneset_plot_multi",
  "aliases": [
   "geneset_plot_multi",
   "ov.bulk.geneset_plot_multi",
   "geneset plot multi"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Plot multiple enrichment result tables in a unified dot-clustermap panel.",
  "examples": [
   "ov.bulk.geneset_plot_multi(enr_dict, colors_dict, num=3, figsize=(2, 5), text_knock=3, fontsize=8, cmap='Reds')"
  ],
  "related": [
   "ov.bulk.geneset_enrichment",
   "ov.utils.geneset_prepare"
  ]
 },
 "ov.bulk.pyDEG": {
  "_module": "omicverse.bulk._Deseq2",
  "_name": "pyDEG",
  "aliases": [
   "pyDEG",
   "ov.bulk.pyDEG",
   "py d e g",
   "different expression analysis with ov",
   "差异表达分析",
   "step create pydeg object",
   "使用ov进行差异表达分析",
   "通过ov",
   "只需提供表达矩阵",
   "即可非常简便地",
   "运行DEG只需"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Differential-expression analysis helper for bulk RNA-seq count tables.",
  "examples": [
   "ov.bulk.pyDEG(data)"
  ],
  "related": [
   "ov.utils.download_geneid_annotation_pair",
   "ov.bulk.Matrix_ID_mapping",
   "ov.utils.download_pathway_database",
   "ov.utils.geneset_prepare",
   "ov.pd.read_csv"
  ]
 },
 "ov.bulk.pyGSEA": {
  "_module": "omicverse.bulk._Enrichment",
  "_name": "pyGSEA",
  "aliases": [
   "pyGSEA",
   "ov.bulk.pyGSEA",
   "py g s e a"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Gene Set Enrichment Analysis (GSEA) wrapper for ranked gene lists.",
  "examples": [
   "ov.bulk.pyGSEA(rnk, pathway_dict)"
  ],
  "related": [
   "ov.bulk.pyDEG",
   "ov.utils.download_pathway_database",
   "ov.utils.geneset_prepare"
  ]
 },
 "ov.bulk.pyPPI": {
  "_module": "omicverse.bulk._network",
  "_name": "pyPPI",
  "aliases": [
   "pyPPI",
   "ov.bulk.pyPPI",
   "py p p i",
   "string ppi network",
   "PPI网络"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Protein-protein interaction (PPI) analysis wrapper based on STRING.",
  "examples": [
   "ov.bulk.pyPPI(gene=gene_list, gene_type_dict=gene_type_dict, gene_color_dict=gene_color_dict, species=4932)"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.bulk.string_interaction"
  ]
 },
 "ov.bulk.pyTCGA": {
  "_module": "omicverse.bulk._tcga",
  "_name": "pyTCGA",
  "aliases": [
   "pyTCGA",
   "ov.bulk.pyTCGA",
   "py t c g a",
   "tcga ov"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "TCGA (The Cancer Genome Atlas) data analysis module.",
  "examples": [
   "ov.bulk.pyTCGA(gdc_sample_sheep, gdc_download_files, clinical_cart)"
  ],
  "related": [
   "ov.plot_set"
  ]
 },
 "ov.bulk.pyWGCNA": {
  "_module": "omicverse.bulk._wgcna",
  "_name": "pyWGCNA",
  "aliases": [
   "pyWGCNA",
   "ov.bulk.pyWGCNA",
   "py w g c n a",
   "correlation matrix calculate"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Weighted Gene Co-expression Network Analysis.",
  "examples": [
   "ov.bulk.pyWGCNA(name='5xFAD_2k', species='mus musculus', geneExp=data.T, outputPath='', save=True)"
  ],
  "related": [
   "ov.plot_set",
   "ov.utils.read",
   "ov.bulk.readWGCNA",
   "ov.utils.ov_plot_set",
   "ov.utils.read_csv"
  ]
 },
 "ov.bulk.string_interaction": {
  "_module": "omicverse.bulk._network",
  "_name": "string_interaction",
  "aliases": [
   "string_interaction",
   "ov.bulk.string_interaction",
   "string interaction",
   "string interaction analysis"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Analyze protein-protein interaction network using STRING database.",
  "examples": [
   "ov.bulk.string_interaction(gene_list, 4932)"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.bulk.pyPPI"
  ]
 },
 "ov.bulk.temporal_clusters": {
  "_module": "omicverse.bulk._Deseq2",
  "_name": "temporal_clusters",
  "aliases": [
   "temporal_clusters",
   "ov.bulk.temporal_clusters",
   "temporal clusters"
  ],
  "auto_fix": "none",
  "category": "bulk",
  "description": "Soft-cluster temporal expression trajectories by fuzzy c-means.",
  "examples": [
   "ov.bulk.temporal_clusters(lognorm, time, genes=temporal, n_clusters=6, m='auto', seed=0)"
  ],
  "related": []
 },
 "ov.pl.CellChatViz": {
  "_module": "omicverse.pl._cpdbviz",
  "_name": "CellChatViz",
  "aliases": [
   "CellChatViz",
   "ov.pl.CellChatViz",
   "cell chat viz"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Visualization helper for CellPhoneDB cell-cell communication outputs.",
  "examples": [
   "ov.pl.CellChatViz(adata_cpdb, palette=color_dict)"
  ],
  "related": [
   "ov.pl.ccc_stat_plot"
  ]
 },
 "ov.pl.ConvexHull": {
  "_module": "omicverse.pl._single",
  "_name": "ConvexHull",
  "aliases": [
   "ConvexHull",
   "ov.pl.ConvexHull",
   "convex hull",
   "arguments"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot the ConvexHull for a cluster in embedding.",
  "examples": [
   "ov.pl.ConvexHull(adata, basis='X_umap', cluster_key='clusters', hull_cluster='Granule mature', ax=ax)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.utils.gen_mpl_labels",
   "ov.pl.dotplot",
   "ov.pl.cellstackarea",
   "ov.pl.embedding_celltype"
  ]
 },
 "ov.pl.ForbiddenCity": {
  "_module": "omicverse.pl._palette",
  "_name": "ForbiddenCity",
  "aliases": [
   "ForbiddenCity",
   "ov.pl.ForbiddenCity",
   "forbidden city",
   "understanding the color system"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Forbidden City traditional-color palette utility.",
  "examples": [
   "ov.pl.ForbiddenCity()"
  ],
  "related": [
   "ov.plot_set",
   "ov.read",
   "ov.pl.embedding"
  ]
 },
 "ov.pl.add_density_contour": {
  "_module": "omicverse.pl._density",
  "_name": "add_density_contour",
  "aliases": [
   "add_density_contour",
   "ov.pl.add_density_contour",
   "add density contour"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Add KDE-based density contours to an existing matplotlib plot.",
  "examples": [
   "ov.pl.add_density_contour(ax, embeddings=adata[adata.obs['density_Sox4'] > 0.03].obsm['X_umap'][:, :2], weights=adata[adata.obs['density_Sox4'] > 0.03].obs['density_Sox4'].to_numpy(), levels='quantile', n_quantiles=4, bw_adjust=0.25, fill=False, linewidth=1.0, cmap_contour='Greys', zorder=10)"
  ],
  "related": [
   "ov.pl.calculate_gene_density",
   "ov.pl.embedding",
   "ov.single.geneset_aucell",
   "ov.style",
   "ov.pl.violin"
  ]
 },
 "ov.pl.add_palue": {
  "_module": "omicverse.pl._general",
  "_name": "add_palue",
  "aliases": [
   "add_palue",
   "ov.pl.add_palue",
   "add palue",
   "嵌入_density",
   "嵌入"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Add p-value annotation with connecting line to a matplotlib plot.",
  "examples": [
   "ov.pl.add_palue(ax, line_x1=-0.5, line_x2=0.5, line_y=40, text_y=0.2, text='$p={}$'.format(round(0.001, 3)), fontsize=11, fontcolor='#000000', horizontalalignment='center')"
  ],
  "related": [
   "ov.pl.volcano",
   "ov.pl.boxplot",
   "ov.style",
   "ov.pl.violin",
   "ov.pl.bardotplot"
  ]
 },
 "ov.pl.add_pie2spatial": {
  "_module": "omicverse.pl._space",
  "_name": "add_pie2spatial",
  "aliases": [
   "add_pie2spatial",
   "ov.pl.add_pie2spatial",
   "add pie2spatial"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Overlay per-spot pie charts of cell-type composition on a spatial map.",
  "examples": [
   "ov.pl.add_pie2spatial(adata_s, img_key='hires', cell_type_columns=annotation_list[:], ax=ax, colors=color_dict, pie_radius=10, remainder='gap', legend_loc=(0.5, -0.25), ncols=4, alpha=0.8)"
  ],
  "related": [
   "ov.pl.plot_spatial",
   "ov.space.crop_space_visium",
   "ov.space.Tangram",
   "ov.plt.subplots",
   "ov.space.Deconvolution"
  ]
 },
 "ov.pl.add_streamplot": {
  "_module": "omicverse.pl._animation_lines",
  "_name": "add_streamplot",
  "aliases": [
   "add_streamplot",
   "ov.pl.add_streamplot",
   "add streamplot",
   "比较扰动前后的",
   "比较扰动前后",
   "扰动后复用相同",
   "坐标",
   "比较",
   "后的"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Overlay velocity streamlines on a low-dimensional embedding.",
  "examples": [
   "ov.pl.add_streamplot(adata, basis='X_umap', velocity_key='velo_regvelo_umap', ax=ax)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.plt.figure",
   "ov.plt.subplot",
   "ov.plt.title",
   "ov.single.Velo"
  ]
 },
 "ov.pl.bardotplot": {
  "_module": "omicverse.pl._single",
  "_name": "bardotplot",
  "aliases": [
   "bardotplot",
   "ov.pl.bardotplot"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a combined bar-and-dot summary plot by groups.",
  "examples": [
   "ov.pl.bardotplot(adata, groupby='clusters', color='Sox_aucell', figsize=(6, 2), ax=ax, ylabel='Expression', bar_kwargs={'alpha': 0.5, 'linewidth': 2, 'width': 0.6, 'capsize': 4}, scatter_kwargs={'alpha': 0.8, 's': 10, 'marker': 'o'})"
  ],
  "related": [
   "ov.single.geneset_aucell",
   "ov.style",
   "ov.pl.violin",
   "ov.pl.add_palue"
  ]
 },
 "ov.pl.boxplot": {
  "_module": "omicverse.pl._bulk",
  "_name": "boxplot",
  "aliases": [
   "boxplot",
   "ov.pl.boxplot"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a boxplot with jittered points to visualize data distribution across categories.",
  "examples": [
   "ov.pl.boxplot(data, hue='sex', x_value='day', y_value='total_bill', palette=ov.pl.red_color, figsize=(4, 2), fontsize=12, title='Tips')"
  ],
  "related": [
   "ov.pl.volcano",
   "ov.pl.add_palue",
   "ov.pl.upset",
   "ov.pl.venn",
   "ov.read"
  ]
 },
 "ov.pl.branch_streamplot": {
  "_module": "omicverse.pl._branch_streamplot",
  "_name": "branch_streamplot",
  "aliases": [
   "branch_streamplot",
   "ov.pl.branch_streamplot",
   "branch streamplot",
   "伪时间流图",
   "伪时间",
   "分支感知的伪时间流图",
   "分支感知",
   "细胞状态标签",
   "这个轨迹推断方法",
   "图中",
   "富集位置"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Render a branch-aware pseudotime stream plot.",
  "examples": [
   "ov.pl.branch_streamplot(adata, group_key='clusters', pseudotime_key='development_pseudotime', trunk_groups=['Ductal', 'Ngn3 low EP', 'Ngn3 high EP', 'Pre-endocrine'], branch_center=0.62, figsize=(6, 4), xlabel='Development pseudotime', show=False)"
  ],
  "related": [
   "ov.single.dynamic_features",
   "ov.pl.dynamic_trends",
   "ov.pl.embedding",
   "ov.pl.dynamic_heatmap",
   "ov.utils.plot_paga"
  ]
 },
 "ov.pl.calculate_gene_density": {
  "_module": "omicverse.pl._density",
  "_name": "calculate_gene_density",
  "aliases": [
   "calculate_gene_density",
   "ov.pl.calculate_gene_density",
   "calculate gene density"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Calculate weighted kernel density estimates for gene expression on 2D embeddings.",
  "examples": [
   "ov.pl.calculate_gene_density(adata, features=['Sox4'], basis='X_umap', dims=(0, 1), adjust=0.2, min_expr=0.01)"
  ],
  "related": [
   "ov.plt.show",
   "ov.pl.embedding_density",
   "ov.pl.embedding",
   "ov.pl.add_density_contour"
  ]
 },
 "ov.pl.ccc_heatmap": {
  "_module": "omicverse.pl._ccc",
  "_name": "ccc_heatmap",
  "aliases": [
   "ccc_heatmap",
   "ov.pl.ccc_heatmap",
   "ccc heatmap",
   "哪个",
   "key constraints to keep in mind"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot communication matrices as heatmaps, dot plots, or bubble maps.",
  "examples": [
   "ov.pl.ccc_heatmap(adata, plot_type='heatmap', display_by='aggregation', cmap='Reds', show=False)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.single.run_cellphonedb_v5",
   "ov.single.extract_comm_adata",
   "ov.single.run_liana",
   "ov.single.to_comm_adata"
  ]
 },
 "ov.pl.ccc_network_plot": {
  "_module": "omicverse.pl._ccc",
  "_name": "ccc_network_plot",
  "aliases": [
   "ccc_network_plot",
   "ov.pl.ccc_network_plot",
   "ccc network plot",
   "key constraints"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot cell-cell communication networks with multiple graph styles.",
  "examples": [
   "ov.pl.ccc_network_plot(adata_plot, plot_type='pathway', signaling=['Signaling by Interleukin'], palette=color_dict, top_n=50, figsize=(6, 6), show=False)"
  ],
  "related": [
   "ov.pl.ccc_heatmap",
   "ov.read"
  ]
 },
 "ov.pl.ccc_stat_plot": {
  "_module": "omicverse.pl._ccc",
  "_name": "ccc_stat_plot",
  "aliases": [
   "ccc_stat_plot",
   "ov.pl.ccc_stat_plot",
   "ccc stat plot"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot communication summaries, distributions, and pathway statistics.",
  "examples": [
   "ov.pl.ccc_stat_plot(adata_plot, plot_type='bar', figsize=(6, 4), top_n=10, show=False)"
  ],
  "related": [
   "ov.pl.ccc_network_plot",
   "ov.read"
  ]
 },
 "ov.pl.cell_cor_heatmap": {
  "_module": "omicverse.pl._heatmap_marsilea",
  "_name": "cell_cor_heatmap",
  "aliases": [
   "cell_cor_heatmap",
   "ov.pl.cell_cor_heatmap",
   "cell cor heatmap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Compute pairwise correlation/similarity between cell groups and plot as heatmap.",
  "examples": [
   "ov.pl.cell_cor_heatmap(adata, group_by='major_celltype', ref_adata=adata, ref_group_by='scsa_celltype_cellmarker', method='pearson', standard_scale='var', cmap='RdBu_r', figsize=(2, 2.5), row_cluster=True, col_cluster=True, show_values=True, value_cutoff=0.3, border=False, show=False)"
  ],
  "related": [
   "ov.single.scanpy_cellanno_from_dict",
   "ov.utils.embedding",
   "ov.utils.palette",
   "ov.single.get_celltype_marker"
  ]
 },
 "ov.pl.cell_fate": {
  "_module": "omicverse.pl._trajectory",
  "_name": "cell_fate",
  "aliases": [
   "cell_fate",
   "ov.pl.cell_fate",
   "cell fate",
   "会复用",
   "中保存的",
   "中保存",
   "结果",
   "它只负责可视化",
   "不会重新计算"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot CellRank macrostates from an estimator or fitted OV wrapper.",
  "examples": [
   "ov.pl.cell_fate(estimator, which='terminal', basis='umap')"
  ],
  "related": [
   "ov.single.cellrank_fate",
   "ov.single.Velo",
   "ov.plt.subplots",
   "ov.single.state_names",
   "ov.plt.title"
  ]
 },
 "ov.pl.cellproportion": {
  "_module": "omicverse.pl._single",
  "_name": "cellproportion",
  "aliases": [
   "cellproportion",
   "ov.pl.cellproportion",
   "stacked histogram of cell proportions"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot cell proportion of each cell type in each visual cluster.",
  "examples": [
   "ov.pl.cellproportion(adata=adata, celltype_clusters='clusters', groupby='age(days)', legend=True, ax=ax)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.plt.subplots",
   "ov.bulk.Deconvolution",
   "ov.plt.legend",
   "ov.plt.show"
  ]
 },
 "ov.pl.cnv_heatmap": {
  "_module": "omicverse.pl._cnv",
  "_name": "cnv_heatmap",
  "aliases": [
   "cnv_heatmap",
   "ov.pl.cnv_heatmap",
   "cnv heatmap",
   "layered annotation"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot the genome-wide CNV heatmap.",
  "examples": [
   "ov.pl.cnv_heatmap(cnv_obj, groupby='cell_type', annotations=['sample', 'leiden'])"
  ],
  "related": [
   "ov.single.CNV",
   "ov.plot_set",
   "ov.pl.cnv_summary",
   "ov.single.auto_resolution",
   "ov.single.NMF"
  ]
 },
 "ov.pl.cnv_summary": {
  "_module": "omicverse.pl._cnv",
  "_name": "cnv_summary",
  "aliases": [
   "cnv_summary",
   "ov.pl.cnv_summary",
   "cnv summary"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot mean CN per genomic bin as a filled step plot.",
  "examples": [
   "ov.pl.cnv_summary(adata, groupby='cnv_prediction', subset='aneuploid', figsize=(8, 2.6), title='Aneuploid mean CN profile')"
  ],
  "related": [
   "ov.pl.cnv_heatmap",
   "ov.pl.cnv_umap",
   "ov.plot_set",
   "ov.single.CNV"
  ]
 },
 "ov.pl.cnv_umap": {
  "_module": "omicverse.pl._cnv",
  "_name": "cnv_umap",
  "aliases": [
   "cnv_umap",
   "ov.pl.cnv_umap",
   "cnv umap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "UMAP coloured by CNV outputs.",
  "examples": [
   "ov.pl.cnv_umap(adata)"
  ],
  "related": [
   "ov.pl.cnv_heatmap",
   "ov.pl.cnv_summary",
   "ov.single.CNV"
  ]
 },
 "ov.pl.complexheatmap": {
  "_module": "omicverse.pl._heatmap",
  "_name": "complexheatmap",
  "aliases": [
   "complexheatmap",
   "ov.pl.complexheatmap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Generate a complex annotated heatmap using PyComplexHeatmap.",
  "examples": [],
  "related": []
 },
 "ov.pl.contour": {
  "_module": "omicverse.pl._single",
  "_name": "contour",
  "aliases": [
   "contour",
   "ov.pl.contour"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Overlay a KDE contour for selected clusters on embedding axes.",
  "examples": [
   "ov.pl.contour(ax=ax, adata=adata, groupby='clusters', clusters=['Granule immature', 'Granule mature'], basis='X_umap', contour_threshold=0.1, colors='#000000', linestyles='dashed')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.embedding_adjust",
   "ov.pl.ConvexHull",
   "ov.plt.show",
   "ov.utils.embedding"
  ]
 },
 "ov.pl.create_custom_colormap": {
  "_module": "omicverse.pl._spatialseg",
  "_name": "create_custom_colormap",
  "aliases": [
   "create_custom_colormap",
   "ov.pl.create_custom_colormap",
   "create custom colormap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Build a transparent-to-opaque LinearSegmentedColormap of a single colour.",
  "examples": [
   "ov.pl.create_custom_colormap('#a51616')"
  ],
  "related": [
   "ov.pl.spatialseg"
  ]
 },
 "ov.pl.dotplot": {
  "_module": "omicverse.pl._dotplot",
  "_name": "dotplot",
  "aliases": [
   "dotplot",
   "ov.pl.dotplot",
   "why this step matters"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Make a dot plot of the expression values of `var_names`.",
  "examples": [
   "ov.pl.dotplot(adata, marker_genes_dict, groupby='clusters')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.ConvexHull",
   "ov.utils.gen_mpl_labels",
   "ov.pl.violin",
   "ov.single.get_markers"
  ]
 },
 "ov.pl.dynamic_heatmap": {
  "_module": "omicverse.pl._heatmap_marsilea",
  "_name": "dynamic_heatmap",
  "aliases": [
   "dynamic_heatmap",
   "ov.pl.dynamic_heatmap",
   "dynamic heatmap",
   "使用",
   "概括",
   "热图",
   "压缩成一张按伪时间排序",
   "启动顺序",
   "标记基因程序",
   "pseudotime heatmap per lineage ov"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot dynamic feature trends along pseudotime, optionally by lineage.",
  "examples": [
   "ov.pl.dynamic_heatmap(adata, var_names=cellrank_marker_modules, pseudotime='development_pseudotime', layer='Ms', use_cell_columns=False, cell_annotation='clusters', cell_bins=180, smooth_window=17, fitted_window=31, figsize=(5, 4), standard_scale='var', cmap='RdBu_r', use_fitted=True, show_row_names=True, border=False, show=False)"
  ],
  "related": [
   "ov.single.dynamic_features",
   "ov.pl.dynamic_trends",
   "ov.utils.cal_paga",
   "ov.utils.plot_paga",
   "ov.pl.branch_streamplot"
  ]
 },
 "ov.pl.dynamic_trends": {
  "_module": "omicverse.pl._dynamic_trends",
  "_name": "dynamic_trends",
  "aliases": [
   "dynamic_trends",
   "ov.pl.dynamic_trends",
   "dynamic trends",
   "single-line global trends",
   "用细胞注释给原始散点着色",
   "它适合区分",
   "整体伪时间表达趋势",
   "多标记基因趋势比较",
   "这里把多个",
   "把多个",
   "方便直接比较不同程序"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot GAM-fitted pseudotime trends for one or more genes.",
  "examples": [
   "ov.pl.dynamic_trends(beta_dyn, genes=['Pdx1', 'Ins1', 'Ins2', 'Sox9'], compare_features=True, add_point=True, point_color_by='clusters', line_style_by='features', figsize=(6, 3), linewidth=2, legend_loc='right margin', legend_fontsize=8)"
  ],
  "related": [
   "ov.single.dynamic_features",
   "ov.pl.branch_streamplot",
   "ov.pl.dynamic_heatmap",
   "ov.pl.embedding",
   "ov.utils.plot_paga"
  ]
 },
 "ov.pl.embedding": {
  "_module": "omicverse.pl._scatterplot_backend",
  "_name": "embedding",
  "aliases": [
   "embedding",
   "ov.pl.embedding",
   "default colormap",
   "嵌入",
   "uncorrected baseline",
   "corrected embedding",
   "arguments",
   "if you have too many labels",
   "zero-shot embedding generation",
   "原生"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Scatter plot for user specified embedding basis (e.g. umap, pca, etc).",
  "examples": [
   "ov.pl.embedding(adata, basis='spatial_fov', color=['Max.PanCK', 'fov'], vmax='p99.2', cmap='Reds', wspace=0.35)"
  ],
  "related": [
   "ov.read",
   "ov.pp.pca",
   "ov.pp.preprocess",
   "ov.plot_set",
   "ov.pl.umap"
  ]
 },
 "ov.pl.embedding_adjust": {
  "_module": "omicverse.pl._single",
  "_name": "embedding_adjust",
  "aliases": [
   "embedding_adjust",
   "ov.pl.embedding_adjust",
   "embedding adjust",
   "嵌入",
   "嵌入_adjust"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Get locations of cluster median and adjust text labels accordingly.",
  "examples": [
   "ov.pl.embedding_adjust(adata, groupby='clusters', exclude=('OL',), basis='X_umap', ax=ax, adjust_kwargs=dict(arrowprops=dict(arrowstyle='-', color='black')), text_kwargs=dict(fontsize=12, weight='bold', path_effects=[patheffects.withStroke(linewidth=2, foreground='w')]))"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.contour",
   "ov.plt.show",
   "ov.pl.embedding_density",
   "ov.utils.embedding"
  ]
 },
 "ov.pl.embedding_atlas": {
  "_module": "omicverse.pl._embedding",
  "_name": "embedding_atlas",
  "aliases": [
   "embedding_atlas",
   "ov.pl.embedding_atlas",
   "embedding atlas"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Render large-scale embeddings with Datashader.",
  "examples": [],
  "related": []
 },
 "ov.pl.embedding_celltype": {
  "_module": "omicverse.pl._single",
  "_name": "embedding_celltype",
  "aliases": [
   "embedding_celltype",
   "ov.pl.embedding_celltype",
   "embedding celltype",
   "嵌入"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot embedding with celltype color by omicverse.",
  "examples": [
   "ov.pl.embedding_celltype(adata, figsize=(7, 4), basis='X_umap', celltype_key='clusters', title='            Cell type', celltype_range=(1, 10), embedding_range=(4, 10))"
  ],
  "related": [
   "ov.pl.cellproportion",
   "ov.pl.cellstackarea",
   "ov.pl.embedding",
   "ov.pl.ConvexHull"
  ]
 },
 "ov.pl.embedding_density": {
  "_module": "omicverse.pl._single",
  "_name": "embedding_density",
  "aliases": [
   "embedding_density",
   "ov.pl.embedding_density",
   "embedding density",
   "嵌入"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot cluster-specific density on an existing embedding.",
  "examples": [
   "ov.pl.embedding_density(adata, basis='X_umap', groupby='clusters', target_clusters='Granule mature', frameon='small', show=False, cmap='RdBu_r', alpha=0.8)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.embedding_adjust",
   "ov.plt.show",
   "ov.pl.calculate_gene_density"
  ]
 },
 "ov.pl.feature_heatmap": {
  "_module": "omicverse.pl._heatmap_marsilea",
  "_name": "feature_heatmap",
  "aliases": [
   "feature_heatmap",
   "ov.pl.feature_heatmap",
   "feature heatmap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot cell-level feature expression ordered by groups or metadata.",
  "examples": [],
  "related": []
 },
 "ov.pl.funky_heatmap": {
  "_module": "omicverse.pl._funkyheatmap",
  "_name": "funky_heatmap",
  "aliases": [
   "funky_heatmap",
   "ov.pl.funky_heatmap",
   "funky heatmap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Generate a funky heatmap from a :class:`pandas.DataFrame`.",
  "examples": [
   "ov.pl.funky_heatmap(mtcars_small)"
  ],
  "related": [
   "ov.single.mouse_hsc_nestorowa16",
   "ov.single.perturb",
   "ov.style",
   "ov.plot_set"
  ]
 },
 "ov.pl.gen_mpl_labels": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "gen_mpl_labels",
  "aliases": [
   "gen_mpl_labels",
   "ov.pl.gen_mpl_labels",
   "gen mpl labels"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Add cluster labels at median positions in embedding plots with automatic text positioning.",
  "examples": [],
  "related": []
 },
 "ov.pl.geneset_wordcloud": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "geneset_wordcloud",
  "aliases": [
   "geneset_wordcloud",
   "ov.pl.geneset_wordcloud",
   "geneset wordcloud"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Build cluster-wise gene-set word clouds along pseudotime.",
  "examples": [
   "gw_obj = ov.utils.geneset_wordcloud(adata=adata_aucs[:, var_name], cluster_key=\"g1\", pseudotime=\"pt_via\")"
  ],
  "related": []
 },
 "ov.pl.group_heatmap": {
  "_module": "omicverse.pl._heatmap_marsilea",
  "_name": "group_heatmap",
  "aliases": [
   "group_heatmap",
   "ov.pl.group_heatmap",
   "group heatmap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot grouped mean expression as a Marsilea heatmap.",
  "examples": [
   "ov.pl.group_heatmap(adata, var_names=marker_genes_heatmap, groupby='leiden', figsize=(4, 5), standard_scale='var', cmap='RdBu_r', border=False, show=False)"
  ],
  "related": [
   "ov.utils.plot_cellproportion",
   "ov.utils.plot_embedding_celltype",
   "ov.utils.roe",
   "ov.single.scanpy_cellanno_from_dict",
   "ov.utils.embedding"
  ]
 },
 "ov.pl.marker_heatmap": {
  "_module": "omicverse.pl._heatmap",
  "_name": "marker_heatmap",
  "aliases": [
   "marker_heatmap",
   "ov.pl.marker_heatmap",
   "marker heatmap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a dot plot heatmap showing marker gene expression using PyComplexHeatmap.",
  "examples": [
   "ov.pl.marker_heatmap(adata, marker_genes_dict=marker_dict, groupby='flowsom', use_raw=False, standard_scale='var', figsize=(8, 5))"
  ],
  "related": []
 },
 "ov.pl.markers_dotplot": {
  "_module": "omicverse.pl._dotplot",
  "_name": "markers_dotplot",
  "aliases": [
   "markers_dotplot",
   "ov.pl.markers_dotplot",
   "markers dotplot",
   "code https"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Dot plot of marker genes — clean drop-in for :func:`rank_genes_groups_dotplot`.",
  "examples": [
   "ov.pl.markers_dotplot(adata, groupby='leiden', n_genes=3, key='rank_genes_groups')"
  ],
  "related": [
   "ov.single.get_markers",
   "ov.pl.embedding",
   "ov.single.find_markers",
   "ov.single.MetaCell",
   "ov.utils.gen_mpl_labels"
  ]
 },
 "ov.pl.metacell_codebook_umap": {
  "_module": "omicverse.pl._metacell",
  "_name": "metacell_codebook_umap",
  "aliases": [
   "metacell_codebook_umap",
   "ov.pl.metacell_codebook_umap",
   "metacell codebook umap"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Project MetaQ's codebook to 2D and colour each entry by majority cell label.",
  "examples": [
   "ov.pl.metacell_codebook_umap(mc, label_key='clusters')"
  ],
  "related": []
 },
 "ov.pl.metacell_metrics": {
  "_module": "omicverse.pl._metacell",
  "_name": "metacell_metrics",
  "aliases": [
   "metacell_metrics",
   "ov.pl.metacell_metrics",
   "metacell metrics"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Compute purity / separation / compactness and plot 3 histograms.",
  "examples": [
   "ov.pl.metacell_metrics(mc, label_key='clusters', use_rep='X_pca')"
  ],
  "related": [
   "ov.pp.umap",
   "ov.single.MetaCell",
   "ov.pl.rigor_scatter",
   "ov.pl.embedding",
   "ov.pl.metacell_purity_box"
  ]
 },
 "ov.pl.metacell_purity_box": {
  "_module": "omicverse.pl._metacell",
  "_name": "metacell_purity_box",
  "aliases": [
   "metacell_purity_box",
   "ov.pl.metacell_purity_box",
   "metacell purity box"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Box plot of per-metacell purity, split by majority celltype.",
  "examples": [
   "ov.pl.metacell_purity_box(mc, label_key='clusters')"
  ],
  "related": [
   "ov.pl.metacell_metrics",
   "ov.pl.rigor_scatter",
   "ov.pp.preprocess",
   "ov.pp.scale",
   "ov.pp.pca"
  ]
 },
 "ov.pl.metacell_soft_heatmap": {
  "_module": "omicverse.pl._metacell",
  "_name": "metacell_soft_heatmap",
  "aliases": [
   "metacell_soft_heatmap",
   "ov.pl.metacell_soft_heatmap",
   "metacell soft heatmap",
   "seacells different from hard partitioner"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Heatmap of a random subset of the soft membership matrix.",
  "examples": [
   "ov.pl.metacell_soft_heatmap(mc, n_cells=80, n_mc=40, random_state=0)"
  ],
  "related": [
   "ov.single.find_markers",
   "ov.single.get_markers",
   "ov.pl.markers_dotplot",
   "ov.single.MetaCell"
  ]
 },
 "ov.pl.palette": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "palette",
  "aliases": [
   "palette",
   "ov.pl.palette"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Returns the default OmicVerse color palette.",
  "examples": [],
  "related": []
 },
 "ov.pl.perturb_cell_quiver": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_cell_quiver",
  "aliases": [
   "perturb_cell_quiver",
   "ov.pl.perturb_cell_quiver",
   "perturb cell quiver"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Per-cell arrow plot of the perturbation flow.",
  "examples": [
   "ov.pl.perturb_cell_quiver(adata_sub, result, cluster_col='cell_type_roughly', arrow_target_length=0.005, subsample=3)"
  ],
  "related": []
 },
 "ov.pl.perturb_celloracle_layout": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_celloracle_layout",
  "aliases": [
   "perturb_celloracle_layout",
   "ov.pl.perturb_celloracle_layout",
   "perturb celloracle layout"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Run CellOracle's own development-module pipeline on this PerturbResult and return its `visualize_development_module_layout_0` figure — 1:1 with the published Paul15 Gata1-KO tutorial.",
  "examples": [
   "ov.pl.perturb_celloracle_layout(adata, result, pseudotime_key='Pseudotime', cluster_column_name='louvain_annot', vm=0.02)"
  ],
  "related": [
   "ov.single.perturb",
   "ov.pl.perturb_sankey",
   "ov.pl.perturb_markov_endpoints",
   "ov.pl.perturb_volcano"
  ]
 },
 "ov.pl.perturb_development_layout": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_development_layout",
  "aliases": [
   "perturb_development_layout",
   "ov.pl.perturb_development_layout",
   "perturb development layout"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Reproduce CellOracle's ``visualize_development_module_layout_0`` figure panel-by-panel.",
  "examples": [],
  "related": []
 },
 "ov.pl.perturb_inner_product_on_grid": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_inner_product_on_grid",
  "aliases": [
   "perturb_inner_product_on_grid",
   "ov.pl.perturb_inner_product_on_grid",
   "perturb inner product on grid"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot the per-grid-cell Perturbation Score as a colored heatmap.",
  "examples": [
   "ov.pl.perturb_inner_product_on_grid(adata_sub, result, pseudotime='dpt_pseudotime', cluster_col='cell_type_roughly', grid_size=25, overlay_arrows=True)"
  ],
  "related": []
 },
 "ov.pl.perturb_markov_endpoints": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_markov_endpoints",
  "aliases": [
   "perturb_markov_endpoints",
   "ov.pl.perturb_markov_endpoints",
   "perturb markov endpoints"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "One-call wrapper around `result.run_markov` that plots the endpoint cluster distribution as a horizontal bar chart.",
  "examples": [
   "ov.pl.perturb_markov_endpoints(result, adata=adata, start_cells=list(mep_cells), cluster_col='main_cluster', n_steps=15, n_walks_per_cell=50)"
  ],
  "related": [
   "ov.pl.perturb_celloracle_layout",
   "ov.pl.perturb_sankey",
   "ov.pl.perturb_volcano"
  ]
 },
 "ov.pl.perturb_quiver": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_quiver",
  "aliases": [
   "perturb_quiver",
   "ov.pl.perturb_quiver",
   "perturb quiver"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "CellOracle-style aggregated arrow plot of the perturbation flow.",
  "examples": [
   "ov.pl.perturb_quiver(adata, result_co, cluster_col='main_cluster', grid_size=25, arrow_target_length=0.0025)"
  ],
  "related": [
   "ov.single.perturb",
   "ov.pl.perturb_sankey",
   "ov.pl.perturb_volcano"
  ]
 },
 "ov.pl.perturb_sankey": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_sankey",
  "aliases": [
   "perturb_sankey",
   "ov.pl.perturb_sankey",
   "perturb sankey"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Two-column Sankey of cluster→cluster post-perturbation flow.",
  "examples": [
   "ov.pl.perturb_sankey(result, adata=adata, cluster_col='main_cluster', min_flow=0.03)"
  ],
  "related": [
   "ov.pl.perturb_volcano",
   "ov.single.perturb",
   "ov.pl.perturb_quiver",
   "ov.pl.perturb_celloracle_layout",
   "ov.pl.perturb_markov_endpoints"
  ]
 },
 "ov.pl.perturb_volcano": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturb_volcano",
  "aliases": [
   "perturb_volcano",
   "ov.pl.perturb_volcano",
   "perturb volcano"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Volcano of delta vs −log10(p) for the per-gene table.",
  "examples": [
   "ov.pl.perturb_volcano(result, top_n=15)"
  ],
  "related": [
   "ov.pl.perturb_sankey",
   "ov.pl.perturb_quiver",
   "ov.pl.perturb_celloracle_layout",
   "ov.pl.perturb_markov_endpoints",
   "ov.single.perturb"
  ]
 },
 "ov.pl.perturbation_embedding_shift": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturbation_embedding_shift",
  "aliases": [
   "perturbation_embedding_shift",
   "ov.pl.perturbation_embedding_shift",
   "perturbation embedding shift"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot per-cell embedding shift arrows on an existing 2-D basis.",
  "examples": [],
  "related": []
 },
 "ov.pl.perturbation_shift_violin": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturbation_shift_violin",
  "aliases": [
   "perturbation_shift_violin",
   "ov.pl.perturbation_shift_violin",
   "perturbation shift violin",
   "cell-level cosine similarity",
   "lineage specificity"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Violin of per-cell cosine similarity for each perturbed gene.",
  "examples": [
   "ov.pl.perturbation_shift_violin(perturb_result, title='Geneformer in-silico delete — TF panel')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.perturbation_top_downstream_genes"
  ]
 },
 "ov.pl.perturbation_top_downstream_genes": {
  "_module": "omicverse.pl._perturbation",
  "_name": "perturbation_top_downstream_genes",
  "aliases": [
   "perturbation_top_downstream_genes",
   "ov.pl.perturbation_top_downstream_genes",
   "perturbation top downstream genes"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot the top-N most-shifted downstream genes after a TF knockout.",
  "examples": [
   "ov.pl.perturbation_top_downstream_genes(perturb_result, gene='PAX5', top_n=20)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.perturbation_shift_violin"
  ]
 },
 "ov.pl.plot1cell": {
  "_module": "omicverse.pl._plot1cell",
  "_name": "plot1cell",
  "aliases": [
   "plot1cell",
   "ov.pl.plot1cell"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Circular UMAP with metadata tracks.",
  "examples": [
   "ov.pl.plot1cell(a10k, clusters='cell_type', basis='X_tSNE', tracks=['donor_id', 'compartment', 'sex', 'age'], point_size=6, point_alpha=0.5, figsize=(9, 9), label_fontsize=7)"
  ],
  "related": [
   "ov.datasets.download_data",
   "ov.read"
  ]
 },
 "ov.pl.plot_ConvexHull": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "plot_ConvexHull",
  "aliases": [
   "plot_ConvexHull",
   "ov.pl.plot_ConvexHull",
   "plot convex hull"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Add convex hull outline for a specific cluster in embedding plot.",
  "examples": [
   "import omicverse as ov",
   "import matplotlib.pyplot as plt",
   "# Create embedding plot with convex hull"
  ],
  "related": []
 },
 "ov.pl.plot_cellproportion": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "plot_cellproportion",
  "aliases": [
   "plot_cellproportion",
   "ov.pl.plot_cellproportion",
   "plot cellproportion"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot stacked bar chart showing cell type proportions across groups.",
  "examples": [],
  "related": []
 },
 "ov.pl.plot_embedding_celltype": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "plot_embedding_celltype",
  "aliases": [
   "plot_embedding_celltype",
   "ov.pl.plot_embedding_celltype",
   "plot embedding celltype"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create combined embedding plot with cell type legend and counts.",
  "examples": [],
  "related": []
 },
 "ov.pl.plot_flowsig_network": {
  "_module": "omicverse.pl._flowsig",
  "_name": "plot_flowsig_network",
  "aliases": [
   "plot_flowsig_network",
   "ov.pl.plot_flowsig_network",
   "plot flowsig network",
   "visualize the flowsig network",
   "可视化"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a flowsig network visualization showing GEM modules and gene flows.",
  "examples": [
   "ov.pl.plot_flowsig_network(flow_network=flow_network, gem_plot=['GEM-2', 'GEM-7', 'GEM-1', 'GEM-3', 'GEM-4', 'GEM-5'], figsize=(8, 4), curve_awarg={'eps': 2}, node_shape={'GEM': '^', 'Sender': 'o', 'Receptor': 'o'}, ylim=(-0.5, 0.5), xlim=(-3, 3))"
  ],
  "related": [
   "ov.external.flowsig.tl.construct_intercellular_flow_network",
   "ov.external.flowsig.tl.apply_biological_flow",
   "ov.external.flowsig.tl.filter_low_confidence_edges"
  ]
 },
 "ov.pl.plot_grouped_fractions": {
  "_module": "omicverse.pl._bulk",
  "_name": "plot_grouped_fractions",
  "aliases": [
   "plot_grouped_fractions",
   "ov.pl.plot_grouped_fractions",
   "plot grouped fractions"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot grouped cell-fraction summaries as stacked bars.",
  "examples": [
   "ov.pl.plot_grouped_fractions(res, bulk_ad.obs, group_key='severity', color_dict=color_dict, agg='mean', normalize=True, figsize=(2, 3))"
  ],
  "related": [
   "ov.bulk.Deconvolution",
   "ov.plt.legend",
   "ov.plt.show"
  ]
 },
 "ov.pl.plot_pca_variance_ratio": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "plot_pca_variance_ratio",
  "aliases": [
   "plot_pca_variance_ratio",
   "ov.pl.plot_pca_variance_ratio",
   "plot pca variance ratio"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot PCA variance ratio to determine optimal number of principal components.",
  "examples": [
   "import omicverse as ov",
   "# Basic PCA variance ratio plot",
   "ov.pp.pca(adata, n_pcs=50)"
  ],
  "related": []
 },
 "ov.pl.plot_set": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "plot_set",
  "aliases": [
   "plot_set",
   "ov.pl.plot_set",
   "plot set"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Configure plotting settings for OmicVerse.",
  "examples": [],
  "related": []
 },
 "ov.pl.plot_spatial": {
  "_module": "omicverse.pl._space",
  "_name": "plot_spatial",
  "aliases": [
   "plot_spatial",
   "ov.pl.plot_spatial",
   "plot spatial"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create spatial plot from Visium data with color gradient and interpolation.",
  "examples": [
   "ov.pl.plot_spatial(adata=decov_obj.adata_cell2location, color=clust_col, labels=clust_labels, show_img=True, style='fast', max_color_quantile=0.992, circle_diameter=4, colorbar_position='right')"
  ],
  "related": [
   "ov.space.crop_space_visium",
   "ov.pl.add_pie2spatial",
   "ov.space.Deconvolution",
   "ov.plt.subplots",
   "ov.space.svg"
  ]
 },
 "ov.pl.plot_stream": {
  "_module": "omicverse.pl._trajectory",
  "_name": "plot_stream",
  "aliases": [
   "plot_stream",
   "ov.pl.plot_stream",
   "plot stream"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot streamlines through a method-aware OV interface.",
  "examples": [
   "ov.pl.plot_stream(stavia, method='stavia', figsize=(5, 5), dpi=100, density_grid=1.0, density_stream=2.5, scatter_size=18, scatter_alpha=0.28, linewidth=0.8)"
  ],
  "related": []
 },
 "ov.pl.plot_text_set": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "plot_text_set",
  "aliases": [
   "plot_text_set",
   "ov.pl.plot_text_set",
   "plot text set"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Format text for plotting by adding line breaks.",
  "examples": [],
  "related": []
 },
 "ov.pl.pyomic_palette": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "pyomic_palette",
  "aliases": [
   "pyomic_palette",
   "ov.pl.pyomic_palette",
   "pyomic palette"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Returns the default OmicVerse color palette.",
  "examples": [],
  "related": []
 },
 "ov.pl.qc": {
  "_module": "omicverse.pl._qc",
  "_name": "qc",
  "aliases": [
   "qc",
   "ov.pl.qc"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot QC-metric distributions to guide threshold choice.",
  "examples": [],
  "related": []
 },
 "ov.pl.rank_genes_groups_dotplot": {
  "_module": "omicverse.pl._dotplot",
  "_name": "rank_genes_groups_dotplot",
  "aliases": [
   "rank_genes_groups_dotplot",
   "ov.pl.rank_genes_groups_dotplot",
   "rank genes groups dotplot",
   "finding marker genes",
   "code https"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a dot plot from rank_genes_groups results.",
  "examples": [
   "ov.pl.rank_genes_groups_dotplot(adata, groupby='leiden', cmap='Spectral_r', key='leiden_ttest', standard_scale='var', n_genes=3)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.single.cosg",
   "ov.utils.gen_mpl_labels",
   "ov.pl.dotplot",
   "ov.plt.tight_layout"
  ]
 },
 "ov.pl.rigor_scatter": {
  "_module": "omicverse.pl._metacell",
  "_name": "rigor_scatter",
  "aliases": [
   "rigor_scatter",
   "ov.pl.rigor_scatter",
   "rigor scatter"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Scatter plot of mcDiv vs metacell size, with the rigor threshold.",
  "examples": [
   "ov.pl.rigor_scatter(rep)"
  ],
  "related": [
   "ov.single.MetaCell",
   "ov.pl.metacell_metrics",
   "ov.pp.preprocess",
   "ov.pl.embedding",
   "ov.pl.metacell_purity_box"
  ]
 },
 "ov.pl.single_group_boxplot": {
  "_module": "omicverse.pl._single",
  "_name": "single_group_boxplot",
  "aliases": [
   "single_group_boxplot",
   "ov.pl.single_group_boxplot",
   "single group boxplot"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "adata (AnnData object): The data object containing the information for plotting. groupby (str): The variable used for grouping the data. color (str): The variable used for coloring the data points. type_color_dict (dict): A dictionary mapping group categories to specific colors. title (str): The title for the plot. ylabel (str): The label for the y-axis. kruskal_test (bool): Whether to perform a Kruskal-Wallis test and display the p-value on the plot. figsize (tuple): The size of the plot figure in inches (width, height). x_ticks_plot (bool): Whether to display x-axis tick labels. legend_plot (bool): Whether to display a legend for the groups. bbox_to_anchor (tuple): The position of the legend bbox (x, y) in axes coordinates. save (bool): Whether to save the plot to a file. point_number (int): The number of data points to be plotted for each group. save_pathway (str): The file path for saving the plot (if save is True). sort (bool): Whether to sort the groups based on their mean values. scatter_kwargs (dict): Additional keyword arguments for customizing the scatter plot. ax (matplotlib.axes.Axes): A pre-existing axes object for plotting (optional).",
  "examples": [
   "ov.pl.single_group_boxplot(adata, groupby='clusters', color='Sox_aucell', type_color_dict=dict(zip(pd.Categorical(adata.obs['clusters']).categories, adata.uns['clusters_colors'])), x_ticks_plot=True, figsize=(5, 2), kruskal_test=True, ylabel='Sox_aucell', legend_plot=False, bbox_to_anchor=(1, 1), title='Expression', scatter_kwargs={'alpha': 0.8, 's': 10, 'marker': 'o'}, point_number=15, sort=False, save=False)"
  ],
  "related": [
   "ov.pl.add_palue",
   "ov.pl.bardotplot",
   "ov.pl.dotplot",
   "ov.pp.preprocess"
  ]
 },
 "ov.pl.stacking_vol": {
  "_module": "omicverse.pl._plot_backend",
  "_name": "stacking_vol",
  "aliases": [
   "stacking_vol",
   "ov.pl.stacking_vol",
   "stacking vol"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create stacked volcano plots for comparing differential expression across multiple datasets.",
  "examples": [],
  "related": []
 },
 "ov.pl.trajectory": {
  "_module": "omicverse.pl._trajectory",
  "_name": "trajectory",
  "aliases": [
   "trajectory",
   "ov.pl.trajectory"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Draw cells in an embedding and overlay a trajectory backbone.",
  "examples": [
   "ov.pl.trajectory(adata, method='paga', basis='X_umap', groups='clusters', color='clusters', title='CellRank development trajectory graph')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.utils.cal_paga",
   "ov.pl.trajectory_overlay",
   "ov.pl.branch_streamplot",
   "ov.plt.show"
  ]
 },
 "ov.pl.trajectory_graph": {
  "_module": "omicverse.pl._trajectory",
  "_name": "trajectory_graph",
  "aliases": [
   "trajectory_graph",
   "ov.pl.trajectory_graph",
   "trajectory graph"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot a method-specific trajectory graph summary.",
  "examples": [
   "ov.pl.trajectory_graph(mono.adata, method='monocle', basis='X_DDRTree', color='subtype', figsize=(3, 3))"
  ],
  "related": [
   "ov.pl.trajectory",
   "ov.pl.trajectory_projection",
   "ov.plt.show"
  ]
 },
 "ov.pl.trajectory_overlay": {
  "_module": "omicverse.pl._trajectory",
  "_name": "trajectory_overlay",
  "aliases": [
   "trajectory_overlay",
   "ov.pl.trajectory_overlay",
   "trajectory overlay"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Overlay a trajectory backbone on an existing embedding axis.",
  "examples": [
   "ov.pl.trajectory_overlay(adata, ax=ax, method='paga', basis='X_umap', groups='clusters')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.utils.cal_paga",
   "ov.pl.trajectory",
   "ov.pl.branch_streamplot",
   "ov.single.dynamic_features"
  ]
 },
 "ov.pl.trajectory_projection": {
  "_module": "omicverse.pl._trajectory",
  "_name": "trajectory_projection",
  "aliases": [
   "trajectory_projection",
   "ov.pl.trajectory_projection",
   "trajectory projection"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot method-specific trajectory curves on an embedding.",
  "examples": [
   "ov.pl.trajectory_projection(mono.adata, method='monocle', basis='X_DDRTree', color='subtype', figsize=(3.5, 3))"
  ],
  "related": [
   "ov.pl.trajectory_graph",
   "ov.pl.embedding",
   "ov.plt.show",
   "ov.plt.subplots"
  ]
 },
 "ov.pl.trajectory_tree": {
  "_module": "omicverse.pl._trajectory",
  "_name": "trajectory_tree",
  "aliases": [
   "trajectory_tree",
   "ov.pl.trajectory_tree",
   "trajectory tree"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Draw a tree-layout trajectory view using real pseudotime on the y-axis.",
  "examples": [
   "ov.pl.trajectory_tree(mono.adata, method='monocle', color='subtype', figsize=(4, 3))"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.branch_streamplot",
   "ov.pl.trajectory_overlay",
   "ov.plt.show",
   "ov.pl.dynamic_heatmap"
  ]
 },
 "ov.pl.tsne": {
  "_module": "omicverse.pl._single",
  "_name": "tsne",
  "aliases": [
   "tsne",
   "ov.pl.tsne"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot t-SNE embedding.",
  "examples": [],
  "related": []
 },
 "ov.pl.umap": {
  "_module": "omicverse.pl._single",
  "_name": "umap",
  "aliases": [
   "umap",
   "ov.pl.umap",
   "below we preview",
   "for small set of categories",
   "additionally we can use the sc",
   "both engines are bit-identical on fp"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Plot UMAP embedding.",
  "examples": [
   "ov.pl.umap(adata, color=['predicted_celltype'], frameon='small', palette=ov.pl.sc_color)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pp.pca",
   "ov.pp.scale",
   "ov.utils.plot_pca_variance_ratio",
   "ov.single.TrajInfer"
  ]
 },
 "ov.pl.upset": {
  "_module": "omicverse.pl._upset",
  "_name": "upset",
  "aliases": [
   "upset",
   "ov.pl.upset",
   "集合字典",
   "对象",
   "例如"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create an UpSet plot to visualize overlaps across multiple sets.",
  "examples": [
   "ov.pl.upset(gene_sets, top_n=15, min_size=1, figsize=(8, 5), style=ov.style)"
  ],
  "related": [
   "ov.plot_set",
   "ov.pl.venn",
   "ov.pl.volcano",
   "ov.pl.boxplot"
  ]
 },
 "ov.pl.venn": {
  "_module": "omicverse.pl._bulk",
  "_name": "venn",
  "aliases": [
   "venn",
   "ov.pl.venn",
   "venn plot"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a Venn diagram to visualize set overlaps.",
  "examples": [
   "ov.pl.venn(sets=sets, palette=ov.pl.sc_color, fontsize=5.5, ax=ax)"
  ],
  "related": [
   "ov.plot_set",
   "ov.read",
   "ov.pl.upset",
   "ov.pl.volcano",
   "ov.pp.qc"
  ]
 },
 "ov.pl.violin": {
  "_module": "omicverse.pl._violin",
  "_name": "violin",
  "aliases": [
   "violin",
   "ov.pl.violin",
   "why this step matters"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Enhanced violin plot compatible with omicverse's interface.",
  "examples": [
   "ov.pl.violin(adata, keys='Sox4', groupby='clusters', figsize=(8, 3), rotation=90, alternating_background=True, add_box=True, use_group_colors_background=True, verbose=False, comparisons=[('Neuroblast', 'OL'), ('Mossy', 'Cck-Tox'), ('nIPC', 'OL')])"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.dotplot",
   "ov.pl.add_density_contour",
   "ov.single.geneset_aucell",
   "ov.style"
  ]
 },
 "ov.pl.volcano": {
  "_module": "omicverse.pl._bulk",
  "_name": "volcano",
  "aliases": [
   "volcano",
   "ov.pl.volcano"
  ],
  "auto_fix": "none",
  "category": "plotting",
  "description": "Create a volcano plot for differential expression analysis.",
  "examples": [
   "ov.pl.volcano(result, pval_name='qvalue', fc_name='log2FoldChange', pval_threshold=0.05, fc_max=1.5, fc_min=-1.5, pval_max=10, FC_max=10, figsize=(4, 4), title='DEGs in Bulk', titlefont={'weight': 'normal', 'size': 14}, up_color='#e25d5d', down_color='#7388c1', normal_color='#d7d7d7', up_fontcolor='#e25d5d', down_fontcolor='#7388c1', normal_fontcolor='#d7d7d7', legend_bbox=(0.8, -0.2), legend_ncol=2, legend_fontsize=12, plot_genes=None, plot_genes_num=10, plot_genes_fontsize=11, ticks_fontsize=12)"
  ],
  "related": [
   "ov.pl.venn",
   "ov.pl.boxplot",
   "ov.pl.add_palue",
   "ov.pl.upset",
   "ov.read"
  ]
 },
 "ov.pp.ambient_negative_marker_check": {
  "_module": "omicverse.pp.ambient._diagnostics",
  "_name": "ambient_negative_marker_check",
  "aliases": [
   "ambient_negative_marker_check",
   "ov.pp.ambient_negative_marker_check",
   "ambient negative marker check"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Check a negative marker drops to ~0 after ambient correction.",
  "examples": [],
  "related": []
 },
 "ov.pp.anndata_to_CPU": {
  "_module": "omicverse.pp._preprocess",
  "_name": "anndata_to_CPU",
  "aliases": [
   "anndata_to_CPU",
   "ov.pp.anndata_to_CPU",
   "anndata to c p u"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Migrate AnnData objects from GPU back to CPU memory after analysis.",
  "examples": [
   "ov.pp.anndata_to_CPU(adata)"
  ],
  "related": [
   "ov.pp.umap",
   "ov.pl.embedding",
   "ov.pp.leiden",
   "ov.pl.ConvexHull"
  ]
 },
 "ov.pp.anndata_to_GPU": {
  "_module": "omicverse.pp._preprocess",
  "_name": "anndata_to_GPU",
  "aliases": [
   "anndata_to_GPU",
   "ov.pp.anndata_to_GPU",
   "anndata to g p u",
   "preprocessing",
   "quantity control"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Migrate AnnData objects to GPU memory for accelerated processing.",
  "examples": [
   "ov.pp.anndata_to_GPU(adata)"
  ],
  "related": [
   "ov.settings.gpu_init",
   "ov.pl.embedding",
   "ov.utils.mde"
  ]
 },
 "ov.pp.binary_search": {
  "_module": "omicverse.pp._recover",
  "_name": "binary_search",
  "aliases": [
   "binary_search",
   "ov.pp.binary_search",
   "binary search"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Infer a size factor from one normalized expression vector.",
  "examples": [],
  "related": []
 },
 "ov.pp.champ": {
  "_module": "omicverse.pp._champ",
  "_name": "champ",
  "aliases": [
   "champ",
   "ov.pp.champ"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Pick the modularity-stablest Leiden partition via CHAMP (Weir et al. 2017).",
  "examples": [
   "ov.pp.champ(adata, n_seeds=20, modularity='cpm', width_metric='log')"
  ],
  "produces": {
   "obs": [
    "champ"
   ],
   "uns": [
    "champ"
   ]
  },
  "related": [
   "ov.es.decoupler",
   "ov.single.auto_resolution",
   "ov.single.NMF",
   "ov.single.CNV"
  ],
  "requires": {
   "obsp": [
    "connectivities"
   ]
  }
 },
 "ov.pp.contamination_report": {
  "_module": "omicverse.pp.ambient._diagnostics",
  "_name": "contamination_report",
  "aliases": [
   "contamination_report",
   "ov.pp.contamination_report",
   "contamination report"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Compact summary of an ambient-correction run.",
  "examples": [],
  "related": []
 },
 "ov.pp.count_integrity_check": {
  "_module": "omicverse.pp.ambient._diagnostics",
  "_name": "count_integrity_check",
  "aliases": [
   "count_integrity_check",
   "ov.pp.count_integrity_check",
   "count integrity check"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Verify corrected counts respect the raw counts.",
  "examples": [],
  "related": []
 },
 "ov.pp.estimate_contamination": {
  "_module": "omicverse.pp.ambient._ambient",
  "_name": "estimate_contamination",
  "aliases": [
   "estimate_contamination",
   "ov.pp.estimate_contamination",
   "estimate contamination"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Estimate the per-cell contamination fraction without correcting.",
  "examples": [],
  "related": []
 },
 "ov.pp.filter_cells": {
  "_module": "omicverse.pp._qc",
  "_name": "filter_cells",
  "aliases": [
   "filter_cells",
   "ov.pp.filter_cells",
   "filter cells",
   "standard preprocessing"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Filter cell outliers based on counts and numbers of genes expressed.",
  "examples": [
   "ov.pp.filter_cells(adata, min_counts=20)"
  ],
  "related": [
   "ov.pp.filter_genes",
   "ov.space.read_visium_10x",
   "ov.space.visium_10x_hd_cellpose_he",
   "ov.space.visium_10x_hd_cellpose_expand",
   "ov.space.visium_10x_hd_cellpose_gex"
  ]
 },
 "ov.pp.filter_genes": {
  "_module": "omicverse.pp._qc",
  "_name": "filter_genes",
  "aliases": [
   "filter_genes",
   "ov.pp.filter_genes",
   "filter genes",
   "standard preprocessing"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Filter genes based on number of cells or counts.",
  "examples": [
   "ov.pp.filter_genes(adata, min_cells=10)"
  ],
  "related": [
   "ov.pp.filter_cells",
   "ov.space.read_visium_10x",
   "ov.space.visium_10x_hd_cellpose_he",
   "ov.space.visium_10x_hd_cellpose_expand",
   "ov.space.subset_window"
  ]
 },
 "ov.pp.highly_variable_features": {
  "_module": "omicverse.pp._preprocess",
  "_name": "highly_variable_features",
  "aliases": [
   "highly_variable_features",
   "ov.pp.highly_variable_features",
   "highly variable features"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Select highly variable features (HVF/HVG) for downstream modeling.",
  "examples": [],
  "produces": {
   "var": [
    "hvf_rank"
   ]
  },
  "related": [],
  "requires": {
   "var": [
    "robust"
   ]
  }
 },
 "ov.pp.highly_variable_genes": {
  "_module": "omicverse.pp._preprocess",
  "_name": "highly_variable_genes",
  "aliases": [
   "highly_variable_genes",
   "ov.pp.highly_variable_genes",
   "highly variable genes"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Annotate highly variable genes (Satija 2015 / Zheng 2017 / Stuart 2019).",
  "examples": [
   "ov.pp.highly_variable_genes(adata, n_top_genes=2000, batch_key=None)"
  ],
  "produces": {
   "var": [
    "highly_variable",
    "means"
   ]
  },
  "related": [
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.pp.filter_genes",
   "ov.pp.normalize_total",
   "ov.pp.log1p"
  ]
 },
 "ov.pp.identify_robust_genes": {
  "_module": "omicverse.pp._preprocess",
  "_name": "identify_robust_genes",
  "aliases": [
   "identify_robust_genes",
   "ov.pp.identify_robust_genes",
   "identify robust genes"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Identify robust genes for downstream HVG selection.",
  "examples": [],
  "produces": {
   "var": [
    "highly_variable_features",
    "n_cells",
    "percent_cells",
    "robust"
   ]
  },
  "related": []
 },
 "ov.pp.leiden": {
  "_module": "omicverse.pp._preprocess",
  "_name": "leiden",
  "aliases": [
   "leiden",
   "ov.pp.leiden",
   "clustering the neighborhood graph",
   "fate gene of lineages",
   "lazy preprocess",
   "聚类",
   "注意",
   "roughly"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "leiden clustering",
  "examples": [
   "ov.pp.leiden(adata, resolution=0.1)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.neighbors",
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pl.embedding",
   "ov.pp.neighbors",
   "ov.pp.umap",
   "ov.pp.pca",
   "ov.pl.spatialseg"
  ],
  "requires": {
   "obsp": [
    "connectivities"
   ]
  }
 },
 "ov.pp.log1p": {
  "_module": "omicverse.pp._normalization",
  "_name": "log1p",
  "aliases": [
   "log1p",
   "ov.pp.log1p",
   "对数变换",
   "变换",
   "standard preprocessing"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Log-transform expression values with ``log(1 + x)``.",
  "examples": [
   "ov.pp.log1p(bdata)"
  ],
  "produces": {
   "uns": [
    "log1p"
   ]
  },
  "related": [
   "ov.pp.normalize_total",
   "ov.pl.embedding",
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.space.svg"
  ]
 },
 "ov.pp.louvain": {
  "_module": "omicverse.pp._preprocess",
  "_name": "louvain",
  "aliases": [
   "louvain",
   "ov.pp.louvain"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Run Louvain clustering on the precomputed kNN graph.",
  "examples": [],
  "produces": {
   "obs": [
    "louvain"
   ]
  },
  "related": [],
  "requires": {
   "obsp": [
    "connectivities"
   ],
   "uns": [
    "neighbors"
   ]
  }
 },
 "ov.pp.mde": {
  "_module": "omicverse.pp._preprocess",
  "_name": "mde",
  "aliases": [
   "mde",
   "ov.pp.mde"
  ],
  "auto_fix": "auto",
  "category": "preprocessing",
  "description": "Run MDE (Minimum Distortion Embedding) from a latent representation.",
  "examples": [
   "ov.pp.mde(adata, use_rep='scaled|original|X_pca')"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "produces": {
   "obsm": [
    "X_mde"
   ]
  },
  "related": [
   "ov.pl.embedding",
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.pp.preprocess",
   "ov.single.batch_correction"
  ],
  "requires": {
   "obsm": [
    "X_pca"
   ]
  }
 },
 "ov.pp.neighbors": {
  "_module": "omicverse.pp._preprocess",
  "_name": "neighbors",
  "aliases": [
   "neighbors",
   "ov.pp.neighbors",
   "preprocess pca cluster",
   "lazy preprocess",
   "main parameters",
   "standard omicverse flow",
   "roughly"
  ],
  "auto_fix": "auto",
  "category": "preprocessing",
  "description": "Compute a neighborhood graph of observations [McInnes18]_.",
  "examples": [
   "ov.pp.neighbors(adata, n_neighbors=15, n_pcs=512, use_rep='X_cast')"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pp.umap",
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.pp.preprocess",
   "ov.pl.embedding"
  ],
  "requires": {
   "obsm": [
    "X_pca"
   ]
  }
 },
 "ov.pp.normalize_pearson_residuals": {
  "_module": "omicverse.pp._preprocess",
  "_name": "normalize_pearson_residuals",
  "aliases": [
   "normalize_pearson_residuals",
   "ov.pp.normalize_pearson_residuals",
   "normalize pearson residuals"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Normalize a count matrix using analytic Pearson residuals (Lause 2021).",
  "examples": [],
  "related": []
 },
 "ov.pp.pca": {
  "_module": "omicverse.pp._preprocess",
  "_name": "pca",
  "aliases": [
   "pca",
   "ov.pp.pca",
   "preprocess pca cluster",
   "data preprocessing",
   "lazy preprocess",
   "principal component analysis",
   "visualize the reference and mapping",
   "standard omicverse flow",
   "预处理",
   "roughly"
  ],
  "auto_fix": "auto",
  "category": "preprocessing",
  "description": "Performs Principal Component Analysis (PCA) on the data stored in a scanpy AnnData object.",
  "examples": [
   "ov.pp.pca(adata, layer='scaled', n_pcs=50)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pp.scale",
   "ov.pp.preprocess",
   "ov.pp.neighbors",
   "ov.pp.qc",
   "ov.pl.embedding"
  ],
  "requires": {
   "layers": [
    "scaled"
   ]
  }
 },
 "ov.pp.plot_contamination": {
  "_module": "omicverse.pp.ambient._plotting",
  "_name": "plot_contamination",
  "aliases": [
   "plot_contamination",
   "ov.pp.plot_contamination",
   "plot contamination"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Plot the per-cell contamination-fraction distribution.",
  "examples": [],
  "related": []
 },
 "ov.pp.preprocess": {
  "_module": "omicverse.pp._preprocess",
  "_name": "preprocess",
  "aliases": [
   "preprocess",
   "ov.pp.preprocess",
   "preprocess pca cluster",
   "data preprocessing",
   "lazy preprocess",
   "standard omicverse flow",
   "预处理",
   "roughly",
   "alpha etc"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Preprocesses the AnnData object adata using either a scanpy or a pearson residuals workflow for size normalization and highly variable genes (HVGs) selection, and calculates signature scores if necessary.",
  "examples": [
   "ov.pp.preprocess(adata, mode='shiftlog|pearson', n_HVGs=2000)"
  ],
  "produces": {
   "layers": [
    "counts"
   ],
   "var": [
    "highly_variable_features",
    "means",
    "residual_variances",
    "variances"
   ]
  },
  "related": [
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.pp.qc",
   "ov.pp.neighbors",
   "ov.read"
  ]
 },
 "ov.pp.qc": {
  "_module": "omicverse.pp._qc",
  "_name": "qc",
  "aliases": [
   "qc",
   "ov.pp.qc",
   "preprocess pca cluster",
   "data preprocessing",
   "preprocessing",
   "quantity control",
   "data preprocess and batch visualize",
   "lazy preprocess",
   "quality control",
   "standard omicverse flow"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Perform quality control on a dictionary of AnnData objects.",
  "examples": [
   "ov.pp.qc(adata, tresh={'mito_perc': 0.05, 'nUMIs': 500, 'detected_genes': 250})"
  ],
  "produces": {
   "obs": [
    "n_counts",
    "n_genes",
    "pct_counts_mt"
   ],
   "var": [
    "mt"
   ]
  },
  "related": [
   "ov.pp.preprocess",
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.plot_set",
   "ov.utils.store_layers"
  ]
 },
 "ov.pp.qc_metrics": {
  "_module": "omicverse.pp._qc",
  "_name": "qc_metrics",
  "aliases": [
   "qc_metrics",
   "ov.pp.qc_metrics",
   "qc metrics"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Compute per-cell QC metrics without filtering.",
  "examples": [],
  "produces": {
   "obs": [
    "detected_genes",
    "mito_perc",
    "nUMIs",
    "pct_counts_hb",
    "pct_counts_mt",
    "pct_counts_ribo"
   ],
   "var": [
    "hb",
    "mt",
    "ribo"
   ]
  },
  "related": []
 },
 "ov.pp.recover_counts": {
  "_module": "omicverse.pp._recover",
  "_name": "recover_counts",
  "aliases": [
   "recover_counts",
   "ov.pp.recover_counts",
   "recover counts"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Given log-normalized gene expression data, recover the raw read/UMI counts by inferring the unknown size factors.",
  "examples": [
   "ov.pp.recover_counts(adata.X, 50 * 10000.0, 50 * 100000.0, log_base=None, chunk_size=10000)"
  ],
  "related": [
   "ov.settings.cpu_gpu_mixed_init",
   "ov.pl.pca",
   "ov.pl.umap",
   "ov.pp.mde",
   "ov.datasets.download_data_requests"
  ]
 },
 "ov.pp.regress": {
  "_module": "omicverse.pp._preprocess",
  "_name": "regress",
  "aliases": [
   "regress",
   "ov.pp.regress"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Regress out technical covariates from each gene.",
  "examples": [],
  "produces": {
   "layers": [
    "regressed"
   ]
  },
  "related": [],
  "requires": {
   "obs": [
    "mito_perc",
    "nUMIs"
   ]
  }
 },
 "ov.pp.regress_and_scale": {
  "_module": "omicverse.pp._preprocess",
  "_name": "regress_and_scale",
  "aliases": [
   "regress_and_scale",
   "ov.pp.regress_and_scale",
   "regress and scale"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Scale the regressed layer and store it as a new analysis layer.",
  "examples": [],
  "produces": {
   "layers": [
    "regressed_and_scaled"
   ]
  },
  "related": [],
  "requires": {
   "layers": [
    "regressed"
   ]
  }
 },
 "ov.pp.remove_ambient": {
  "_module": "omicverse.pp.ambient._ambient",
  "_name": "remove_ambient",
  "aliases": [
   "remove_ambient",
   "ov.pp.remove_ambient",
   "remove ambient"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Remove ambient (\"soup\") RNA contamination from droplet scRNA-seq.",
  "examples": [],
  "related": []
 },
 "ov.pp.remove_cc_genes": {
  "_module": "omicverse.pp._preprocess",
  "_name": "remove_cc_genes",
  "aliases": [
   "remove_cc_genes",
   "ov.pp.remove_cc_genes",
   "remove cc genes"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Remove cell-cycle-correlated genes from ``highly_variable_features``.",
  "examples": [],
  "related": [],
  "requires": {
   "var": [
    "highly_variable_features"
   ]
  }
 },
 "ov.pp.scale": {
  "_module": "omicverse.pp._preprocess",
  "_name": "scale",
  "aliases": [
   "scale",
   "ov.pp.scale",
   "preprocess pca cluster",
   "data preprocessing",
   "principal component analysis",
   "lazy preprocess",
   "scale the data",
   "visualize the reference and mapping",
   "standard omicverse flow",
   "预处理"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Scale the input AnnData object.",
  "examples": [
   "ov.pp.scale(adata)"
  ],
  "produces": {
   "layers": [
    "scaled"
   ]
  },
  "related": [
   "ov.pp.pca",
   "ov.pp.preprocess",
   "ov.pp.qc",
   "ov.pp.neighbors",
   "ov.pp.umap"
  ]
 },
 "ov.pp.score_genes_cell_cycle": {
  "_module": "omicverse.pp._preprocess",
  "_name": "score_genes_cell_cycle",
  "aliases": [
   "score_genes_cell_cycle",
   "ov.pp.score_genes_cell_cycle",
   "score genes cell cycle",
   "score cell cyle"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Score cell cycle phases using predefined or custom gene sets.",
  "examples": [
   "ov.pp.score_genes_cell_cycle(adata_raw, species='human')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.mde",
   "ov.pp.leiden",
   "ov.single.auto_resolution"
  ]
 },
 "ov.pp.scrublet": {
  "_module": "omicverse.pp._scrublet",
  "_name": "scrublet",
  "aliases": [
   "scrublet",
   "ov.pp.scrublet"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Predict cell doublets using Scrublet with optional GPU acceleration.",
  "examples": [],
  "produces": {
   "obs": [
    "doublet_score",
    "predicted_doublet"
   ],
   "uns": [
    "scrublet"
   ]
  },
  "related": []
 },
 "ov.pp.scrublet_simulate_doublets": {
  "_module": "omicverse.pp._scrublet",
  "_name": "scrublet_simulate_doublets",
  "aliases": [
   "scrublet_simulate_doublets",
   "ov.pp.scrublet_simulate_doublets",
   "scrublet simulate doublets"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Simulate synthetic doublets from random cell pairs.",
  "examples": [],
  "related": []
 },
 "ov.pp.select_hvf_pegasus": {
  "_module": "omicverse.pp._preprocess",
  "_name": "select_hvf_pegasus",
  "aliases": [
   "select_hvf_pegasus",
   "ov.pp.select_hvf_pegasus",
   "select hvf pegasus"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Select highly variable features with the Pegasus strategy.",
  "examples": [],
  "produces": {
   "var": [
    "hvf_loess",
    "hvf_rank"
   ]
  },
  "related": [],
  "requires": {
   "var": [
    "robust"
   ]
  }
 },
 "ov.pp.sude": {
  "_module": "omicverse.pp._sude",
  "_name": "sude",
  "aliases": [
   "sude",
   "ov.pp.sude"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "SUDE (Scalable Unsupervised Dimensionality reduction via Embedding) dimensionality reduction.",
  "examples": [
   "import omicverse as ov",
   "adata = ov.datasets.pbmc3k()",
   "ov.pp.sude(adata)"
  ],
  "produces": {
   "obsm": [
    "X_sude"
   ]
  },
  "related": []
 },
 "ov.pp.tsne": {
  "_module": "omicverse.pp._preprocess",
  "_name": "tsne",
  "aliases": [
   "tsne",
   "ov.pp.tsne"
  ],
  "auto_fix": "none",
  "category": "preprocessing",
  "description": "Compute t-SNE coordinates for cells, dispatching by ``ov.settings.mode``.",
  "examples": [
   "ov.pp.tsne(ev1, use_rep='scaled|original|X_pca', n_pcs=30)"
  ],
  "produces": {
   "obsm": [
    "X_tsne"
   ]
  },
  "related": [],
  "requires": {
   "obsm": [
    "X_pca"
   ]
  }
 },
 "ov.pp.umap": {
  "_module": "omicverse.pp._preprocess",
  "_name": "umap",
  "aliases": [
   "umap",
   "ov.pp.umap",
   "uncorrected baseline",
   "lazy preprocess",
   "standard omicverse flow"
  ],
  "auto_fix": "escalate",
  "category": "preprocessing",
  "description": "Compute UMAP embedding, dispatching to the best backend for ``ov.settings.mode``.",
  "examples": [
   "ov.pp.umap(adata)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.neighbors",
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pp.neighbors",
   "ov.pp.pca",
   "ov.pl.embedding",
   "ov.pp.scale",
   "ov.pp.leiden"
  ],
  "requires": {
   "obsp": [
    "connectivities"
   ],
   "uns": [
    "neighbors"
   ]
  }
 },
 "ov.single.Annotation": {
  "_module": "omicverse.single._annotation",
  "_name": "Annotation",
  "aliases": [
   "Annotation",
   "ov.single.Annotation",
   "annotation",
   "automated annotation",
   "scsa automated annotation",
   "load ref dataset"
  ],
  "auto_fix": "escalate",
  "category": "single",
  "description": "Unified single-cell annotation manager for cell-type labeling.",
  "examples": [
   "ov.single.Annotation(adata)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.neighbors",
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pp.leiden",
   "ov.pp.umap",
   "ov.pl.umap",
   "ov.pl.embedding",
   "ov.datasets.pbmc3k"
  ]
 },
 "ov.single.AnnotationRef": {
  "_module": "omicverse.single._annotation_ref",
  "_name": "AnnotationRef",
  "aliases": [
   "AnnotationRef",
   "ov.single.AnnotationRef",
   "annotation ref"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Reference-based label transfer helper for single-cell annotation.",
  "examples": [
   "ov.single.AnnotationRef(adata_query=adata, adata_ref=adata_ref, celltype_key='cell_type')"
  ],
  "related": [
   "ov.np.log1p",
   "ov.pl.embedding",
   "ov.pp.mde",
   "ov.pp.recover_counts"
  ]
 },
 "ov.single.Augur": {
  "_module": "omicverse.single._augur",
  "_name": "Augur",
  "aliases": [
   "Augur",
   "ov.single.Augur",
   "augur"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Cell type prioritization via machine-learning cross-validation.",
  "examples": [
   "augur = ov.single.Augur(adata, label_col='condition', cell_type_col='cell_type')",
   "augur.run(n_subsamples=50)",
   "augur.plot_lollipop()"
  ],
  "related": []
 },
 "ov.single.CNV": {
  "_module": "omicverse.single._cnv",
  "_name": "CNV",
  "aliases": [
   "CNV",
   "ov.single.CNV",
   "c n v",
   "after cnv",
   "copykat same plot calls work unchanged"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Single-cell CNV inference dispatcher.",
  "examples": [
   "ov.single.CNV(adata, method='copykat')"
  ],
  "related": [
   "ov.pl.cnv_heatmap",
   "ov.plot_set",
   "ov.pp.champ",
   "ov.single.auto_resolution",
   "ov.single.NMF"
  ]
 },
 "ov.single.CellOntologyMapper": {
  "_module": "omicverse.single._cellmatch",
  "_name": "CellOntologyMapper",
  "aliases": [
   "CellOntologyMapper",
   "ov.single.CellOntologyMapper",
   "cell ontology mapper",
   "prepare the cellontologymapper"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Map free-text cell-type annotations to the Cell Ontology (CL) via NLP.",
  "examples": [
   "ov.single.CellOntologyMapper(cl_obo_file='new_ontology/cl.json', model_name='sentence-transformers/all-MiniLM-L6-v2', local_model_dir='./my_models')"
  ],
  "related": [
   "ov.single.download_cl"
  ]
 },
 "ov.single.CellVote": {
  "_module": "omicverse.single._cellvote",
  "_name": "CellVote",
  "aliases": [
   "CellVote",
   "ov.single.CellVote",
   "cell vote"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Ensemble cell-type annotation manager with multiple backends.",
  "examples": [
   "ov.single.CellVote(adata)"
  ],
  "related": [
   "ov.single.get_celltype_marker"
  ]
 },
 "ov.single.DCT": {
  "_module": "omicverse.single._deg_ct",
  "_name": "DCT",
  "aliases": [
   "DCT",
   "ov.single.DCT",
   "d c t",
   "dct with sccoda",
   "differential abundance testing with glm",
   "tutorials could be found in https"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Differential cell-type abundance testing wrapper.",
  "examples": [
   "ov.single.DCT(adata, condition='condition', ctrl_group='Control', test_group='Salmonella', cell_type_key='cell_label', method='sccoda', sample_key='batch')"
  ],
  "related": [
   "ov.pp.preprocess",
   "ov.settings.cpu_gpu_mixed_init",
   "ov.single.DEG",
   "ov.style",
   "ov.plt.show"
  ]
 },
 "ov.single.DEG": {
  "_module": "omicverse.single._deg_ct",
  "_name": "DEG",
  "aliases": [
   "DEG",
   "ov.single.DEG",
   "d e g",
   "deg with wilcoxon t-test",
   "deg with memento"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Differential gene-expression testing wrapper for single-cell datasets.",
  "examples": [
   "ov.single.DEG(adata, condition='condition', ctrl_group='Control', test_group='Treatment')"
  ],
  "related": [
   "ov.alignment.STAR",
   "ov.alignment.featureCount",
   "ov.alignment.single",
   "ov.single.DCT",
   "ov.style"
  ]
 },
 "ov.single.Drug_Response": {
  "_module": "omicverse.single._scdrug",
  "_name": "Drug_Response",
  "aliases": [
   "Drug_Response",
   "ov.single.Drug_Response",
   "drug response"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Predict drug sensitivity from single-cell transcriptomes using CaDRReS models.",
  "examples": [
   "ov.single.Drug_Response(adata, scriptpath='CaDRReS-Sc', modelpath='models/', output='result')"
  ],
  "related": [
   "ov.utils.download_GDSC_data",
   "ov.utils.download_CaDRReS_model",
   "ov.single.autoResolution"
  ]
 },
 "ov.single.Fate": {
  "_module": "omicverse.single._cellfategenie",
  "_name": "Fate",
  "aliases": [
   "Fate",
   "ov.single.Fate",
   "fate",
   "initialize the timing model"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Adaptive ridge-regression framework for pseudotime-associated gene discovery.",
  "examples": [
   "ov.single.Fate(adata, pseudotime='palantir_pseudotime')"
  ],
  "related": [
   "ov.ov_plot_set",
   "ov.read",
   "ov.pl.embedding",
   "ov.utils.plot_heatmap",
   "ov.pp.leiden"
  ]
 },
 "ov.single.GLUE_pair": {
  "_module": "omicverse.single._mofa",
  "_name": "GLUE_pair",
  "aliases": [
   "GLUE_pair",
   "ov.single.GLUE_pair",
   "g l u e pair",
   "pair the omics"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Pair RNA and ATAC cells using GLUE latent embeddings and neighbor matching.",
  "examples": [
   "ov.single.GLUE_pair(rna, atac)"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.read",
   "ov.single.pyMOFA",
   "ov.single.pyMOFAART"
  ]
 },
 "ov.single.MetaCell": {
  "_module": "omicverse.single._metacell",
  "_name": "MetaCell",
  "aliases": [
   "MetaCell",
   "ov.single.MetaCell",
   "meta cell",
   "constructing metacellular object",
   "three random flavours on this dataset",
   "on this dataset leiden resolution",
   "leiden-vs-celltype agreement of"
  ],
  "auto_fix": "escalate",
  "category": "single",
  "description": "Unified metacell wrapper with dispatchable backends.",
  "examples": [
   "ov.single.MetaCell(adata, use_rep='scaled|original|X_pca', n_metacells=150, use_gpu=True)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.neighbors",
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "produces": {
   "obs": [
    "metacell_conf",
    "metacell_id"
   ],
   "obsm": [
    "X_metacell",
    "metacell_soft"
   ],
   "uns": [
    "metacell"
   ]
  },
  "related": [
   "ov.pp.pca",
   "ov.pp.neighbors",
   "ov.pp.umap",
   "ov.pl.embedding",
   "ov.pl.metacell_metrics"
  ]
 },
 "ov.single.MetaTiME": {
  "_module": "omicverse.single._anno",
  "_name": "MetaTiME",
  "aliases": [
   "MetaTiME",
   "ov.single.MetaTiME",
   "meta ti m e",
   "metetime model init"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "MetaTiME wrapper for tumor microenvironment cell-state annotation.",
  "examples": [
   "ov.single.MetaTiME(adata, mode='table')"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.mde"
  ]
 },
 "ov.single.Metabolism": {
  "_module": "omicverse.single._metabolism",
  "_name": "Metabolism",
  "aliases": [
   "Metabolism",
   "ov.single.Metabolism",
   "metabolism"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Single-cell metabolic-state inference dispatcher.",
  "examples": [
   "ov.single.Metabolism(adata, method='scmetabolism')"
  ],
  "related": [
   "ov.pl.embedding"
  ]
 },
 "ov.single.MetaboliteCCC": {
  "_module": "omicverse.single._metabolism",
  "_name": "MetaboliteCCC",
  "aliases": [
   "MetaboliteCCC",
   "ov.single.MetaboliteCCC",
   "metabolite c c c"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Metabolite-mediated cell-cell communication (MEBOCOST).",
  "examples": [
   "ov.single.MetaboliteCCC(adata, group_key='celltype')"
  ],
  "related": [
   "ov.plot_set",
   "ov.datasets.metabolism_hnsc",
   "ov.pl.ccc_heatmap"
  ]
 },
 "ov.single.Monocle": {
  "_module": "omicverse.single._monocle",
  "_name": "Monocle",
  "aliases": [
   "Monocle",
   "ov.single.Monocle",
   "monocle"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Monocle2-style single-cell trajectory analysis.",
  "examples": [
   "mono = ov.single.Monocle(adata)",
   "mono.preprocess()              # size factors + dispersions",
   "mono.select_ordering_genes()   # high-variance gene selection"
  ],
  "related": []
 },
 "ov.single.SCENIC": {
  "_module": "omicverse.single._scenic",
  "_name": "SCENIC",
  "aliases": [
   "SCENIC",
   "ov.single.SCENIC",
   "s c e n i c",
   "对象",
   "creating the scenic analysis object",
   "key parameters",
   "注释文件",
   "可选参数",
   "database loading",
   "during initialization the scenic object"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "omicverse callable ov.single.SCENIC (no docstring summary available)",
  "examples": [
   "ov.single.SCENIC(adata=adata, species='mm10', n_jobs=8)"
  ],
  "related": [
   "ov.single.mouse_hsc_nestorowa16",
   "ov.pl.embedding",
   "ov.utils.save",
   "ov.utils.load"
  ]
 },
 "ov.single.StaVIA": {
  "_module": "omicverse.single._stavia",
  "_name": "StaVIA",
  "aliases": [
   "StaVIA",
   "ov.single.StaVIA",
   "sta v i a",
   "构建并运行模型"
  ],
  "auto_fix": "escalate",
  "category": "single",
  "description": "AnnData-native wrapper around the StaVIA/VIA backend.",
  "examples": [
   "ov.single.StaVIA(adata, use_rep=use_rep, n_comps=ncomps, basis=basis, cluster_key=clusters, spatial_key=None, time_key=None, sample_key=None, key_added='stavia', root=root, knn=knn, random_seed=random_seed, memory=memory, dataset='group', num_threads=1, n_iter_leiden=5, small_pop=5, num_mcmc_simulations=200, edgepruning_clustering_resolution=0.15, cluster_graph_pruning=0.15, resolution_parameter=1.5)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.neighbors",
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pl.embedding",
   "ov.pp.neighbors",
   "ov.pp.umap"
  ]
 },
 "ov.single.TrajInfer": {
  "_module": "omicverse.single._traj",
  "_name": "TrajInfer",
  "aliases": [
   "TrajInfer",
   "ov.single.TrajInfer",
   "traj infer",
   "slingshot",
   "diffusion map",
   "palantir",
   "这里使用",
   "构建轨迹推断对象"
  ],
  "auto_fix": "auto",
  "category": "single",
  "description": "Trajectory inference class for single-cell data analysis.",
  "examples": [
   "ov.single.TrajInfer(adata, basis='X_umap', groupby='clusters', use_rep='scaled|original|X_pca', n_comps=50)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pp.pca",
   "ov.utils.plot_pca_variance_ratio",
   "ov.pl.umap",
   "ov.pl.embedding",
   "ov.utils.cal_paga"
  ]
 },
 "ov.single.Velo": {
  "_module": "omicverse.single._velo",
  "_name": "Velo",
  "aliases": [
   "Velo",
   "ov.single.Velo",
   "velo",
   "原生",
   "多个",
   "同时",
   "参数也可以传入多个",
   "参数也",
   "传入多个",
   "组合扰动通常",
   "探索协同调控"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "RNA velocity analysis wrapper for directional cell-state transition inference.",
  "examples": [
   "ov.single.Velo(adata)"
  ],
  "related": [
   "ov.plt.figure",
   "ov.plt.subplot",
   "ov.pl.embedding",
   "ov.plot_set",
   "ov.single.velocity"
  ]
 },
 "ov.single.annotate_ev_subtype": {
  "_module": "omicverse.single.ev._annotate",
  "_name": "annotate_ev_subtype",
  "aliases": [
   "annotate_ev_subtype",
   "ov.single.annotate_ev_subtype",
   "annotate ev subtype"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Assign each EV to a tetraspanin-defined surface subset.",
  "examples": [],
  "related": []
 },
 "ov.single.autoResolution": {
  "_module": "omicverse.single._scdrug",
  "_name": "autoResolution",
  "aliases": [
   "autoResolution",
   "ov.single.autoResolution",
   "auto resolution"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Automatically determine clustering resolution.",
  "examples": [
   "ov.single.autoResolution(adata, cpus=4)"
  ],
  "related": [
   "ov.utils.get_gene_annotation",
   "ov.utils.download_GDSC_data",
   "ov.utils.download_CaDRReS_model",
   "ov.single.Drug_Response"
  ]
 },
 "ov.single.auto_resolution": {
  "_module": "omicverse.single._autoresolution",
  "_name": "auto_resolution",
  "aliases": [
   "auto_resolution",
   "ov.single.auto_resolution",
   "auto resolution"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Pick the most reproducible Leiden resolution via null-adjusted bootstrap-ARI (Lange, Roth, Braun & Buhmann, *Neural Computation* 2004).",
  "examples": [
   "ov.single.auto_resolution(adata, method='champ')"
  ],
  "related": [
   "ov.es.decoupler",
   "ov.pp.champ",
   "ov.single.NMF",
   "ov.single.CNV",
   "ov.pl.cnv_heatmap"
  ]
 },
 "ov.single.batch_correction": {
  "_module": "omicverse.single._batch",
  "_name": "batch_correction",
  "aliases": [
   "batch_correction",
   "ov.single.batch_correction",
   "batch correction",
   "run ov",
   "cellanova",
   "concord",
   "per-method tutorial"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Run batch-effect correction for single-cell data integration.",
  "examples": [
   "ov.single.batch_correction(adata, batch_key='batch', methods='CCA')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.utils.mde",
   "ov.pp.umap",
   "ov.pp.neighbors",
   "ov.pp.pca"
  ]
 },
 "ov.single.classify_markers": {
  "_module": "omicverse.single.ev._annotate",
  "_name": "classify_markers",
  "aliases": [
   "classify_markers",
   "ov.single.classify_markers",
   "classify markers"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Classify ``var`` proteins into MISEV2023 marker categories.",
  "examples": [],
  "related": []
 },
 "ov.single.coexpression_network": {
  "_module": "omicverse.single.ev._coloc",
  "_name": "coexpression_network",
  "aliases": [
   "coexpression_network",
   "ov.single.coexpression_network",
   "coexpression network"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Marker-marker co-occurrence graph from single-EV colocalization.",
  "examples": [],
  "related": []
 },
 "ov.single.colocalization": {
  "_module": "omicverse.single.ev._coloc",
  "_name": "colocalization",
  "aliases": [
   "colocalization",
   "ov.single.colocalization"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Pairwise / multi-way marker colocalization across single EVs.",
  "examples": [],
  "related": []
 },
 "ov.single.colocalization_plot": {
  "_module": "omicverse.single.ev._coloc",
  "_name": "colocalization_plot",
  "aliases": [
   "colocalization_plot",
   "ov.single.colocalization_plot",
   "colocalization plot"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Colocalization heatmap from a :func:`colocalization` result.",
  "examples": [],
  "related": []
 },
 "ov.single.compare_metacell_backends": {
  "_module": "omicverse.single._metacell",
  "_name": "compare_metacell_backends",
  "aliases": [
   "compare_metacell_backends",
   "ov.single.compare_metacell_backends",
   "compare metacell backends"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Side-by-side benchmark for the user's own data.",
  "examples": [
   "ov.single.compare_metacell_backends(adata, backends=['seacells', 'metaq', 'supercell', 'kmeans', 'random', 'geosketch'], n_metacells=N_METACELLS, use_rep='X_pca', layer='counts', layer_lognorm='lognorm', eval_label='clusters', n_rigor_rep=30, random_state=RANDOM_STATE, train_epoch=40, warm_epochs=5)"
  ],
  "related": [
   "ov.single.MetaCell",
   "ov.pp.neighbors",
   "ov.pp.umap",
   "ov.pl.embedding",
   "ov.pp.pca"
  ]
 },
 "ov.single.contaminant_score": {
  "_module": "omicverse.single.ev._qc",
  "_name": "contaminant_score",
  "aliases": [
   "contaminant_score",
   "ov.single.contaminant_score",
   "contaminant score"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Score MISEV2023 co-isolated / organelle contamination.",
  "examples": [],
  "related": []
 },
 "ov.single.convert_human_to_mouse_network": {
  "_module": "omicverse.single._cefcon",
  "_name": "convert_human_to_mouse_network",
  "aliases": [
   "convert_human_to_mouse_network",
   "ov.single.convert_human_to_mouse_network",
   "convert human to mouse network"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Convert a human-symbol interaction network to mouse symbols.",
  "examples": [
   "ov.single.convert_human_to_mouse_network(prior_network, server_name='asia')"
  ],
  "related": [
   "ov.plot_set",
   "ov.single.mouse_hsc_nestorowa16",
   "ov.single.load_human_prior_interaction_network",
   "ov.read",
   "ov.single.pyCEFCON"
  ]
 },
 "ov.single.cosg": {
  "_module": "omicverse.single._cosg",
  "_name": "cosg",
  "aliases": [
   "cosg",
   "ov.single.cosg",
   "code https",
   "论文",
   "代码"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Identify cluster-specific marker genes with COSG.",
  "examples": [
   "ov.single.cosg(adata, key_added='leiden_cosg', groupby='leiden')"
  ],
  "produces": {
   "uns": [
    "rank_genes_groups"
   ]
  },
  "related": [
   "ov.utils.gen_mpl_labels",
   "ov.pl.rank_genes_groups_dotplot",
   "ov.utils.plot_ConvexHull",
   "ov.utils.embedding",
   "ov.utils.stacking_vol"
  ]
 },
 "ov.single.cytotrace2": {
  "_module": "omicverse.single._cytotrace2",
  "_name": "cytotrace2",
  "aliases": [
   "cytotrace2",
   "ov.single.cytotrace2"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Predict developmental potency with CytoTRACE2.",
  "examples": [
   "ov.single.cytotrace2(adata, use_model_dir='cymodels/5_models_weights', species='mouse', batch_size=10000, smooth_batch_size=1000, disable_parallelization=False, max_cores=None, max_pcs=200, seed=14, output_dir='cytotrace2_results')"
  ],
  "related": [
   "ov.utils.embedding",
   "ov.plot_set",
   "ov.datasets.download_data"
  ]
 },
 "ov.single.detect_doublets": {
  "_module": "omicverse.single.ev._qc",
  "_name": "detect_doublets",
  "aliases": [
   "detect_doublets",
   "ov.single.detect_doublets",
   "detect doublets"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Flag multi-vesicle / barcode-collision artifacts.",
  "examples": [],
  "related": []
 },
 "ov.single.differential_abundance": {
  "_module": "omicverse.single.ev._markers",
  "_name": "differential_abundance",
  "aliases": [
   "differential_abundance",
   "ov.single.differential_abundance",
   "differential abundance"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Per-protein differential abundance between two conditions.",
  "examples": [],
  "related": []
 },
 "ov.single.differential_metabolism": {
  "_module": "omicverse.single._metabolism",
  "_name": "differential_metabolism",
  "aliases": [
   "differential_metabolism",
   "ov.single.differential_metabolism",
   "differential metabolism"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Differential metabolic features between two groups of cells.",
  "examples": [
   "ov.single.differential_metabolism(adata, groupby='malignant', group1='Malignant')"
  ],
  "related": []
 },
 "ov.single.differential_subpopulation": {
  "_module": "omicverse.single.ev._markers",
  "_name": "differential_subpopulation",
  "aliases": [
   "differential_subpopulation",
   "ov.single.differential_subpopulation",
   "differential subpopulation"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Test EV-subpopulation frequency shifts between two conditions.",
  "examples": [],
  "related": []
 },
 "ov.single.download_cellphonedb_database": {
  "_module": "omicverse.single._cpdb",
  "_name": "download_cellphonedb_database",
  "aliases": [
   "download_cellphonedb_database",
   "ov.single.download_cellphonedb_database",
   "download cellphonedb database"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Download CellPhoneDB database with fallback URLs.",
  "examples": [],
  "related": []
 },
 "ov.single.download_cl": {
  "_module": "omicverse.single._cellmatch",
  "_name": "download_cl",
  "aliases": [
   "download_cl",
   "ov.single.download_cl",
   "download cl",
   "download the cl model",
   "蓝奏云"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "📥 Download Cell Ontology file from multiple sources with automatic fallback",
  "examples": [
   "ov.single.download_cl(output_dir='new_ontology', filename='cl.json')"
  ],
  "related": [
   "ov.single.CellOntologyMapper"
  ]
 },
 "ov.single.dynamic_features": {
  "_module": "omicverse.single._dynamic_features",
  "_name": "dynamic_features",
  "aliases": [
   "dynamic_features",
   "ov.single.dynamic_features",
   "dynamic features",
   "给原始散点着色",
   "趋势",
   "并用",
   "使用",
   "可以沿",
   "拟合",
   "展示分支相关的表达变化",
   "展示分支相关"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Fit GAM-based pseudotime trends for one or more datasets or groups.",
  "examples": [
   "ov.single.dynamic_features(adata_beta, genes=['Pdx1', 'Ins1', 'Ins2', 'Sox9'], pseudotime='development_pseudotime', layer='Ms', distribution='normal', link='identity', n_splines=8, store_raw=True, raw_obs_keys=['clusters'])"
  ],
  "related": [
   "ov.pl.dynamic_trends",
   "ov.pl.branch_streamplot",
   "ov.pl.dynamic_heatmap",
   "ov.pl.embedding",
   "ov.utils.plot_paga"
  ]
 },
 "ov.single.ev_summary": {
  "_module": "omicverse.single.ev._report",
  "_name": "ev_summary",
  "aliases": [
   "ev_summary",
   "ov.single.ev_summary",
   "ev summary"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Compact run summary of a single-EV proteomics dataset.",
  "examples": [],
  "related": []
 },
 "ov.single.factor_correlation": {
  "_module": "omicverse.single._mofa",
  "_name": "factor_correlation",
  "aliases": [
   "factor_correlation",
   "ov.single.factor_correlation",
   "factor correlation"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Score MOFA-factor enrichment across annotated groups.",
  "examples": [
   "ov.single.factor_correlation(adata=rna, cluster='cell_type', factor_list=[1, 2, 3, 4, 5])"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.read",
   "ov.single.factor_exact",
   "ov.single.get_weights",
   "ov.single.pyMOFAART"
  ]
 },
 "ov.single.factor_exact": {
  "_module": "omicverse.single._mofa",
  "_name": "factor_exact",
  "aliases": [
   "factor_exact",
   "ov.single.factor_exact",
   "factor exact"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Add MOFA latent factors from model file into ``adata.obs``.",
  "examples": [
   "ov.single.factor_exact(rna, hdf5_path='data/sample/MOFA_POS.hdf5')"
  ],
  "related": [
   "ov.single.pyMOFA",
   "ov.utils.ov_plot_set",
   "ov.utils.read",
   "ov.single.factor_correlation",
   "ov.single.get_weights"
  ]
 },
 "ov.single.find_markers": {
  "_module": "omicverse.single._markers",
  "_name": "find_markers",
  "aliases": [
   "find_markers",
   "ov.single.find_markers",
   "find markers",
   "alpha etc"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Find marker genes for each cluster / group in single-cell data.",
  "examples": [
   "ov.single.find_markers(ad_mc_de, groupby='clusters', method='wilcoxon', key_added='rank_genes_groups', pts=True, use_gpu=False)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pp.neighbors",
   "ov.pp.umap",
   "ov.single.get_markers",
   "ov.pl.markers_dotplot"
  ]
 },
 "ov.single.flowsom": {
  "_module": "omicverse.single.ev._cluster",
  "_name": "flowsom",
  "aliases": [
   "flowsom",
   "ov.single.flowsom"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Native FlowSOM clustering of EV subpopulations.",
  "examples": [],
  "related": []
 },
 "ov.single.format_liana_results": {
  "_module": "omicverse.single._liana",
  "_name": "format_liana_results",
  "aliases": [
   "format_liana_results",
   "ov.single.format_liana_results",
   "format liana results"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Format LIANA results into the communication AnnData expected by ``ov.pl.ccc_*``.",
  "examples": [],
  "related": []
 },
 "ov.single.gene_trends": {
  "_module": "omicverse.single._cellfategenie",
  "_name": "gene_trends",
  "aliases": [
   "gene_trends",
   "ov.single.gene_trends",
   "gene trends"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Fit and visualize smooth feature trends along pseudotime.",
  "examples": [
   "ov.single.gene_trends(adata_aucs, 'pt_via', var_name)"
  ],
  "related": [
   "ov.utils.geneset_prepare",
   "ov.single.pathway_aucell_enrichment",
   "ov.single.cellfategenie",
   "ov.utils.plot_heatmap",
   "ov.utils.geneset_wordcloud"
  ]
 },
 "ov.single.generate_scRNA_report": {
  "_module": "omicverse.single._lazy_report",
  "_name": "generate_scRNA_report",
  "aliases": [
   "generate_scRNA_report",
   "ov.single.generate_scRNA_report",
   "generate sc r n a report",
   "report generation"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Generate a MultiQC-style HTML report for single-cell RNA-seq analysis.",
  "examples": [
   "ov.single.generate_scRNA_report(adata, species='mouse', sample_key='batch', output_path='scRNA_analysis_report.html')"
  ],
  "related": [
   "ov.single.lazy",
   "ov.plot_set",
   "ov.pl.embedding",
   "ov.generate_reference_table"
  ]
 },
 "ov.single.geneset_aucell": {
  "_module": "omicverse.single._scgsea",
  "_name": "geneset_aucell",
  "aliases": [
   "geneset_aucell",
   "ov.single.geneset_aucell",
   "geneset aucell",
   "additionally we can use the sc"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Calculate the AUC-ell score for a given gene set.",
  "examples": [
   "ov.single.geneset_aucell(adata, geneset_name='Sox', geneset=['Sox17', 'Sox4', 'Sox7', 'Sox18', 'Sox5'])"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.add_density_contour",
   "ov.style",
   "ov.pl.violin",
   "ov.pl.bardotplot"
  ]
 },
 "ov.single.get_celltype_marker": {
  "_module": "omicverse.single._anno",
  "_name": "get_celltype_marker",
  "aliases": [
   "get_celltype_marker",
   "ov.single.get_celltype_marker",
   "get celltype marker",
   "get genes for each cluster automatically"
  ],
  "auto_fix": "auto",
  "category": "single",
  "description": "Get marker genes for each cluster/cell type.",
  "examples": [
   "ov.single.get_celltype_marker(adata, clustertype='leiden', rank=True, key='rank_genes_groups', foldchange=2, topgenenumber=5)"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "produces": {
   "uns": [
    "rank_genes_groups"
   ]
  },
  "related": [
   "ov.utils.palette",
   "ov.pl.embedding",
   "ov.single.gptcelltype",
   "ov.utils.embedding",
   "ov.pl.cell_cor_heatmap"
  ]
 },
 "ov.single.get_cluster_celltype": {
  "_module": "omicverse.single._cellvote",
  "_name": "get_cluster_celltype",
  "aliases": [
   "get_cluster_celltype",
   "ov.single.get_cluster_celltype",
   "get cluster celltype"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Resolve one final cell type for each cluster with LLM calls.",
  "examples": [],
  "related": []
 },
 "ov.single.get_markers": {
  "_module": "omicverse.single._markers",
  "_name": "get_markers",
  "aliases": [
   "get_markers",
   "ov.single.get_markers",
   "get markers",
   "finding marker genes"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Extract top marker genes from ``rank_genes_groups`` results.",
  "examples": [
   "ov.single.get_markers(adata, groups=['0'], key='rank_genes_groups')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pl.markers_dotplot",
   "ov.pp.umap",
   "ov.single.find_markers",
   "ov.single.MetaCell"
  ]
 },
 "ov.single.get_obs_value": {
  "_module": "omicverse.single._metacell",
  "_name": "get_obs_value",
  "aliases": [
   "get_obs_value",
   "ov.single.get_obs_value",
   "get obs value"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Transfer per-cell annotations/statistics to metacells.",
  "examples": [
   "ov.single.get_obs_value(ad, adata, groupby='S_score', type='mean')"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.plot_set",
   "ov.single.plot_metacells",
   "ov.pp.scale",
   "ov.pp.pca"
  ]
 },
 "ov.single.get_weights": {
  "_module": "omicverse.single._mofa",
  "_name": "get_weights",
  "aliases": [
   "get_weights",
   "ov.single.get_weights",
   "get weights"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Extract feature loadings for one factor from a MOFA model.",
  "examples": [
   "ov.single.get_weights(hdf5_path='data/sample/MOFA_POS.hdf5', view='RNA', factor=1)"
  ],
  "related": [
   "ov.utils.read",
   "ov.single.factor_exact",
   "ov.single.factor_correlation",
   "ov.single.pyMOFAART"
  ]
 },
 "ov.single.gptcelltype": {
  "_module": "omicverse.single._gptcelltype",
  "_name": "gptcelltype",
  "aliases": [
   "gptcelltype",
   "ov.single.gptcelltype",
   "简体中文",
   "请选择您需要使用的模型",
   "请选择您",
   "模型",
   "支持的模型列表",
   "支持",
   "模型列表",
   "月之暗面"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Annotate cluster cell types with a remote LLM service.",
  "examples": [
   "ov.single.gptcelltype(all_markers, tissuename='PBMC', speciename='human', model='qwen-plus', provider='qwen', topgenenumber=5)"
  ],
  "related": [
   "ov.utils.mde",
   "ov.pl.embedding",
   "ov.utils.palette",
   "ov.single.get_celltype_marker"
  ]
 },
 "ov.single.gptcelltype_local": {
  "_module": "omicverse.single._gptcelltype_local",
  "_name": "gptcelltype_local",
  "aliases": [
   "gptcelltype_local",
   "ov.single.gptcelltype_local",
   "gptcelltype local",
   "use ov"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Annotate cell types with a local instruction-tuned LLM.",
  "examples": [
   "ov.single.gptcelltype_local(all_markers, tissuename='PBMC', speciename='human', model_name=anno_model, topgenenumber=5)"
  ],
  "related": [
   "ov.single.gptcelltype"
  ]
 },
 "ov.single.grn": {
  "_module": "omicverse.single._scenic",
  "_name": "grn",
  "aliases": [
   "grn",
   "ov.single.grn",
   "推断"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Infer a TF-target GRN edge list from an AnnData expression matrix.",
  "examples": [
   "ov.single.grn(adata, method='grnboost2', regulators=regulators, layer='spliced', top=120, seed=42, n_workers=2, threads=2, key_added='grnboost2_prior')"
  ],
  "related": [
   "ov.plot_set",
   "ov.single.Velo",
   "ov.single.velocity",
   "ov.plt.figure"
  ]
 },
 "ov.single.hematopoiesis": {
  "_module": "omicverse.single._via",
  "_name": "hematopoiesis",
  "aliases": [
   "hematopoiesis",
   "ov.single.hematopoiesis"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Load scRNA-seq hematopoiesis dataset for trajectory inference.",
  "examples": [
   "import omicverse as ov",
   "adata = ov.single.scRNA_hematopoiesis()",
   "print(adata.shape)"
  ],
  "related": []
 },
 "ov.single.lazy": {
  "_module": "omicverse.single._lazy_function",
  "_name": "lazy",
  "aliases": [
   "lazy",
   "ov.single.lazy"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Run a one-click single-cell analysis pipeline with resumable steps.",
  "examples": [
   "ov.single.lazy(adata, species='mouse', reforce_steps=['qc', 'preprocess', 'scaled', 'pca', 'cell_cycle', 'Harmony', 'scVI', 'eval_bench', 'umap', 'tsne'], sample_key='batch', qc_kwargs={'tresh': {'mito_perc': 0.2, 'nUMIs': 500, 'detected_genes': 250}, 'doublets_method': 'scrublet', 'batch_key': 'batch'}, preprocess_kwargs={'mode': 'shiftlog|pearson', 'n_HVGs': 2000, 'target_sum': 50 * 10000.0}, pca_kwargs={'layer': 'scaled', 'n_pcs': 50, 'use_highly_variable': True}, harmony_kwargs={'n_pcs': 50}, scvi_kwargs={'n_layers': 2, 'n_latent': 30, 'gene_likelihood': 'nb'})"
  ],
  "related": [
   "ov.plot_set",
   "ov.settings.cpu_gpu_mixed_init",
   "ov.pl.embedding",
   "ov.single.generate_scRNA_report"
  ]
 },
 "ov.single.lineage_pseudotime": {
  "_module": "omicverse.single._perturb",
  "_name": "lineage_pseudotime",
  "aliases": [
   "lineage_pseudotime",
   "ov.single.lineage_pseudotime",
   "lineage pseudotime"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Compute lineage-specific DPT pseudotime via CellOracle.",
  "examples": [
   "ov.single.lineage_pseudotime(adata, lineage_dictionary={'Lineage_ME': ['Ery_0', 'Ery_1', 'Ery_2', 'Ery_3', 'Ery_4', 'Ery_5', 'Ery_6', 'Ery_7', 'Ery_8', 'Ery_9', 'MEP_0', 'Mk_0'], 'Lineage_GM': ['GMP_0', 'GMP_1', 'GMP_2', 'GMPl_0', 'GMPl_1', 'Gran_0', 'Gran_1', 'Gran_2', 'Gran_3', 'Mo_0', 'Mo_1', 'Mo_2']}, root_cells={'Lineage_ME': '1539', 'Lineage_GM': '2244'}, obsm_key='X_draw_graph_fa', cluster_column_name='louvain_annot')"
  ],
  "related": [
   "ov.single.perturb",
   "ov.single.PerturbResult.load"
  ]
 },
 "ov.single.load_human_prior_interaction_network": {
  "_module": "omicverse.single._cefcon",
  "_name": "load_human_prior_interaction_network",
  "aliases": [
   "load_human_prior_interaction_network",
   "ov.single.load_human_prior_interaction_network",
   "load human prior interaction network"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Load one of the packaged human prior interaction networks.",
  "examples": [
   "ov.single.load_human_prior_interaction_network(dataset='nichenet')"
  ],
  "related": [
   "ov.plot_set",
   "ov.single.mouse_hsc_nestorowa16",
   "ov.single.convert_human_to_mouse_network",
   "ov.read",
   "ov.single.pyCEFCON"
  ]
 },
 "ov.single.marker_enrichment": {
  "_module": "omicverse.single.ev._annotate",
  "_name": "marker_enrichment",
  "aliases": [
   "marker_enrichment",
   "ov.single.marker_enrichment",
   "marker enrichment"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Hypergeometric enrichment of cluster markers vs an EV-cargo reference.",
  "examples": [],
  "related": []
 },
 "ov.single.misev_marker_plot": {
  "_module": "omicverse.single.ev.plotting",
  "_name": "misev_marker_plot",
  "aliases": [
   "misev_marker_plot",
   "ov.single.misev_marker_plot",
   "misev marker plot"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Bar plot of MISEV positive vs contaminant marker levels.",
  "examples": [],
  "related": []
 },
 "ov.single.misev_markers": {
  "_module": "omicverse.single.ev._annotate",
  "_name": "misev_markers",
  "aliases": [
   "misev_markers",
   "ov.single.misev_markers",
   "misev markers"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Built-in MISEV2023 EV protein-marker panels.",
  "examples": [],
  "related": []
 },
 "ov.single.misev_report": {
  "_module": "omicverse.single.ev._report",
  "_name": "misev_report",
  "aliases": [
   "misev_report",
   "ov.single.misev_report",
   "misev report"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Assemble a MISEV2023-aligned EV characterization report.",
  "examples": [],
  "related": []
 },
 "ov.single.mouse_hsc_nestorowa16": {
  "_module": "omicverse.single._cefcon",
  "_name": "mouse_hsc_nestorowa16",
  "aliases": [
   "mouse_hsc_nestorowa16",
   "ov.single.mouse_hsc_nestorowa16",
   "mouse hsc nestorowa16",
   "data loading and processing",
   "loading the dataset",
   "dataset information",
   "注意"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Load Nestorowa16 mouse HSC reference data used by CEFCON.",
  "examples": [
   "ov.single.mouse_hsc_nestorowa16()"
  ],
  "related": [
   "ov.plot_set",
   "ov.single.SCENIC",
   "ov.pl.embedding",
   "ov.utils.save",
   "ov.single.load_human_prior_interaction_network"
  ]
 },
 "ov.single.normalize": {
  "_module": "omicverse.single.ev._preprocess",
  "_name": "normalize",
  "aliases": [
   "normalize",
   "ov.single.normalize"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Value-type-aware normalization for single-EV proteomics.",
  "examples": [],
  "related": []
 },
 "ov.single.optimize_granularity": {
  "_module": "omicverse.single._metacell",
  "_name": "optimize_granularity",
  "aliases": [
   "optimize_granularity",
   "ov.single.optimize_granularity",
   "optimize granularity"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Sweep ``n_metacells`` and return the optimal value per mcRigor.",
  "examples": [],
  "related": []
 },
 "ov.single.pathway_aucell": {
  "_module": "omicverse.single._scgsea",
  "_name": "pathway_aucell",
  "aliases": [
   "pathway_aucell",
   "ov.single.pathway_aucell",
   "pathway aucell"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Calculate the area under the curve (AUC) for a set of pathways in an AnnData object.",
  "examples": [
   "ov.single.pathway_aucell(adata, pathway_names=geneset_names, pathways_dict=pathway_dict)"
  ],
  "related": [
   "ov.utils.geneset_prepare",
   "ov.single.geneset_aucell",
   "ov.pl.umap",
   "ov.pl.embedding"
  ]
 },
 "ov.single.pathway_aucell_enrichment": {
  "_module": "omicverse.single._scgsea",
  "_name": "pathway_aucell_enrichment",
  "aliases": [
   "pathway_aucell_enrichment",
   "ov.single.pathway_aucell_enrichment",
   "pathway aucell enrichment"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Enrich cell annotations with pathway activity scores using the AUC-ell method.",
  "examples": [
   "ov.single.pathway_aucell_enrichment(adata, pathways_dict=pathway_dict, num_workers=8)"
  ],
  "related": [
   "ov.read",
   "ov.ov_plot_set",
   "ov.utils.geneset_prepare",
   "ov.single.cellfategenie",
   "ov.single.gene_trends"
  ]
 },
 "ov.single.pathway_enrichment": {
  "_module": "omicverse.single._scgsea",
  "_name": "pathway_enrichment",
  "aliases": [
   "pathway_enrichment",
   "ov.single.pathway_enrichment",
   "pathway enrichment"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Perform pathway enrichment analysis on gene expression data.",
  "examples": [
   "ov.single.pathway_enrichment(adata, pathways_dict=pathway_dict, organism='Mouse', group_by='clusters', plot=True)"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.utils.plot_text_set",
   "ov.single.pathway_enrichment_plot",
   "ov.pl.rank_genes_groups_dotplot"
  ]
 },
 "ov.single.pathway_enrichment_plot": {
  "_module": "omicverse.single._scgsea",
  "_name": "pathway_enrichment_plot",
  "aliases": [
   "pathway_enrichment_plot",
   "ov.single.pathway_enrichment_plot",
   "pathway enrichment plot"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Visualize the pathway enrichment analysis results as a heatmap.",
  "examples": [
   "ov.single.pathway_enrichment_plot(res, plot_title='Enrichment', cmap='Reds', xticklabels=True, cbar=False, square=True, vmax=10, yticklabels=True, cbar_kws={'label': '-log10(qvalue)', 'shrink': 0.5})"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.utils.plot_text_set",
   "ov.single.pathway_enrichment"
  ]
 },
 "ov.single.plot_metacells": {
  "_module": "omicverse.single._metacell",
  "_name": "plot_metacells",
  "aliases": [
   "plot_metacells",
   "ov.single.plot_metacells",
   "plot metacells"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Plot metacell centroids on a given embedding axis.",
  "examples": [
   "ov.single.plot_metacells(ax, meta_obj.adata, color='#CB3E35')"
  ],
  "related": [
   "ov.utils.load",
   "ov.plot_set",
   "ov.pl.embedding",
   "ov.single.get_obs_value",
   "ov.pp.scale"
  ]
 },
 "ov.single.protein_combinations": {
  "_module": "omicverse.single.ev._coloc",
  "_name": "protein_combinations",
  "aliases": [
   "protein_combinations",
   "ov.single.protein_combinations",
   "protein combinations"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Enumerate EV protein combinations and find DEPCs between conditions.",
  "examples": [],
  "related": []
 },
 "ov.single.pseudobulk": {
  "_module": "omicverse.single._pseudobulk",
  "_name": "pseudobulk",
  "aliases": [
   "pseudobulk",
   "ov.single.pseudobulk"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Summarise single-cell profiles into pseudobulk profiles.",
  "examples": [],
  "related": []
 },
 "ov.single.pseudobulk_de": {
  "_module": "omicverse.single.ev._pseudobulk",
  "_name": "pseudobulk_de",
  "aliases": [
   "pseudobulk_de",
   "ov.single.pseudobulk_de",
   "pseudobulk de"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Bulk-style differential expression on a pseudo-bulk matrix.",
  "examples": [],
  "related": []
 },
 "ov.single.purity_report": {
  "_module": "omicverse.single.ev._annotate",
  "_name": "purity_report",
  "aliases": [
   "purity_report",
   "ov.single.purity_report",
   "purity report"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "MISEV-style EV-preparation purity report.",
  "examples": [],
  "related": []
 },
 "ov.single.pyCEFCON": {
  "_module": "omicverse.single._cefcon",
  "_name": "pyCEFCON",
  "aliases": [
   "pyCEFCON",
   "ov.single.pyCEFCON",
   "py c e f c o n",
   "training cefcon model"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "CEFCON workflow wrapper for driver-regulator discovery.",
  "examples": [
   "ov.single.pyCEFCON(adata, prior_network, repeats=5, solver='GUROBI')"
  ],
  "related": [
   "ov.single.load_human_prior_interaction_network",
   "ov.single.convert_human_to_mouse_network",
   "ov.read",
   "ov.utils.embedding"
  ]
 },
 "ov.single.pyMOFA": {
  "_module": "omicverse.single._mofa",
  "_name": "pyMOFA",
  "aliases": [
   "pyMOFA",
   "ov.single.pyMOFA",
   "py m o f a",
   "mofa analysis"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Train MOFA models for latent factor discovery across multiple omics layers.",
  "examples": [
   "ov.single.pyMOFA(omics=[rna, atac], omics_name=['RNA', 'ATAC'])"
  ],
  "related": [
   "ov.utils.read",
   "ov.utils.ov_plot_set",
   "ov.single.factor_exact",
   "ov.single.GLUE_pair",
   "ov.single.pyMOFAART"
  ]
 },
 "ov.single.pyMOFAART": {
  "_module": "omicverse.single._mofa",
  "_name": "pyMOFAART",
  "aliases": [
   "pyMOFAART",
   "ov.single.pyMOFAART",
   "py m o f a a r t",
   "mofa visualization"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Load pretrained MOFA models for downstream factor interpretation.",
  "examples": [
   "ov.single.pyMOFAART(model_path='data/sample/MOFA_POS.hdf5')"
  ],
  "related": [
   "ov.single.factor_exact",
   "ov.single.factor_correlation",
   "ov.single.get_weights",
   "ov.utils.read",
   "ov.single.GLUE_pair"
  ]
 },
 "ov.single.pySCSA": {
  "_module": "omicverse.single._anno",
  "_name": "pySCSA",
  "aliases": [
   "pySCSA",
   "ov.single.pySCSA",
   "py s c s a",
   "百度云",
   "设为",
   "cell annotate automatically",
   "并将",
   "来进行细胞类型注释",
   "细胞类型注释",
   "版本",
   "基于"
  ],
  "auto_fix": "auto",
  "category": "single",
  "description": "Automated cell-type annotation using SCSA marker-enrichment scoring.",
  "examples": [
   "ov.single.pySCSA(adata=adata, foldchange=1.5, pvalue=0.01, celltype='normal', target='cellmarker', tissue='All', model_path='temp/pySCSA_2024_v1_plus.db')"
  ],
  "prerequisites": {
   "functions": [
    "ov.pp.pca",
    "ov.pp.scale"
   ]
  },
  "related": [
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.utils.mde",
   "ov.utils.embedding",
   "ov.utils.palette"
  ]
 },
 "ov.single.pySIMBA": {
  "_module": "omicverse.single._simba",
  "_name": "pySIMBA",
  "aliases": [
   "pySIMBA",
   "ov.single.pySIMBA",
   "py s i m b a"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "SIMBA wrapper for single-cell batch integration and graph-embedding construction.",
  "examples": [
   "ov.single.pySIMBA(adata, workdir)"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.read"
  ]
 },
 "ov.single.pyTOSICA": {
  "_module": "omicverse.single._tosica",
  "_name": "pyTOSICA",
  "aliases": [
   "pyTOSICA",
   "ov.single.pyTOSICA",
   "py t o s i c a",
   "initialisation the tosica model"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "TOSICA wrapper for pathway-informed transformer-based cell-type annotation.",
  "examples": [
   "ov.single.pyTOSICA(adata=ref_adata, gmt_path='genesets/GO_bp.gmt', depth=1, label_name='Celltype', project_path='hGOBP_demo', batch_size=8)"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.download_tosica_gmt",
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.utils.mde"
  ]
 },
 "ov.single.pyVIA": {
  "_module": "omicverse.single._via",
  "_name": "pyVIA",
  "aliases": [
   "pyVIA",
   "ov.single.pyVIA",
   "py v i a",
   "initialize and run via",
   "指定",
   "model construct and run"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "VIA-based trajectory inference and lineage visualization wrapper.",
  "examples": [
   "ov.single.pyVIA(adata=adata, adata_key='X_pca', adata_ncomps=100, basis='X_mde', clusters='clusters', knn=20, random_seed=4, root_user=['nIPC'], dataset='group')"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.pyomic_palette",
   "ov.utils.embedding",
   "ov.utils.cal_paga",
   "ov.utils.plot_paga"
  ]
 },
 "ov.single.qc": {
  "_module": "omicverse.single.ev._qc",
  "_name": "qc",
  "aliases": [
   "qc",
   "ov.single.qc"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Run single-EV quality control.",
  "examples": [],
  "related": []
 },
 "ov.single.rank_markers": {
  "_module": "omicverse.single.ev._markers",
  "_name": "rank_markers",
  "aliases": [
   "rank_markers",
   "ov.single.rank_markers",
   "rank markers"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Identify marker proteins for each EV subpopulation.",
  "examples": [],
  "related": []
 },
 "ov.single.read_digital_ev": {
  "_module": "omicverse.single.ev.io",
  "_name": "read_digital_ev",
  "aliases": [
   "read_digital_ev",
   "ov.single.read_digital_ev",
   "read digital ev"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Read a droplet-digital / Simoa per-EV binary call matrix.",
  "examples": [],
  "related": []
 },
 "ov.single.read_ev_matrix": {
  "_module": "omicverse.single.ev.io",
  "_name": "read_ev_matrix",
  "aliases": [
   "read_ev_matrix",
   "ov.single.read_ev_matrix",
   "read ev matrix"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Read a generic EV x protein table into a single-EV AnnData.",
  "examples": [],
  "related": []
 },
 "ov.single.read_exoview": {
  "_module": "omicverse.single.ev.io",
  "_name": "read_exoview",
  "aliases": [
   "read_exoview",
   "ov.single.read_exoview",
   "read exoview"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Read an ExoView / SP-IRIS exported per-particle table.",
  "examples": [],
  "related": []
 },
 "ov.single.read_fcs": {
  "_module": "omicverse.single.ev.io",
  "_name": "read_fcs",
  "aliases": [
   "read_fcs",
   "ov.single.read_fcs",
   "read fcs"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Read an FCS-format single-EV flow event file into an AnnData.",
  "examples": [],
  "related": []
 },
 "ov.single.read_nanofcm": {
  "_module": "omicverse.single.ev.io",
  "_name": "read_nanofcm",
  "aliases": [
   "read_nanofcm",
   "ov.single.read_nanofcm",
   "read nanofcm"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Read a NanoFCM nano-flow-cytometry single-EV event table.",
  "examples": [],
  "related": []
 },
 "ov.single.read_pba": {
  "_module": "omicverse.single.ev.io",
  "_name": "read_pba",
  "aliases": [
   "read_pba",
   "ov.single.read_pba",
   "read pba"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Read a PBA / DBS-Pro single-EV surface-protein count matrix.",
  "examples": [],
  "related": []
 },
 "ov.single.refresh_ev_metrics": {
  "_module": "omicverse.single.ev.io",
  "_name": "refresh_ev_metrics",
  "aliases": [
   "refresh_ev_metrics",
   "ov.single.refresh_ev_metrics",
   "refresh ev metrics"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Compute / refresh ``total_signal`` and ``n_proteins`` in ``obs``.",
  "examples": [],
  "produces": {
   "obs": [
    "n_proteins",
    "total_signal"
   ]
  },
  "related": []
 },
 "ov.single.run_cellphonedb_v5": {
  "_module": "omicverse.single._cpdb",
  "_name": "run_cellphonedb_v5",
  "aliases": [
   "run_cellphonedb_v5",
   "ov.single.run_cellphonedb_v5",
   "run cellphonedb v5",
   "run cellphonedb"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Run CellPhoneDB statistical analysis with automatic database download",
  "examples": [
   "ov.single.run_cellphonedb_v5(adata, cpdb_file_path='./cellphonedb.zip', celltype_key='cell_labels', min_cell_fraction=0.005, min_genes=200, min_cells=3, iterations=1000, threshold=0.1, pvalue=0.05, threads=10, output_dir='./cpdb_results', cleanup_temp=True)"
  ],
  "related": [
   "ov.read",
   "ov.pl.embedding",
   "ov.single.extract_comm_adata",
   "ov.pl.ccc_heatmap",
   "ov.plot_set"
  ]
 },
 "ov.single.run_liana": {
  "_module": "omicverse.single._liana",
  "_name": "run_liana",
  "aliases": [
   "run_liana",
   "ov.single.run_liana",
   "run liana"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Run LIANA ligand-receptor inference on an AnnData object.",
  "examples": [
   "ov.single.run_liana(adata, groupby='bulk_labels', method='rank_aggregate', resource_name='consensus', key_added='liana_res', inplace=True)"
  ],
  "produces": {
   "uns": [
    "liana_res"
   ]
  },
  "related": [
   "ov.pl.embedding",
   "ov.single.to_comm_adata",
   "ov.pl.ccc_heatmap"
  ]
 },
 "ov.single.scanpy_cellanno_from_dict": {
  "_module": "omicverse.single._anno",
  "_name": "scanpy_cellanno_from_dict",
  "aliases": [
   "scanpy_cellanno_from_dict",
   "ov.single.scanpy_cellanno_from_dict",
   "scanpy cellanno from dict"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Add cell type annotation from dict to anndata object.",
  "examples": [
   "ov.single.scanpy_cellanno_from_dict(adata, anno_dict=cluster2annotation, clustertype='leiden')"
  ],
  "related": [
   "ov.utils.plot_embedding_celltype",
   "ov.utils.roe",
   "ov.pl.group_heatmap",
   "ov.utils.embedding",
   "ov.utils.palette"
  ]
 },
 "ov.single.simulate_ev": {
  "_module": "omicverse.single.ev.io",
  "_name": "simulate_ev",
  "aliases": [
   "simulate_ev",
   "ov.single.simulate_ev",
   "simulate ev"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Simulate a single-EV proteomics AnnData.",
  "examples": [],
  "related": []
 },
 "ov.single.subpopulation_abundance": {
  "_module": "omicverse.single.ev._cluster",
  "_name": "subpopulation_abundance",
  "aliases": [
   "subpopulation_abundance",
   "ov.single.subpopulation_abundance",
   "subpopulation abundance"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Per-sample frequency of each EV subpopulation.",
  "examples": [],
  "related": []
 },
 "ov.single.subtract_isotype": {
  "_module": "omicverse.single.ev._qc",
  "_name": "subtract_isotype",
  "aliases": [
   "subtract_isotype",
   "ov.single.subtract_isotype",
   "subtract isotype"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Subtract isotype / blank background and call positivity.",
  "examples": [],
  "related": []
 },
 "ov.single.tissue_of_origin": {
  "_module": "omicverse.single.ev._annotate",
  "_name": "tissue_of_origin",
  "aliases": [
   "tissue_of_origin",
   "ov.single.tissue_of_origin",
   "tissue of origin"
  ],
  "auto_fix": "none",
  "category": "single",
  "description": "Score each EV / cluster for cell- and tissue-of-origin marker sets.",
  "examples": [],
  "related": []
 },
 "ov.space.CAST": {
  "_module": "omicverse.space._cast",
  "_name": "CAST",
  "aliases": [
   "CAST",
   "ov.space.CAST",
   "c a s t"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "CAST (Cell Annotation for Spatial Transcriptomics) embedding for multiple spatial samples.",
  "examples": [
   "import scanpy as sc",
   "import omicverse as ov",
   "# Load multiple samples"
  ],
  "related": []
 },
 "ov.space.Cal_Spatial_Net": {
  "_module": "omicverse.space._integrate",
  "_name": "Cal_Spatial_Net",
  "aliases": [
   "Cal_Spatial_Net",
   "ov.space.Cal_Spatial_Net",
   "cal spatial net",
   "preprocess data"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Construct spatial neighbor networks for spatial integration.",
  "examples": [
   "ov.space.Cal_Spatial_Net(adata, rad_cutoff=50)"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.utils.cluster"
  ]
 },
 "ov.space.CellLoc": {
  "_module": "omicverse.space._spatrio",
  "_name": "CellLoc",
  "aliases": [
   "CellLoc",
   "ov.space.CellLoc",
   "cell loc"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "SpatRio CellLoc class for probabilistic cell localization.",
  "examples": [
   "import scanpy as sc",
   "import omicverse as ov",
   "# Load data"
  ],
  "related": []
 },
 "ov.space.CellMap": {
  "_module": "omicverse.space._spatrio",
  "_name": "CellMap",
  "aliases": [
   "CellMap",
   "ov.space.CellMap",
   "cell map"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "SpatRio CellMap class for mapping single cells to spatial coordinates.",
  "examples": [
   "import scanpy as sc",
   "import omicverse as ov",
   "# Load data"
  ],
  "related": []
 },
 "ov.space.Deconvolution": {
  "_module": "omicverse.space._deconvolution",
  "_name": "Deconvolution",
  "aliases": [
   "Deconvolution",
   "ov.space.Deconvolution",
   "deconvolution",
   "key parameters",
   "step deconvolution with starfysh",
   "细胞类型",
   "step run flashdeconv deconvolution",
   "step tangram deconvolution min",
   "purpose",
   "step run rctd",
   "步骤"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Spatial deconvolution pipeline that aligns scRNA-seq references with spatial transcriptomics.",
  "examples": [
   "ov.space.Deconvolution(adata_sc=adata_sc, adata_sp=adata_sp)"
  ],
  "related": [
   "ov.datasets.sc_ref_Lymph_Node",
   "ov.pl.plot_spatial",
   "ov.space.crop_space_visium",
   "ov.utils.save",
   "ov.space.calculate_gene_signature"
  ]
 },
 "ov.space.GASTON": {
  "_module": "omicverse.space._gaston",
  "_name": "GASTON",
  "aliases": [
   "GASTON",
   "ov.space.GASTON",
   "g a s t o n"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "GASTON spatial depth estimation and clustering.",
  "examples": [
   "ov.space.GASTON(adata)"
  ],
  "related": [
   "ov.plot_set",
   "ov.pd.read_csv"
  ]
 },
 "ov.space.STT": {
  "_module": "omicverse.space._stt",
  "_name": "STT",
  "aliases": [
   "STT",
   "ov.space.STT",
   "s t t",
   "参数",
   "training stt model"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Spatial Transition Tensor (STT) analysis class.",
  "examples": [
   "ov.space.STT(adata, spatial_loc='xy_loc', region='Region')"
  ],
  "related": [
   "ov.plot_set",
   "ov.pl.embedding",
   "ov.utils.geneset_prepare"
  ]
 },
 "ov.space.Tangram": {
  "_module": "omicverse.space._tangram",
  "_name": "Tangram",
  "aliases": [
   "Tangram",
   "ov.space.Tangram",
   "tangram",
   "tangram model"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Tangram spatial deconvolution class for cell type mapping.",
  "examples": [
   "ov.space.Tangram(adata_sc, adata_sp, clusters='Subset')"
  ],
  "related": [
   "ov.pp.preprocess",
   "ov.space.svg",
   "ov.pl.plot_spatial",
   "ov.space.crop_space_visium",
   "ov.pl.add_pie2spatial"
  ]
 },
 "ov.space.available_backbones": {
  "_module": "omicverse.space.histo._embed",
  "_name": "available_backbones",
  "aliases": [
   "available_backbones",
   "ov.space.available_backbones",
   "available backbones"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Return the curated list of pathology FMs recommended for HE→ST.",
  "examples": [],
  "related": []
 },
 "ov.space.bin2cell": {
  "_module": "omicverse.space._tools",
  "_name": "bin2cell",
  "aliases": [
   "bin2cell",
   "ov.space.bin2cell",
   "bin to cell",
   "export to spaceranger format",
   "cell-level spatial comparison"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Aggregate binned Visium signals into cell-level profiles.",
  "examples": [
   "ov.space.bin2cell(adata, labels_key='labels_joint', spatial_keys=['spatial', 'spatial_cropped_150_buffer'])"
  ],
  "related": [
   "ov.space.visium_10x_hd_cellpose_expand",
   "ov.space.visium_10x_hd_cellpose_gex",
   "ov.space.salvage_secondary_labels",
   "ov.pl.embedding",
   "ov.space.write_visium_hd_cellseg"
  ]
 },
 "ov.space.calculate_gene_signature": {
  "_module": "omicverse.space._deconvolution",
  "_name": "calculate_gene_signature",
  "aliases": [
   "calculate_gene_signature",
   "ov.space.calculate_gene_signature",
   "calculate gene signature",
   "step prepare the gene sig marker"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Build a marker-gene signature table for each cell type in a reference scRNA-seq dataset.",
  "examples": [
   "ov.space.calculate_gene_signature(adata_sc, clustertype='Subset', rank=True, key='rank_genes_groups', foldchange=2, topgenenumber=20)"
  ],
  "related": [
   "ov.style",
   "ov.datasets.sc_ref_Lymph_Node",
   "ov.pd.read_csv",
   "ov.space.Deconvolution",
   "ov.pl.plot_spatial"
  ]
 },
 "ov.space.cellcharter": {
  "_module": "omicverse.space._cellcharter",
  "_name": "cellcharter",
  "aliases": [
   "cellcharter",
   "ov.space.cellcharter"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Run a minimal CellCharter workflow on a spatial AnnData object.",
  "examples": [],
  "related": []
 },
 "ov.space.clusters": {
  "_module": "omicverse.space._cluster",
  "_name": "clusters",
  "aliases": [
   "clusters",
   "ov.space.clusters",
   "method",
   "dong kangning and shihua zhang",
   "graphst long et al",
   "binary lin et al",
   "stagate dong zhang nat",
   "cast tang et al",
   "banksy singhal et al"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Perform clustering analysis on spatial transcriptomics data using multiple methods.",
  "examples": [
   "ov.space.clusters(adata, methods=['GraphST'], methods_kwargs=methods_kwargs, lognorm=10000.0)"
  ],
  "related": [
   "ov.utils.cluster",
   "ov.utils.refine_label",
   "ov.space.merge_cluster",
   "ov.style",
   "ov.space.svg"
  ]
 },
 "ov.space.create_communication_anndata": {
  "_module": "omicverse.space._commot",
  "_name": "create_communication_anndata",
  "aliases": [
   "create_communication_anndata",
   "ov.space.create_communication_anndata",
   "create communication anndata"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Build a CellChat-style communication AnnData from commot outputs.",
  "examples": [],
  "related": []
 },
 "ov.space.download_breast": {
  "_module": "omicverse.space.histo._demo",
  "_name": "download_breast",
  "aliases": [
   "download_breast",
   "ov.space.download_breast",
   "download breast"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Download a Visium Breast Cancer Block A section.",
  "examples": [],
  "related": []
 },
 "ov.space.embed": {
  "_module": "omicverse.space.histo._embed",
  "_name": "embed",
  "aliases": [
   "embed",
   "ov.space.embed"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Extract per-tile foundation-model embeddings.",
  "examples": [],
  "related": []
 },
 "ov.space.load_breast": {
  "_module": "omicverse.space.histo._demo",
  "_name": "load_breast",
  "aliases": [
   "load_breast",
   "ov.space.load_breast",
   "load breast"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Download a Visium Breast Cancer Block A section and return ``(adata, wsi)``.",
  "examples": [
   "import omicverse as ov",
   "adata, wsi = ov.space.histo.load_breast()              # section 1",
   "adata2, wsi2 = ov.space.histo.load_breast(section=2)   # held-out"
  ],
  "related": []
 },
 "ov.space.map_spatial_auto": {
  "_module": "omicverse.space._tools",
  "_name": "map_spatial_auto",
  "aliases": [
   "map_spatial_auto",
   "ov.space.map_spatial_auto",
   "map spatial auto",
   "rotating the spatial data"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Automatically map and align spatial transcriptomics data.",
  "examples": [
   "ov.space.map_spatial_auto(adata_rotated, method='phase')"
  ],
  "related": [
   "ov.plt.subplots",
   "ov.space.crop_space_visium",
   "ov.space.rotate_space_visium",
   "ov.np.concatenate",
   "ov.space.map_spatial_manual"
  ]
 },
 "ov.space.map_spatial_manual": {
  "_module": "omicverse.space._tools",
  "_name": "map_spatial_manual",
  "aliases": [
   "map_spatial_manual",
   "ov.space.map_spatial_manual",
   "map spatial manual",
   "manual adjustment of spatial mapping"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Manually adjust spatial transcriptomics data alignment.",
  "examples": [
   "ov.space.map_spatial_manual(adata_rotated, offset=(-1500, 1000))"
  ],
  "related": [
   "ov.space.rotate_space_visium",
   "ov.space.map_spatial_auto",
   "ov.np.concatenate"
  ]
 },
 "ov.space.merge_cluster": {
  "_module": "omicverse.space._cluster",
  "_name": "merge_cluster",
  "aliases": [
   "merge_cluster",
   "ov.space.merge_cluster",
   "merge cluster",
   "method",
   "如果"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Merge clusters based on hierarchical clustering of their representation.",
  "examples": [
   "ov.space.merge_cluster(adata, groupby='mclust_GraphST', use_rep='graphst|original|X_pca', threshold=0.2, plot=True)"
  ],
  "related": [
   "ov.space.clusters",
   "ov.utils.cluster",
   "ov.utils.refine_label"
  ]
 },
 "ov.space.moranI": {
  "_module": "omicverse.space._svg",
  "_name": "moranI",
  "aliases": [
   "moranI",
   "ov.space.moranI",
   "moran i"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Compute Moran's I spatial autocorrelation for gene expression.",
  "examples": [
   "import omicverse as ov",
   "ov.space.spatial_neighbors(adata, n_neighs=6)",
   "df = ov.space.moranI(adata)"
  ],
  "related": []
 },
 "ov.space.nmf_tissue_zones": {
  "_module": "omicverse.space._tissue_zones",
  "_name": "nmf_tissue_zones",
  "aliases": [
   "nmf_tissue_zones",
   "ov.space.nmf_tissue_zones",
   "nmf tissue zones"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Discover tissue zones via NMF on a per-spot cell-abundance matrix.",
  "examples": [
   "ov.space.nmf_tissue_zones(adata_sp, n_components=8, normalize='rows')"
  ],
  "related": [
   "ov.llm.SCLLMManager",
   "ov.pl.perturbation_shift",
   "ov.space.Deconvolution",
   "ov.io.read_atera",
   "ov.io.read_xenium"
  ]
 },
 "ov.space.open_wsi": {
  "_module": "omicverse.space.histo._io",
  "_name": "open_wsi",
  "aliases": [
   "open_wsi",
   "ov.space.open_wsi",
   "open wsi"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Open a whole-slide image as a :class:`wsidata.WSIData` container.",
  "examples": [],
  "related": []
 },
 "ov.space.predict_expression": {
  "_module": "omicverse.space.histo._dispatch",
  "_name": "predict_expression",
  "aliases": [
   "predict_expression",
   "ov.space.predict_expression",
   "predict expression"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Predict spot-level spatial gene expression from a tiled WSI.",
  "examples": [],
  "related": []
 },
 "ov.space.pySTAGATE": {
  "_module": "omicverse.space._cluster",
  "_name": "pySTAGATE",
  "aliases": [
   "pySTAGATE",
   "ov.space.pySTAGATE",
   "py s t a g a t e"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "A class representing the PyTorch implementation of STAGATE (Spatial Transcriptomics Analysis using Graph Attention autoEncoder).",
  "examples": [
   "ov.space.pySTAGATE(adata, num_batch_x=3, num_batch_y=2, spatial_key=['X', 'Y'], rad_cutoff=200, num_epoch=1000, lr=0.001, weight_decay=0.0001, hidden_dims=[512, 30], device='cuda:0')"
  ],
  "related": [
   "ov.utils.cluster",
   "ov.utils.refine_label"
  ]
 },
 "ov.space.pySTAligner": {
  "_module": "omicverse.space._integrate",
  "_name": "pySTAligner",
  "aliases": [
   "pySTAligner",
   "ov.space.pySTAligner",
   "py s t aligner"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "STAligner for spatial transcriptomics data integration.",
  "examples": [
   "import scanpy as sc",
   "import omicverse as ov",
   "# Load data"
  ],
  "related": []
 },
 "ov.space.pySpaceFlow": {
  "_module": "omicverse.space._spaceflow",
  "_name": "pySpaceFlow",
  "aliases": [
   "pySpaceFlow",
   "ov.space.pySpaceFlow",
   "py space flow",
   "training the spaceflow model"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "SpaceFlow spatial flow analysis class.",
  "examples": [
   "ov.space.pySpaceFlow(adata)"
  ],
  "related": [
   "ov.utils.cluster",
   "ov.utils.ov_plot_set",
   "ov.space.svg"
  ]
 },
 "ov.space.read_visium_10x": {
  "_module": "omicverse.space._tools",
  "_name": "read_visium_10x",
  "aliases": [
   "read_visium_10x",
   "ov.space.read_visium_10x",
   "read visium 10x"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Read and standardize 10x Visium data with bin2cell-compatible loader.",
  "examples": [
   "ov.space.read_visium_10x(path, source_image_path=source_image_path)"
  ],
  "related": [
   "ov.pp.filter_genes",
   "ov.pp.filter_cells",
   "ov.space.visium_10x_hd_cellpose_he"
  ]
 },
 "ov.space.read_visium_with_image": {
  "_module": "omicverse.space.histo._io",
  "_name": "read_visium_with_image",
  "aliases": [
   "read_visium_with_image",
   "ov.space.read_visium_with_image",
   "read visium with image"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Load a 10x Visium output **and** wrap its source H&E as ``WSIData``.",
  "examples": [],
  "related": []
 },
 "ov.space.rotate_space_visium": {
  "_module": "omicverse.space._tools",
  "_name": "rotate_space_visium",
  "aliases": [
   "rotate_space_visium",
   "ov.space.rotate_space_visium",
   "rotate space visium",
   "rotating the spatial data"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Rotate Visium spatial data image and coordinates by a specified angle.",
  "examples": [
   "ov.space.rotate_space_visium(adata, angle, center, library_id=library_id, interpolation_order=interpolation_order)"
  ],
  "related": [
   "ov.plot_set",
   "ov.plt.subplots",
   "ov.space.crop_space_visium",
   "ov.space.map_spatial_auto",
   "ov.np.concatenate"
  ]
 },
 "ov.space.salvage_secondary_labels": {
  "_module": "omicverse.space._tools",
  "_name": "salvage_secondary_labels",
  "aliases": [
   "salvage_secondary_labels",
   "ov.space.salvage_secondary_labels",
   "salvage secondary labels"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Merge primary and secondary segmentation labels.",
  "examples": [
   "ov.space.salvage_secondary_labels(adata, primary_label='labels_he_expanded', secondary_label='labels_gex', labels_key='labels_joint')"
  ],
  "related": [
   "ov.space.visium_10x_hd_cellpose_he",
   "ov.space.visium_10x_hd_cellpose_expand",
   "ov.space.visium_10x_hd_cellpose_gex",
   "ov.space.bin2cell",
   "ov.pl.embedding"
  ]
 },
 "ov.space.spatial_autocorr": {
  "_module": "omicverse.space._svg",
  "_name": "spatial_autocorr",
  "aliases": [
   "spatial_autocorr",
   "ov.space.spatial_autocorr",
   "spatial autocorr"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Compute spatial autocorrelation statistics for gene expression.",
  "examples": [
   "import omicverse as ov",
   "ov.space.spatial_neighbors(adata, n_neighs=6)",
   "df = ov.space.spatial_autocorr(adata, mode='moran')"
  ],
  "related": []
 },
 "ov.space.spatial_neighbors": {
  "_module": "omicverse.space._svg",
  "_name": "spatial_neighbors",
  "aliases": [
   "spatial_neighbors",
   "ov.space.spatial_neighbors",
   "spatial neighbors"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Build a spatial neighborhood graph from coordinates stored in ``adata.obsm``.",
  "examples": [
   "import omicverse as ov",
   "ov.space.spatial_neighbors(adata, n_neighs=6)",
   "# radius graph"
  ],
  "related": []
 },
 "ov.space.split_balance": {
  "_module": "omicverse.space._split",
  "_name": "split_balance",
  "aliases": [
   "split_balance",
   "ov.space.split_balance",
   "split balance"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Keep raw profiles for low-contamination cells and purified profiles otherwise.",
  "examples": [],
  "related": []
 },
 "ov.space.split_purify": {
  "_module": "omicverse.space._split",
  "_name": "split_purify",
  "aliases": [
   "split_purify",
   "ov.space.split_purify",
   "split purify"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Purify spatial transcript counts with generic SPLIT inputs.",
  "examples": [],
  "related": []
 },
 "ov.space.split_reassign_residuals": {
  "_module": "omicverse.space._split",
  "_name": "split_reassign_residuals",
  "aliases": [
   "split_reassign_residuals",
   "ov.space.split_reassign_residuals",
   "split reassign residuals"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Reassign positive residual counts from purified cells to neighbors.",
  "examples": [],
  "related": []
 },
 "ov.space.split_spatial_score": {
  "_module": "omicverse.space._split",
  "_name": "split_spatial_score",
  "aliases": [
   "split_spatial_score",
   "ov.space.split_spatial_score",
   "split spatial score"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Compute local support for each cell's primary and secondary type.",
  "examples": [],
  "related": []
 },
 "ov.space.spot_features": {
  "_module": "omicverse.space.histo._hest_fm",
  "_name": "spot_features",
  "aliases": [
   "spot_features",
   "ov.space.spot_features",
   "spot features"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Embed every Visium spot's H&E patch with a pathology FM.",
  "examples": [],
  "related": []
 },
 "ov.space.subset_window": {
  "_module": "omicverse.space._tools",
  "_name": "subset_window",
  "aliases": [
   "subset_window",
   "ov.space.subset_window",
   "subset window",
   "render cell polygons in small region",
   "background image selection",
   "channel pairing rationale"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Subset an AnnData by a rectangular spatial window.",
  "examples": [
   "ov.space.subset_window(adata, xlim=(crop_window[0], crop_window[1]), ylim=(crop_window[2], crop_window[3]))"
  ],
  "related": [
   "ov.pl.to_rgb_grayscale",
   "ov.pl.sync_categorical_palette",
   "ov.pl.spatial",
   "ov.pl.spatialseg",
   "ov.pp.filter_cells"
  ]
 },
 "ov.space.super_resolve": {
  "_module": "omicverse.space.histo._dispatch",
  "_name": "super_resolve",
  "aliases": [
   "super_resolve",
   "ov.space.super_resolve",
   "super resolve"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Super-resolve a paired (Visium, H&E) sample to near-single-cell tiles.",
  "examples": [],
  "related": []
 },
 "ov.space.svg": {
  "_module": "omicverse.space._svg",
  "_name": "svg",
  "aliases": [
   "svg",
   "ov.space.svg",
   "important parameters",
   "使用"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Identify spatially variable genes using multiple methods.",
  "examples": [
   "ov.space.svg(bdata, mode='moranI', n_svgs=3000, n_perms=100, n_jobs=8)"
  ],
  "related": [
   "ov.utils.cluster",
   "ov.read",
   "ov.plot_set",
   "ov.pl.spatialseg",
   "ov.pp.normalize_total"
  ]
 },
 "ov.space.sync_visium_hd_seg_geometries": {
  "_module": "omicverse.space._tools",
  "_name": "sync_visium_hd_seg_geometries",
  "aliases": [
   "sync_visium_hd_seg_geometries",
   "ov.space.sync_visium_hd_seg_geometries",
   "sync visium hd seg geometries"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Synchronize ``adata.uns[\"spatial\"][sample][\"geometries\"]`` with current ``adata.obs_names``.",
  "examples": [],
  "related": []
 },
 "ov.space.tile": {
  "_module": "omicverse.space.histo._io",
  "_name": "tile",
  "aliases": [
   "tile",
   "ov.space.tile"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Tile a WSI into a grid of patches (delegates to LazySlide).",
  "examples": [],
  "related": []
 },
 "ov.space.update_classification_from_database": {
  "_module": "omicverse.space._commot",
  "_name": "update_classification_from_database",
  "aliases": [
   "update_classification_from_database",
   "ov.space.update_classification_from_database",
   "update classification from database"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Update communication interaction annotations from commot database metadata.",
  "examples": [],
  "related": []
 },
 "ov.space.visium_10x_hd_cellpose_expand": {
  "_module": "omicverse.space._tools",
  "_name": "visium_10x_hd_cellpose_expand",
  "aliases": [
   "visium_10x_hd_cellpose_expand",
   "ov.space.visium_10x_hd_cellpose_expand",
   "visium 10x hd cellpose expand"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Expand segmentation labels from nuclei to nearby bins.",
  "examples": [
   "ov.space.visium_10x_hd_cellpose_expand(adata, labels_key='labels_he', expanded_labels_key='labels_he_expanded', max_bin_distance=4)"
  ],
  "related": [
   "ov.pp.filter_genes",
   "ov.pp.filter_cells",
   "ov.space.visium_10x_hd_cellpose_he",
   "ov.space.visium_10x_hd_cellpose_gex",
   "ov.space.salvage_secondary_labels"
  ]
 },
 "ov.space.visium_10x_hd_cellpose_gex": {
  "_module": "omicverse.space._tools",
  "_name": "visium_10x_hd_cellpose_gex",
  "aliases": [
   "visium_10x_hd_cellpose_gex",
   "ov.space.visium_10x_hd_cellpose_gex",
   "visium 10x hd cellpose gex",
   "gex cell segmenation with cellpose"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Run expression-image segmentation and map labels back to spatial bins.",
  "examples": [
   "ov.space.visium_10x_hd_cellpose_gex(adata, obs_key='n_counts_adjusted', log1p=False, mpp=0.3, sigma=5, gex_save_path='stardist/gex_colon1.tiff', prob_thresh=0.01, nms_thresh=0.1, gpu=True, buffer=150)"
  ],
  "related": [
   "ov.pp.filter_cells",
   "ov.space.visium_10x_hd_cellpose_he",
   "ov.space.visium_10x_hd_cellpose_expand",
   "ov.space.salvage_secondary_labels",
   "ov.space.bin2cell"
  ]
 },
 "ov.space.visium_10x_hd_cellpose_he": {
  "_module": "omicverse.space._tools",
  "_name": "visium_10x_hd_cellpose_he",
  "aliases": [
   "visium_10x_hd_cellpose_he",
   "ov.space.visium_10x_hd_cellpose_he",
   "visium 10x hd cellpose he",
   "图像",
   "he cell segmenation with cellpose"
  ],
  "auto_fix": "none",
  "category": "space",
  "description": "Convert Visium 10x data to cell-level data.",
  "examples": [
   "ov.space.visium_10x_hd_cellpose_he(adata, mpp=0.3, he_save_path='stardist/he_colon1.tiff', prob_thresh=0, flow_threshold=0.4, gpu=True, buffer=150, backend='tifffile')"
  ],
  "related": [
   "ov.space.read_visium_10x",
   "ov.pp.filter_genes",
   "ov.pp.filter_cells",
   "ov.space.visium_10x_hd_cellpose_expand",
   "ov.space.visium_10x_hd_cellpose_gex"
  ]
 },
 "ov.utils.LDA_topic": {
  "_module": "omicverse.utils._cluster",
  "_name": "LDA_topic",
  "aliases": [
   "LDA_topic",
   "ov.utils.LDA_topic",
   "l d a topic"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Latent Dirichlet Allocation (LDA) topic modeling for single-cell data using MIRA.",
  "examples": [
   "ov.utils.LDA_topic(adata, feature_type='expression', highly_variable_key='highly_variable_features', layers='counts', batch_key=None, learning_rate=0.001)"
  ],
  "related": [
   "ov.utils.cluster",
   "ov.pl.embedding",
   "ov.plot_set",
   "ov.utils.embedding",
   "ov.utils.ov_plot_set"
  ]
 },
 "ov.utils._download_enrichr_library": {
  "_module": "omicverse.utils._data",
  "_name": "_download_enrichr_library",
  "aliases": [
   "_download_enrichr_library",
   "ov.utils._download_enrichr_library",
   "download enrichr library"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Fetch a gene-set library from Enrichr by name, cache it, return its path.",
  "examples": [],
  "related": []
 },
 "ov.utils.align_samples": {
  "_module": "omicverse.utils._sample_metadata_alignment",
  "_name": "align_samples",
  "aliases": [
   "align_samples",
   "ov.utils.align_samples",
   "align samples"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "One-shot ``(aligned_matrix, aligned_meta, result)`` convenience.",
  "examples": [],
  "related": []
 },
 "ov.utils.align_to_common": {
  "_module": "omicverse.utils._sample_metadata_alignment",
  "_name": "align_to_common",
  "aliases": [
   "align_to_common",
   "ov.utils.align_to_common",
   "align to common"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Drop duplicates + intersect to the common sample set.",
  "examples": [],
  "related": []
 },
 "ov.utils.cal_paga": {
  "_module": "omicverse.utils._paga",
  "_name": "cal_paga",
  "aliases": [
   "cal_paga",
   "ov.utils.cal_paga",
   "cal paga",
   "paga graph"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Compute a PAGA graph with optional velocity/time priors.",
  "examples": [
   "ov.utils.cal_paga(adata, use_time_prior='pt_via', vkey='paga', groups='clusters')"
  ],
  "related": [
   "ov.utils.plot_paga",
   "ov.pl.embedding",
   "ov.utils.embedding",
   "ov.single.pyVIA",
   "ov.pl.trajectory_overlay"
  ]
 },
 "ov.utils.call_tool": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "call_tool",
  "aliases": [
   "call_tool",
   "ov.utils.call_tool",
   "call tool"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Call any BioContext MCP tool by name.",
  "examples": [],
  "related": []
 },
 "ov.utils.cluster": {
  "_module": "omicverse.utils._cluster",
  "_name": "cluster",
  "aliases": [
   "cluster",
   "ov.utils.cluster",
   "clustering the space",
   "unsupervised clustering",
   "supervised clustering",
   "louvain"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Run a selected clustering backend on single-cell data.",
  "examples": [
   "ov.utils.cluster(adata, use_rep='spaceflow', method='GMM', n_components=7, covariance_type='full', tol=1e-09, max_iter=1000, random_state=3607)"
  ],
  "related": [
   "ov.utils.refine_label",
   "ov.space.clusters",
   "ov.space.merge_cluster",
   "ov.style",
   "ov.space.svg"
  ]
 },
 "ov.utils.convert2gene_id": {
  "_module": "omicverse.utils._gene_id_conversion",
  "_name": "convert2gene_id",
  "aliases": [
   "convert2gene_id",
   "ov.utils.convert2gene_id",
   "convert2gene id"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Convert official gene symbols to Ensembl gene IDs using pyensembl.",
  "examples": [
   "df = ov.utils.convert2gene_id(['TP53', 'GAPDH'])",
   "df = ov.utils.convert2gene_id(",
   "df = ov.utils.convert2gene_id(['TP53'], multi='join')"
  ],
  "related": []
 },
 "ov.utils.convert2gene_symbol": {
  "_module": "omicverse.utils._gene_id_conversion",
  "_name": "convert2gene_symbol",
  "aliases": [
   "convert2gene_symbol",
   "ov.utils.convert2gene_symbol",
   "convert2gene symbol"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Convert Ensembl gene IDs to official gene symbols using pyensembl.",
  "examples": [
   "df = ov.utils.convert2gene_symbol(list(adata.var_names))",
   "df = ov.utils.convert2gene_symbol("
  ],
  "related": []
 },
 "ov.utils.convert2symbol": {
  "_module": "omicverse.utils._gene_id_conversion",
  "_name": "convert2symbol",
  "aliases": [
   "convert2symbol",
   "ov.utils.convert2symbol"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Convert Ensembl IDs in ``adata.var_names`` to official gene symbols.",
  "examples": [
   "adata = ov.utils.convert2symbol(adata)",
   "adata = ov.utils.convert2symbol(adata, subset=False)"
  ],
  "related": []
 },
 "ov.utils.download_CaDRReS_model": {
  "_module": "omicverse.utils._data",
  "_name": "download_CaDRReS_model",
  "aliases": [
   "download_CaDRReS_model",
   "ov.utils.download_CaDRReS_model",
   "download ca d r re s model"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Download pretrained CaDRReS model parameter/output files.",
  "examples": [
   "ov.utils.download_CaDRReS_model()"
  ],
  "related": [
   "ov.utils.get_gene_annotation",
   "ov.utils.download_GDSC_data",
   "ov.single.autoResolution",
   "ov.single.Drug_Response"
  ]
 },
 "ov.utils.download_GDSC_data": {
  "_module": "omicverse.utils._data",
  "_name": "download_GDSC_data",
  "aliases": [
   "download_GDSC_data",
   "ov.utils.download_GDSC_data",
   "download g d s c data"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Download GDSC expression and drug mask tables.",
  "examples": [
   "ov.utils.download_GDSC_data()"
  ],
  "related": [
   "ov.utils.get_gene_annotation",
   "ov.utils.download_CaDRReS_model",
   "ov.single.autoResolution",
   "ov.single.Drug_Response"
  ]
 },
 "ov.utils.download_geneid_annotation_pair": {
  "_module": "omicverse.utils._data",
  "_name": "download_geneid_annotation_pair",
  "aliases": [
   "download_geneid_annotation_pair",
   "ov.utils.download_geneid_annotation_pair",
   "download geneid annotation pair",
   "id mapping",
   "geneset download"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Download gene ID annotation mapping files for various organisms.",
  "examples": [
   "ov.utils.download_geneid_annotation_pair()"
  ],
  "related": [
   "ov.bulk.Matrix_ID_mapping",
   "ov.bulk.pyDEG",
   "ov.utils.download_pathway_database",
   "ov.utils.ov_plot_set",
   "ov.utils.read"
  ]
 },
 "ov.utils.download_pathway_database": {
  "_module": "omicverse.utils._data",
  "_name": "download_pathway_database",
  "aliases": [
   "download_pathway_database",
   "ov.utils.download_pathway_database",
   "download pathway database",
   "pathway enrichment analysis by pyomic",
   "pathway enrichment analysis by ov",
   "通路富集分析",
   "这里我们使用",
   "包含GSEA分析",
   "富集分析",
   "我们优化了该包的输出",
   "优化了该包"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Download pathway and gene set databases for enrichment analysis.",
  "examples": [
   "ov.utils.download_pathway_database()"
  ],
  "related": [
   "ov.bulk.Matrix_ID_mapping",
   "ov.bulk.pyDEG",
   "ov.utils.geneset_prepare",
   "ov.utils.download_geneid_annotation_pair",
   "ov.bulk.pyGSEA"
  ]
 },
 "ov.utils.download_tosica_gmt": {
  "_module": "omicverse.utils._data",
  "_name": "download_tosica_gmt",
  "aliases": [
   "download_tosica_gmt",
   "ov.utils.download_tosica_gmt",
   "download tosica gmt",
   "download genesets"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Download curated GMT files used by TOSICA workflows.",
  "examples": [
   "ov.utils.download_tosica_gmt()"
  ],
  "related": [
   "ov.utils.ov_plot_set",
   "ov.single.pyTOSICA",
   "ov.pp.scale",
   "ov.pp.pca"
  ]
 },
 "ov.utils.get_ensembl_id": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "get_ensembl_id",
  "aliases": [
   "get_ensembl_id",
   "ov.utils.get_ensembl_id",
   "get ensembl id"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Convert gene symbol to Ensembl ID.",
  "examples": [],
  "related": []
 },
 "ov.utils.get_fulltext": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "get_fulltext",
  "aliases": [
   "get_fulltext",
   "ov.utils.get_fulltext",
   "get fulltext"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Get full text from Europe PMC.",
  "examples": [],
  "related": []
 },
 "ov.utils.get_gene_annotation": {
  "_module": "omicverse.utils._data",
  "_name": "get_gene_annotation",
  "aliases": [
   "get_gene_annotation",
   "ov.utils.get_gene_annotation",
   "get gene annotation",
   "infer the tumor from scrna-seq",
   "so we provide utility function ov"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Annotate ``adata.var`` by merging with gene-level GTF attributes.",
  "examples": [
   "ov.utils.get_gene_annotation(adata, gtf='gencode.v43.basic.annotation.gtf.gz', gtf_by='gene_name')"
  ],
  "related": [
   "ov.utils.download_GDSC_data",
   "ov.utils.download_CaDRReS_model",
   "ov.single.autoResolution"
  ]
 },
 "ov.utils.get_uniprot_id": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "get_uniprot_id",
  "aliases": [
   "get_uniprot_id",
   "ov.utils.get_uniprot_id",
   "get uniprot id"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Get UniProt accession ID from protein symbol.",
  "examples": [],
  "related": []
 },
 "ov.utils.gtf_to_pair_tsv": {
  "_module": "omicverse.utils._data",
  "_name": "gtf_to_pair_tsv",
  "aliases": [
   "gtf_to_pair_tsv",
   "ov.utils.gtf_to_pair_tsv",
   "gtf to pair tsv"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Convert GTF file to gene ID mapping pairs TSV format.",
  "examples": [
   "import omicverse as ov",
   "# Convert GTF to mapping pairs",
   "gene_count = ov.utils.gtf_to_pair_tsv('genes.gtf', 'gene_pairs.tsv')"
  ],
  "related": []
 },
 "ov.utils.list_tools": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "list_tools",
  "aliases": [
   "list_tools",
   "ov.utils.list_tools",
   "list tools"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "List all available BioContext tools.",
  "examples": [],
  "related": []
 },
 "ov.utils.load_metabolights": {
  "_module": "omicverse.utils._metabolights",
  "_name": "load_metabolights",
  "aliases": [
   "load_metabolights",
   "ov.utils.load_metabolights",
   "load metabolights"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Load a Metabolights study into a samples × metabolites AnnData.",
  "examples": [
   "ov.utils.load_metabolights('MTBLS1', group_col='Factor Value[Metabolic syndrome]', cache_dir='mtbls1_demo')"
  ],
  "related": []
 },
 "ov.utils.mde": {
  "_module": "omicverse.utils._mde",
  "_name": "mde",
  "aliases": [
   "mde",
   "ov.utils.mde",
   "corrected embedding",
   "data preprocessing",
   "visualize the reference and mapping"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Util to run :func:`pymde.preserve_neighbors` for visualization of scvi-tools embeddings.",
  "examples": [
   "ov.utils.mde(adata.obsm['X_pca_harmony'])"
  ],
  "related": [
   "ov.pl.embedding",
   "ov.pp.scale",
   "ov.pp.pca",
   "ov.single.batch_correction",
   "ov.pp.umap"
  ]
 },
 "ov.utils.plot_paga": {
  "_module": "omicverse.utils._paga",
  "_name": "plot_paga",
  "aliases": [
   "plot_paga",
   "ov.utils.plot_paga",
   "plot paga"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Plot PAGA graph and optional embedding-level annotations.",
  "examples": [
   "ov.utils.plot_paga(adata, basis='mde', size=50, alpha=0.1, title='PAGA LTNN-graph', min_edge_width=2, node_size_scale=1.5, show=False, legend_loc=False)"
  ],
  "related": [
   "ov.utils.cal_paga",
   "ov.pl.embedding",
   "ov.single.pyVIA",
   "ov.pl.dynamic_heatmap",
   "ov.pl.branch_streamplot"
  ]
 },
 "ov.utils.preflight_alignment": {
  "_module": "omicverse.utils._sample_metadata_alignment",
  "_name": "preflight_alignment",
  "aliases": [
   "preflight_alignment",
   "ov.utils.preflight_alignment",
   "preflight alignment"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Diagnose sample-axis alignment between `matrix` and `meta`.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_alphafold": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_alphafold",
  "aliases": [
   "query_alphafold",
   "ov.utils.query_alphafold",
   "query alphafold"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query AlphaFold DB for predicted protein structure.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_cell_ontology": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_cell_ontology",
  "aliases": [
   "query_cell_ontology",
   "ov.utils.query_cell_ontology",
   "query cell ontology"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query Cell Ontology for cell type terms.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_chebi": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_chebi",
  "aliases": [
   "query_chebi",
   "ov.utils.query_chebi",
   "query chebi"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query ChEBI for chemical entities.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_efo": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_efo",
  "aliases": [
   "query_efo",
   "ov.utils.query_efo",
   "query efo"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query EFO for disease ontology terms.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_go": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_go",
  "aliases": [
   "query_go",
   "ov.utils.query_go",
   "query go"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query Gene Ontology terms for a gene.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_hpa": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_hpa",
  "aliases": [
   "query_hpa",
   "ov.utils.query_hpa",
   "query hpa"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query Human Protein Atlas for tissue-level expression.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_interpro": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_interpro",
  "aliases": [
   "query_interpro",
   "ov.utils.query_interpro",
   "query interpro"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query InterPro for protein domains.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_opentargets": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_opentargets",
  "aliases": [
   "query_opentargets",
   "ov.utils.query_opentargets",
   "query opentargets"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query Open Targets via GraphQL.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_panglaodb": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_panglaodb",
  "aliases": [
   "query_panglaodb",
   "ov.utils.query_panglaodb",
   "query panglaodb"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query PanglaoDB for cell type marker genes.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_reactome": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_reactome",
  "aliases": [
   "query_reactome",
   "ov.utils.query_reactome",
   "query reactome"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query Reactome pathway database.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_string": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_string",
  "aliases": [
   "query_string",
   "ov.utils.query_string",
   "query string"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query STRING for protein-protein interactions.",
  "examples": [],
  "related": []
 },
 "ov.utils.query_uniprot": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "query_uniprot",
  "aliases": [
   "query_uniprot",
   "ov.utils.query_uniprot",
   "query uniprot"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Query UniProt protein information.",
  "examples": [],
  "related": []
 },
 "ov.utils.refine_label": {
  "_module": "omicverse.utils._cluster",
  "_name": "refine_label",
  "aliases": [
   "refine_label",
   "ov.utils.refine_label",
   "refine label",
   "clustering the space"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Refine labels with neighborhood majority voting.",
  "examples": [
   "ov.utils.refine_label(adata, radius=50, key='mclust')"
  ],
  "related": [
   "ov.utils.cluster",
   "ov.space.clusters",
   "ov.space.merge_cluster",
   "ov.style",
   "ov.space.svg"
  ]
 },
 "ov.utils.retrieve_layers": {
  "_module": "omicverse.utils._data",
  "_name": "retrieve_layers",
  "aliases": [
   "retrieve_layers",
   "ov.utils.retrieve_layers",
   "retrieve layers"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Retrieve previously stored X matrix from adata.uns and restore to adata.X.",
  "examples": [
   "ov.utils.retrieve_layers(adata_counts, layers='counts')"
  ],
  "related": [
   "ov.pp.qc",
   "ov.utils.store_layers",
   "ov.pp.preprocess",
   "ov.pp.scale",
   "ov.pp.pca"
  ]
 },
 "ov.utils.roe": {
  "_module": "omicverse.utils._roe",
  "_name": "roe",
  "aliases": [
   "roe",
   "ov.utils.roe"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Compute the Ro/e (observed/expected) cell-type enrichment matrix.",
  "examples": [
   "ov.utils.roe(adata, sample_key='group', cell_type_key='scsa_celltype_cellmarker')"
  ],
  "related": [
   "ov.utils.embedding",
   "ov.utils.plot_cellproportion",
   "ov.utils.plot_embedding_celltype",
   "ov.pl.group_heatmap",
   "ov.single.scanpy_cellanno_from_dict"
  ]
 },
 "ov.utils.roe_plot_heatmap": {
  "_module": "omicverse.utils._roe",
  "_name": "roe_plot_heatmap",
  "aliases": [
   "roe_plot_heatmap",
   "ov.utils.roe_plot_heatmap",
   "roe plot heatmap"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Plot the Ro/e heat-map stored in ``adata.uns`` by :func:`roe`.",
  "examples": [],
  "related": []
 },
 "ov.utils.search_clinical_trials": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "search_clinical_trials",
  "aliases": [
   "search_clinical_trials",
   "ov.utils.search_clinical_trials",
   "search clinical trials"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Search ClinicalTrials.gov by condition.",
  "examples": [],
  "related": []
 },
 "ov.utils.search_drugs": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "search_drugs",
  "aliases": [
   "search_drugs",
   "ov.utils.search_drugs",
   "search drugs"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Search FDA drug database.",
  "examples": [],
  "related": []
 },
 "ov.utils.search_interpro": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "search_interpro",
  "aliases": [
   "search_interpro",
   "ov.utils.search_interpro",
   "search interpro"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Search InterPro entries.",
  "examples": [],
  "related": []
 },
 "ov.utils.search_literature": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "search_literature",
  "aliases": [
   "search_literature",
   "ov.utils.search_literature",
   "search literature"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Search Europe PMC for biomedical literature.",
  "examples": [],
  "related": []
 },
 "ov.utils.search_preprints": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "search_preprints",
  "aliases": [
   "search_preprints",
   "ov.utils.search_preprints",
   "search preprints"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Search bioRxiv or medRxiv preprints.",
  "examples": [],
  "related": []
 },
 "ov.utils.search_pride": {
  "_module": "omicverse.utils.biocontext._tools",
  "_name": "search_pride",
  "aliases": [
   "search_pride",
   "ov.utils.search_pride",
   "search pride"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Search PRIDE proteomics repository.",
  "examples": [],
  "related": []
 },
 "ov.utils.store_layers": {
  "_module": "omicverse.utils._data",
  "_name": "store_layers",
  "aliases": [
   "store_layers",
   "ov.utils.store_layers",
   "store layers",
   "preprocess pca cluster"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Store the X matrix of AnnData in adata.uns for later retrieval.",
  "examples": [
   "ov.utils.store_layers(adata, layers='counts')"
  ],
  "related": [
   "ov.pp.qc",
   "ov.pp.preprocess",
   "ov.datasets.get_adata",
   "ov.pp.scale",
   "ov.pp.pca"
  ]
 },
 "ov.utils.symbol2id": {
  "_module": "omicverse.utils._gene_id_conversion",
  "_name": "symbol2id",
  "aliases": [
   "symbol2id",
   "ov.utils.symbol2id"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Convert gene symbols in ``adata.var_names`` to Ensembl gene IDs.",
  "examples": [
   "adata = ov.utils.symbol2id(adata, species='human')",
   "adata = ov.utils.symbol2id(adata, species='mouse', subset=True)"
  ],
  "related": []
 },
 "ov.utils.weighted_knn_trainer": {
  "_module": "omicverse.utils._knn",
  "_name": "weighted_knn_trainer",
  "aliases": [
   "weighted_knn_trainer",
   "ov.utils.weighted_knn_trainer",
   "weighted knn trainer",
   "celltype transfer"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Trains a weighted KNN classifier on ``train_adata``.",
  "examples": [
   "ov.utils.weighted_knn_trainer(train_adata=rna, train_adata_emb='X_glue', n_neighbors=15)"
  ],
  "related": [
   "ov.utils.weighted_knn_transfer",
   "ov.pl.embedding",
   "ov.utils.mde",
   "ov.utils.embedding",
   "ov.palette"
  ]
 },
 "ov.utils.weighted_knn_transfer": {
  "_module": "omicverse.utils._knn",
  "_name": "weighted_knn_transfer",
  "aliases": [
   "weighted_knn_transfer",
   "ov.utils.weighted_knn_transfer",
   "weighted knn transfer"
  ],
  "auto_fix": "none",
  "category": "utils",
  "description": "Annotates ``query_adata`` cells with an input trained weighted KNN classifier.",
  "examples": [
   "ov.utils.weighted_knn_transfer(query_adata=atac, query_adata_emb='X_glue', label_keys='major_celltype', knn_model=knn_transformer, ref_adata_obs=rna.obs)"
  ],
  "related": [
   "ov.utils.weighted_knn_trainer",
   "ov.pl.embedding",
   "ov.utils.embedding",
   "ov.utils.mde",
   "ov.palette"
  ]
 }
}
""")

AUTO_PROVENANCE: dict = json.loads(r"""
{
 "ov.bulk.Deconvolution": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.Matrix_ID_mapping": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.batch_correction": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.geneset_enrichment": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.geneset_plot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.geneset_plot_multi": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.pyDEG": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.pyGSEA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.pyPPI": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.pyTCGA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.pyWGCNA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.string_interaction": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.bulk.temporal_clusters": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.CellChatViz": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.ConvexHull": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.ForbiddenCity": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.add_density_contour": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.add_palue": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.add_pie2spatial": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.add_streamplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.bardotplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.boxplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.branch_streamplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.calculate_gene_density": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.ccc_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.ccc_network_plot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.ccc_stat_plot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.cell_cor_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.cell_fate": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.cellproportion": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.cnv_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.cnv_summary": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.cnv_umap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.complexheatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.contour": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.create_custom_colormap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.dotplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.dynamic_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.dynamic_trends": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.embedding": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.embedding_adjust": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.embedding_atlas": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.embedding_celltype": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.embedding_density": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.feature_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.funky_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.gen_mpl_labels": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.geneset_wordcloud": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.group_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.marker_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.markers_dotplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.metacell_codebook_umap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.metacell_metrics": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.metacell_purity_box": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.metacell_soft_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.palette": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_cell_quiver": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_celloracle_layout": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_development_layout": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_inner_product_on_grid": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_markov_endpoints": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_quiver": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_sankey": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturb_volcano": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturbation_embedding_shift": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturbation_shift_violin": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.perturbation_top_downstream_genes": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot1cell": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_ConvexHull": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_cellproportion": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_embedding_celltype": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_flowsig_network": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_grouped_fractions": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_pca_variance_ratio": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_set": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_spatial": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_stream": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.plot_text_set": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.pyomic_palette": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.qc": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.rank_genes_groups_dotplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.rigor_scatter": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.single_group_boxplot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.stacking_vol": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.trajectory": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.trajectory_graph": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.trajectory_overlay": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.trajectory_projection": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.trajectory_tree": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.tsne": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.umap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.upset": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.venn": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.violin": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pl.volcano": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.ambient_negative_marker_check": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.anndata_to_CPU": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.anndata_to_GPU": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.binary_search": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.champ": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.contamination_report": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.count_integrity_check": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.estimate_contamination": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.filter_cells": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.filter_genes": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.highly_variable_features": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.highly_variable_genes": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.identify_robust_genes": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.leiden": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 3 > 2, no workflow-level candidate",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.log1p": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.louvain": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.mde": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 2 <= 2",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.neighbors": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 2 <= 2",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.normalize_pearson_residuals": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.pca": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 1 <= 2",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.plot_contamination": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.preprocess": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.qc": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.qc_metrics": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.recover_counts": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.regress": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.regress_and_scale": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.remove_ambient": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.remove_cc_genes": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.scale": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.score_genes_cell_cycle": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.scrublet": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.scrublet_simulate_doublets": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.select_hvf_pegasus": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.sude": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.tsne": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.pp.umap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: workflow-level candidate(s) ['ov.pp.preprocess']",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Annotation": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: workflow-level candidate(s) ['ov.pp.preprocess']",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.AnnotationRef": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Augur": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.CNV": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.CellOntologyMapper": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.CellVote": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.DCT": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.DEG": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Drug_Response": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Fate": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.GLUE_pair": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.MetaCell": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: workflow-level candidate(s) ['ov.pp.preprocess']",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.MetaTiME": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Metabolism": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.MetaboliteCCC": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Monocle": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.SCENIC": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.StaVIA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: workflow-level candidate(s) ['ov.pp.preprocess']",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.TrajInfer": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 2 <= 2",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.Velo": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.annotate_ev_subtype": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.autoResolution": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.auto_resolution": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.batch_correction": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.classify_markers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.coexpression_network": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.colocalization": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.colocalization_plot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.compare_metacell_backends": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.contaminant_score": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.convert_human_to_mouse_network": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.cosg": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.cytotrace2": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.detect_doublets": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.differential_abundance": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.differential_metabolism": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.differential_subpopulation": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.download_cellphonedb_database": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.download_cl": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.dynamic_features": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.ev_summary": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.factor_correlation": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.factor_exact": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.find_markers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.flowsom": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.format_liana_results": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.gene_trends": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.generate_scRNA_report": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.geneset_aucell": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.get_celltype_marker": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 2 <= 2",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.get_cluster_celltype": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.get_markers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.get_obs_value": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.get_weights": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.gptcelltype": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.gptcelltype_local": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.grn": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.hematopoiesis": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.lazy": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.lineage_pseudotime": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.load_human_prior_interaction_network": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.marker_enrichment": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.misev_marker_plot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.misev_markers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.misev_report": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.mouse_hsc_nestorowa16": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.normalize": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.optimize_granularity": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pathway_aucell": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pathway_aucell_enrichment": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pathway_enrichment": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pathway_enrichment_plot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.plot_metacells": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.protein_combinations": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pseudobulk": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pseudobulk_de": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.purity_report": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pyCEFCON": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pyMOFA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pyMOFAART": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pySCSA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: chain length 2 <= 2",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pySIMBA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pyTOSICA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.pyVIA": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.qc": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.rank_markers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.read_digital_ev": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.read_ev_matrix": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.read_exoview": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.read_fcs": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.read_nanofcm": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.read_pba": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.refresh_ev_metrics": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.run_cellphonedb_v5": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.run_liana": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.scanpy_cellanno_from_dict": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.simulate_ev": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.subpopulation_abundance": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.subtract_isotype": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.single.tissue_of_origin": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.CAST": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.Cal_Spatial_Net": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.CellLoc": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.CellMap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.Deconvolution": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.GASTON": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.STT": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.Tangram": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.available_backbones": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.bin2cell": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.calculate_gene_signature": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.cellcharter": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.clusters": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.create_communication_anndata": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.download_breast": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.embed": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.load_breast": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.map_spatial_auto": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.map_spatial_manual": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.merge_cluster": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.moranI": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.nmf_tissue_zones": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.open_wsi": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.predict_expression": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.pySTAGATE": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.pySTAligner": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.pySpaceFlow": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.read_visium_10x": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.read_visium_with_image": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.rotate_space_visium": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.salvage_secondary_labels": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.spatial_autocorr": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.spatial_neighbors": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.split_balance": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.split_purify": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.split_reassign_residuals": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.split_spatial_score": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.spot_features": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.subset_window": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.super_resolve": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.svg": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.sync_visium_hd_seg_geometries": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.tile": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.update_classification_from_database": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.visium_10x_hd_cellpose_expand": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.visium_10x_hd_cellpose_gex": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.space.visium_10x_hd_cellpose_he": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.LDA_topic": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils._download_enrichr_library": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.align_samples": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.align_to_common": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.cal_paga": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.call_tool": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.cluster": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.convert2gene_id": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.convert2gene_symbol": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.convert2symbol": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.download_CaDRReS_model": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.download_GDSC_data": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.download_geneid_annotation_pair": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.download_pathway_database": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.download_tosica_gmt": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.get_ensembl_id": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.get_fulltext": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.get_gene_annotation": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.get_uniprot_id": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.gtf_to_pair_tsv": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.list_tools": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.load_metabolights": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.mde": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.plot_paga": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.preflight_alignment": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_alphafold": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_cell_ontology": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_chebi": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_efo": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_go": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_hpa": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_interpro": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_opentargets": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_panglaodb": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_reactome": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_string": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.query_uniprot": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.refine_label": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.retrieve_layers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.roe": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.roe_plot_heatmap": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.search_clinical_trials": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.search_drugs": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.search_interpro": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.search_literature": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.search_preprints": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.search_pride": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.store_layers": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.symbol2id": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.weighted_knn_trainer": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 },
 "ov.utils.weighted_knn_transfer": {
  "aliases": "mined (unverified)",
  "auto_fix": "derived: no confirmed prerequisite chain",
  "category": "derived (unverified)",
  "description": "docstring (unverified)",
  "examples": "tutorial call site (unverified)",
  "prerequisites": "probe-verified (ablation)",
  "produces": "probe-verified",
  "related": "mined co-occurrence (unverified)",
  "requires": "probe-verified"
 }
}
""")
