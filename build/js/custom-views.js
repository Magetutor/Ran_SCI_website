/**
 * custom-views.js — 自定义视图控制
 */

/**
 * 导出当前 UMAP 视图为 PNG
 */
function exportUMAP() {
  const canvas = document.querySelector(".vitessce-scatter-plot canvas");
  if (!canvas) {
    alert("UMAP plot not found. Please select a UMAP view first.");
    return;
  }
  const link = document.createElement("a");
  link.download = "UMAP_sci.png";
  link.href = canvas.toDataURL("image/png");
  link.click();
}

/**
 * 高亮选中的细胞类型
 */
function highlightCellType(cellType) {
  const vc = window.vitessceChain || window.vc;
  if (!vc) return;
  try {
    vc.changeObsSetSelection([`cell_type=${cellType}`]);
  } catch (e) {
    console.warn("Could not highlight cell type:", e);
  }
}

/**
 * 条件对比模式
 */
function setConditionView(condA, condB) {
  const vc = window.vitessceChain || window.vc;
  if (!vc) return;
  try {
    vc.changeObsSetSelection([
      `condition=${condA}`,
      `condition=${condB}`,
    ]);
  } catch (e) {
    console.warn("Could not set condition view:", e);
  }
}

/**
 * 生成可分享的 URL
 * 编码当前选择的基因和细胞类型到 URL hash
 */
function generateShareLink() {
  const state = {
    genes: document.getElementById("geneSearch")?.value || "",
    cellTypes: getSelectedCellTypes(),
  };
  const hash = btoa(JSON.stringify(state));
  const url = `${window.location.origin}${window.location.pathname}#${hash}`;
  navigator.clipboard.writeText(url).then(() => {
    showToast("Share link copied to clipboard!");
  });
}

/**
 * 从 URL hash 恢复视图状态
 */
function restoreFromHash() {
  const hash = window.location.hash.slice(1);
  if (!hash) return;
  try {
    const state = JSON.parse(atob(hash));
    if (state.genes) {
      document.getElementById("geneSearch")?.value = state.genes;
      dispatchGeneSelect(state.genes.split(",").map(g => g.trim()));
    }
  } catch (e) {
    console.warn("Could not restore state from URL:", e);
  }
}

/**
 * 简易 toast 提示
 */
function showToast(message) {
  const toast = document.createElement("div");
  toast.style.cssText = `
    position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
    background: #1a3a5c; color: white; padding: 0.75rem 1.5rem;
    border-radius: 8px; font-size: 0.9rem; z-index: 9999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    animation: fadeInOut 3s ease forwards;
  `;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
}

// 添加 CSS animation
const style = document.createElement("style");
style.textContent = `
  @keyframes fadeInOut {
    0% { opacity: 0; transform: translateX(-50%) translateY(10px); }
    15% { opacity: 1; transform: translateX(-50%) translateY(0); }
    85% { opacity: 1; }
    100% { opacity: 0; }
  }
`;
document.head.appendChild(style);
