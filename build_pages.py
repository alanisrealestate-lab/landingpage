"""Build the secondary pages (privacy, terms, thank-you, booked) from index.html.

They reuse index.html's CSS tokens, buttons, header, heading classes and footer, so after you change
any of those in index.html, run:   python3 build_pages.py && python3 build_ghl.py
Each page gets a copy of the CSS so it also works on its own when pasted into a GHL funnel step.
"""
import re

src = open("index.html").read()
def between(a, b):
    i = src.index(a); return src[i:src.index(b, i)]

BASE_CSS = (between("/* ============================== TOKENS", "/* ============================== HERO")
            + re.search(r"\.card-title\{[^}]*\}", src).group(0) + "\n"
            + between("/* ============================== METHOD", ".perks{")
            + between("/* ============================== FOOTER", "/* ============================== STICKY"))
PAGE_CSS = """
/* ============================== SECONDARY PAGES ============================== */
.page-hero{background:var(--orange-tint);padding:40px 0 36px;border-bottom:1px solid var(--orange-tint-2)}
@media (min-width:900px){.page-hero{padding:72px 0 56px}}
.page-hero h1{margin-bottom:8px}
.page-hero .sub{font-size:1.08rem;margin:0;max-width:640px}
.page-body{padding:40px 0 64px}
@media (min-width:900px){.page-body{padding:64px 0 96px}}
.effective{margin:0;font-weight:600;color:var(--ink-2)}
/* Legal text: ~70 characters per line on desktop, comfortable line spacing on phones */
.prose{max-width:720px;margin:0 auto;font-size:1.02rem;line-height:1.75}
.prose .card-title{margin:40px 0 10px;font-size:clamp(1.25rem,3.8vw,1.5rem)}
.prose .card-title:first-child{margin-top:0}
.prose ul{padding-left:1.25em;margin:0 0 1em}
.prose li{margin-bottom:8px}
.prose li::marker{color:var(--logo-orange)}
.narrow{max-width:860px;margin:0 auto}
.back-home{margin-top:48px;padding-top:28px;border-top:1px solid var(--line)}
.card{background:#fff;border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);padding:22px 18px}
@media (min-width:600px){.card{padding:32px}}
.cal-card{padding:8px;overflow:hidden}
@media (min-width:600px){.cal-card{padding:16px}}
.cal-card iframe{display:block;width:100%;min-height:720px;border:0;overflow:hidden}
.talk{display:flex;flex-direction:column;gap:14px;align-items:flex-start;margin-top:16px}
@media (min-width:700px){.talk{flex-direction:row;align-items:center;justify-content:space-between}}
.talk p{margin:0}
.steps.three{margin-top:20px}
@media (min-width:900px){.steps.three{grid-template-columns:repeat(3,1fr)}}
.step::before{background:var(--logo-orange)}
.next-h{margin:48px 0 0;text-align:center}
.done-ic{width:64px;height:64px;border-radius:50%;background:var(--logo-orange);color:var(--ink);display:grid;place-items:center;margin-bottom:18px}
.done-ic svg{width:32px;height:32px}
"""
SPRITE = between('<svg width="0" height="0"', "<!-- ============================== 1. HEADER")
LOGO = re.search(r'src="(data:image/png;base64,[^"]+)"', src).group(1)
FOOTER = between('<footer class="footer">', "<!-- ============================== STICKY")
FOOTER = FOOTER.replace('<a class="logo" href="#top" aria-label="The Orange Real Estate Group, back to top">',
                        '<a class="logo" data-cfg-href="homeUrl" href="index.html" aria-label="The Orange Real Estate Group home">')
for h in ["calculator", "compare", "faq", "book"]:
    FOOTER = FOOTER.replace(f'<a href="#{h}">', f'<a data-cfg-href="homeUrl" data-hash="#{h}" href="index.html#{h}">')
FONTS = between('<link rel="preconnect" href="https://fonts.googleapis.com">', "<!-- ===================== TRACKING")
TRACKING = """<!-- TODO: paste the same Meta Pixel / GTM snippets you use on the main page here. -->"""

