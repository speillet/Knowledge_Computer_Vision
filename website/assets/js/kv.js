// Enhance native details: controls, direct card links and complete printed answers.
(() => {
  "use strict";
  const cards = () => document.querySelectorAll("details.kv-card, details.kv-fold");
  document.querySelectorAll("[data-kv-tools]").forEach((tools) => { tools.hidden = false; });
  document.querySelectorAll("[data-kv-expand]").forEach((button) => button.addEventListener("click", () => {
    cards().forEach((card) => { card.open = true; });
  }));
  document.querySelectorAll("[data-kv-collapse]").forEach((button) => button.addEventListener("click", () => {
    cards().forEach((card) => { card.open = false; });
  }));
  const reveal = () => {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)).toLowerCase(); } catch { return; }
    const target = id && document.getElementById(id);
    if (!target) return;
    for (let node = target; node; node = node.parentElement) {
      if (node.tagName === "DETAILS") node.open = true;
    }
    target.scrollIntoView({ block: "start" });
  };
  window.addEventListener("hashchange", reveal);
  reveal();
  let printState = [];
  window.addEventListener("beforeprint", () => {
    printState = [...document.querySelectorAll("details")].map((node) => [node, node.open]);
    printState.forEach(([node]) => { node.open = true; });
  });
  window.addEventListener("afterprint", () => printState.forEach(([node, open]) => { node.open = open; }));
})();
