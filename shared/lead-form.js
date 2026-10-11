/* Lead form for every public page. Posts to the rep portal's lead intake (the form's `action`),
   which saves the lead and assigns it to a rep or to Ali. No third-party links or calls.
   Also asks the portal whether the website launch offer (50% off setup) is still open and hides
   the offer notes if it isn't. Works without JavaScript too (plain form post, portal redirects back). */
(function () {
  var form = document.getElementById("lead-form");
  if (!form) return;
  var note = document.getElementById("form-note");
  var url = form.getAttribute("action");
  function say(t, err) { note.textContent = t; note.className = "formnote" + (err ? " err" : ""); }

  // Back from a no-JavaScript post (?lead=thanks / ?lead=error&lead_error=...)
  var qs = new URLSearchParams(location.search);
  if (qs.get("lead") === "thanks") say("Thanks! We got it and will reach out within one business day.");
  if (qs.get("lead") === "error") say(qs.get("lead_error") || "Something went wrong. Please try again.", true);

  // Hide the launch offer if the portal says it's closed. If the portal can't be reached, leave it as written.
  fetch(url, { method: "GET", mode: "cors" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
    if (j && j.websiteOffer && j.websiteOffer.open === false) {
      document.querySelectorAll("[data-offer]").forEach(function (el) { el.hidden = true; });
    }
  }).catch(function () {});

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var d = Object.fromEntries(new FormData(form).entries());
    if (!d.name || !d.business) return say("Please add your name and your business name.", true);
    if (!d.phone && !d.email) return say("Please add a phone number or an email so we can reach you.", true);
    if (!d.industry) return say("Please pick your industry.", true);
    var btn = form.querySelector("button[type=submit]");
    btn.disabled = true; say("Sending…");
    fetch(url, { method: "POST", mode: "cors", headers: { "content-type": "application/json" }, body: JSON.stringify(d) })
      .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
      .then(function (j) {
        if (j && j.ok) { form.reset(); say("Thanks! We got it and will reach out within one business day."); }
        else say((j && j.error) || "Something went wrong. Please try again.", true);
      })
      .catch(function () { say("We couldn't send that just now. Please try again in a minute.", true); })
      .then(function () { btn.disabled = false; });
  });
})();