def page(fn, title, desc, main, *, book_btn=True, noindex=False, extra_js=""):
    plain = title.replace("&amp;", "&")
    book = ('\n      <a class="btn btn-primary" data-cfg-href="homeUrl" data-hash="#book" href="index.html#book">Book a Visit</a>'
            if book_btn else "")
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<!-- {plain}: built by build_pages.py from index.html. Edit the build script, not this file. -->
<title>{plain} | The Orange Real Estate Group</title>
<meta name="description" content="{desc}">{robots}
<meta name="theme-color" content="#FAA32A">
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
{FONTS.rstrip()}
{TRACKING}
<style>
{BASE_CSS}{PAGE_CSS}</style>
</head>

<body>
<a class="skip" href="#main">Skip to content</a>
{SPRITE.rstrip()}

<header class="header">
  <div class="wrap">
    <a class="logo" data-cfg-href="homeUrl" href="index.html" aria-label="The Orange Real Estate Group home">
      <img src="{LOGO}" width="499" height="96" alt="The Orange Real Estate Group">
    </a>
    <div class="header-actions">
      <a class="header-phone" data-tel href="tel:+19413450141"><svg aria-hidden="true"><use href="#i-phone"/></svg><span data-cfg="phoneDisplay">(941) 345-0141</span></a>{book}
      <a class="call-icon" data-tel href="tel:+19413450141" aria-label="Call The Orange Real Estate Group"><svg aria-hidden="true"><use href="#i-phone"/></svg></a>
    </div>
  </div>
</header>

<main id="main">
{main.strip()}
</main>

{FOOTER.rstrip()}

