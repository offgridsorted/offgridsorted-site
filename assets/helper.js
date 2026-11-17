/* Off-Grid Sorted simple helper: answers common questions from our guides. No AI, nothing sent anywhere. */
(function(){
  if(window.self !== window.top) return;
  var me = document.currentScript, pre = (me && me.getAttribute("data-pre")) || "";
  var G = function(slug){ return pre + "guides/" + slug + ".html"; };
  var PLAN = pre + "planner.html";
  var QA = [
    {k:["start","new","begin","basics","beginner","overwhelm","confus","where do i","what do i need","four"], q:"I'm new. Where do I start?",
     a:"Start with the four main parts: a <b>battery</b> stores power, <b>solar</b> tops it up, a <b>DC-DC charger</b> fills it while you drive, and an <b>inverter</b> runs normal 240V plugs. When you're ready, the Power Planner works out sizes for you.",
     l:[["The basics of off-grid power", G("van-power-basics")],["Open the Power Planner", PLAN]]},
    {k:["size","how big","how much battery","battery size","amp hour","ah","capacity"], q:"What size battery do I need?",
     a:"It depends on what you run and for how long. The fridge is usually the biggest user. The Power Planner adds up your gear, the sun where you camp and your driving, then suggests a size. Lots of weekenders land around 100 to 200Ah of lithium.",
     l:[["Work it out in the Power Planner", PLAN],["Battery size for a 12V fridge", G("battery-size-for-12v-fridge")]]},
    {k:["lithium","agm","lead","lifepo4","which battery","battery type"], q:"Lithium or AGM?",
     a:"<b>Lithium</b> costs more but you can use almost all of it, it's much lighter and lasts years longer. <b>AGM</b> is cheaper to buy, but you can only use about half, so it needs to be about twice the size and is much heavier.",
     l:[["Lithium vs AGM", G("lithium-vs-agm")]]},
    {k:["solar","panel","watt","how much solar","sun"], q:"How much solar do I need?",
     a:"Enough to put back what you use each day. That depends on where and when you camp: the sun is much weaker in a southern winter. The Power Planner uses Bureau of Meteorology sun data for your state and season.",
     l:[["How much solar you need in Australia", G("how-much-solar-australia")],["Open the Power Planner", PLAN]]},
    {k:["blanket","fixed","portable panel","folding"], q:"Solar blanket or roof panels?",
     a:"<b>Roof panels</b> are set and forget and charge while you drive, but the van has to sit in the sun. A <b>blanket</b> lets you park in the shade and lay it in the sun, but you set it up each time.",
     l:[["Solar blanket vs fixed panel", G("solar-blanket-vs-fixed-panel")]]},
    {k:["dc-dc","dcdc","dc to dc","charge while driving","drive","alternator","bcdc"], q:"Do I need a DC-DC charger?",
     a:"If you drive between camps, usually yes. It's the charger that fills your camping battery from the engine while you drive. Newer cars with a \"smart\" alternator need one to charge properly. Many also take solar, so one box does both jobs.",
     l:[["DC-DC chargers explained", G("dc-dc-chargers-explained")],["Do I have a smart alternator?", G("smart-alternator-check")]]},
    {k:["smart alternator","variable voltage","euro 5","euro 6"], q:"Do I have a smart alternator?",
     a:"Most newer vehicles do. There's a simple check with a multimeter. If you have one, you'll want a DC-DC charger that supports it.",
     l:[["The smart alternator check", G("smart-alternator-check")]]},
    {k:["inverter","240","240v","house power","plug","hair dryer","kettle","coffee","laptop"], q:"Do I need an inverter?",
     a:"Only if you want to run things with a normal 240V plug. Get a <b>pure sine wave</b> one, sized for your biggest appliance. Kettles, hair dryers and coffee machines need a big inverter and drain the battery fast, so many people swap to gas or 12V versions.",
     l:[["Open the Power Planner", PLAN]]},
    {k:["fridge","flat","dies","drain","last","weekend","overnight"], q:"Will my fridge last the weekend?",
     a:"Work out what it uses in a day, then compare that to the battery you can actually use. Heat, a full sun-baked van and opening the lid a lot all make it work harder.",
     l:[["Will my fridge last the weekend?", G("will-my-fridge-last")],["Why is my fridge flattening my battery?", G("fridge-flattening-battery")]]},
    {k:["caravan","trailer","tow","anderson","not charging"], q:"My caravan isn't charging while I drive",
     a:"Usually it's the long thin cable to the van losing power, a dodgy Anderson plug, or a smart alternator. The fix is often a DC-DC charger fitted in the van. Get an auto electrician to check it.",
     l:[["Caravan not charging while driving", G("caravan-not-charging-while-driving")],["Caravan power setup", G("caravan-power-setup")]]},
    {k:["4wd","ute","dual battery","under bonnet","bonnet","engine bay"], q:"Setting up a dual battery in a 4WD",
     a:"A second battery runs your camping gear so the starting battery stays full. Lithium usually goes in the cabin or canopy, because engine bays get very hot.",
     l:[["4WD dual battery basics", G("4wd-dual-battery-basics")],["Lithium under the bonnet?", G("lithium-under-the-bonnet")]]},
    {k:["power station","ecoflow","jackery","all-in-one","box","portable power","plug and play"], q:"Is a portable power station enough?",
     a:"For a weekend with a small fridge and phones, often yes. Watch how you charge it: a cigarette socket charges slowly, and the 240V outlets tempt you into running a kettle.",
     l:[["Portable power stations", G("portable-power-stations")]]},
    {k:["winter","cold","not keeping up","cloud","grey"], q:"Why isn't my solar keeping up in winter?",
     a:"Shorter days and a low sun that hits flat panels side-on. Cold lithium batteries also can't charge below about 0°C unless they have a heater.",
     l:[["Winter solar not keeping up", G("winter-solar-not-keeping-up")]]},
    {k:["already","got","have","existing","my gear","check"], q:"I already have some gear. Is it enough?",
     a:"Use the Power Planner's <b>Check what I've got</b> option. Pick the battery, solar and charger you have, and it shows how many days it lasts and what's missing.",
     l:[["Check my gear", PLAN + "#check"]]},
    {k:["kit","weekender","road trip","living","ready-made","ready made"], q:"Can I just get a ready-made kit?",
     a:"Yes. There are three: <b>Weekender</b> (drive there, set up camp, come home), <b>Road trips</b>, and <b>Living in it</b>. Each has budget, mid-range and premium options.",
     l:[["See the ready-made kits", pre + "kits/index.html"]]},
    {k:["install","wire","wiring","electrician","diy","fuse","cable"], q:"Can I install it myself?",
     a:"Have a licensed auto electrician install or check your system, and never work on 240V wiring yourself. Batteries store a lot of energy, and the right cables and fuses matter.",
     l:[["The basics of off-grid power", G("van-power-basics")]]},
    {k:["cost","price","budget","cheap","expensive","how much does"], q:"How much will it cost?",
     a:"It depends on the size. The Power Planner shows real products at budget, mid-range and premium levels, with a rough total.",
     l:[["Open the Power Planner", PLAN]]},
    {k:["commission","affiliate","money","paid","sponsor","trust"], q:"Do you get paid for recommendations?",
     a:"Some links earn us a small commission, at no cost to you. It never decides what we recommend: we pick by fit, and show options at three price levels.",
     l:[["How we make money", pre + "disclosure.html"]]},
    {k:["word","jargon","mean","what is","explain"], q:"What does that word mean?",
     a:"Our <b>Big words, made simple</b> page explains the jargon in everyday language, with a search box.",
     l:[["Big words, made simple", pre + "big-words.html"]]},
    {k:["contact","email","talk","human","kiran","mitch"], q:"Can I ask Kiran & Mitch?",
     a:"Of course. Send us a message and we'll get back to you.",
     l:[["Contact us", pre + "contact.html"]]}
  ];
  var CHIPS = [0, 1, 2, 5, 13];
  var FACE = '<svg class="hb-face" viewBox="0 0 56 52" aria-hidden="true" fill="none" stroke="#1c1f1b" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M17 9l2 5M28 5v6M39 9l-2 5M8 17l4 3M48 17l-4 3"/><rect x="10" y="20" width="32" height="24" rx="6" fill="#f5cb3c"/><path d="M42 27h4v10h-4"/><circle cx="20" cy="30" r="1.6" fill="#1c1f1b" stroke="none"/><circle cx="32" cy="30" r="1.6" fill="#1c1f1b" stroke="none"/><path d="M20 36q6 5 12 0"/></svg>';
  function norm(t){ return (" " + t.toLowerCase().replace(/[^a-z0-9\- ]/g, " ") + " ").replace(/\s+/g, " "); }
  function match(text){
    var t = norm(text), best = null, bestScore = 0;
    QA.forEach(function(e){
      var s = 0;
      e.k.forEach(function(k){ if(t.indexOf(k.length <= 3 ? " " + k + " " : k) !== -1) s += k.length > 5 ? 2 : 1; });
      if(s > bestScore){ bestScore = s; best = e; }
    });
    return best;
  }
  var btn = document.createElement("button");
  btn.type = "button"; btn.className = "helper-btn"; btn.setAttribute("aria-expanded", "false"); btn.setAttribute("aria-controls", "helper-panel");
  btn.innerHTML = FACE + '<span class="hb-t"><span class="hb-1">Feeling confused?</span><span class="hb-2">Ask me a question</span></span>';
  var panel = document.createElement("div");
  panel.className = "helper-panel"; panel.id = "helper-panel"; panel.hidden = true; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Ask a question");
  panel.innerHTML = '<div class="hp-head"><span class="hp-who">' + FACE + '<span><b>Sunny</b><small>Your friendly power helper</small></span></span><button type="button" class="hp-x" aria-label="Close">×</button></div>' +
    '<div class="hp-log" aria-live="polite"></div>' +
    '<form class="hp-form"><input type="text" placeholder="Type your question…" aria-label="Your question" maxlength="200"><button type="submit">Ask</button></form>' +
    '<p class="hp-note">A simple helper that answers common questions from our guides. Answers are general, not advice for your exact setup.</p>';
  document.body.appendChild(btn); document.body.appendChild(panel);
  var log = panel.querySelector(".hp-log"), input = panel.querySelector("input");
  function say(html, who){ var d = document.createElement("div"); d.className = "hp-msg " + (who || "bot"); d.innerHTML = html; log.appendChild(d); log.scrollTop = log.scrollHeight; }
  function esc(t){ return String(t).replace(/[&<>"]/g, function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }
  function answer(e){
    say(e.a + '<span class="hp-links">' + e.l.map(function(x){ return '<a href="' + x[1] + '">' + x[0] + ' <span aria-hidden="true">→</span></a>'; }).join("") + '</span>');
  }
  function chips(){
    var d = document.createElement("div"); d.className = "hp-chips";
    CHIPS.forEach(function(i){ var c = document.createElement("button"); c.type = "button"; c.textContent = QA[i].q; c.addEventListener("click", function(){ say(esc(QA[i].q), "you"); answer(QA[i]); }); d.appendChild(c); });
    log.appendChild(d);
  }
  var started = false;
  function open(){
    panel.hidden = false; btn.setAttribute("aria-expanded", "true"); btn.classList.add("is-open");
    if(!started){ started = true; say("Hi, I'm Sunny! I can help with the common questions about batteries, solar and chargers. Tap one below or type your own."); chips(); }
    setTimeout(function(){ input.focus(); }, 50);
  }
  function close(){ panel.hidden = true; btn.setAttribute("aria-expanded", "false"); btn.classList.remove("is-open"); btn.focus(); }
  btn.addEventListener("click", function(){ panel.hidden ? open() : close(); });
  panel.querySelector(".hp-x").addEventListener("click", close);
  document.addEventListener("keydown", function(e){ if(e.key === "Escape" && !panel.hidden) close(); });
  panel.querySelector(".hp-form").addEventListener("submit", function(e){
    e.preventDefault(); var t = input.value.trim(); if(!t) return; input.value = "";
    say(esc(t), "you");
    var m = match(t);
    if(m) answer(m);
    else say("I'm a simple helper, so I don't know that one yet. Try the <a href=\"" + PLAN + "\">Power Planner</a>, the <a href=\"" + pre + "guides/index.html\">easy guides</a>, or <a href=\"" + pre + "contact.html\">ask Kiran &amp; Mitch</a>.");
  });
  if(/netlify\.app$/.test(location.hostname)) btn.classList.add("np");
  if(document.body.classList.contains("planner") || /planner\.html/.test(location.pathname)) btn.classList.add("lift");
})();
