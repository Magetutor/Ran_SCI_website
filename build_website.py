#!/usr/bin/env python3
"""
build_website.py — 生成 h5vc.json 配置 (remote mode)
"""
import json
import subprocess
from pathlib import Path

PYTHON = "/home/bio/miniconda3/envs/vitessce/bin/python"
BUILD = Path("build")
BUILD.mkdir(parents=True, exist_ok=True)

# Generate h5vc.json using vitessce Python SDK
config_code = '''
import json
from vitessce import VitessceConfig, ViewType, AnnDataWrapper

vc = VitessceConfig(
    name="Mouse Spinal Cord Injury snRNA-seq atlas",
    description="Single-nucleus RNA-seq atlas of mouse spinal cord injury. 48,709 nuclei from 4 samples: WT female/male x IFNAR-KO female/male. Harmony-integrated, 7 cell types.",
    schema_version="1.0.0",
)

dataset = vc.add_dataset(name="SCI snRNA-seq (WT x IFNAR-KO)", uid="own_data")

h5ad_url = "https://huggingface.co/datasets/Magetutor/sci-snrnaseq-atlas/resolve/main/own_data.h5ad"
ref_url = "https://huggingface.co/datasets/Magetutor/sci-snrnaseq-atlas/resolve/main/own_data.reference.json"

wrapper = AnnDataWrapper(
    adata_url=h5ad_url,
    ref_url=ref_url,
    obs_set_paths=[ref_url],
    obs_labels_paths=[ref_url],
)
dataset.add_object(wrapper)

# Views — mapping must be the obsm key name (e.g. "X_umap"), NOT cell type or gene name
vc.add_view(ViewType.SCATTERPLOT, dataset=dataset, x=0, y=0, w=3, h=3, mapping="X_umap")
vc.add_view(ViewType.SCATTERPLOT, dataset=dataset, x=3, y=0, w=3, h=3, mapping="X_umap")
vc.add_view(ViewType.CELL_SET_SIZES, dataset=dataset, x=0, y=3, w=2, h=2)
vc.add_view(ViewType.CELL_SET_EXPRESSION, dataset=dataset, x=2, y=3, w=2, h=2)
vc.add_view(ViewType.HEATMAP, dataset=dataset, x=4, y=3, w=2, h=2)
vc.add_view(ViewType.STATUS, dataset=dataset, x=0, y=5, w=6, h=1)
vc.add_view(ViewType.DESCRIPTION, dataset=dataset, x=0, y=6, w=6, h=2, props={
    "title": "Mouse Spinal Cord Injury snRNA-seq atlas",
    "markdown": """## Overview
Single-nucleus RNA-seq analysis of spinal cord injury (SCI) in mice.

### Samples
| Condition | Genotype | Sex |
|-----------|----------|-----|
| WT_F | C57BL/6 (WT) | Female |
| WT_M | C57BL/6 (WT) | Male |
| KO_F | IFNAR Knockout | Female |
| KO_M | IFNAR Knockout | Male |

### Data
- **48,709 nuclei** after QC (DecontX + scDblFinder)
- **21,839 genes**
- **7 cell types**: Neuron, Astrocyte, Oligodendrocyte, OPC, Microglia, Endothelial, Pericyte
- **Harmony** integration
- **14 clusters** (resolution = 0.4)

### m1A Genes
- **Writers**: Trmt10c, Trmt6, Trmt61a
- **Erasers**: Alkbh1, Alkbh3, Fto
- **Readers**: Ythdc1, Ythdf1, Ythdf2, Ythdf3
""",
})

config_dict = vc.to_dict(base_url=".")
with open("h5vc.json", "w") as f:
    json.dump(config_dict, f, indent=2)
print("h5vc.json generated")
'''

result = subprocess.run([PYTHON, "-c", config_code], capture_output=True, text=True)
if result.returncode != 0:
    print(f"ERROR: {result.stderr}")
    raise RuntimeError("Failed to build config")
print(result.stdout)
print("Build complete!")
