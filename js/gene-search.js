/**
 * gene-search.js — m1A 基因搜索与自动补全
 */

const M1A_GENES = {
  writers: { genes: ["Trmt10c", "Trmt6", "Trmt61a"], color: "#59a14f", label: "Writer" },
  erasers: { genes: ["Alkbh1", "Alkbh3", "Fto"], color: "#e15759", label: "Eraser" },
  readers: { genes: ["Ythdc1", "Ythdf1", "Ythdf2", "Ythdf3"], color: "#4e79a7", label: "Reader" },
};

const CELL_TYPE_MARKERS = {
  Neuron: ["Syp", "Syt1", "Snap25", "Tubb3", "Nefl", "Nefm", "Rbfox3"],
  Astrocyte: ["Aqp4", "Gfap", "Slc1a3", "Aldh1l1", "Fgfr3"],
  Oligodendrocyte: ["Mbp", "Plp1", "Mog", "Mag", "Cnp", "Olig1", "Olig2"],
  OPC: ["Pdgfra", "Cspg4", "Sox10", "Nkx2-2", "Olig1"],
  Microglia: ["Cx3cr1", "Csf1r", "Itgam", "Aif1", "Tmem119", "P2ry12"],
  Endothelial: ["Cldn5", "Pecam1", "Flt1", "Tek", "Cdh5"],
  Pericyte: ["Pdgfrb", "Rgs5", "Cspg4", "Anpep"],
};

// Build flat gene list with category info
const ALL_GENES = [];
for (const [cat, info] of Object.entries(M1A_GENES)) {
  for (const gene of info.genes) {
    ALL_GENES.push({ symbol: gene, category: cat, color: info.color, label: info.label });
  }
}
for (const [ct, markers] of Object.entries(CELL_TYPE_MARKERS)) {
  for (const gene of markers) {
    if (!ALL_GENES.find(g => g.symbol === gene)) {
      ALL_GENES.push({ symbol: gene, category: "marker", color: "#af7aa1", label: ct });
    }
  }
}
ALL_GENES.sort((a, b) => a.symbol.localeCompare(b.symbol));

/**
 * Create gene search UI
 */
function createGeneSearch() {
  const container = document.createElement("div");
  container.className = "gene-search-container";

  container.innerHTML = `
    <span class="gene-search-label">🔬 Gene</span>
    <div style="position:relative; flex:1; min-width:200px; max-width:400px;">
      <input type="text" class="gene-search-input" id="geneSearch"
             placeholder="Search m1A genes..." autocomplete="off">
      <div class="autocomplete-dropdown" id="geneAutocomplete" style="display:none;"></div>
    </div>
    <div class="gene-presets">
      <button class="gene-preset-btn all-m1a" data-genes="all">All m1A</button>
      <button class="gene-preset-btn writers" data-genes="writers">Writers</button>
      <button class="gene-preset-btn erasers" data-genes="erasers">Erasers</button>
      <button class="gene-preset-btn readers" data-genes="readers">Readers</button>
    </div>
  `;

  document.body.prepend(container);

  const input = document.getElementById("geneSearch");
  const dropdown = document.getElementById("geneAutocomplete");

  // ─── Input handler ───────────────────────────────
  input.addEventListener("input", () => {
    const val = input.value.trim().toUpperCase();
    if (val.length === 0) {
      dropdown.style.display = "none";
      return;
    }
    const matches = ALL_GENES.filter(g => g.symbol.toUpperCase().includes(val)).slice(0, 10);
    if (matches.length === 0) {
      dropdown.style.display = "none";
      return;
    }
    dropdown.innerHTML = matches.map((g, i) => `
      <div class="autocomplete-item${i === 0 ? ' selected' : ''}" data-gene="${g.symbol}">
        <span>${g.symbol}</span>
        <span class="gene-category ${g.category}" style="background:${g.color}">${g.label}</span>
      </div>
    `).join("");
    dropdown.style.display = "block";

    dropdown.querySelectorAll(".autocomplete-item").forEach(item => {
      item.addEventListener("click", () => selectGene(item.dataset.gene));
    });
  });

  // ─── Preset buttons ──────────────────────────────
  container.querySelectorAll(".gene-preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const type = btn.dataset.genes;
      container.querySelectorAll(".gene-preset-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      let genes;
      if (type === "all") {
        genes = Object.values(M1A_GENES).flatMap(info => info.genes);
      } else {
        genes = M1A_GENES[type].genes;
      }
      input.value = genes.join(", ");
      dispatchGeneSelect(genes);
    });
  });

  // ─── Enter key ───────────────────────────────────
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const val = input.value.trim();
      const genes = val.split(",").map(g => g.trim()).filter(g => g);
      if (genes.length > 0) dispatchGeneSelect(genes);
    }
  });

  // ─── Click outside ───────────────────────────────
  document.addEventListener("click", (e) => {
    if (!container.contains(e.target)) {
      dropdown.style.display = "none";
    }
  });
}

/**
 * Dispatch gene selection to Vitessce
 */
function dispatchGeneSelect(geneList) {
  // Try to find Vitessce instance and update feature selection
  const vc = window.vitessceChain || window.vc;
  if (vc) {
    try {
      // Vitessce API for feature selection
      vc.changeFeatureSelection(geneList);
    } catch (e) {
      console.warn("Could not dispatch gene to Vitessce:", e);
    }
  }
  console.log("Selected genes:", geneList);
}
