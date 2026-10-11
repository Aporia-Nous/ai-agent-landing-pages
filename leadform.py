# One lead form for every public page (demo landing pages + home page).
# Until Ali is on a white-label plan, visitors never reach Votel directly: every
# "get started / try it / book" button goes to this form, which posts to the rep portal's
# lead intake (POST /api/lead-intake), where the lead is auto-assigned to a rep or to Ali.
import os, html
E = html.escape

# Rep portal intake URL. Local preview default; set LEAD_INTAKE_URL to the live portal
# (e.g. https://reps.aporianous.com/api/lead-intake) when the portal is deployed, then rebuild.
ENDPOINT = os.environ.get("LEAD_INTAKE_URL", "http://localhost:3100/api/lead-intake")

INDUSTRIES = ["Restaurant", "Dental or medical office", "Salon or spa", "Home services", "Law firm",
              "Insurance agency", "Real estate", "Auto shop", "Other local business"]
BEST_TIMES = ["Weekday mornings", "Weekday afternoons", "Weekday evenings", "Weekends", "Anytime"]

OFFER_SHORT = "Launch offer: 50% off setup for our first few clients"
OFFER_LONG = "We're taking on our first few clients at 50% off the setup fee. The monthly plan stays the same, and you get a fixed quote before anything starts."

CSS = """
select{font:inherit;font-size:16px;color:var(--text);background:#0c1426;border:1px solid rgba(148,163,184,.28);border-radius:11px;padding:13px 14px;width:100%}
select:focus-visible{outline:3px solid color-mix(in srgb,var(--acc) 67%,transparent);outline-offset:2px}
.offer{display:inline-flex;align-items:center;gap:8px;margin-top:22px;font-size:14.5px;font-weight:700;color:var(--acc);border:1px solid color-mix(in srgb,var(--acc) 45%,transparent);background:color-mix(in srgb,var(--acc) 9%,transparent);border-radius:999px;padding:8px 14px}
.offercard{margin-top:22px;padding:18px 20px;border-radius:14px;border:1px solid color-mix(in srgb,var(--acc) 45%,transparent);background:color-mix(in srgb,var(--acc) 8%,transparent)}
.offercard b{display:block;color:var(--acc);font-size:15px;letter-spacing:.02em}
.offercard p{color:var(--muted);font-size:15px;margin-top:6px}
.hp{position:absolute!important;left:-10000px!important;width:1px;height:1px;overflow:hidden}
.formfine{grid-column:1/-1;font-size:13px;color:var(--dim);line-height:1.45}
.formnote.err{color:#fca5a5}
[data-offer][hidden]{display:none!important}
"""

def offer_badge():
    return f'<p class="offer" data-offer>{E(OFFER_SHORT)}</p>'

def offer_card():
    return f'<div class="offercard" data-offer><b>{E(OFFER_SHORT)}</b><p>{E(OFFER_LONG)}</p></div>'

def form(page_path, industry="", msg_placeholder="What would you like the agent to handle?"):
    inds = "".join(f'<option{" selected" if i == industry else ""}>{E(i)}</option>' for i in INDUSTRIES)
    times = "".join(f"<option>{E(t)}</option>" for t in BEST_TIMES)
    return f'''<form class="card" id="lead-form" action="{E(ENDPOINT)}" method="post">
   <input type="hidden" name="page" value="{E(page_path)}">
   <label class="hp" aria-hidden="true">Leave this empty<input name="company_website" tabindex="-1" autocomplete="off"></label>
   <label>Name<input name="name" autocomplete="name" placeholder="Your name" required maxlength="120"></label>
   <label>Business<input name="business" autocomplete="organization" placeholder="Business name" required maxlength="160"></label>
   <label>Phone<input name="phone" type="tel" autocomplete="tel" placeholder="(555) 555-5555" maxlength="40"></label>
   <label>Email<input name="email" type="email" autocomplete="email" placeholder="you@business.com" maxlength="200"></label>
   <label>Industry<select name="industry" required><option value="">Choose one</option>{inds}</select></label>
   <label>Best time to reach you<select name="bestTime"><option value="">Choose one</option>{times}</select></label>
   <label class="full">Anything else? (optional)<textarea name="message" maxlength="1500" placeholder="{E(msg_placeholder)}"></textarea></label>
   <p class="formfine">Add a phone number or an email (or both). A real person replies within one business day. We only use your details to answer this request.</p>
   <button class="btn pri" type="submit">Get my quote</button>
   <p class="formnote" id="form-note" role="status" aria-live="polite"></p>
  </form>'''

def script_tag(prefix):
    return f'<script src="{prefix}shared/lead-form.js"></script>'
