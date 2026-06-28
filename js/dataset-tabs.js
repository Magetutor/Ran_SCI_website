/**
 * dataset-tabs.js — 数据集切换标签 (v2 预留)
 *
 * v1: 仅展示自有数据, 此文件预留
 * v2: 添加 GSE234774 公共数据后启用
 */

const DATASETS = {
  own: {
    name: "Own Data",
    subtitle: "48,709 nuclei (4 samples)",
    file: "data/own/own_data.h5ad",
  },
  // public: {
  //   name: "GSE234774",
  //   subtitle: "435K cells (multi-condition)",
  //   file: "data/public/public_data.h5ad.zarr",
  // },
};

/**
 * 初始化数据集标签 (v1: 隐藏, v2 时取消注释)
 */
function initDatasetTabs() {
  // const tabContainer = document.createElement("div");
  // tabContainer.className = "dataset-tabs";
  // ... tab HTML and logic
  console.log("Dataset tabs: v2 feature (not enabled in v1)");
}
