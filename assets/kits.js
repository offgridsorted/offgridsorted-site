// Kit pages: price-level tabs, "Make it yours" choices (vehicle, build, solar) and live totals.
(function () {
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  // Price-level tabs (phones)
  document.querySelectorAll(".kit-table").forEach(function (box) {
    box.querySelectorAll(".tier-tabs button").forEach(function (b) {
      b.addEventListener("click", function () {
        box.setAttribute("data-tier", b.dataset.t);
        box.querySelectorAll(".tier-tabs button").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      });
    });
  });

  var choices = document.querySelectorAll(".kit-choices .seg");
  if (!choices.length) return;
  var state = {};
  choices.forEach(function (seg) {
    var on = seg.querySelector('[aria-pressed="true"]');
    if (on) state[on.dataset.g] = on.dataset.v;
  });
  var solarDefault = state.solar, solarTouched = false;
  var urlV = (location.search.match(/[?&]v=(van|caravan|4wd)/) || [])[1];
  state.veh = urlV || store("ogs-veh") || state.veh || "van";
  if (state.veh === "4wd" && state.solar) state.solar = "blanket";

  var table = document.querySelector(".kit-table[data-totals]");
  var totals = table ? JSON.parse(table.getAttribute("data-totals")) : null;
  var groups = [];
  choices.forEach(function (seg) { var g = seg.querySelector("button").dataset.g; if (g !== "veh") groups.push(g); });

  function money(n) { return "$" + Math.round(n).toLocaleString("en-AU"); }

  function apply() {
    choices.forEach(function (seg) {
      seg.querySelectorAll("button").forEach(function (b) { b.setAttribute("aria-pressed", state[b.dataset.g] === b.dataset.v ? "true" : "false"); });
    });
    document.querySelectorAll("tr[data-g]").forEach(function (tr) {
      var g = tr.dataset.g;
      tr.hidden = state[g] !== undefined && state[g] !== tr.dataset.v;
    });
    if (totals) {
      var key = groups.map(function (g) { return g + "=" + state[g]; }).join("|");
      var d = totals[key];
      if (d) {
        table.querySelectorAll(".totrow .tot").forEach(function (el, i) { el.textContent = money(d.t[i]); });
        var nm = table.querySelector(".tot-names"); if (nm) nm.textContent = d.n;
      }
    }
    document.querySelectorAll(".veh-tip").forEach(function (t) { t.hidden = t.dataset.for !== state.veh; });
    var cz = document.getElementById("customise");
    if (cz) { var main = document.querySelector("main[data-preset]"); cz.setAttribute("href", cz.getAttribute("href").split("#")[0] + "#" + main.dataset.preset + (state.veh !== "van" ? "+" + state.veh : "")); }
    document.querySelectorAll("a.kit-card").forEach(function (a) { a.setAttribute("href", a.getAttribute("href").split("?")[0] + (state.veh !== "van" ? "?v=" + state.veh : "")); });
    store("ogs-veh", state.veh);
  }

  choices.forEach(function (seg) {
    seg.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      state[b.dataset.g] = b.dataset.v;
      if (b.dataset.g === "solar") solarTouched = true;
      if (b.dataset.g === "veh" && solarDefault && !solarTouched) state.solar = b.dataset.v === "4wd" ? "blanket" : solarDefault;
      apply();
    });
  });
  apply();
})();
