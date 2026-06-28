# Ran_SCI Website — 脊髓损伤单细胞数据交互式可视化

Interactive single-cell data visualization website for the Ran_SCI project.

## Quick Start

```bash
# 1. 创建 vitessce conda 环境
conda create -n vitessce -c conda-forge python=3.10 scanpy anndata numpy pandas h5py zarr rpy2 matplotlib -y
conda activate vitessce
pip install vitessce==3.4.0

# 2. 进入 website 目录
cd /home/data/Projects/2026/Ran_SCI/website

# 3. 一键构建
python build_website.py

# 4. 本地预览
python preview.py
# 自动打开浏览器访问 vitessce.io
```

## Directory Structure

```
website/
├── src/                      # 源代码
│   ├── config/               #   Vitessce 配置
│   │   ├── build_config.py   #     配置生成
│   │   ├── colors.py         #     配色方案
│   │   └── gene_sets.py      #     基因集定义
│   ├── data_prep/            #   数据转换
│   │   └── convert_own_data.py #   .qs → zarr
│   └── static/               #   前端文件
│       ├── index.html        #     主页面
│       ├── css/              #     样式
│       └── js/               #     交互脚本
├── data/                     # zarr 数据文件 (~3 GB)
│   └── own/
│       ├── own_data.h5ad.zarr/
│       └── own_data.cell_sets.json
├── build/                    # 构建输出 → 部署
│   ├── index.html
│   ├── h5vc.json
│   └── data/ → ../data/
├── build_website.py          # 一键构建脚本
├── preview.py                # 本地预览脚本
└── requirements.txt
```

## Data Pipeline

```
06_sci_annotated.qs (R)
        ↓ [R script: convert_own_data.R]
counts.mtx + barcodes.txt + genes.txt + UMAP.npy + PCA.npy + Harmony.npy + metadata.csv
        ↓ [Python: convert_own_data.py]
own_data.h5ad.zarr (~150 MB)
        ↓ [build_config.py]
h5vc.json
        ↓ [build_website.py]
build/ (static website)
```

## Views

1. **UMAP** — 按细胞类型着色 (7 colors)
2. **Gene Expression** — m1A 基因在 UMAP 上的表达
3. **Composition** — 条件 × 细胞类型比例
4. **Cell Set Expression** — 条件对比箱线图
5. **Heatmap** — 基因集 × 细胞类型
6. **Status** — 细胞数、QC 指标
7. **Description** — 项目介绍

## Tech Stack

- **Vitessce** 3.4.0 — 单细胞可视化框架
- **Scanpy** — AnnData 操作
- **zarr** — 数据存储格式
- **HTML/CSS/JS** — 自定义前端

## Deployment

- 代码 → GitHub (gh-pages branch)
- 数据 → Zenodo (zarr files, ~150 MB)
- 网站通过 vitessce.io 渲染 (无需后端)

## Next Steps (v2)

1. 添加 GSE234774 公共数据 (435K cells)
2. 数据集切换标签 (Own Data | GSE234774)
3. m1A 时间进程 dotplot
4. 差异表达分析 (KO vs WT per cell type)
