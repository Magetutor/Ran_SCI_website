#!/usr/bin/env python3
"""
preview.py — 本地预览
使用 vitessce.io + 本地数据服务器
"""

import sys
import os
import webbrowser
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
BUILD_DIR = PROJECT_DIR / "build"

# Try conda vitessce env first, then fall back to system python
CONDA_PYTHON = Path("/home/bio/miniconda3/envs/vitessce/bin/python")
if CONDA_PYTHON.exists():
    sys.path.insert(0, str(CONDA_PYTHON.parent / "lib/python3.10/site-packages"))

sys.path.insert(0, str(PROJECT_DIR))

from vitessce import VitessceConfig, ViewType, AnnDataWrapper
from vitessce.widget import launch_vitessce_io


def main():
    if not BUILD_DIR.exists():
        print(f"ERROR: build/ not found at {BUILD_DIR}")
        print("Run build_website.py first:")
        print(f"  cd {PROJECT_DIR}")
        print(f"  python build_website.py")
        sys.exit(1)

    # Ensure data symlink exists
    import os
    data_link = BUILD_DIR / "data"
    if not data_link.exists() and not data_link.is_symlink():
        os.symlink("../data", str(data_link))

    print("=" * 50)
    print("  Ran_SCI Website Preview")
    print("=" * 50)

    # Build Vitessce config
    vc = VitessceConfig(
        name="Ran_SCI — Mouse Spinal Cord Injury snRNA-seq",
        description=(
            "Single-nucleus RNA-seq of mouse spinal cord injury. "
            "48,709 nuclei from 4 samples."
        ),
        schema_version="1.0.0",
    )
    vc.base_dir = str(BUILD_DIR)

    dataset = vc.add_dataset(
        name="SCI snRNA-seq (WT x IFNAR-KO)",
        uid="own_data",
    )

    wrapper = AnnDataWrapper(
        adata_path="data/own/own_data.h5ad",
        ref_path="data/own/own_data.reference.json",
        obs_set_paths=["data/own/own_data.reference.json"],
        obs_labels_paths=["data/own/own_data.reference.json"],
    )
    dataset.add_object(wrapper)

    # Views
    vc.add_view(ViewType.SCATTERPLOT, dataset=dataset, x=0, y=0, w=3, h=3, mapping="cell_type_auto")
    vc.add_view(ViewType.SCATTERPLOT, dataset=dataset, x=3, y=0, w=3, h=3, mapping="gene_expression")
    vc.add_view(ViewType.CELL_SET_SIZES, dataset=dataset, x=0, y=3, w=2, h=2)
    vc.add_view(ViewType.CELL_SET_EXPRESSION, dataset=dataset, x=2, y=3, w=2, h=2)
    vc.add_view(ViewType.HEATMAP, dataset=dataset, x=4, y=3, w=2, h=2)
    vc.add_view(ViewType.STATUS, dataset=dataset, x=0, y=5, w=6, h=1)
    vc.add_view(ViewType.DESCRIPTION, dataset=dataset, x=0, y=6, w=6, h=2, props={
        "title": "Ran_SCI: Mouse Spinal Cord Injury snRNA-seq",
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
- **48,709 nuclei** after QC
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

    # Launch vitessce.io with local server
    print("\nStarting local data server...")
    print("Opening vitessce.io in browser...\n")

    url = launch_vitessce_io(vc, open=True)
    print(f"\nVitessce URL: {url[:200]}...")
    print(f"\nLocal server is running on the port shown above.")
    print("Press Ctrl+C to stop the server.")


if __name__ == "__main__":
    main()
