// "My list": add products from any kit page or the Power Planner, then buy from one list at the bottom.
// Saved only in this browser (localStorage), shared across kit pages and the planner.
(function () {
  var KEY = "ogs-list";
  var list = [];
  try { list = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { list = []; }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) {} }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function money(n) { return "$" + Math.round(n).toLocaleString("en-AU"); }
  function has(name) { return list.some(function (x) { return x.n === name; }); }
  function total() { return list.reduce(function (a, x) { return a + (x.p || 0); }, 0); }

  function markButtons() {
    document.querySelectorAll(".add-list").forEach(function (b) {
      var it = JSON.parse(b.getAttribute("data-item"));
      var on = has(it.n);
      b.classList.toggle("on", on);
      b.textContent = on ? "✓ On my list" : "+ Add to my list";
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
  }

  function render() {
    var box = document.getElementById("my-list");
    if (box) {
      if (!list.length) {
        box.innerHTML = '<h2>My list</h2><p class="small">Nothing here yet. Tap <b>+ Add to my list</b> on anything above and it will appear here, with a link to buy it.</p>';
      } else {
        var byStore = {};
        list.forEach(function (x, i) { (byStore[x.s] = byStore[x.s] || []).push({ x: x, i: i }); });
        var html = '<h2>My list</h2><p class="ml-sum"><b>' + list.length + " item" + (list.length > 1 ? "s" : "") + "</b> · about <b>" + money(total()) + "</b> in parts</p>";
        Object.keys(byStore).forEach(function (s) {
          html += '<div class="ml-store"><h3>' + esc(s) + "</h3><ul>";
          byStore[s].forEach(function (o) {
            html += '<li><span class="ml-name">' + esc(o.x.n) + '</span><span class="ml-price">' + (o.x.p ? (o.x.a ? "about " : "") + money(o.x.p) : "") + '</span>' +
              '<a class="ml-buy" href="' + esc(o.x.u) + '" target="_blank" rel="sponsored nofollow noopener">Buy at ' + esc(s) + ' ↗</a>' +
              '<button type="button" class="ml-rm" data-i="' + o.i + '" aria-label="Remove ' + esc(o.x.n) + '">Remove</button></li>';
          });
          html += "</ul></div>";
        });
        html += '<div class="ml-actions"><button type="button" class="btn ghost" id="ml-copy">Copy my list</button><button type="button" class="link-btn" id="ml-clear">Clear list</button></div>' +
          '<p class="small" id="ml-msg" role="status"></p>' +
          '<p class="small">Saved on this device, and shared between the kit pages and the Power Planner. Links go to the cheapest shop we found when we checked; prices change. Remember installation is extra.</p>';
        box.innerHTML = html;
      }
    }
    var pill = document.getElementById("list-pill");
    if (pill) { pill.querySelector("span").textContent = "My list · " + list.length + " · " + money(total()); updatePill(); }
    markButtons();
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest(".add-list");
    if (b) {
      var it = JSON.parse(b.getAttribute("data-item"));
      if (has(it.n)) list = list.filter(function (x) { return x.n !== it.n; });
      else list.push(it);
      save(); render(); return;
    }
    var rm = e.target.closest(".ml-rm");
    if (rm) { list.splice(+rm.dataset.i, 1); save(); render(); return; }
    if (e.target.id === "ml-clear") { list = []; save(); render(); return; }
    if (e.target.id === "ml-copy") {
      var lines = ["My power shopping list (Off-Grid Sorted)", ""];
      list.forEach(function (x) { lines.push("- " + x.n + (x.p ? ", " + (x.a ? "about " : "") + money(x.p) : "") + " at " + x.s + ": " + x.u); });
      lines.push("", "Total parts: about " + money(total()) + ". Have a licensed auto electrician install or check it.");
      var msg = document.getElementById("ml-msg");
      try { navigator.clipboard.writeText(lines.join("\n")).then(function () { msg.textContent = "Copied. Paste it into your notes or send it to your auto electrician."; }, function () { msg.textContent = "Couldn't copy here."; }); }
      catch (err) { msg.textContent = "Couldn't copy here."; }
    }
  });

  // Floating pill that jumps to the list
  var pill = document.createElement("a");
  pill.id = "list-pill"; pill.className = "list-pill"; pill.href = "#my-list"; pill.hidden = true;
  pill.innerHTML = "<span></span> ↓";
  document.body.appendChild(pill);
  var listVisible = false;
  function updatePill() { pill.hidden = !list.length || listVisible || !document.getElementById("my-list"); }
  var target = document.getElementById("my-list");
  if (target && "IntersectionObserver" in window) new IntersectionObserver(function (es) { listVisible = es[0].isIntersecting; updatePill(); }).observe(target);

  window.ogsList = { refresh: render };
  render();
})();
