"""Generates the static pages of the kornall demo website (header and footer shared)."""
import pathlib
import sys

OUT = pathlib.Path(sys.argv[1])
SITE = 'https://[YOUR-GITHUB-NAME].github.io/kornall-website/'

LOGO = '<svg width="{s}" height="{s}" viewBox="0 0 160 160" aria-hidden="true" focusable="false"><rect width="160" height="160" rx="4" fill="{bg}"/><rect x="34" y="94" width="32" height="32" fill="#C27A4A"/><path d="M34 79H81V126M34 59H101V126M34 39H121V126" fill="none" stroke="#DCE6E4" stroke-width="10"/></svg>'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 160 160'%3E%3Crect width='160' height='160' rx='8' fill='%23123B45'/%3E%3Crect x='28' y='92' width='40' height='40' fill='%23C27A4A'/%3E%3Cpath d='M28 68H92V132M28 36H124V132' fill='none' stroke='%23DCE6E4' stroke-width='16'/%3E%3C/svg%3E"

ICON = {
    'lock': '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="10" width="16" height="11"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
    'review': '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h10M4 18h7"/><path d="M16 15l2 2 4-4"/></svg>',
    'undo': '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 14L4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/></svg>',
    'shield': '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" style="width:16px;height:16px"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>',
    'menu': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

NAV = [('data-books.html', 'Data Books', 'databooks'), ('everyone.html', 'For everyone', 'everyone'), ('pricing.html', 'Pricing', 'pricing'), ('download.html', 'Download', 'download'), ('contact.html', 'Contact', 'contact')]


def head(title, desc, page):
    full = f'{title} | kornall' if title != 'kornall' else 'kornall: assemble, check and deliver your documentation, offline'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#123B45">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta property="og:type" content="website">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<script src="assets/js/site.js" defer></script>
</head>
<body data-page="{page}">
<a class="skip" href="#main">Skip to content</a>
<div class="demo-bar" role="note"><strong>Demo website.</strong> Purchases, payments and downloads are simulated. Nothing is charged.</div>
'''


def header(active):
    cur = ' aria-current="page"'
    links = ''.join(f'<li><a href="{h}"{cur if key and key == active else ""}>{t}</a></li>' for h, t, key in NAV)
    return f'''<header class="site-header">
<div class="wrap">
<nav class="nav" aria-label="Main">
<a class="brand" href="index.html" aria-label="kornall home">{LOGO.format(s=30, bg='#123B45')}<span>kornall</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">{ICON['menu']}</button>
<ul class="nav-links" id="nav-links">{links}</ul>
<div class="nav-actions">
<a class="btn btn-ghost" href="account.html">Account</a>
<a class="btn btn-copper" href="trial.html">Start 7-day trial</a>
</div>
</nav>
</div>
</header>
'''


FOOTER = f'''<footer class="site-footer">
<div class="wrap">
<div class="foot-brand">{LOGO.format(s=24, bg='#1B4C57')}<strong>kornall</strong><span>© <span data-year>2026</span> <span class="ph">[COMPANY NAME]</span></span></div>
<nav aria-label="Legal and contact">
<ul>
<li><a href="legal.html">Legal notice</a></li>
<li><a href="terms.html">Terms of sale</a></li>
<li><a href="eula.html">Licence agreement</a></li>
<li><a href="privacy.html">Privacy</a></li>
<li><a href="contact.html">Contact</a></li>
</ul>
</nav>
</div>
<div class="foot-note">No cookies, no trackers, no analytics on this site. Fonts are served from this site.</div>
</footer>
</body>
</html>
'''


def page(name, title, desc, key, body):
    (OUT / name).write_text(head(title, desc, key) + header(key) + '<main id="main">\n' + body + '\n</main>\n' + FOOTER, encoding='utf-8')


def faq(items, first_open=True):
    out = '<div class="faq">'
    for i, (q, a) in enumerate(items):
        out += f'<details{" open" if i == 0 and first_open else ""}><summary>{q}</summary><p>{a}</p></details>'
    return out + '</div>'


DEV = '<span class="badge badge-dev">Early access</span>'
NOW = '<span class="badge badge-now">Available</span>'

# A Data Book completeness view, drawn in HTML. Clearly labelled as an illustration.
DB_ROWS = [
    ('01', 'Certificates of conformity', 12, 12),
    ('02', 'Material certificates (3.1)', 41, 46),
    ('03', 'Welding: WPS, PQR, welder qualifications', 18, 18),
    ('04', 'NDT reports', 9, 14),
    ('05', 'Pressure test reports', 2, 2),
    ('06', 'Painting and coating', 0, 3),
    ('07', 'Dimensional reports', 4, 4),
]


def dbook(caption=True):
    rows = ''
    for n, t, got, need in DB_ROWS:
        pct = round(got / need * 100)
        ok = got == need
        st = '<span class="st st-ok">Complete</span>' if ok else f'<span class="st st-miss">{need - got} missing</span>'
        rows += f'<tr><td class="n">{n}</td><td>{t}</td><td class="hide-s"><div class="bar"><i class="{"" if ok else "part"}" style="width:{pct}%"></i></div></td><td class="c">{got}/{need}</td><td>{st}</td></tr>'
    got = sum(r[2] for r in DB_ROWS)
    need = sum(r[3] for r in DB_ROWS)
    cap = '<span class="illus">Illustration of the Data Book module, in development</span>' if caption else ''
    return f'''<figure style="margin:0">
<div class="dbook" role="img" aria-label="Illustration: a Data Book index with 7 sections, {got} of {need} documents received, 13 missing">
<div class="dbook-head"><strong>MDR · Pump skid P-101</strong><span>Client index rev. C</span></div>
<table><thead><tr><th>No.</th><th>Section</th><th class="hide-s">Progress</th><th style="text-align:right">Docs</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table>
<div class="dbook-foot"><div><div class="big">{round(got / need * 100)}%</div><div class="small">{got} of {need} documents in place</div></div><div class="small">13 missing · 1 superseded revision · 2 duplicates</div></div>
</div>{cap}
</figure>'''


BILLING = '''<div class="billing" role="group" aria-label="Billing period for Personal and Professional">
<button type="button" data-billing="year" aria-pressed="true">Yearly <span class="save">2 months free</span></button>
<button type="button" data-billing="month" aria-pressed="false">Monthly</button>
</div>'''

PLANS = '''<div class="plans plans-4" id="plans">
<article class="plan">
<h3>Personal</h3>
<p class="who">Your own folders, up to 2 PCs</p>
<p class="price" id="personal-price">€27<small> / year</small></p>
<p class="note" id="personal-note">That is €2.25 a month. VAT included.</p>
<ul class="ticks"><li>Workspace map and tree editor</li><li>Structured numbering</li><li>Duplicate detection</li><li>One-page state report (WDS)</li></ul>
<a class="btn btn-line btn-block" id="personal-buy" href="checkout.html?plan=personal&amp;billing=year">Buy Personal</a>
<p class="under"><a href="everyone.html">What Personal is for</a></p>
</article>
<article class="plan featured">
<div class="plan-top"><h3>Professional</h3><span class="pill">For Data Books</span></div>
<p class="who">One documentation professional, up to 2 PCs</p>
<p class="price" id="pro-price">€190<small> / year</small></p>
<p class="note" id="pro-note">That is €15.83 a month, 2 months free. Excl. VAT.</p>
<ul class="ticks"><li>Everything in Personal</li><li>Data Book templates and client index import</li><li>Completeness check and progress report</li><li>Final PDF compilation and revisions</li></ul>
<a class="btn btn-copper btn-block" id="pro-buy" href="checkout.html?plan=professional&amp;billing=year">Buy Professional</a>
<p class="under">Data Book module in <a href="data-books.html#status">early access</a></p>
</article>
<article class="plan">
<h3>Team</h3>
<p class="who">5 to 50 users, one shared library</p>
<p class="price">€15<small> / user / month</small></p>
<p class="note">Billed yearly. Excl. VAT.</p>
<label class="stepper-label" for="team-seats">Number of users</label>
<div class="stepper"><button type="button" id="seat-minus" aria-label="One user less">−</button><input id="team-seats" type="number" min="5" max="50" value="10" inputmode="numeric"><button type="button" id="seat-plus" aria-label="One user more">+</button></div>
<p class="note" id="team-total" aria-live="polite">10 users: €1,800.00 a year, excl. VAT</p>
<ul class="ticks"><li>Everything in Professional</li><li>Shared template library</li><li>Licence management and company invoices</li></ul>
<a class="btn btn-line btn-block" id="team-buy" href="checkout.html?plan=team&amp;seats=10">Buy for 10 users</a>
</article>
<article class="plan">
<h3>Enterprise</h3>
<p class="who">More than 50 users</p>
<p class="price">On quote</p>
<p class="note">Volume pricing and contract terms</p>
<ul class="ticks"><li>Everything in Team</li><li>Deployment help and onboarding</li><li>Templates set up with your clients' indexes</li><li>Purchase order and bank transfer</li></ul>
<a class="btn btn-line btn-block" href="contact.html?topic=enterprise">Contact sales</a>
<p class="under">Answer within <span class="ph">[2]</span> business days</p>
</article>
</div>'''

FAQ_HOME = [
    ('What is a Data Book?', 'A Data Book, also called a Manufacturing Data Record (MDR) or final documentation dossier, is the set of documents a supplier hands over with equipment: certificates, material certificates, welding and NDT records, test reports, drawings. The client sets the index and the numbering, and checks that every document is there. <a href="data-books.html">Read more</a>.'),
    ('Do my documents go to a server?', 'No. kornall runs on your Windows PC and works without an internet connection. Your documents, names and folders stay on your computer, which matters when they are under a client confidentiality agreement.'),
    ('Is the Data Book module available today?', 'kornall 2.0 is available today with the map, numbering, duplicate detection and state report. The Data Book module (templates, index import, completeness check, PDF compilation, revisions) is in development and released to early-access users first. It is included in Professional and Team at no extra cost.'),
    ('I am not in industry. Is kornall for me?', 'Yes. The Personal plan is made for anyone who wants clean, numbered folders without duplicates: students, freelancers, researchers, photographers. <a href="everyone.html">See kornall for everyone</a>.'),
    ('What happens after the 7-day trial?', 'Choose a plan to keep using kornall. Nothing is charged automatically, and your folders stay exactly as they are.'),
    ('Can kornall delete my files by mistake?', 'No. Every change is shown for review first, removed files go to the Recycle Bin, and moves, renames and copies can be undone.'),
]

# ---------------- Home ----------------
page('index.html', 'kornall', 'kornall assembles, checks and compiles Data Books and manufacturing records against your client\'s index. On your Windows PC, offline. Also for anyone who wants clean, numbered folders.', 'home', f'''
<section class="hero">
<div class="wrap hero-grid center">
<div class="hero-copy">
<p class="eyebrow">For Data Books and manufacturing records</p>
<h1>Assemble, check and deliver your documentation, offline.</h1>
<p class="lead">kornall files every certificate, report and drawing under your client's index, tells you what is still missing, and compiles the final book. Your documents never leave your PC.</p>
<div class="cta-row">
<a class="btn btn-copper" href="trial.html">Start your 7-day trial</a>
<a class="btn btn-on-dark" href="data-books.html">See how it works</a>
</div>
<p class="fine">No card needed for the trial. Professional from €19 a month.</p>
</div>
<div>{dbook()}</div>
</div>
</section>

<section class="promises" aria-label="Promises">
<div class="wrap">
<ul>
<li>{ICON['lock']}<span><strong>Offline by design.</strong> No upload, no cloud, nothing to clear with your client's security team.</span></li>
<li>{ICON['review']}<span><strong>Review before anything moves.</strong> Every rename and move is listed and confirmed by you.</span></li>
<li>{ICON['undo']}<span><strong>Undo when you change your mind.</strong> The history keeps every change reversible.</span></li>
</ul>
</div>
</section>

<section class="section" aria-labelledby="problem-title">
<div class="wrap">
<div class="section-head">
<h2 id="problem-title">Data Books are still built by hand</h2>
<p>An index in Excel, hundreds of PDFs in folders, and an evening in Acrobat before the deadline. Then the client sends it back.</p>
</div>
<div class="cards">
<article class="card"><span class="k">Index in Excel</span><h3>Numbers typed one by one</h3><p>Every file is renamed by hand to match the client's numbering, and one slip shifts the whole section.</p></article>
<article class="card"><span class="k">Files in folders</span><h3>Missing documents found late</h3><p>A missing material certificate or NDT report is discovered at compilation, or by the client's inspector.</p></article>
<article class="card"><span class="k">PDF by hand</span><h3>Hours of merging</h3><p>Cover, table of contents, bookmarks and page numbers are redone at every revision of the book.</p></article>
</div>
</div>
</section>

<section class="section section-alt" aria-labelledby="flow-title">
<div class="wrap">
<div class="section-head">
<h2 id="flow-title">Four steps, from the client's index to the final book</h2>
<p>The same order you already work in, with the checking done for you.</p>
</div>
<div class="steps" style="background:var(--white)">
<article class="step"><span class="tag">01</span><h3>Index</h3><p>Import the client's index from Excel, or start from a template: MDR, Data Book, O&amp;M manual, turnover package.</p></article>
<article class="step"><span class="tag">02</span><h3>Collect</h3><p>Drop documents in. kornall files them under the right section and gives them the client's numbering.</p></article>
<article class="step"><span class="tag">03</span><h3>Check</h3><p>See what is missing, duplicated or superseded, section by section, before the client does. Send the progress report.</p></article>
<article class="step"><span class="tag tag-copper">04</span><h3>Compile</h3><p>One PDF with cover page, clickable table of contents, bookmarks and page numbers. Recompile in one click at each revision.</p></article>
</div>
<p class="small muted" style="margin-top:16px">Steps 01 to 04 are the Data Book module, in early access. <a href="data-books.html#status">What is available today</a></p>
</div>
</section>

<section class="section" aria-labelledby="who-title">
<div class="wrap">
<div class="section-head"><h2 id="who-title">Made for the people who hand documentation over</h2></div>
<div class="cards">
<article class="card"><h3>Fabricators and packagers</h3><p>Pressure vessels, skids, piping, structures, valves: every order ships with its manufacturing record.</p></article>
<article class="card"><h3>Document controllers</h3><p>EPC and project teams who collect supplier documents and must deliver them complete and numbered.</p></article>
<article class="card"><h3>QA/QC and inspection</h3><p>Quality engineers who assemble certificates and test reports, and need to prove nothing is missing.</p></article>
<article class="card"><h3>Handover and O&amp;M</h3><p>Commissioning and handover teams building operation manuals and as-built packages.</p></article>
</div>
</div>
</section>

<section class="section-tight" aria-labelledby="core-title">
<div class="wrap">
<div class="section-head"><h2 id="core-title">Built on the kornall workspace, available today</h2><p>The tools the Data Book module stands on are in kornall 2.0 now, in every plan.</p></div>
<div class="split">
<div>
<h2>Numbering that matches the client's index</h2>
<p>Number folders, or every file, as 01, 01.01, 01.02 or A, A.01. See the old and new name of every item before anything changes, and undo the whole numbering in one step.</p>
<ul class="ticks"><li>Zero-padded, so Windows sorts 01 to 99 correctly</li><li>Replaces old numbers cleanly</li><li class="copper">Folders only or all items, one level or all</li></ul>
</div>
<img class="shot" src="assets/img/numbering.webp" width="1440" height="900" alt="Numbering preview: current names on the left, new numbered names on the right" loading="lazy">
</div>
<div class="split">
<img class="shot" src="assets/img/duplicates.webp" width="1440" height="900" alt="Duplicate files grouped, with the copy to keep marked and the others ticked for removal" loading="lazy">
<div>
<h2>No certificate twice, no old revision left behind</h2>
<p>Identical files are matched by content, whatever their names. Probable versions such as "rev B", "copy" or "final 2" are shown separately and never removed for you.</p>
<ul class="ticks"><li>Keep the newest, the oldest or the shortest path</li><li class="copper">Removed files go to the Recycle Bin</li></ul>
</div>
</div>
<div class="split">
<div>
<h2>A one-page state of the whole folder</h2>
<p>The Workflow Digital State report fits on one A4 page: structure, content types, recent activity and health checks. Attach it to a delivery or a weekly update.</p>
<ul class="ticks"><li>Health checks: duplicates, numbering, empty folders, long paths</li><li class="copper">Compare with a saved state, when you choose to</li></ul>
</div>
<div class="shot-frame"><img src="assets/img/wds-report.webp" width="900" height="1273" alt="A sample one-page Workflow Digital State report" loading="lazy"></div>
</div>
</div>
</section>

<section class="section section-alt" aria-labelledby="tracks-title">
<div class="wrap">
<div class="section-head"><h2 id="tracks-title">Two ways to use kornall</h2></div>
<div class="tracks">
<article class="track copper"><span class="eyebrow" style="margin:0">Professional and Team</span><h3>For industrial documentation</h3><p>Data Books, MDRs, O&amp;M manuals and turnover packages, assembled against the client's index and compiled into one PDF.</p><a class="btn btn-copper" href="data-books.html">Data Books</a></article>
<article class="track"><span class="eyebrow" style="margin:0;color:var(--petrol)">Personal</span><h3>For everyone else</h3><p>Clean, numbered folders without duplicates, for your studies, your clients, your photos or your archives. €27 a year.</p><a class="btn btn-line" href="everyone.html">kornall for everyone</a></article>
</div>
</div>
</section>

<section class="section" id="pricing" aria-labelledby="pricing-title">
<div class="wrap">
<div class="section-head"><h2 id="pricing-title">Pricing</h2><p>Every plan starts with a free 7-day trial with all features.</p></div>
{BILLING}
{PLANS}
<p class="small muted" style="margin-top:16px">Personal prices include VAT. Professional, Team and Enterprise prices exclude VAT. <a href="pricing.html">Compare plans in detail</a></p>
</div>
</section>

<section class="section section-alt" id="faq" aria-labelledby="faq-title">
<div class="wrap" style="max-width:860px">
<h2 id="faq-title" style="margin-bottom:28px">Questions</h2>
{faq(FAQ_HOME)}
</div>
</section>

<section class="band" aria-label="Get started">
<div class="wrap">
<div><h2>Deliver your next Data Book complete</h2><p>Join the early access, or try kornall 2.0 free for 7 days.</p></div>
<div class="cta-row"><a class="btn btn-copper" href="early-access.html">Join early access</a><a class="btn btn-on-dark" href="trial.html">Start 7-day trial</a></div>
</div>
</section>
''')

# ---------------- Data Books ----------------
CONTENTS = [
    ('01', 'Index and cover', 'Client index, document register, cover page'),
    ('02', 'Certificates of conformity', 'Declaration of conformity, CE / PED or ASME documentation, nameplate'),
    ('03', 'Material certificates', 'Mill certificates (EN 10204 3.1 / 3.2), material traceability'),
    ('04', 'Welding', 'Welding procedures (WPS), qualification records (PQR), welder qualifications, weld map'),
    ('05', 'Non-destructive testing', 'RT, UT, MT, PT reports and NDT personnel certificates'),
    ('06', 'Tests', 'Hydrostatic or pressure test reports, functional and factory acceptance tests'),
    ('07', 'Surface treatment', 'Painting, coating, galvanizing reports'),
    ('08', 'Dimensional and final inspection', 'Dimensional reports, release notes, inspection certificates'),
    ('09', 'Drawings', 'As-built general arrangement and detail drawings'),
]
crow = ''.join(f'<tr><td>{a}</td><th scope="row">{b}</th><td>{c}</td></tr>' for a, b, c in CONTENTS)
TEMPLATES = [
    ('MDR / Data Book', 'Manufacturing record for equipment and fabrications.'),
    ('Final documentation dossier', 'The European name for the same handover file.'),
    ('O&amp;M manual', 'Operation and maintenance documentation for the end user.'),
    ('Turnover package', 'System-by-system handover at the end of construction.'),
    ('As-built package', 'Final drawings and records after commissioning.'),
    ('Quality dossier', 'Inspection and test plan with its records.'),
]
tcards = ''.join(f'<article class="card"><span class="k">Template</span><h3>{a}</h3><p>{b}</p></article>' for a, b in TEMPLATES)
STATUS = [
    ('Workspace map, staged moves, review, undo', NOW),
    ('Structured numbering (01.01, A.01)', NOW),
    ('Duplicate and version detection', NOW),
    ('One-page state report (WDS), PDF export', NOW),
    ('Data Book templates', DEV),
    ('Client index import from Excel', DEV),
    ('Completeness check and progress report', DEV),
    ('Final PDF compilation: cover, table of contents, bookmarks, page numbers', DEV),
    ('Revisions of the book (rev A, B, C) and change list', DEV),
    ('Shared template library for teams', DEV),
]
srow = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in STATUS)
FAQ_DB = [
    ('Does kornall follow a specific standard?', 'Data Book contents are set by each client and each project. kornall does not impose a structure: you import the client\'s own index, or start from a template and adapt it.'),
    ('Which file types can go into the book?', 'Any file can be filed and checked. For the compiled PDF, PDF documents are merged directly; other formats are listed in the index so nothing is forgotten.'),
    ('Can several people work on the same book?', 'With the Team plan, templates are shared across the team. Each person works on files on their PC or on a shared network drive.'),
    ('How do I get the Data Book module?', 'Join the early access. Professional and Team subscribers receive it as a free update when it is released.'),
]
page('data-books.html', 'Data Books', 'How kornall assembles Data Books, MDRs and handover dossiers: client index import, templates, completeness check, PDF compilation and revisions, offline.', 'databooks', f'''
<section class="hero">
<div class="wrap hero-grid center">
<div class="hero-copy">
<p class="eyebrow">Data Book module · early access</p>
<h1>Every document in its place, before the client checks.</h1>
<p class="lead">Import the client's index, file documents under it, see what is missing and compile the final book. For MDRs, Data Books, O&amp;M manuals and turnover packages.</p>
<div class="cta-row"><a class="btn btn-copper" href="early-access.html">Join early access</a><a class="btn btn-on-dark" href="#status">What is available today</a></div>
</div>
<div>{dbook()}</div>
</div>
</section>

<section class="section" aria-labelledby="what-title">
<div class="wrap">
<div class="split" style="align-items:start">
<div>
<h2 id="what-title">What a Data Book is</h2>
<p>When a manufacturer delivers equipment, it hands over the proof that it was built as specified: certificates, material traceability, welding and inspection records, test reports and drawings. The client decides the index, the numbering and the format. The book is checked, and the last payment often waits for it.</p>
<p style="margin-top:14px">Different industries call it a Manufacturing Data Record (MDR), Data Book, Final Documentation, Quality Dossier or Turnover Package. The work is the same: collect, number, check, compile.</p>
</div>
<div class="table-box" tabindex="0" role="region" aria-label="Typical Data Book contents">
<table class="compare contents">
<caption class="sr-only">Typical contents of a manufacturing Data Book</caption>
<thead><tr><th scope="col">No.</th><th scope="col">Section</th><th scope="col">Typical documents</th></tr></thead>
<tbody>{crow}</tbody>
</table>
</div>
</div>
<p class="small muted" style="margin-top:12px">Typical example. The real index always comes from the client's specification.</p>
</div>
</section>

<section class="section section-alt" aria-labelledby="tpl-title">
<div class="wrap">
<div class="section-head"><h2 id="tpl-title">Start from the client's index, or from a template</h2><p>Paste or import the index from Excel: numbers, titles and required documents become the structure of the book. Or begin with a template and adapt it.</p></div>
<div class="cards" style="background:var(--white)">{tcards}</div>
</div>
</section>

<section class="section" aria-labelledby="check-title">
<div class="wrap">
<div class="split">
<div>
<h2 id="check-title">Know what is missing, every day</h2>
<p>Each section shows how many documents are in place against what the index requires. Missing, duplicated and superseded documents are listed by name, so you can chase the right supplier the same day.</p>
<ul class="ticks"><li>Completeness per section and for the whole book</li><li>Superseded revisions flagged, never deleted for you</li><li class="copper">Progress report on one page, for the client or your manager</li></ul>
</div>
<div>{dbook()}</div>
</div>
<div class="split">
<div class="cards">
<article class="card"><span class="k">Cover</span><h3>Your title page</h3><p>Project, client, equipment tag, purchase order and revision.</p></article>
<article class="card"><span class="k">Contents</span><h3>Clickable table of contents</h3><p>Generated from the index, linked to each section.</p></article>
<article class="card"><span class="k">Bookmarks</span><h3>Navigation in any reader</h3><p>One bookmark per section and per document.</p></article>
<article class="card"><span class="k">Pages</span><h3>Page numbers</h3><p>Stamped through the whole book, with the revision.</p></article>
</div>
<div>
<h2>Compile the final book in one click</h2>
<p>kornall merges every document in index order into one PDF, with cover, table of contents, bookmarks and page numbers. When the client asks for revision B, change the documents and compile again.</p>
<ul class="ticks"><li>Revisions A, B, C with the list of what changed</li><li class="copper">Everything runs on your PC, even for large books</li></ul>
</div>
</div>
</div>
</section>

<section class="section section-alt" id="status" aria-labelledby="status-title">
<div class="wrap" style="max-width:960px">
<div class="section-head"><h2 id="status-title">What is available today</h2><p>We say clearly what you can use now and what is coming. The Data Book module is released to early-access users first, then to every Professional and Team subscriber at no extra cost.</p></div>
<div class="table-box" tabindex="0" role="region" aria-label="Feature availability">
<table class="compare" style="background:var(--white)">
<thead><tr><th scope="col" style="width:75%">Feature</th><th scope="col">Status</th></tr></thead>
<tbody>{srow}</tbody>
</table>
</div>
</div>
</section>

<section class="section" aria-labelledby="dbfaq-title">
<div class="wrap" style="max-width:860px">
<h2 id="dbfaq-title" style="margin-bottom:28px">Questions about Data Books</h2>
{faq(FAQ_DB)}
</div>
</section>

<section class="band" aria-label="Early access">
<div class="wrap">
<div><h2>Help shape the Data Book module</h2><p>Early-access users test it on real projects and tell us what their clients require.</p></div>
<div class="cta-row"><a class="btn btn-copper" href="early-access.html">Join early access</a><a class="btn btn-on-dark" href="pricing.html">See pricing</a></div>
</div>
</section>
''')

# ---------------- For everyone ----------------
FAQ_EVERY = [
    ('Do I need the Data Book features?', 'No. Personal includes the whole kornall workspace: map, numbering, duplicates and the state report. Data Book features are for industrial documentation and come with Professional.'),
    ('What does "up to 2 PCs" mean?', 'One Personal licence activates kornall on two computers you use, for example a desktop and a laptop. You can move an activation from your account.'),
    ('Can I cancel?', 'Yes, at any time from your account. kornall keeps working until the end of the period you paid for.'),
    ('Which systems are supported?', 'Windows 10 and Windows 11, 64-bit.'),
]
page('everyone.html', 'kornall for everyone', 'kornall Personal: map your folders, number them, remove duplicates and get a one-page report. €27 a year or €2.80 a month, up to 2 PCs.', 'everyone', f'''
<section class="hero">
<div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow">kornall Personal</p>
<h1>Clean, numbered folders, without the effort.</h1>
<p class="lead">See your folders as a map, number them in order, clear out duplicates and get a one-page summary. For studies, client work, photos and archives.</p>
<div class="cta-row"><a class="btn btn-copper" href="trial.html">Start your 7-day trial</a><a class="btn btn-on-dark" href="checkout.html?plan=personal&amp;billing=year">Buy for €27 a year</a></div>
<p class="fine">Or €2.80 a month, cancel anytime. VAT included. Up to 2 PCs.</p>
</div>
<img class="hero-shot" src="assets/img/map.webp" width="1440" height="900" alt="The kornall map: a folder drawn as a tree, with changes waiting for review" fetchpriority="high">
</div>
</section>

<section class="section" aria-labelledby="ev-title">
<div class="wrap">
<div class="section-head"><h2 id="ev-title">Four tools, in the order you need them</h2></div>
<div class="steps">
<article class="step"><span class="tag">01</span><h3>Map</h3><p>See the whole folder as a tree. Drag things where they belong; nothing moves until you approve.</p></article>
<article class="step"><span class="tag">02</span><h3>Number</h3><p>01, 01.01 or A, A.01, so everything sorts in the order you want.</p></article>
<article class="step"><span class="tag">03</span><h3>Clean</h3><p>Find identical files by content. Keep one, send the rest to the Recycle Bin.</p></article>
<article class="step"><span class="tag tag-copper">04</span><h3>Report</h3><p>One page with what the folder holds and what needs attention. Export to PDF.</p></article>
</div>
</div>
</section>

<section class="section-tight">
<div class="wrap">
<div class="cards">
<article class="card"><h3>Students and researchers</h3><p>Courses, sources and drafts numbered by chapter, one copy of each.</p></article>
<article class="card"><h3>Freelancers</h3><p>One clean folder per client and per project, ready to hand over.</p></article>
<article class="card"><h3>Photographers and creatives</h3><p>Find the duplicates eating your disk and keep the right copy.</p></article>
<article class="card"><h3>Home archives</h3><p>Papers, invoices and scans in an order you will still understand next year.</p></article>
</div>
</div>
</section>

<section class="section section-alt" aria-labelledby="evp-title">
<div class="wrap" style="max-width:860px">
<div class="tracks">
<article class="track copper">
<h2 id="evp-title" style="font-size:26px">kornall Personal</h2>
<p class="price">€27<small> / year</small></p>
<p class="small muted">or €2.80 a month · VAT included · up to 2 PCs · cancel anytime</p>
<div class="cta-row" style="margin-top:12px"><a class="btn btn-copper" href="checkout.html?plan=personal&amp;billing=year">Buy yearly</a><a class="btn btn-line" href="checkout.html?plan=personal&amp;billing=month">Buy monthly</a></div>
</article>
<article class="track">
<h3>Try it first</h3>
<p>Every feature for 7 days, no card needed and no automatic payment.</p>
<a class="btn btn-line" href="trial.html">Start 7-day trial</a>
</article>
</div>
</div>
</section>

<section class="section" aria-labelledby="evfaq-title">
<div class="wrap" style="max-width:860px">
<h2 id="evfaq-title" style="margin-bottom:28px">Questions</h2>
{faq(FAQ_EVERY)}
</div>
</section>
''')

# ---------------- Pricing ----------------
Y = '<span class="yes">Included</span>'
ROWS = [
    ('Workspace map, review, history and undo', Y, Y, Y, Y),
    ('Structured numbering (01.01, A.01)', Y, Y, Y, Y),
    ('Duplicate and version detection', Y, Y, Y, Y),
    ('One-page state report (WDS)', Y, Y, Y, Y),
    ('Data Book templates ' + DEV, '—', Y, Y, Y),
    ('Client index import from Excel ' + DEV, '—', Y, Y, Y),
    ('Completeness check and progress report ' + DEV, '—', Y, Y, Y),
    ('Final PDF compilation ' + DEV, '—', Y, Y, Y),
    ('Revisions of the book ' + DEV, '—', Y, Y, Y),
    ('Shared template library ' + DEV, '—', '—', Y, Y),
    ('Licence management', '—', '—', Y, Y),
    ('Computers', '2', '2', '1 per user', 'As agreed'),
    ('Invoice', 'Personal', 'Personal or company', 'Company, with VAT number', 'Company, contract'),
    ('Payment', 'Card, PayPal', 'Card, PayPal', 'Card, PayPal, bank transfer', 'Purchase order, bank transfer'),
    ('Support', 'Email', 'Priority email', 'Priority email', 'Named contact, onboarding'),
]
rows = ''.join('<tr><th scope="row">' + r[0] + '</th>' + ''.join('<td>' + c + '</td>' for c in r[1:]) + '</tr>' for r in ROWS)
FAQ_PRICING = [
    ('How does the trial work?', 'Install kornall and use every feature for 7 days. No card, no automatic payment. When the trial ends, choose a plan to continue.'),
    ('Why does Professional cost more than Personal?', 'Professional adds the Data Book module: templates, index import, completeness check, PDF compilation and revisions. It is priced for companies that deliver documentation to their clients.'),
    ('I buy Professional today. Do I get the Data Book module?', 'Yes. It is delivered as a free update to Professional and Team subscribers. Until then, you use the full kornall workspace.'),
    ('How does Team billing work?', '€15 per user per month, billed yearly, from 5 to 50 users. Add users anytime; they are billed pro rata until your renewal date.'),
    ('How do I cancel?', 'From your account, in one click. The plan stays active until the end of the period already paid. No further payment is taken.'),
    ('Do prices include VAT?', 'Personal prices include VAT. Professional, Team and Enterprise prices exclude VAT. EU companies outside France with a valid VAT number are invoiced without VAT (reverse charge), and customers outside the EU pay no EU VAT.'),
    ('Who processes payments?', '<span class="ph">[PAYMENT PROVIDER]</span> processes payments and sends invoices. kornall never sees or stores your card details.'),
]
page('pricing.html', 'Pricing', 'kornall pricing: Personal €27 a year, Professional €190 a year with the Data Book module, Team €15 per user per month, Enterprise on quote. 7-day free trial.', 'pricing', f'''
<section class="wrap page-head">
<h1>Pricing</h1>
<p>Start with a free 7-day trial with all features, no card needed. Then choose the plan that fits your work.</p>
</section>
<section class="wrap" aria-label="Plans" style="padding-bottom:56px">
{BILLING}
{PLANS}
<p class="small muted" style="margin-top:16px">Prices in euros. Personal prices include VAT; Professional, Team and Enterprise prices exclude VAT.</p>
</section>
<section class="wrap" aria-labelledby="compare-title" style="padding-bottom:88px">
<h2 id="compare-title" style="margin-bottom:20px">Compare plans</h2>
<div class="table-box" tabindex="0" role="region" aria-label="Plan comparison table">
<table class="compare">
<thead><tr><th scope="col" style="width:34%">Feature</th><th scope="col">Personal</th><th scope="col">Professional</th><th scope="col">Team</th><th scope="col">Enterprise</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p class="small muted" style="margin-top:12px">{DEV} Released to early-access users first, then to all Professional and Team subscribers at no extra cost.</p>
</section>
<section class="section section-alt" aria-labelledby="pfaq-title">
<div class="wrap" style="max-width:860px">
<h2 id="pfaq-title" style="margin-bottom:28px">Pricing questions</h2>
{faq(FAQ_PRICING)}
</div>
</section>
''')

# ---------------- Early access ----------------
page('early-access.html', 'Early access', 'Join the early access to the kornall Data Book module.', 'early', '''
<section class="wrap page-head">
<h1>Join the Data Book early access</h1>
<p>Test the module on your own projects before its release, and tell us what your clients require.</p>
</section>
<div class="wrap flow">
<div>
<form id="early-form" class="panel" novalidate>
<div class="panel-head">About you</div>
<div class="panel-body">
<div class="row2">
<div class="field"><label for="e-email">Work email</label><input id="e-email" type="email" autocomplete="email" placeholder="name@company.com"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="e-company">Company <span class="muted">(optional)</span></label><input id="e-company" type="text" autocomplete="organization"></div>
</div>
<div class="row2">
<div class="field"><label for="e-role">Your role</label><select id="e-role"><option value="">Choose</option><option>Document controller</option><option>QA/QC engineer</option><option>Project engineer or manager</option><option>Inspector</option><option>Company owner or director</option><option>Something else</option></select><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="e-kind">What you deliver <span class="muted">(optional)</span></label><select id="e-kind"><option value="">Choose</option><option>MDR / Data Books</option><option>Final documentation dossiers</option><option>O&amp;M manuals</option><option>Turnover packages</option><option>Something else</option></select></div>
</div>
<div class="field"><label for="e-size">Books per year <span class="muted">(optional)</span></label><select id="e-size"><option value="">Choose</option><option>1 to 10</option><option>10 to 50</option><option>50 to 200</option><option>More than 200</option></select></div>
<div class="check"><input id="e-consent" type="checkbox"><label for="e-consent">You can email me about the early access. I can unsubscribe at any time.</label><span class="err" aria-live="polite"></span></div>
<button class="btn btn-copper btn-block" type="submit">Join early access</button>
</div>
</form>
<div id="early-done" class="panel" hidden><div class="panel-head">You are on the list</div><div class="panel-body stack" style="gap:12px"><h2 tabindex="-1" style="font-size:24px">Thank you</h2><p>We received your request (simulated in this demo). We will write to you when the next early-access group opens.</p><div class="cta-row"><a class="btn btn-line" href="trial.html">Try kornall 2.0 meanwhile</a><a class="btn btn-ghost" href="index.html">Back to home</a></div></div></div>
</div>
<aside class="summary"><div class="panel"><div class="panel-head">What early access gives you</div><div class="panel-body">
<ul class="ticks"><li>The Data Book module before release</li><li>A direct line to the people building it</li><li>Templates set up with your clients' indexes</li><li class="copper">No payment to join</li></ul>
</div></div></aside>
</div>
''')

# ---------------- Checkout ----------------
COUNTRIES = [('', 'Choose a country'), ('FR', 'France'), ('BE', 'Belgium'), ('LU', 'Luxembourg'), ('DE', 'Germany'), ('ES', 'Spain'), ('IT', 'Italy'), ('NL', 'Netherlands'), ('PT', 'Portugal'), ('IE', 'Ireland'), ('AT', 'Austria'), ('SE', 'Sweden'), ('PL', 'Poland'), ('CH', 'Switzerland'), ('GB', 'United Kingdom'), ('CA', 'Canada'), ('US', 'United States'), ('MA', 'Morocco'), ('TN', 'Tunisia'), ('DZ', 'Algeria'), ('SN', 'Senegal')]
opts = ''.join(f'<option value="{v}"{" selected" if v == "FR" else ""}>{t}</option>' for v, t in COUNTRIES)
page('checkout.html', 'Checkout', 'Demo checkout for kornall.', 'checkout', f'''
<section class="wrap page-head">
<p style="margin:0 0 6px"><a href="pricing.html">Back to pricing</a></p>
<h1 id="plan-title">kornall Personal</h1>
<p>Secure checkout. In this demo, no payment is made and nothing leaves your browser.</p>
</section>
<div class="wrap flow">
<form id="checkout-form" novalidate aria-labelledby="plan-title">
<div class="notice notice-copper" style="margin-bottom:24px"><strong>Demo checkout.</strong> Do not enter real card details. Use the test card <span class="mono">4242 4242 4242 4242</span>, any future date and any 3 digits. The card <span class="mono">4000 0000 0000 0002</span> shows a declined payment.</div>

<fieldset>
<legend>Your details</legend>
<div class="field"><label for="email">Email</label><input id="email" type="email" autocomplete="email" placeholder="name@company.com" aria-describedby="email-hint"><span class="hint" id="email-hint">Your licence key and invoice are sent here.</span><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="full-name">Full name</label><input id="full-name" type="text" autocomplete="name"><span class="err" aria-live="polite"></span></div>
<div class="row2">
<div class="field" data-company hidden><label for="company">Company <span class="muted" id="company-label-opt">(optional)</span></label><input id="company" type="text" autocomplete="organization"><span class="err" aria-live="polite"></span></div>
<div class="field" data-company hidden><label for="vat-id">VAT number <span class="muted">(optional)</span></label><input id="vat-id" type="text" placeholder="FR12345678901" autocomplete="off"><span class="err" aria-live="polite"></span></div>
</div>
<div class="field"><label for="country">Country</label><select id="country" autocomplete="country">{opts}</select><span class="err" aria-live="polite"></span></div>
</fieldset>

<fieldset>
<legend>Payment method</legend>
<div class="choice">
<label><input type="radio" name="method" value="card" checked> Card <span class="right">Visa, Mastercard, CB</span></label>
<label><input type="radio" name="method" value="paypal"> PayPal</label>
<label data-team hidden><input type="radio" name="method" value="transfer"> Bank transfer <span class="right">Licences active when it arrives</span></label>
</div>
</fieldset>

<div data-method="card">
<div class="field"><label for="card-name">Name on card</label><input id="card-name" type="text" autocomplete="off"><span class="err" aria-live="polite"></span></div>
<div class="card-row">
<div class="field"><label for="card-number">Card number</label><input id="card-number" type="text" inputmode="numeric" autocomplete="off" placeholder="4242 4242 4242 4242"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="card-exp">Expiry</label><input id="card-exp" type="text" inputmode="numeric" autocomplete="off" placeholder="MM / YY"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="card-cvc">CVC</label><input id="card-cvc" type="text" inputmode="numeric" autocomplete="off" placeholder="123" maxlength="4"><span class="err" aria-live="polite"></span></div>
</div>
</div>
<div data-method="paypal" hidden><p class="notice" style="margin-bottom:20px">After you confirm, you would be sent to PayPal to approve the payment. In this demo, the approval is simulated.</p></div>
<div data-method="transfer" hidden><p class="notice" style="margin-bottom:20px">You receive an invoice with our bank details. Your licences are activated as soon as the transfer arrives, usually within 1 to 3 business days.</p></div>

<fieldset style="margin-top:8px">
<legend class="sr-only">Agreements</legend>
<div class="check"><input id="accept-terms" type="checkbox"><label for="accept-terms">I accept the <a href="terms.html">terms of sale</a> and the <a href="eula.html">licence agreement</a>.</label><span class="err" aria-live="polite"></span></div>
<div class="check" id="waiver-row"><input id="accept-waiver" type="checkbox"><label for="accept-waiver">I want my licence immediately and understand that I lose my 14-day right of withdrawal once it is activated.</label><span class="err" aria-live="polite"></span></div>
</fieldset>

<p class="notice" id="form-error" role="alert" hidden style="background:var(--danger-soft);color:var(--danger);border-color:#efc9c5;margin-bottom:16px"></p>
<button class="btn btn-copper btn-block" type="submit" style="min-height:52px;font-size:17px">Pay <span id="pay-amount">€27.00</span></button>
<p class="secure">{ICON['shield']} Payments would be processed by <span class="ph">[PAYMENT PROVIDER]</span>. kornall never stores card details.</p>
</form>

<aside class="summary" aria-label="Order summary">
<div class="panel">
<div class="panel-head">Order summary</div>
<div class="panel-body">
<p style="font-weight:600" id="sum-label">kornall Personal</p>
<p class="small muted" id="sum-detail" style="margin-bottom:16px"></p>
<div class="field" data-period><label for="sum-billing">Billing</label><select id="sum-billing"></select></div>
<div class="field" data-team hidden><label for="sum-seats">Users (5 to 50)</label><input id="sum-seats" type="number" min="5" max="50" inputmode="numeric"></div>
<table class="lines">
<tbody>
<tr class="sub"><td>Subtotal excluding VAT</td><td id="sum-net"></td></tr>
<tr class="sub"><td id="sum-vat-label">VAT</td><td id="sum-vat"></td></tr>
<tr class="total"><td>Total today</td><td id="sum-total"></td></tr>
</tbody>
</table>
<p class="small muted" id="sum-recurring" style="margin-top:10px"></p>
</div>
</div>
<ul class="ticks small" style="margin-top:20px"><li>Licence key by email right after payment</li><li>Cancel anytime from your account</li><li>7-day trial available first, <a href="trial.html">no card</a></li><li>Invoice available in your account</li></ul>
</aside>
</div>
<div class="overlay" id="processing" hidden role="dialog" aria-modal="true" aria-labelledby="proc-title">
<div class="dialog"><div class="panel-body" style="text-align:center;padding:36px 24px"><div class="spinner" aria-hidden="true"></div><p id="proc-title" style="font-weight:600">Processing your payment</p><p class="small muted">Demo: no money is moved.</p></div></div>
</div>
''')

# ---------------- Success ----------------
page('success.html', 'Payment confirmed', 'Demo order confirmation for kornall.', 'success', f'''
<section class="wrap page-head">
<h1>Thank you, your licence is ready</h1>
<p>A confirmation was sent to <strong id="ok-email">your email</strong> (simulated in this demo).</p>
</section>
<div class="wrap" style="padding-bottom:96px">
<div id="no-order" hidden class="notice">There is no order in this browser yet. <a href="pricing.html">Choose a plan</a> to run the demo checkout.</div>
<div id="order" class="flow">
<div class="stack">
<div class="panel">
<div class="panel-head">Your licence key</div>
<div class="panel-body">
<div class="keybox"><span id="ok-key">KNP-XXXX-XXXX-XXXX-XXXX</span><button class="btn btn-line" type="button" id="copy-key">Copy</button></div>
<p class="small muted" style="margin-top:10px">Keep this key. You can always find it in your account.</p>
<p class="notice notice-copper" id="transfer-note" hidden style="margin-top:12px">Your licences will be activated when your bank transfer arrives. The invoice with our bank details is in your account.</p>
</div>
</div>
<div class="panel">
<div class="panel-head">Next steps</div>
<div class="panel-body">
<ol class="next">
<li><span><a href="download.html">Download kornall for Windows</a> and install it.</span></li>
<li><span>Open kornall, go to Home, then Settings, and enter your licence key.</span></li>
<li id="ok-seats-note"><span>Assign licences to your team from your account.</span></li>
<li id="ok-databook-note"><span>Your plan includes the Data Book module. <a href="early-access.html">Join the early access</a> to get it first.</span></li>
<li><span>Open a workspace folder and start with the Map.</span></li>
</ol>
</div>
</div>
</div>
<aside class="summary">
<div class="panel">
<div class="panel-head">Order</div>
<div class="panel-body">
<dl class="kv">
<dt>Order number</dt><dd class="mono" id="ok-id"></dd>
<dt>Plan</dt><dd id="ok-plan"></dd>
<dt>Amount</dt><dd id="ok-total"></dd>
<dt>Payment</dt><dd id="ok-method"></dd>
<dt>Next renewal</dt><dd id="ok-renew"></dd>
</dl>
<div class="cta-row" style="margin-top:20px"><a class="btn btn-copper" href="account.html">Go to your account</a><a class="btn btn-line" href="invoice.html">View invoice</a></div>
</div>
</div>
</aside>
</div>
</div>
''')

# ---------------- Invoice ----------------
page('invoice.html', 'Invoice', 'Demo invoice for kornall.', 'invoice', '''
<section class="wrap page-head">
<p style="margin:0 0 6px"><a href="account.html">Back to your account</a></p>
<h1>Invoice</h1>
</section>
<div class="wrap" style="padding-bottom:96px;max-width:860px">
<div id="no-order" hidden class="notice">There is no order in this browser yet. <a href="pricing.html">Choose a plan</a> to run the demo checkout.</div>
<article id="invoice" class="panel">
<div class="panel-body" style="padding:36px">
<div style="display:flex;flex-wrap:wrap;justify-content:space-between;gap:24px;margin-bottom:32px">
<div><p style="font-weight:600;font-size:20px;color:var(--petrol)">kornall</p><p class="small muted"><span class="ph">[COMPANY NAME]</span><br><span class="ph">[ADDRESS]</span><br>SIRET <span class="ph">[SIRET]</span>, VAT <span class="ph">[VAT NUMBER]</span></p></div>
<div style="text-align:right"><p style="font-weight:600">Invoice <span class="mono" id="inv-id"></span></p><p class="small muted">Date: <span id="inv-date"></span><br>Order: <span class="mono" id="inv-order"></span><br>Status: <span id="inv-status"></span></p></div>
</div>
<p class="small muted">Billed to</p>
<p id="inv-to" style="white-space:pre-line;margin-bottom:28px"></p>
<table class="lines">
<tbody>
<tr><td><strong id="inv-label"></strong><br><span class="small muted" id="inv-detail"></span></td><td id="inv-net"></td></tr>
<tr class="sub"><td id="inv-vat-label">VAT</td><td id="inv-vat"></td></tr>
<tr class="total"><td>Total</td><td id="inv-total"></td></tr>
</tbody>
</table>
<p class="small muted" style="margin-top:28px">Demo invoice generated in your browser. It has no legal value.</p>
<button class="btn btn-line" type="button" id="print" style="margin-top:16px">Print or save as PDF</button>
</div>
</article>
</div>
''')

# ---------------- Account ----------------
page('account.html', 'Your account', 'Demo customer account for kornall: subscription, licence key, devices, invoices.', 'account', '''
<section class="wrap page-head">
<h1>Your account</h1>
<p>Manage your subscription, licence and computers. In this demo, everything is stored in this browser only.</p>
</section>
<div class="wrap" style="padding-bottom:96px">
<div id="no-account" hidden class="panel"><div class="panel-body stack" style="gap:14px">
<p>You have no subscription in this browser yet.</p>
<div class="cta-row"><a class="btn btn-copper" href="pricing.html">Choose a plan</a><button class="btn btn-line" type="button" id="sample-order">Load a sample account</button></div>
</div></div>
<div id="account" class="stack">
<p class="notice notice-ok" id="account-msg" role="status" hidden></p>
<div class="flow" style="padding-bottom:0">
<div class="stack">
<section class="panel" aria-labelledby="sub-title">
<div class="panel-head" id="sub-title">Subscription</div>
<div class="panel-body">
<dl class="kv">
<dt>Plan</dt><dd id="acc-plan"></dd>
<dt>Status</dt><dd><span class="status status-ok" id="acc-status">Active</span></dd>
<dt>Price</dt><dd id="acc-price"></dd>
<dt id="acc-renew-label">Renews on</dt><dd id="acc-renew"></dd>
<dt>Payment method</dt><dd id="acc-method"></dd>
<dt>Email</dt><dd id="acc-email"></dd>
</dl>
<div class="cta-row" style="margin-top:22px">
<button class="btn btn-line" type="button" id="switch-yearly">Switch to yearly</button>
<button class="btn btn-line" type="button" id="upgrade-pro">Upgrade to Professional</button>
<button class="btn btn-danger" type="button" id="cancel-btn">Cancel subscription</button>
<button class="btn btn-copper" type="button" id="resume-btn" hidden>Resume subscription</button>
</div>
</div>
</section>
<section class="panel" aria-labelledby="dev-title">
<div class="panel-head" id="dev-title">Computers</div>
<div class="panel-body">
<div id="devices-personal">
<p class="small muted" id="device-count" style="margin-bottom:8px"></p>
<p id="device-empty" class="small">No PC activated yet. Enter your licence key in kornall to activate it.</p>
<ul class="devices" id="device-list"></ul>
<button class="btn btn-line" type="button" id="add-device" style="margin-top:12px">Simulate activating a PC</button>
</div>
<div id="devices-team" hidden>
<p id="seat-count" style="margin-bottom:10px"></p>
<div style="height:10px;background:var(--soft);border:1px solid var(--line-2)"><div id="seat-bar" style="height:100%;background:var(--petrol);width:0"></div></div>
<button class="btn btn-line" type="button" id="assign-seat" style="margin-top:16px">Simulate assigning a user</button>
</div>
</div>
</section>
</div>
<div class="stack">
<section class="panel" aria-labelledby="key-title">
<div class="panel-head" id="key-title">Licence key</div>
<div class="panel-body"><div class="keybox"><span id="acc-key"></span><button class="btn btn-line" type="button" id="copy-acc-key">Copy</button></div></div>
</section>
<section class="panel" aria-labelledby="inv-title">
<div class="panel-head" id="inv-title">Invoices</div>
<div class="panel-body">
<table class="lines"><tbody><tr><td><a href="invoice.html" id="invoice-row-id">Invoice</a><br><span class="small muted" id="invoice-row-date"></span></td><td id="invoice-row-amount"></td></tr></tbody></table>
</div>
</section>
<button class="btn btn-ghost" type="button" id="reset-demo">Reset this demo account</button>
</div>
</div>
</div>
</div>
<div class="overlay" id="cancel-dialog" hidden role="dialog" aria-modal="true" aria-labelledby="cancel-title">
<div class="dialog">
<div class="panel-head" id="cancel-title">Cancel your subscription?</div>
<div class="panel-body">
<p>kornall keeps working until <strong id="cancel-until"></strong>. After that date, no payment is taken and the app stops applying changes. Your folders are never affected.</p>
<p class="small muted">You can resume the subscription until that date.</p>
</div>
<div class="dialog-actions"><button class="btn btn-line" type="button" id="keep-btn">Keep subscription</button><button class="btn btn-danger" type="button" id="confirm-cancel">Cancel subscription</button></div>
</div>
</div>
''')

# ---------------- Trial ----------------
page('trial.html', 'Start your 7-day trial', 'Try every kornall feature free for 7 days. No card needed.', 'trial', '''
<section class="wrap page-head">
<h1>Start your 7-day trial</h1>
<p>Every feature of kornall 2.0, free for 7 days. No card needed and no automatic payment.</p>
</section>
<div class="wrap flow">
<div>
<form id="trial-form" class="panel" novalidate>
<div class="panel-head">Get your trial key</div>
<div class="panel-body">
<div class="field"><label for="trial-email">Email</label><input id="trial-email" type="email" autocomplete="email" placeholder="name@company.com"><span class="hint">We send your trial key here. No newsletter unless you ask for it.</span><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="trial-use">What will you use kornall for? <span class="muted">(optional)</span></label><select id="trial-use"><option value="">Choose</option><option>Data Books / manufacturing records</option><option>O&amp;M manuals or turnover packages</option><option>Project deliveries</option><option>Studies or research</option><option>Personal archives</option><option>Something else</option></select></div>
<div class="check"><input id="trial-consent" type="checkbox"><label for="trial-consent">I accept the <a href="eula.html">licence agreement</a>.</label><span class="err" aria-live="polite"></span></div>
<button class="btn btn-copper btn-block" type="submit">Start my free trial</button>
</div>
</form>
<div id="trial-done" class="panel" hidden>
<div class="panel-head">Your trial is ready</div>
<div class="panel-body stack" style="gap:16px">
<h2 tabindex="-1" style="font-size:24px">Check your inbox</h2>
<p>We sent your trial key to <strong id="trial-to"></strong> (simulated in this demo). It works until <strong id="trial-end"></strong>.</p>
<div class="keybox"><span id="trial-key"></span></div>
<ol class="next"><li><span><a href="download.html">Download kornall</a> and install it.</span></li><li><span>Enter the trial key when kornall asks for it.</span></li><li><span>Before the trial ends, <a href="pricing.html">choose a plan</a> to keep going.</span></li></ol>
</div>
</div>
</div>
<aside class="summary">
<div class="panel"><div class="panel-head">Included in the trial</div><div class="panel-body">
<ul class="ticks"><li>Workspace map and staged reorganization</li><li>Structured numbering</li><li>Duplicate detection</li><li>WDS report and PDF export</li><li class="copper">Then Personal from €2.80 a month or Professional from €19 a month, only if you choose</li></ul>
</div></div>
</aside>
</div>
''')

# ---------------- Download ----------------
page('download.html', 'Download', 'Download kornall 2.0 for Windows 10 and 11, 64-bit.', 'download', f'''
<section class="wrap page-head">
<h1>Download kornall</h1>
<p>Version 2.0 for Windows 10 and Windows 11, 64-bit. Free for 7 days with a trial key.</p>
</section>
<div class="wrap flow">
<div class="stack">
<div class="panel">
<div class="panel-head">kornall 2.0.0 for Windows</div>
<div class="panel-body stack" style="gap:16px">
<dl class="kv">
<dt>File</dt><dd class="mono">kornall-Setup-2.0.0-x64.exe</dd>
<dt>Size</dt><dd>116 MB</dd>
<dt>SHA-256</dt><dd class="mono small" style="word-break:break-all">a4e84e26750fddd634584172dbb0b61cde4309fd3f360e61da08f42d775b08ca</dd>
<dt>Requirements</dt><dd>Windows 10 or 11, 64-bit, 4 GB RAM, 400 MB free space</dd>
</dl>
<button class="btn btn-copper" type="button" id="download-btn" style="justify-self:start">Download for Windows</button>
<p class="notice notice-copper" id="download-msg" tabindex="-1" hidden role="status">Demo: the installer is not hosted on this demo site. On the real site, the download starts here, served from <span class="ph">[GITHUB RELEASES OR CDN]</span>.</p>
</div>
</div>
<div class="panel">
<div class="panel-head">Install</div>
<div class="panel-body">
<ol class="next">
<li><span>Run the installer. If Windows shows "Windows protected your PC", choose <strong>More info</strong>, then <strong>Run anyway</strong>. The warning appears until the installer is code-signed.</span></li>
<li><span>Keep "Only for me": no administrator rights needed.</span></li>
<li><span>Open kornall from the Start menu and enter your trial or licence key.</span></li>
</ol>
</div>
</div>
</div>
<aside class="summary">
<div class="panel"><div class="panel-head">Need a key?</div><div class="panel-body stack" style="gap:12px">
<p>Start a free 7-day trial, or buy a licence. Professional and Team receive the Data Book module as a free update.</p>
<a class="btn btn-copper" href="trial.html">Start 7-day trial</a>
<a class="btn btn-line" href="pricing.html">See pricing</a>
</div></div>
</aside>
</div>
''')

# ---------------- Contact ----------------
page('contact.html', 'Contact', 'Contact kornall sales for Enterprise plans, licence packs and questions.', 'contact', '''
<section class="wrap page-head">
<h1>Contact us</h1>
<p>Enterprise plans, more than 50 users, Data Book templates for your clients, or anything else. We answer within <span class="ph">[2]</span> business days.</p>
</section>
<div class="wrap flow">
<div>
<form id="contact-form" class="panel" novalidate>
<div class="panel-head">Your request</div>
<div class="panel-body">
<div class="row2">
<div class="field"><label for="c-name">Name</label><input id="c-name" type="text" autocomplete="name"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="c-email">Work email</label><input id="c-email" type="email" autocomplete="email"><span class="err" aria-live="polite"></span></div>
</div>
<div class="row2">
<div class="field"><label for="c-company">Organization</label><input id="c-company" type="text" autocomplete="organization"><span class="err" aria-live="polite"></span></div>
<div class="field"><label for="c-seats">Number of users</label><select id="c-seats"><option>1 to 4</option><option>5 to 50</option><option>50 to 200</option><option>200 to 1,000</option><option>More than 1,000</option></select></div>
</div>
<div class="field"><label for="c-topic">Topic</label><select id="c-topic"><option value="enterprise">Enterprise plan</option><option value="team">Team plan</option><option value="databooks">Data Book templates</option><option value="support">Support</option><option value="other">Something else</option></select></div>
<div class="field"><label for="c-message">Message</label><textarea id="c-message" placeholder="Tell us about your team, your clients and the books you deliver."></textarea><span class="err" aria-live="polite"></span></div>
<button class="btn btn-copper" type="submit">Send request</button>
</div>
</form>
<div id="contact-done" class="panel" hidden><div class="panel-head">Request sent</div><div class="panel-body stack" style="gap:12px"><h2 tabindex="-1" style="font-size:24px">Thank you</h2><p>We received your request (simulated in this demo) and will answer by email.</p><a class="btn btn-line" href="index.html" style="justify-self:start">Back to home</a></div></div>
</div>
<aside class="summary"><div class="panel"><div class="panel-head">Other ways to reach us</div><div class="panel-body stack" style="gap:10px">
<p>Email: <span class="ph">[CONTACT EMAIL]</span></p>
<p>Address: <span class="ph">[POSTAL ADDRESS]</span></p>
</div></div></aside>
</div>
''')

# ---------------- Legal templates ----------------
TEMPLATE_NOTE = '<p class="notice notice-copper" style="margin-bottom:24px"><strong>Template.</strong> Replace every highlighted placeholder and have this text checked by a legal professional before selling.</p>'


def legal(name, title, desc, body):
    page(name, title, desc, 'legal', f'<section class="wrap page-head"><h1>{title}</h1></section><div class="wrap"><article class="prose">{TEMPLATE_NOTE}{body}</article></div>')


legal('legal.html', 'Legal notice', 'Legal notice (mentions légales) for kornall.', '''
<h2>Publisher</h2><p><span class="ph">[COMPANY NAME]</span>, <span class="ph">[LEGAL FORM]</span> with a capital of <span class="ph">[AMOUNT]</span> €, registered with the RCS of <span class="ph">[CITY]</span> under number <span class="ph">[SIREN]</span>. Head office: <span class="ph">[ADDRESS]</span>. Intra-community VAT number: <span class="ph">[VAT NUMBER]</span>.</p>
<p>Publication director: <span class="ph">[NAME]</span>. Contact: <span class="ph">[EMAIL]</span>.</p>
<h2>Hosting</h2><p>GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, United States (GitHub Pages).</p>
<h2>Intellectual property</h2><p>The kornall name, logo, software and the content of this site are protected. Any reproduction without permission is prohibited.</p>''')
legal('terms.html', 'Terms of sale', 'Terms of sale for kornall licences.', '''
<h2>1. Purpose</h2><p>These terms govern the sale of kornall software licences by <span class="ph">[COMPANY NAME]</span> to consumers and businesses.</p>
<h2>2. Plans and prices</h2><p>Personal: €27 per year or €2.80 per month, VAT included, for one person on up to 2 computers. Professional: €190 per year or €19 per month, excluding VAT, for one person on up to 2 computers. Team: €15 per user per month, billed yearly, excluding VAT, from 5 to 50 users. Enterprise: by quotation.</p><p>Features marked as early access are delivered as updates during the subscription, without extra charge.</p>
<h2>3. Trial</h2><p>A free 7-day trial is available without payment details. It does not convert into a paid subscription automatically.</p>
<h2>4. Payment and renewal</h2><p>Payments are processed by <span class="ph">[PAYMENT PROVIDER]</span>. Subscriptions renew automatically at the end of each period unless cancelled.</p>
<h2>5. Cancellation</h2><p>The customer can cancel at any time from their account. The licence remains active until the end of the period already paid. No partial refund is due for the current period, except as required by law.</p>
<h2>6. Right of withdrawal</h2><p>Consumers have 14 days to withdraw from a purchase. For digital content supplied immediately, the consumer expressly requests immediate supply and acknowledges losing this right once the licence is activated (article L221-28 13° of the French Consumer Code). <span class="ph">[CONFIRM WITH YOUR LAWYER]</span></p>
<h2>7. Liability</h2><p><span class="ph">[LIABILITY CLAUSE]</span></p>
<h2>8. Mediation and law</h2><p>Consumer mediator: <span class="ph">[MEDIATOR]</span>. These terms are governed by French law.</p>''')
legal('eula.html', 'Licence agreement', 'End-user licence agreement for kornall.', '''
<h2>1. Licence</h2><p>kornall is licensed, not sold. A Personal or Professional licence allows one person to use kornall on up to 2 computers. A Team seat allows one named user on one computer.</p>
<h2>2. Restrictions</h2><p>You may not resell, sublicense, reverse engineer or redistribute kornall, except as permitted by law.</p>
<h2>3. Your data</h2><p>kornall processes your files locally. It does not upload file contents or file names to <span class="ph">[COMPANY NAME]</span>.</p>
<h2>4. Updates</h2><p>Updates are included while the subscription is active.</p>
<h2>5. Warranty and liability</h2><p><span class="ph">[WARRANTY AND LIABILITY CLAUSES]</span></p>''')
legal('privacy.html', 'Privacy policy', 'How kornall handles personal data.', '''
<h2>On this website</h2><p>This site uses no cookies, no trackers and no analytics. Fonts are served from this site. In the demo, the information you type in the checkout, trial and account pages stays in your browser (local storage) and is never sent anywhere. You can erase it from the account page.</p>
<h2>In the kornall app</h2><p>kornall works offline. Your files, file names and folder structures stay on your computer. Licence activation would send only your licence key and an anonymous computer identifier to <span class="ph">[LICENCE SERVER]</span>.</p>
<h2>When you buy</h2><p>Payment data is processed by <span class="ph">[PAYMENT PROVIDER]</span> as independent controller. We keep your name, email, country and invoices for the period required by accounting law (10 years in France).</p>
<h2>Your rights</h2><p>You can access, correct or delete your data and object to its processing by writing to <span class="ph">[EMAIL]</span>. You can also complain to the CNIL (cnil.fr).</p>
<h2>Controller</h2><p><span class="ph">[COMPANY NAME]</span>, <span class="ph">[ADDRESS]</span>.</p>''')

# ---------------- 404 ----------------
page('404.html', 'Page not found', 'This page does not exist.', 'notfound', '''
<section class="wrap page-head" style="padding-bottom:120px">
<p class="mono" style="color:var(--copper-text)">404</p>
<h1>This page is not in the structure</h1>
<p>The address may be mistyped, or the page has moved.</p>
<div class="cta-row" style="margin-top:24px"><a class="btn btn-copper" href="index.html">Go to the home page</a><a class="btn btn-line" href="pricing.html">See pricing</a></div>
</section>
''')

print('pages written to', OUT)