<script>
/* CONFIG: links and contact info for this page. Keep in sync with CONFIG in index.html. */
const CONFIG = {{
  brokerageName:  "The Orange Real Estate Group",
  phoneDisplay:   "(941) 345-0141",
  phoneE164:      "+19413450141",
  email:          "hello@example.com",       // TODO: your contact email
  officeAddress:  "515 9th St E, Ste #101, Bradenton, FL 34208",
  licenseNumber:  "[LICENSE #]",             // TODO: brokerage license number
  homeUrl:          "index.html",            // the Sell for 2% page ("our website" links point here)
  privacyPolicyUrl: "privacy.html",
  termsUrl:         "terms.html",
  ghlCalendarUrl:   "https://api.leadconnectorhq.com/widget/booking/WjZqpJiC2H1LUz47E8ZY",
  social: {{ facebook: "#", instagram: "#", google: "#" }}
}};
(function () {{
  const $$ = s => Array.from(document.querySelectorAll(s));
  const get = path => path.split(".").reduce((o, k) => (o || {{}})[k], CONFIG);
  $$("[data-cfg]").forEach(el => {{ const v = get(el.dataset.cfg); if (typeof v === "string") el.textContent = v; }});
  $$("[data-cfg-href]").forEach(el => {{ const v = get(el.dataset.cfgHref); if (v) el.href = v + (el.dataset.hash || ""); }});
  $$("a[data-tel]").forEach(a => a.href = "tel:" + CONFIG.phoneE164);
  $$("a[data-mailto]").forEach(a => a.href = "mailto:" + CONFIG.email);
  const y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
  // First name saved by the main page's form (never put in the URL)
  let lead = {{}}; try {{ lead = JSON.parse(sessionStorage.getItem("sf2_lead") || "{{}}"); }} catch (e) {{}}
  $$("[data-first-name]").forEach(el => {{ if (lead.first_name) el.textContent = el.dataset.firstName.replace("{{name}}", lead.first_name); }});
{extra_js.rstrip()}
}})();
</script>
</body>
</html>
"""
    open(fn, "w").write(html)
    print("built", fn)

W = '<a data-cfg-href="homeUrl" href="index.html">{}</a>'
ow, OW = W.format("our website"), W.format("Our website")

LEGAL = {
'privacy.html': ('Privacy Policy', 'How The Orange Real Estate Group collects, uses and protects your personal information.', f'''
        <p>At The Orange Real Estate Group, we are committed to protecting your privacy. This Privacy Policy outlines how we collect, use, and safeguard your personal information when you visit {ow} and use our services.</p>

        <h2 class="card-title">1. Information We Collect</h2>
        <p>We may collect the following types of information:</p>
        <ul>
          <li><strong>Personal Identification Information:</strong> Name, email address, phone number, mailing address, and other details you provide when contacting us or subscribing to our services.</li>
          <li><strong>Usage Data:</strong> Information about how you access and use {ow}, including IP address, browser type, and browsing activity.</li>
          <li><strong>Cookies:</strong> Small files stored on your device to enhance user experience and analyze website traffic.</li>
        </ul>

        <h2 class="card-title">2. How We Use Your Information</h2>
        <p>We use the collected information for various purposes, including:</p>
        <ul>
          <li>Providing and improving our services.</li>
          <li>Responding to inquiries and processing transactions.</li>
          <li>Sending promotional materials and updates, with your consent.</li>
          <li>Analyzing website usage to enhance user experience.</li>
        </ul>

        <h2 class="card-title">3. Sharing Your Information</h2>
        <p>We do not sell, trade, or rent your personal information to third parties. However, we may share information with trusted partners who assist us in operating {ow} and conducting our business, provided they agree to keep this information confidential.</p>

        <h2 class="card-title">4. Data Security</h2>
        <p>We implement appropriate security measures to protect your personal information from unauthorized access, alteration, disclosure, or destruction.</p>

        <h2 class="card-title">5. Your Rights</h2>
        <p>You have the right to:</p>
        <ul>
          <li>Access, correct, or delete your personal information.</li>
          <li>Object to or restrict the processing of your data.</li>
          <li>Withdraw consent at any time, where applicable.</li>
        </ul>
        <!-- TODO: set CONFIG.email at the bottom of this file to the address you want here -->
        <p>To exercise these rights, please contact us at <a data-mailto href="mailto:hello@example.com"><span data-cfg="email">hello@example.com</span></a>.</p>

        <h2 class="card-title">6. Third-Party Links</h2>
        <p>{OW} may contain links to external sites. We are not responsible for the content or privacy practices of these sites.</p>

        <h2 class="card-title">7. Changes to This Policy</h2>
        <p>We may update this Privacy Policy periodically. Any changes will be posted on this page with an updated effective date.</p>
'''),
'terms.html': ('Terms &amp; Conditions', 'The terms and conditions for using The Orange Real Estate Group website and services.', f'''
        <h2 class="card-title">1. Acceptance of Terms</h2>
        <p>By accessing or using {ow}, you agree to comply with these Terms &amp; Conditions and all applicable laws and regulations.</p>

        <h2 class="card-title">2. Use of Services</h2>
        <p>You agree to use our services for lawful purposes only and not to engage in any activity that could harm, disable, or impair {ow} or interfere with other users' access.</p>

        <h2 class="card-title">3. Property Listings</h2>
        <p>All property listings are provided for informational purposes only. While we strive for accuracy, we do not guarantee the completeness or correctness of the information.</p>

        <h2 class="card-title">4. Limitation of Liability</h2>
        <p>Our liability is limited to the maximum extent permitted by law. We are not liable for any indirect, incidental, or consequential damages arising from your use of our services.</p>

        <h2 class="card-title">5. Indemnification</h2>
        <p>You agree to indemnify and hold harmless The Orange Real Estate Group and its affiliates from any claims, losses, or damages arising out of your use of our services.</p>

        <h2 class="card-title">6. Governing Law</h2>
        <p>These Terms &amp; Conditions are governed by and construed in accordance with the laws of the United States. Any disputes will be resolved in the competent courts of the United States.</p>

        <h2 class="card-title">7. Changes to Terms</h2>
        <p>We reserve the right to modify these Terms &amp; Conditions at any time. Any changes will be posted on this page with an updated effective date.</p>
'''),
}


for fn, (title, desc, body) in LEGAL.items():
    page(fn, title, desc, f"""
  <section class="page-hero" aria-labelledby="page-h">
    <div class="wrap">
      <div class="prose">
        <span class="eyebrow">Legal</span>
        <h1 class="section-title" id="page-h">{title}</h1>
        <p class="effective">Effective Date: October 18, 2026</p>
      </div>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap">
      <div class="prose">
{body.rstrip()}

        <div class="back-home">
          <a class="btn btn-primary" data-cfg-href="homeUrl" href="index.html">Back to Sell for 2% <svg aria-hidden="true"><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </div>
  </section>""")

# ---------- Thank-you page: shown right after the form. Lets them pick a time on the GHL calendar. ----------
page("thank-you.html", "Pick a Time", "Pick a time for your 15-minute visit with Adrian.", """
  <section class="page-hero" aria-labelledby="page-h">
    <div class="wrap narrow">
      <span class="eyebrow">Almost done</span>
      <h1 class="section-title" id="page-h" data-first-name="Got it, {name}! Pick a time for your 15-minute visit.">Got it! Pick a time for your 15-minute visit.</h1>
      <p class="sub">Choose a day and time that works below. <strong>Nothing to sign at the visit.</strong></p>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap narrow">
      <!-- GHL booking calendar. Its iframe src is filled in by the script below so your name, email and phone carry over. -->
      <div class="card cal-card">
        <iframe id="ghl-cal" title="Pick a time for your visit" scrolling="no" src="https://api.leadconnectorhq.com/widget/booking/WjZqpJiC2H1LUz47E8ZY"></iframe>
      </div>

      <div class="card talk">
        <p><strong>Rather talk first?</strong> No problem. Adrian will call or text you shortly from <span data-cfg="phoneDisplay">(941) 345-0141</span>.</p>
        <a class="btn btn-ghost" data-tel href="tel:+19413450141"><svg aria-hidden="true"><use href="#i-phone"/></svg>Call Adrian</a>
      </div>

      <h2 class="card-title next-h">What happens next</h2>
      <ol class="steps three">
        <li class="step"><h3>Pick a time</h3><p>Choose any open slot above. You'll get a text confirmation right away.</p></li>
        <li class="step"><h3>Adrian confirms</h3><p>A quick call or text to say hi and confirm the address.</p></li>
        <li class="step"><h3>15-minute visit</h3><p>He comes by, walks the house and explains the program. Nothing to sign.</p></li>
      </ol>
    </div>
  </section>""", book_btn=False, noindex=True, extra_js="""
  // Pre-fill the calendar with what they typed on the form (GHL reads these query parameters)
  const cal = document.getElementById("ghl-cal");
  const q = new URLSearchParams();
  ["first_name", "last_name", "email", "phone"].forEach(k => { if (lead[k]) q.set(k, lead[k]); });
  cal.id = "WjZqpJiC2H1LUz47E8ZY_" + Date.now();   // GHL's embed script expects this id format
  cal.src = CONFIG.ghlCalendarUrl + (q.toString() ? "?" + q : "");
  const s = document.createElement("script"); s.src = "https://link.msgsndr.com/js/form_embed.js"; s.async = true; document.body.appendChild(s);""")

# ---------- Booked page: set as the calendar's redirect after someone books a time. ----------
page("booked.html", "You're Booked", "Your 15-minute visit with Adrian is booked.", """
  <section class="page-hero" aria-labelledby="page-h">
    <div class="wrap narrow">
      <div class="done-ic" aria-hidden="true"><svg><use href="#i-tick"/></svg></div>
      <span class="eyebrow">You're booked</span>
      <h1 class="section-title" id="page-h" data-first-name="See you soon, {name}!">See you soon!</h1>
      <p class="sub">Your 15-minute visit is on the calendar. <strong>You'll get a text confirmation shortly</strong>, plus a reminder before the visit.</p>
    </div>
  </section>

  <section class="page-body">
    <div class="wrap narrow">
      <h2 class="card-title" style="text-align:center">What happens next</h2>
      <ol class="steps three">
        <li class="step"><h3>Check your texts</h3><p>Your confirmation with the day and time is on its way.</p></li>
        <li class="step"><h3>Adrian confirms</h3><p>A quick call or text to say hi and confirm the address.</p></li>
        <li class="step"><h3>15-minute visit</h3><p>He walks the house and explains the program. <strong>Nothing to sign.</strong></p></li>
      </ol>

      <div class="card talk" style="margin-top:28px">
        <p><strong>Need to reschedule?</strong> Just call or text <span data-cfg="phoneDisplay">(941) 345-0141</span>.</p>
        <a class="btn btn-ghost" data-tel href="tel:+19413450141"><svg aria-hidden="true"><use href="#i-phone"/></svg>Call Adrian</a>
      </div>

      <div class="back-home" style="text-align:center">
        <a class="btn btn-primary" data-cfg-href="homeUrl" href="index.html">Back to Sell for 2% <svg aria-hidden="true"><use href="#i-arrow"/></svg></a>
      </div>
    </div>
  </section>""", book_btn=False, noindex=True, extra_js="""
  // Counts a booked visit in Meta / Google (if the pixel or GTM is installed on this page)
  if (typeof window.fbq === "function") fbq("track", "Schedule");
  if (typeof window.gtag === "function") gtag("event", "book_appointment");
  (window.dataLayer = window.dataLayer || []).push({ event: "visit_booked" });""")
