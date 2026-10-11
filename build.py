import os, sys, html, re, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, "/workspace/upwork-catalog/gallery/src")
from icons import svg
import content; importlib.reload(content)
from content import PAGES, CLOSING
import leadform
E = html.escape

CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a1020;--card:#111a2e;--line:rgba(148,163,184,.16);--text:#e7ecf5;--muted:#9aa7bd;--dim:#6f7d95;--acc:ACC;--w:1120px}
html{scroll-behavior:smooth}
body{background:radial-gradient(900px 600px at 85% 0%,ACC1a,transparent 65%),radial-gradient(900px 600px at 0% 40%,rgba(94,234,212,.05),transparent 60%),var(--bg);
 color:var(--text);font-family:Inter,"DM Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.55;font-size:17px}
h1,h2,h3,.sig{font-family:"Plus Jakarta Sans",Inter,system-ui,sans-serif;letter-spacing:-.02em}
a{color:inherit}
.wrap{max-width:var(--w);margin:0 auto;padding:0 24px}
.card{background:linear-gradient(180deg,rgba(255,255,255,.035),rgba(255,255,255,.01)),var(--card);border:1px solid var(--line);border-radius:18px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font-weight:700;font-size:16px;padding:14px 22px;border-radius:12px;text-decoration:none;border:1.5px solid transparent;cursor:pointer;font-family:inherit;transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translateY(-1px)}
.btn.pri{background:var(--acc);color:#0a1020;box-shadow:0 8px 30px ACC40}
.btn.sec{background:transparent;color:var(--text);border-color:ACC66}
.btn:focus-visible,input:focus-visible,textarea:focus-visible,summary:focus-visible{outline:3px solid ACCaa;outline-offset:2px}
/* nav */
nav{position:sticky;top:0;z-index:20;background:rgba(10,16,32,.78);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;align-items:center;justify-content:space-between;height:64px;gap:16px}
.navlabel{display:flex;align-items:center;gap:10px;font-weight:700;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.navlabel i{flex:none;width:28px;height:28px;border-radius:9px;display:grid;place-items:center;background:ACC1f;border:1px solid ACC59}
.navlinks{display:flex;align-items:center;gap:22px;font-size:15px;color:var(--muted)}
.navlinks a{text-decoration:none}.navlinks a:hover{color:var(--text)}
.navlinks .btn{padding:9px 16px;font-size:14px;color:#0a1020}
/* hero */
.hero{padding:72px 0 56px}
.hero .wrap{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.mark{width:56px;height:5px;border-radius:5px;background:var(--acc);margin-bottom:26px}
.hero h1{font-size:clamp(38px,5.4vw,62px);line-height:1.06;font-weight:800;text-wrap:balance}
.hero h1 span{color:var(--acc)}
.sub{margin-top:22px;font-size:clamp(17px,1.6vw,19px);color:var(--muted);max-width:600px}
.ticks{list-style:none;margin-top:26px;display:flex;flex-direction:column;gap:12px}
.ticks li{display:flex;align-items:center;gap:12px;font-weight:600}
.tk{flex:none;width:30px;height:30px;border-radius:9px;display:grid;place-items:center;background:ACC1f;border:1.5px solid ACC66}
.ctas{margin-top:32px;display:flex;flex-wrap:wrap;gap:12px}
.art{position:relative;width:100%;max-width:440px;aspect-ratio:1;margin:0 auto}
.ring{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border-radius:50%;border:2px dashed ACC2e}
.core{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:46%;aspect-ratio:1;border-radius:50%;display:grid;place-items:center;
 background:radial-gradient(circle at 35% 30%,ACC33,ACC0d 70%),var(--card);border:2px solid ACC80;box-shadow:0 0 0 12px ACC0f,0 0 90px ACC40}
.core svg{width:46%;height:auto}
.fc{position:absolute;width:40%;display:flex;align-items:center;gap:10px;padding:12px;box-shadow:0 14px 34px rgba(0,0,0,.35)}
.fc .ic{flex:none;width:36px;height:36px;border-radius:11px;display:grid;place-items:center;background:ACC1f;border:1.5px solid ACC59}
.fc .ic svg{width:20px;height:20px}
.bars{display:flex;flex-direction:column;gap:7px;flex:1}
.bars b{display:block;height:7px;border-radius:5px;background:rgba(231,236,245,.22)}
.bars b:last-child{background:rgba(231,236,245,.11);width:65%}
/* sections */
section{padding:64px 0}
.kicker{font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--acc)}
h2{font-size:clamp(28px,3.4vw,38px);line-height:1.15;font-weight:800;margin-top:10px;text-wrap:balance}
.lead{color:var(--muted);margin-top:12px;max-width:640px}
.steps{margin-top:36px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px;counter-reset:s}
.step{padding:24px}
.step .n{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;font-weight:800;color:#0a1020;background:var(--acc);font-family:"Plus Jakarta Sans",Inter,sans-serif}
.step h3{font-size:19px;margin-top:16px}
.step p{color:var(--muted);font-size:15.5px;margin-top:8px}
.inc{margin-top:36px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.inc .card{padding:22px;display:flex;gap:14px;align-items:flex-start}
.inc h3{font-size:17px}
.inc p{color:var(--muted);font-size:15.5px;margin-top:4px}
.demo{display:grid;grid-template-columns:.9fr 1.1fr;gap:28px;align-items:stretch;margin-top:32px}
.prompts{list-style:none;margin-top:18px;display:flex;flex-direction:column;gap:10px}
.prompts li{padding:12px 16px;border-radius:12px;background:rgba(255,255,255,.03);border:1px solid var(--line);font-size:15.5px}
.slot{min-height:340px;border:2px dashed ACC80;border-radius:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:32px;gap:14px;
 background:repeating-linear-gradient(135deg,ACC08 0 14px,transparent 14px 28px),var(--card)}
.slot .pill{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:#0a1020;background:var(--acc);padding:6px 12px;border-radius:999px}
.slot h3{font-size:22px}
.slot p{color:var(--muted);font-size:15px;max-width:380px}
.slot .ico{width:72px;height:72px;border-radius:50%;display:grid;place-items:center;background:ACC1f;border:1.5px solid ACC66}
/* form */
.formgrid{display:grid;grid-template-columns:.85fr 1.15fr;gap:32px;margin-top:8px;align-items:start}
form{padding:28px;display:grid;grid-template-columns:1fr 1fr;gap:16px}
label{display:flex;flex-direction:column;gap:7px;font-size:14px;font-weight:600;color:var(--muted)}
label.full{grid-column:1/-1}
input,textarea{font:inherit;font-size:16px;color:var(--text);background:#0c1426;border:1px solid rgba(148,163,184,.28);border-radius:11px;padding:13px 14px;width:100%}
textarea{min-height:120px;resize:vertical}
input::placeholder,textarea::placeholder{color:#5f6c84}
form .btn{grid-column:1/-1;justify-self:start}
.formnote{grid-column:1/-1;font-size:14px;color:var(--acc);min-height:1px}
/* faq */
.faq{margin-top:28px;display:flex;flex-direction:column;gap:12px;max-width:860px}
details{padding:0 22px}
summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:20px 0;font-weight:700;font-size:17px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";flex:none;width:28px;height:28px;border-radius:8px;display:grid;place-items:center;background:ACC1f;color:var(--acc);font-size:20px;font-weight:600}
details[open] summary::after{content:"\2212"}
details p{color:var(--muted);padding:0 0 20px;font-size:16px}
/* closing + referral */
.closing{padding:44px 36px;text-align:center;border-color:ACC4d;background:radial-gradient(600px 240px at 50% 0%,ACC1f,transparent 70%),var(--card)}
.closing p{font-family:"Plus Jakarta Sans",Inter,sans-serif;font-size:clamp(22px,2.6vw,30px);font-weight:800;line-height:1.25;max-width:760px;margin:0 auto;text-wrap:balance}
.closing .btn{margin-top:24px}
.ref{padding:30px 32px;display:grid;grid-template-columns:1fr auto;gap:12px 32px;align-items:center}
.ref .badge{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--acc);border:1px solid ACC66;border-radius:999px;padding:4px 10px;margin-bottom:10px}
.ref h2{font-size:clamp(22px,2.4vw,28px);margin:0}
.ref p.body{color:var(--muted);margin-top:8px;font-size:15.5px;max-width:640px}
.ref .act{display:flex;flex-direction:column;align-items:flex-start;gap:10px}
.ref small{color:var(--dim);font-size:12.5px;max-width:280px;line-height:1.4}
footer{padding:24px 0 36px;color:var(--dim);font-size:13px;border-top:1px solid var(--line)}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
/* responsive */
@media (max-width:960px){
 .steps{grid-template-columns:1fr 1fr}.inc{grid-template-columns:1fr 1fr}
 .hero .wrap,.demo,.formgrid{grid-template-columns:1fr}
 .art{max-width:360px}
}
@media (max-width:640px){
 body{font-size:16px}
 .wrap{padding:0 20px}
 .navlinks a:not(.btn){display:none}
 .hero{padding:44px 0 28px}
 section{padding:44px 0}
 .steps,.inc{grid-template-columns:1fr}
 form{grid-template-columns:1fr;padding:22px}
 form .btn{justify-self:stretch}
 .ref{grid-template-columns:1fr;padding:26px 22px}
 .closing{padding:34px 22px}
 .slot{min-height:280px;padding:24px}
 .art{max-width:250px;margin-top:8px}
 .step{display:grid;grid-template-columns:38px 1fr;column-gap:14px;padding:20px}
 .step h3{margin-top:6px}.step p{grid-column:2}
 .inc .card{padding:18px}
 .ctas .btn{flex:1 1 100%}
}
"""

INDUSTRY = {"restaurant-phone-agent": "Restaurant", "dental-front-desk": "Dental or medical office", "real-estate-lead-caller": "Real estate"}

def page(p):
    a = p["acc"]
    css = CSS.replace("ACC", a) + leadform.CSS
    tick = svg("check", 16, a, 3.2)
    ticks = "".join(f'<li><span class="tk">{tick}</span>{E(t)}</li>' for t in p["ticks"])
    pos = [("left:-2%;top:12%"), ("right:-4%;top:46%"), ("left:6%;bottom:6%")]
    fcs = "".join(f'<div class="card fc" style="{s}"><div class="ic">{svg(c,20,a,2.2)}</div><div class="bars"><b></b><b></b></div></div>' for s, c in zip(pos, p["cards"]))
    steps = "".join(f'<div class="card step"><div class="n">{i}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(p["steps"], 1))
    inc = "".join(f'<div class="card"><span class="tk">{tick}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></div>' for t, d in p["included"])
    prompts = "".join(f"<li>{E(x)}</li>" for x in p["demo_prompts"])
    faq = "".join(f'<details class="card"><summary>{E(q)}</summary><p>{E(ans)}</p></details>' for q, ans in p["faq"])
    head = re.sub("<[^>]+>", "", p["h1"])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(p["title"])}</title>
<meta name="description" content="{E(p["sub"][:155])}">
<style>{css}</style>
</head>
<body>
<nav><div class="wrap">
 <div class="navlabel"><i>{svg(p["icon"],16,a,2.2)}</i><span>{E(p["label"])}</span></div>
 <div class="navlinks"><a href="#how">How it works</a><a href="#demo">Demo</a><a href="#faq">FAQ</a><a class="btn pri" href="#contact">Get started</a></div>
</div></nav>

<header class="hero"><div class="wrap">
 <div>
  <div class="mark"></div>
  <h1>{p["h1"]}</h1>
  <p class="sub">{E(p["sub"])}</p>
  <ul class="ticks">{ticks}</ul>
  {leadform.offer_badge()}
  <div class="ctas"><a class="btn pri" href="#contact">Get started</a><a class="btn sec" href="#demo">Watch the demo</a></div>
 </div>
 <div class="art" aria-hidden="true">
  <div class="ring" style="width:76%;height:76%"></div><div class="ring" style="width:100%;height:100%;opacity:.55"></div>
  <div class="core">{svg(p["icon"],120,a,1.6)}</div>{fcs}
 </div>
</div></header>

<section id="how"><div class="wrap">
 <div class="kicker">How it works</div>
 <h2>Live in a few weeks, with the setup handled for you</h2>
 <p class="lead">You tell me how things work today. I build, test, and tune the agent so it fits your business.</p>
 <div class="steps">{steps}</div>
</div></section>

<section id="included"><div class="wrap">
 <div class="kicker">What's included</div>
 <h2>Everything it takes to run on its own</h2>
 <p class="lead">Each agent is built around your business. Pick what you need now and add more later.</p>
 <div class="inc">{inc}</div>
</div></section>

<section id="demo"><div class="wrap">
 <div class="kicker">Try the demo</div>
 <h2>Hear it for yourself</h2>
 <div class="demo">
  <div>
   <p class="lead" style="margin-top:0">{E(p["demo_intro"])}</p>
   <p style="margin-top:18px;font-weight:700">Things to try:</p>
   <ul class="prompts">{prompts}</ul>
  </div>
  <div class="slot" id="demo-widget-slot" data-placeholder="chat-voice-widget">
   <!-- DEMO WIDGET PLACEHOLDER: paste the chat/voice widget embed snippet for the "{E(p["slug"])}" demo agent here, replacing this box's contents. -->
   <span class="pill">Placeholder</span>
   <div class="ico">{svg("mic",32,a,2)}</div>
   <h3>Live chat and voice demo goes here</h3>
   <p>The interactive demo agent will appear in this spot. Until then, use the form below and I'll set up a demo call for you.</p>
  </div>
 </div>
</div></section>

<section id="contact"><div class="wrap">
 <div class="formgrid">
  <div>
   <div class="kicker">Get started</div>
   <h2>Tell me about your business</h2>
   <p class="lead">{E(p["form_msg"])} I'll get back to you with how I'd build it.</p>
   {leadform.offer_card()}
  </div>
  <!-- LEAD FORM: posts to the rep portal lead intake (leadform.ENDPOINT); leads are auto-assigned to a rep or to Ali. -->
  {leadform.form("/" + p["slug"] + "/", INDUSTRY.get(p["slug"], ""))}
 </div>
</div></section>

<section id="faq"><div class="wrap">
 <div class="kicker">FAQ</div>
 <h2>Common questions</h2>
 <div class="faq">{faq}</div>
</div></section>

<section id="custom" style="padding-top:24px"><div class="wrap">
 <div class="card closing"><p>{E(CLOSING)}</p><a class="btn pri" href="#contact">Tell me what you need</a></div>
</div></section>
<footer><div class="wrap"><span>&copy; 2026 Aporia Nous</span></div></footer>

{leadform.script_tag("../")}
</body>
</html>
'''

if __name__ == "__main__":
    for p in PAGES:
        d = os.path.join(HERE, p["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(p))
        print(d + "/index.html")
