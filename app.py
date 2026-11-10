from flask import (
    Flask, request, redirect, url_for,
    flash, render_template_string
)
from datetime import datetime
import os
import re

app = Flask(__name__)

from flask import send_from_directory
from urllib.parse import quote

@app.route("/logo")
def company_logo():
    return send_from_directory(app.root_path, "LOGO_1.jpg")

@app.route("/photos/<path:filename>")
def leader_photo(filename):
    allowed_photos = {
        "pushpraj-singh.jpg.jpeg",
        "bandna-singh.jpg.jpeg"
    }

    if filename not in allowed_photos:
        return "Photo not found", 404

    return send_from_directory(app.root_path, filename)

app.secret_key = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET_KEY")

# ==========================================================
# COMPANY CONFIGURATION
# ==========================================================

COMPANY_NAME = "Sarvocch Microcare Foundation"
CIN = "U88900MP2026NPL084139"

EMAIL = "sarvocchmicrocare@gmail.com"
GRIEVANCE_EMAIL = "sarvocchmicrocare@gmail.com"

PHONE = "9111199101"
WEBSITE_URL = "https://sarvocchfinance.com"

ADDRESS = (
    "Shop No. 10A/GF, Sagar High Street, "
    "Ayodhya Bypass, Huzur, Bhopal, "
    "Madhya Pradesh - 462041"
)

MAP_URL = "https://maps.app.goo.gl/rRg5VuxdNicDwRYc8"

# ==========================================================
# BRANCH DIRECTORY
# Add additional verified branches here.
# Do not publish placeholder addresses as real branches.
# ==========================================================



# ==========================================================
# BRANCH DIRECTORY
# Add branches using Google Maps URLs
# ==========================================================

BRANCHES = [
    {
        "name": "Registered Office - Bhopal",
        "address": ADDRESS,
        "google_maps_url": "https://maps.app.goo.gl/rRg5VuxdNicDwRYc8",
        "phone": PHONE,
        "email": EMAIL,
        "status": "Registered Office"
    },
    {
        "name": "Pipariya Branch",
        "address": "Pipariya Madhya Pradesh, 461775",
        "google_maps_url": "https://www.google.com/maps?q=22.738750457763672,78.3563461303711&z=17&hl=en",
        "phone": PHONE,
        "email": EMAIL,
        "status": "Branch Office"
    }

]

# ==========================================================
# GOOGLE MAPS BRANCH LOCATION
# ==========================================================

def prepare_branch(branch):

    google_url = branch.get("google_maps_url", "")

    address = branch.get("address", "")

    # Default map using branch address
    map_embed = (
        "https://www.google.com/maps"
        "?q=" + quote(address) +
        "&output=embed"
    )

    map_url = google_url or (
        "https://www.google.com/maps/search/"
        "?api=1&query=" + quote(address)
    )

    # Handle direct Google Maps coordinate URLs
    if google_url:

        coordinate_match = re.search(
            r'@(-?\d+\.\d+),(-?\d+\.\d+)',
            google_url
        )

        if not coordinate_match:
            coordinate_match = re.search(
                r'[?&]q=(-?\d+\.\d+),(-?\d+\.\d+)',
                google_url
            )

        if coordinate_match:

            latitude = coordinate_match.group(1)
            longitude = coordinate_match.group(2)

            map_embed = (
                "https://www.google.com/maps"
                f"?q={latitude},{longitude}"
                "&z=18&output=embed"
            )

            map_url = (
                "https://www.google.com/maps/dir/?api=1"
                f"&destination={latitude},{longitude}"
            )

    return {
        **branch,
        "map_embed": map_embed,
        "map_url": map_url
    }

# ==========================================================
# LEADERSHIP DIRECTORY
# Biographies are editable sample descriptions.
# ==========================================================

LEADERS = [
    {
        "name": "Pushpraj Singh",
        "designation": "Director",
        "email": EMAIL,
        "photo": "pushpraj-singh.jpg.jpeg",
        "initials": "PS",
        "bio": (
            "Pushpraj Singh serves as Director of Sarvocch "
            "Microcare Foundation. He contributes to strategic "
            "planning, institutional development, responsible "
            "financial practices and transparent organisational "
            "operations."
        )
    },
    {
        "name": "Bandna Singh",
        "designation": "Managing Director",
        "email": EMAIL,
        "photo": "bandna-singh.jpg.jpeg",
        "initials": "BS",
        "bio": (
            "Bandna Singh serves as Managing Director of "
            "Sarvocch Microcare Foundation. She focuses on "
            "organisational leadership, operational management, "
            "customer relationships, financial inclusion and "
            "sustainable business development."
        )
    }
]

# These are proposed reporting levels, not verified
# appointments. Update when the actual organisation chart
# is approved.

MANAGEMENT_LEVELS = [
    "Board of Directors",
    "Managing Director",
    "Director",
    "Vice President"
]

# ==========================================================
# HTML TEMPLATE
# ==========================================================

HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
 content="width=device-width, initial-scale=1">

<title>{{ company_name }} | Financial Inclusion</title>

<meta name="description"
 content="Sarvocch Microcare Foundation - Responsible financial services, financial inclusion and community development.">

<meta name="keywords"
 content="Sarvocch Microcare Foundation, microfinance, Bhopal, financial inclusion">

<meta name="author" content="{{ company_name }}">
<meta name="robots" content="index,follow">

<link rel="canonical" href="{{ website_url }}/">

<meta name="theme-color" content="#0757b8">

<meta property="og:title"
 content="Sarvocch Microcare Foundation">

<meta property="og:description"
 content="Responsible financial solutions for inclusive growth.">

<meta property="og:url" content="{{ website_url }}">
<meta property="og:type" content="website">

<style>
:root {
    --blue:#0757b8;
    --blue2:#0a83df;
    --dark:#052c5c;
    --dark2:#041f40;
    --pale:#eef6ff;
    --light:#f6f9fc;
    --text:#1d3045;
    --muted:#66788c;
    --border:#dbe6f1;
    --green:#158653;
    --shadow:0 10px 35px rgba(4,45,90,.09);
}

* {
    box-sizing:border-box;
    margin:0;
    padding:0;
}

html { scroll-behavior:smooth; }

body {
    font-family:Inter,Segoe UI,Arial,sans-serif;
    color:var(--text);
    line-height:1.6;
    background:#fff;
}

a { text-decoration:none;color:inherit; }

button,input,textarea,select { font:inherit; }

.container {
    width:min(1180px,92%);
    margin:auto;
}

.topbar {
    background:var(--dark2);
    color:#d8e9fb;
    padding:9px 0;
    font-size:12px;
}

.topbar .container {
    display:flex;
    justify-content:space-between;
    gap:15px;
}

header {
    position:sticky;
    top:0;
    z-index:1000;
    background:#fff;
    border-bottom:1px solid var(--border);
    box-shadow:0 3px 16px rgba(0,0,0,.05);
}

.nav {
    min-height:75px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:15px;
}

.logo {
    display: flex;
    align-items: center;
    text-decoration: none;
}

.company-logo {
    height: 65px;
    width: auto;
    max-width: 230px;
    object-fit: contain;
    display: block;
}

.logo span { color:var(--blue); }

.logo small {
    display:block;
    font-size:9px;
    letter-spacing:3px;
}

.menu {
    display:flex;
    align-items:center;
    gap:17px;
    font-size:12px;
    font-weight:750;
}

.menu a:hover { color:var(--blue); }

.btn {
    display:inline-flex;
    justify-content:center;
    align-items:center;
    padding:11px 18px;
    border-radius:8px;
    border:1px solid transparent;
    font-size:13px;
    font-weight:800;
    cursor:pointer;
}

.primary {
    background:var(--blue);
    color:white;
}

.primary:hover { background:var(--dark); }

.outline {
    border-color:#b9cde1;
    color:var(--blue);
    background:white;
}

.menu-btn {
    display:none;
    border:0;
    background:var(--pale);
    color:var(--blue);
    border-radius:8px;
    padding:9px 13px;
    font-size:20px;
}

.hero {
    background:linear-gradient(125deg,#f3f9ff,#fff 55%,#eaf5ff);
    padding:85px 0;
}

.hero-grid {
    display:grid;
    grid-template-columns:1.1fr .9fr;
    gap:45px;
    align-items:center;
}

.eyebrow {
    display:inline-block;
    background:#e7f2ff;
    color:var(--blue);
    padding:7px 13px;
    border-radius:30px;
    font-size:10px;
    font-weight:900;
    letter-spacing:1px;
    margin-bottom:15px;
}

h1 {
    color:var(--dark);
    font-size:clamp(38px,5vw,61px);
    line-height:1.1;
    margin-bottom:18px;
}

h1 span { color:var(--blue); }

.hero p {
    color:var(--muted);
    font-size:16px;
    margin-bottom:25px;
}

.hero-box {
    background:linear-gradient(140deg,var(--blue),var(--blue2));
    padding:45px 30px;
    min-height:290px;
    border-radius:22px;
    color:white;
    box-shadow:var(--shadow);
}

.hero-box h2 { font-size:30px; }

.hero-box p {
    color:#dceeff;
    margin-top:12px;
}

.hero-actions {
    display:flex;
    gap:10px;
    flex-wrap:wrap;
}

.stats {
    background:var(--blue);
    color:white;
    padding:25px 0;
}

.stats-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
}

.stat {
    text-align:center;
    padding:10px;
    border-right:1px solid #ffffff35;
}

.stat:last-child { border:0; }

.stat strong {
    display:block;
    font-size:22px;
}

.stat span {
    font-size:11px;
    color:#dceeff;
}

.section { padding:75px 0; }

.soft { background:var(--light); }

.section-head {
    max-width:750px;
    margin:0 auto 40px;
    text-align:center;
}

.section-head h2 {
    font-size:clamp(28px,4vw,40px);
    color:var(--dark);
    line-height:1.2;
    margin-bottom:12px;
}

.section-head p { color:var(--muted); }

.grid-2 {
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:25px;
}

.grid-3 {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
}

.card {
    padding:25px;
    border:1px solid var(--border);
    border-radius:15px;
    background:white;
    box-shadow:0 5px 20px #0a366408;
}

.card h3 {
    color:var(--dark);
    margin-bottom:10px;
}

.card p {
    font-size:13px;
    color:var(--muted);
}

.icon {
    width:48px;
    height:48px;
    border-radius:12px;
    background:var(--pale);
    color:var(--blue);
    display:grid;
    place-items:center;
    font-size:22px;
    margin-bottom:15px;
}

.notice {
    background:#eaf4ff;
    border-left:4px solid var(--blue);
    padding:14px;
    margin-top:20px;
    border-radius:5px;
    font-size:12px;
    color:#40576d;
}

/* LEADERSHIP */

.leader-card {
    text-align:center;
    overflow:hidden;
    padding:0;
}

.leader-photo {
    width:100%;
    height:auto;
    aspect-ratio: 1100 / 1300;
    max-height:390px;
    background:linear-gradient(135deg,var(--blue),var(--blue2));
    display:flex;
    justify-content:center;
    align-items:center;
    color:white;
    font-size:55px;
    font-weight:900;
    overflow:hidden;
    margin:auto;
}

.leader-photo img {
    width:100%;
    height:100%;
    object-fit:contain;
    object-position:center;
    display:block;
}


.leader-info { padding:23px; }

.leader-info h3 {
    font-size:19px;
    margin-bottom:3px;
}

.designation {
    color:var(--blue);
    font-weight:850;
    font-size:12px;
    margin-bottom:12px;
}

.leader-info p {
    margin-bottom:13px;
}

.leader-email {
    font-size:11px;
    color:var(--blue);
    overflow-wrap:anywhere;
}

.hierarchy {
    max-width:650px;
    margin:35px auto 0;
}

.hierarchy-item {
    background:white;
    border:1px solid var(--border);
    border-left:4px solid var(--blue);
    padding:13px 18px;
    margin:10px auto;
    border-radius:8px;
    text-align:center;
    font-weight:800;
    color:var(--dark);
    width:90%;
}

.hierarchy-item:nth-child(2) { width:85%; }
.hierarchy-item:nth-child(3) { width:80%; }
.hierarchy-item:nth-child(4) { width:75%; }
.hierarchy-item:nth-child(5) { width:70%; }

/* BRANCHES */

.branch-card { overflow:hidden; }

.branch-card iframe {
    width:100%;
    height:280px;
    border:0;
    border-radius:10px;
    margin-top:16px;
}

.branch-address {
    color:var(--muted);
    font-size:13px;
    margin:10px 0;
}

.branch-status {
    display:inline-block;
    color:var(--green);
    background:#e8f7ef;
    padding:5px 10px;
    font-size:10px;
    border-radius:20px;
    font-weight:800;
}

/* FORMS */

.form-card {
    background:white;
    padding:28px;
    border:1px solid var(--border);
    border-radius:17px;
    box-shadow:var(--shadow);
}

.field { margin-bottom:15px; }

.field label {
    display:block;
    font-size:12px;
    font-weight:800;
    margin-bottom:6px;
}

.field input,
.field select,
.field textarea {
    width:100%;
    padding:12px;
    border:1px solid #cad8e6;
    border-radius:8px;
    outline:none;
}

.field textarea {
    min-height:100px;
    resize:vertical;
}

.field input:focus,
.field textarea:focus,
.field select:focus {
    border-color:var(--blue);
}

.form-row {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:12px;
}

.consent {
    display:flex;
    gap:8px;
    align-items:flex-start;
    font-size:11px;
    margin-bottom:16px;
}

.consent input { margin-top:4px; }

.calc-box {
    background:white;
    border:1px solid var(--border);
    border-radius:16px;
    padding:25px;
}

.range-value {
    color:var(--blue);
    font-weight:900;
    margin-bottom:5px;
}

input[type=range] { width:100%; }

.result {
    background:var(--dark);
    color:white;
    padding:18px;
    border-radius:12px;
    margin-top:15px;
}

.result-row {
    display:flex;
    justify-content:space-between;
    gap:10px;
    padding:9px 0;
    border-bottom:1px solid #ffffff25;
    font-size:12px;
}

.result-row:last-child { border:0; }

/* CONTACT */

.contact-dark {
    background:var(--dark);
    color:white;
    border-radius:17px;
    padding:30px;
}

.contact-dark h2 { margin-bottom:15px; }

.contact-dark p {
    color:#c9dcf1;
    font-size:13px;
    margin-bottom:12px;
}

.contact-dark a {
    color:#bce0ff;
    overflow-wrap:anywhere;
}

/* FAQ */

.faq {
    max-width:850px;
    margin:auto;
}

.faq-item {
    border-bottom:1px solid var(--border);
}

.faq-q {
    width:100%;
    background:white;
    border:0;
    padding:17px 5px;
    text-align:left;
    font-weight:800;
    color:var(--dark);
    cursor:pointer;
}

.faq-a {
    display:none;
    padding:0 5px 17px;
    color:var(--muted);
    font-size:13px;
}

.faq-item.active .faq-a { display:block; }

/* FOOTER */

footer {
    background:var(--dark2);
    color:white;
    padding:45px 0 20px;
}

.footer-grid {
    display:grid;
    grid-template-columns:2fr 1fr 1fr;
    gap:30px;
}

footer h3 {
    font-size:14px;
    margin-bottom:13px;
}

footer p,footer a {
    color:#a9bdd2;
    font-size:12px;
}

.footer-links {
    display:grid;
    gap:9px;
}

.footer-bottom {
    border-top:1px solid #ffffff20;
    margin-top:30px;
    padding-top:17px;
    display:flex;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:10px;
    font-size:11px;
    color:#9eb4ca;
}

.flash {
    background:#e8f7ef;
    color:#14643d;
    padding:13px;
    border-left:4px solid var(--green);
    margin:10px auto;
    width:92%;
    border-radius:6px;
    font-size:13px;
}

.mobile-nav { display:none; }

@media(max-width:900px) {
    .menu-btn { display:block; }

    .menu {
        display:none;
        position:absolute;
        top:75px;
        left:0;
        right:0;
        background:white;
        padding:20px;
        flex-direction:column;
        align-items:stretch;
        box-shadow:var(--shadow);
    }

    .menu.open { display:flex; }

    .hero-grid { grid-template-columns:1fr; }

    .grid-3 { grid-template-columns:repeat(2,1fr); }

    .footer-grid { grid-template-columns:1fr 1fr; }
}

@media(max-width:600px) {
    .container { width:92%; }

    .hero { padding:55px 0; }

    .hero h1 { font-size:38px; }

    .grid-2,.grid-3,
    .form-row { grid-template-columns:1fr; }

    .stats-grid { grid-template-columns:1fr 1fr; }

    .stat:nth-child(2) { border-right:0; }

    .section { padding:55px 0; }

    .footer-grid { grid-template-columns:1fr; }

    .footer-bottom { flex-direction:column; }

    .topbar .container { justify-content:center; }

    .mobile-nav {
        position:fixed;
        bottom:0;
        left:0;
        right:0;
        display:flex;
        background:white;
        border-top:1px solid var(--border);
        z-index:900;
    }

    .mobile-nav a {
        flex:1;
        text-align:center;
        padding:12px 2px;
        font-size:10px;
        font-weight:800;
        color:var(--blue);
    }

    body { padding-bottom:50px; }
}
</style>
</head>

<body>

{% with messages = get_flashed_messages() %}
{% for message in messages %}
<div class="flash">{{ message }}</div>
{% endfor %}
{% endwith %}

<div class="topbar">
<div class="container">
    <span>Responsible Finance | Financial Inclusion</span>
    <span>{{ email }}</span>
</div>
</div>

<header>
<div class="container nav">

<a href="#home" class="logo">
    <img
        src="{{ url_for('company_logo') }}"
        alt="Sarvocch Microcare Foundation Logo"
        class="company-logo"
    >
</a>

<button class="menu-btn" onclick="toggleMenu()">☰</button>

<nav class="menu" id="menu">
    <a href="#home">Home</a>
    <a href="#about">About</a>
    <a href="#products">Services</a>
    <a href="#leadership">Leadership</a>
    <a href="#branches">Branches</a>
    <a href="#corporate">Corporate</a>
    <a href="#application">Apply</a>
    <a href="#grievance">Grievance</a>
    <a href="#contact">Contact</a>
</nav>

</div>
</header>

<main>

<!-- HOME -->

<section class="hero" id="home">
<div class="container hero-grid">

<div>
<div class="eyebrow">FINANCIAL INCLUSION • RESPONSIBLE FINANCE</div>

<h1>Creating opportunities for a
<span>stronger tomorrow.</span></h1>

<p>
Sarvocch Microcare Foundation is focused on
expanding access to responsible financial services,
supporting livelihoods and encouraging inclusive
community development.
</p>

<div class="hero-actions">
<a href="#products" class="btn primary">Explore Services →</a>
<a href="#application" class="btn outline">Loan Enquiry</a>
</div>
</div>

<div class="hero-box">
<h2>Finance with purpose.</h2>
<p>
Building access to responsible financial opportunities
through transparency, customer awareness and
sustainable development.
</p>
</div>

</div>
</section>

<section class="stats">
<div class="container stats-grid">
<div class="stat"><strong>2026</strong><span>Incorporation Year</span></div>
<div class="stat"><strong>Bhopal</strong><span>Madhya Pradesh</span></div>
<div class="stat"><strong>Customer First</strong><span>Service Approach</span></div>
<div class="stat"><strong>Trust</strong><span>Transparency</span></div>
</div>
</section>

<!-- ABOUT -->

<section class="section" id="about">
<div class="container grid-2">

<div>
<div class="eyebrow">WHO WE ARE</div>
<h2 style="color:var(--dark);font-size:34px">
About Sarvocch Microcare Foundation
</h2>
<p style="color:var(--muted);margin-top:15px">
Sarvocch Microcare Foundation is a Bhopal-based
organisation focused on financial inclusion,
responsible financial services and community-oriented
development.
</p>
<p style="color:var(--muted);margin-top:12px">
Our approach emphasises transparent communication,
customer awareness, responsible practices and
long-term institutional growth.
</p>
</div>

<div class="card">
<h3>Our Core Values</h3>
<p>✓ Customer-first approach</p>
<p>✓ Transparent communication</p>
<p>✓ Responsible financial practices</p>
<p>✓ Financial awareness</p>
<p>✓ Community development</p>
<p>✓ Ethical business practices</p>
</div>

</div>
</section>

<!-- SERVICES -->

<section class="section soft" id="products">
<div class="container">

<div class="section-head">
<div class="eyebrow">OUR SERVICES</div>
<h2>Financial solutions built around real needs</h2>
<p>Service descriptions are indicative and subject to actual approved offerings.</p>
</div>

<div class="grid-3">

{% for service in services %}
<div class="card">
<div class="icon">{{ service.icon }}</div>
<h3>{{ service.name }}</h3>
<p>{{ service.description }}</p>
<a href="#application" style="color:var(--blue);font-size:12px;font-weight:800">
Make an Enquiry →
</a>
</div>
{% endfor %}

</div>

<div class="notice">
Important: Actual financial products, interest rates, fees,
eligibility, tenure and regulatory permissions must be
verified before publication.
</div>

</div>
</section>

<!-- LEADERSHIP -->

<section class="section" id="leadership">
<div class="container">

<div class="section-head">
<div class="eyebrow">OUR LEADERSHIP</div>
<h2>Directors & Management Team</h2>
<p>
Meet the leadership team of Sarvocch Microcare Foundation.
</p>
</div>

<div class="grid-2">

{% for person in leaders %}
<div class="card leader-card">

<div class="leader-photo">
    {% if person.photo %}
    <img
        src="{{ url_for('leader_photo', filename=person.photo) }}"
        alt="{{ person.name }}"
        onerror="this.remove();this.parentElement.textContent='{{ person.initials }}';"
    >
    {% else %}
    <span>{{ person.initials }}</span>
    {% endif %}
</div>

<div class="leader-info">
<h3>{{ person.name }}</h3>

<div class="designation">{{ person.designation }}</div>

<p>{{ person.bio }}</p>

<a class="leader-email"
href="mailto:{{ person.email }}">
{{ person.email }}
</a>

</div>
</div>
{% endfor %}

</div>

<div class="notice">
Management biographies are sample descriptions for
website layout purposes. Replace them with verified
professional biographies before publication.
</div>

<h2 style="text-align:center;color:var(--dark);margin-top:55px">
Management Hierarchy
</h2>

<p style="text-align:center;color:var(--muted);font-size:13px">
Proposed organisational reporting structure
</p>

<div class="hierarchy">
{% for level in management_levels %}
<div class="hierarchy-item">{{ level }}</div>
{% endfor %}
</div>

<div class="notice">
The reporting hierarchy above is illustrative.
Confirm actual positions, appointments and reporting
relationships before representing it as the official
organisation chart.
</div>

</div>
</section>

<!-- BRANCH DIRECTORY -->

<section class="section soft" id="branches">
<div class="container">

<div class="section-head">
<div class="eyebrow">OUR NETWORK</div>
<h2>Our Branch Locations</h2>
<p>
Find our offices and access Google Maps directions.
</p>
</div>

<div class="grid-2">

{% for branch in branches %}
<div class="card branch-card">

<span class="branch-status">{{ branch.status }}</span>

<h3 style="margin-top:13px">{{ branch.name }}</h3>

<p class="branch-address">{{ branch.address }}</p>

<p style="font-size:12px">
<strong>Phone:</strong>
<a href="tel:{{ branch.phone }}"
style="color:var(--blue)">
{{ branch.phone }}
</a>
</p>

<p style="font-size:12px">
<strong>Email:</strong>
<a href="mailto:{{ branch.email }}"
style="color:var(--blue)">
{{ branch.email }}
</a>
</p>

<iframe
src="{{ branch.map_embed }}"
loading="lazy"
referrerpolicy="no-referrer-when-downgrade"
allowfullscreen
title="Google Maps - {{ branch.name }}">
</iframe>

<a class="btn primary"
href="{{ branch.map_url }}"
target="_blank"
rel="noopener"
style="margin-top:15px">
Get Directions →
</a>

</div>
{% endfor %}

</div>

<div class="notice">
Additional branches can be displayed here after their
official addresses and Google Maps locations have been
verified and added to the BRANCHES configuration.
</div>

</div>
</section>

<!-- LOAN CALCULATOR -->

<section class="section" id="calculator">
<div class="container grid-2">

<div>
<div class="eyebrow">LOAN CALCULATOR</div>
<h2 style="color:var(--dark);font-size:34px">
Estimate your monthly repayment.
</h2>
<p style="color:var(--muted);margin-top:12px">
Calculate an illustrative monthly instalment using
the amount, annual interest rate and tenure.
</p>

<div class="notice">
This calculator is illustrative only. It is not a loan
offer, sanction or guarantee of approval.
</div>
</div>

<div class="calc-box">

<div class="field">
<label>Loan Amount</label>
<div class="range-value" id="amountValue">₹50,000</div>
<input id="amount" type="range"
min="5000" max="500000" step="5000" value="50000">
</div>

<div class="field">
<label>Annual Interest Rate</label>
<div class="range-value" id="rateValue">18%</div>
<input id="rate" type="range"
min="1" max="30" step=".5" value="18">
</div>

<div class="field">
<label>Tenure</label>
<div class="range-value" id="tenureValue">24 months</div>
<input id="tenure" type="range"
min="6" max="60" value="24">
</div>

<div class="result">
<div class="result-row">
<span>Estimated EMI</span>
<strong id="emi">₹0</strong>
</div>
<div class="result-row">
<span>Estimated Interest</span>
<strong id="interest">₹0</strong>
</div>
<div class="result-row">
<span>Total Repayment</span>
<strong id="total">₹0</strong>
</div>
</div>

</div>
</div>
</section>

<!-- CORPORATE INFORMATION -->

<section class="section soft" id="corporate">
<div class="container">

<div class="section-head">
<div class="eyebrow">CORPORATE INFORMATION</div>
<h2>Company Information</h2>
<p>Important corporate information for customers and stakeholders.</p>
</div>

<div class="grid-2">

<div class="card">
<h3>Company Details</h3>
<p><strong>Legal Name:</strong> {{ company_name }}</p>
<p><strong>CIN:</strong> {{ cin }}</p>
<p><strong>Incorporation:</strong> 2026</p>
<p><strong>Registered Office:</strong> Bhopal, Madhya Pradesh</p>
<p><strong>Website:</strong>
<a href="{{ website_url }}" style="color:var(--blue)">
{{ website_url }}
</a>
</p>
<p><strong>Official Email:</strong> {{ email }}</p>
</div>

<div class="card">
<h3>Registered Office Address</h3>
<p>{{ address }}</p>
<a href="{{ map_url }}" target="_blank" rel="noopener"
class="btn primary" style="margin-top:15px">
Open Google Maps →
</a>
</div>

</div>

<div class="notice">
Publish regulatory registrations, licences and financial
service permissions only after verification against
official documents.
</div>

</div>
</section>

<!-- LOAN ENQUIRY -->

<section class="section" id="application">
<div class="container grid-2">

<div>
<div class="eyebrow">LOAN ENQUIRY</div>
<h2 style="color:var(--dark);font-size:34px">
Tell us about your requirement.
</h2>
<p style="color:var(--muted);margin-top:12px">
Submit your details for information about applicable
financial products and eligibility.
</p>
<div class="notice">
An enquiry does not guarantee loan approval or disbursement.
</div>
</div>

<div class="form-card">
<h3>Loan Enquiry Form</h3>
<p style="font-size:12px;color:var(--muted);margin-bottom:18px">
Fields marked with * are required.
</p>

<form method="POST" action="{{ url_for('loan_application') }}">

<div class="form-row">
<div class="field">
<label>Full Name *</label>
<input name="name" required maxlength="100">
</div>
<div class="field">
<label>Mobile Number *</label>
<input name="phone" required pattern="[0-9]{10}"
maxlength="10" inputmode="numeric">
</div>
</div>

<div class="form-row">
<div class="field">
<label>Email</label>
<input type="email" name="email" maxlength="120">
</div>
<div class="field">
<label>State *</label>
<select name="state" required>
<option value="">Select State</option>
<option>Madhya Pradesh</option>
<option>Uttar Pradesh</option>
<option>Rajasthan</option>
<option>Maharashtra</option>
<option>Bihar</option>
<option>Gujarat</option>
<option>Delhi</option>
<option>Other</option>
</select>
</div>
</div>

<div class="field">
<label>Product</label>
<select name="loan_type">
<option>Income Generation Finance</option>
<option>Micro Enterprise Finance</option>
<option>Agriculture & Allied Activities</option>
<option>Housing Improvement</option>
<option>Water & Sanitation</option>
<option>Productive Asset Finance</option>
</select>
</div>

<div class="field">
<label>Approximate Requirement</label>
<input type="number" name="amount"
min="1000" max="5000000">
</div>

<div class="field">
<label>Purpose / Message</label>
<textarea name="message" maxlength="1000"></textarea>
</div>

<label class="consent">
<input type="checkbox" required>
I agree to be contacted regarding this enquiry.
</label>

<button class="btn primary" style="width:100%">
Submit Enquiry →
</button>

</form>
</div>

</div>
</section>

<!-- GRIEVANCE -->

<section class="section soft" id="grievance">
<div class="container grid-2">

<div>
<div class="eyebrow">CUSTOMER PROTECTION</div>
<h2 style="color:var(--dark);font-size:34px">
Grievance Redressal
</h2>
<p style="color:var(--muted);margin-top:12px">
We encourage customers to raise concerns through
the company's official grievance mechanism.
</p>
<div class="notice">
<strong>Grievance Email:</strong> {{ grievance_email }}
</div>
</div>

<div class="form-card">
<h3>Complaint Form</h3>

<form method="POST" action="{{ url_for('complaint') }}">

<div class="field">
<label>Name *</label>
<input name="name" required maxlength="100">
</div>

<div class="field">
<label>Mobile *</label>
<input name="phone" required pattern="[0-9]{10}"
maxlength="10">
</div>

<div class="field">
<label>Complaint Category *</label>
<select name="category" required>
<option value="">Select Category</option>
<option>Loan / Repayment</option>
<option>Staff Conduct</option>
<option>Charges / Fees</option>
<option>Disbursement</option>
<option>Collection</option>
<option>Digital / Technical</option>
<option>Privacy / Data</option>
<option>Other</option>
</select>
</div>

<div class="field">
<label>Complaint Details *</label>
<textarea name="details" required maxlength="2000"></textarea>
</div>

<button class="btn primary">Submit Complaint →</button>

</form>
</div>

</div>
</section>

<!-- CONTACT -->

<section class="section" id="contact">
<div class="container grid-2">

<div class="contact-dark">
<h2>Contact Sarvocch Microcare</h2>

<p><strong>Official Email</strong></p>
<p><a href="mailto:{{ email }}">{{ email }}</a></p>

<p><strong>Grievance Email</strong></p>
<p><a href="mailto:{{ grievance_email }}">{{ grievance_email }}</a></p>

<p><strong>Phone</strong></p>
<p>{{ phone }}</p>

<p><strong>Website</strong></p>
<p><a href="{{ website_url }}">{{ website_url }}</a></p>

<p><strong>Registered Office</strong></p>
<p>{{ address }}</p>

<a class="btn" href="{{ map_url }}"
target="_blank" rel="noopener"
style="background:white;color:var(--blue);margin-top:12px">
Open Google Maps →
</a>
</div>

<div class="form-card">
<h3>Send Us a Message</h3>

<form method="POST" action="{{ url_for('contact') }}">

<div class="field">
<label>Name *</label>
<input name="name" required maxlength="100">
</div>

<div class="field">
<label>Email *</label>
<input type="email" name="email" required maxlength="120">
</div>

<div class="field">
<label>Phone</label>
<input name="phone" pattern="[0-9]{10}" maxlength="10">
</div>

<div class="field">
<label>Message *</label>
<textarea name="message" required maxlength="1500"></textarea>
</div>

<label class="consent">
<input type="checkbox" required>
I agree to be contacted regarding this enquiry.
</label>

<button class="btn primary">Send Message →</button>

</form>
</div>

</div>
</section>

<!-- FAQ -->

<section class="section soft" id="faq">
<div class="container">

<div class="section-head">
<div class="eyebrow">FAQ</div>
<h2>Frequently Asked Questions</h2>
</div>

<div class="faq">

{% for question, answer in faqs %}
<div class="faq-item">
<button class="faq-q"
onclick="this.parentElement.classList.toggle('active')">
{{ question }}　+
</button>
<div class="faq-a">{{ answer }}</div>
</div>
{% endfor %}

</div>
</div>
</section>

</main>

<!-- FOOTER -->

<footer>
<div class="container">

<div class="footer-grid">

<div>
<h3>{{ company_name }}</h3>
<p>
Responsible financial services, financial inclusion
and community-oriented development.
</p>
<p style="margin-top:12px">{{ address }}</p>
</div>

<div>
<h3>Company</h3>
<div class="footer-links">
<a href="#about">About Us</a>
<a href="#leadership">Leadership</a>
<a href="#branches">Our Branches</a>
<a href="#corporate">Corporate Information</a>
</div>
</div>

<div>
<h3>Customer Support</h3>
<div class="footer-links">
<a href="#products">Services</a>
<a href="#application">Loan Enquiry</a>
<a href="#grievance">Grievance Redressal</a>
<a href="#contact">Contact Us</a>
<a href="#faq">FAQs</a>
<a href="{{ url_for('privacy') }}">Privacy Policy</a>
<a href="{{ url_for('terms') }}">Terms & Conditions</a>
</div>
</div>

</div>

<div class="footer-bottom">
<span>© {{ year }} {{ company_name }}. All rights reserved.</span>
<span>CIN: {{ cin }}</span>
<span><a href="{{ website_url }}">{{ website_url }}</a></span>
</div>

</div>
</footer>

<div class="mobile-nav">
<a href="#home">Home</a>
<a href="#products">Services</a>
<a href="#application">Apply</a>
<a href="#branches">Branches</a>
<a href="#contact">Contact</a>
</div>

<script>
function toggleMenu() {
    document.getElementById("menu").classList.toggle("open");
}

document.querySelectorAll("#menu a").forEach(function(link) {
    link.addEventListener("click", function() {
        document.getElementById("menu").classList.remove("open");
    });
});

const amount = document.getElementById("amount");
const rate = document.getElementById("rate");
const tenure = document.getElementById("tenure");

function money(value) {
    return "₹" + Math.round(value).toLocaleString("en-IN");
}

function calculateLoan() {
    const p = Number(amount.value);
    const r = Number(rate.value) / 1200;
    const n = Number(tenure.value);

    let emi;

    if (r === 0) {
        emi = p / n;
    } else {
        emi = p * r * Math.pow(1+r,n) /
              (Math.pow(1+r,n)-1);
    }

    const total = emi * n;

    document.getElementById("amountValue").textContent = money(p);
    document.getElementById("rateValue").textContent = rate.value + "%";
    document.getElementById("tenureValue").textContent = n + " months";
    document.getElementById("emi").textContent = money(emi);
    document.getElementById("interest").textContent = money(total-p);
    document.getElementById("total").textContent = money(total);
}

[amount,rate,tenure].forEach(function(element) {
    element.addEventListener("input",calculateLoan);
});

calculateLoan();

</script>

</body>
</html>
'''

# ==========================================================
# TEMPLATE DATA
# ==========================================================

SERVICES = [
    {
        "icon": "◈",
        "name": "Income Generation Finance",
        "description": "Potential financial support for eligible livelihood and income-generating activities."
    },
    {
        "icon": "▣",
        "name": "Micro Enterprise Finance",
        "description": "Potential financial solutions for eligible micro and small entrepreneurs."
    },
    {
        "icon": "♧",
        "name": "Agriculture & Allied Activities",
        "description": "Purpose-oriented solutions for eligible agriculture and allied activities."
    },
    {
        "icon": "⌂",
        "name": "Housing Improvement",
        "description": "Potential support for eligible household improvements and repairs."
    },
    {
        "icon": "◇",
        "name": "Water & Sanitation",
        "description": "Solutions for eligible water, sanitation and hygiene requirements."
    },
    {
        "icon": "▤",
        "name": "Productive Asset Finance",
        "description": "Potential financing options for eligible productive assets and equipment."
    }
]

FAQS = [
    (
        "Who can apply for financial assistance?",
        "Eligibility depends on the applicable product, customer profile, geography and company policies."
    ),
    (
        "What documents may be required?",
        "Identity, address and other documents may be required according to applicable policies."
    ),
    (
        "Is an online enquiry an approval?",
        "No. An online enquiry is not an approval or guarantee of disbursement."
    ),
    (
        "How can I make a complaint?",
        "Customers can submit a grievance using the grievance form or the official grievance email."
    ),
    (
        "Where is the registered office?",
        ADDRESS
    )
]

# ==========================================================
# CONTEXT PROCESSOR
# ==========================================================

@app.context_processor
def globals_data():
    return {
        "year": datetime.now().year,
        "company_name": COMPANY_NAME,
        "cin": CIN,
        "address": ADDRESS,
        "map_url": MAP_URL,
        "phone": PHONE,
        "email": EMAIL,
        "grievance_email": GRIEVANCE_EMAIL,
        "website_url": WEBSITE_URL,
        "branches": [
            prepare_branch(branch)
            for branch in BRANCHES
        ],
        "leaders": LEADERS,
        "management_levels": MANAGEMENT_LEVELS,
        "services": SERVICES,
        "faqs": FAQS
    }

# ==========================================================
# HELPERS
# ==========================================================

def clean(value, limit=2000):
    return " ".join((value or "").strip().split())[:limit]


def valid_phone(phone):
    return bool(re.fullmatch(r"[0-9]{10}", phone))


def valid_email(email):
    return bool(re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ))


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():
    return render_template_string(HTML)


# ==========================================================
# LOAN APPLICATION
# ==========================================================

@app.route("/apply", methods=["POST"])
def loan_application():

    name = clean(request.form.get("name"), 100)
    phone = clean(request.form.get("phone"), 15)
    email = clean(request.form.get("email"), 120)
    state = clean(request.form.get("state"), 80)
    loan_type = clean(request.form.get("loan_type"), 100)
    amount = clean(request.form.get("amount"), 30)
    message = clean(request.form.get("message"), 1000)

    if not name or not phone or not state:
        flash("Please complete all required fields.")
        return redirect(url_for("home") + "#application")

    if not valid_phone(phone):
        flash("Please enter a valid 10-digit mobile number.")
        return redirect(url_for("home") + "#application")

    if email and not valid_email(email):
        flash("Please enter a valid email address.")
        return redirect(url_for("home") + "#application")

    data = {
        "type": "loan_enquiry",
        "name": name,
        "phone": phone,
        "email": email,
        "state": state,
        "loan_type": loan_type,
        "amount": amount,
        "message": message,
        "created_at": datetime.now().isoformat()
    }

    # Replace with secure database storage or email delivery.
    print(data)

    flash("Your loan enquiry has been received.")

    return redirect(url_for("home") + "#application")


# ==========================================================
# COMPLAINT
# ==========================================================

@app.route("/complaint", methods=["POST"])
def complaint():

    name = clean(request.form.get("name"), 100)
    phone = clean(request.form.get("phone"), 15)
    category = clean(request.form.get("category"), 100)
    details = clean(request.form.get("details"), 2000)

    if not all([name, phone, category, details]):
        flash("Please complete all required complaint fields.")
        return redirect(url_for("home") + "#grievance")

    if not valid_phone(phone):
        flash("Please enter a valid 10-digit mobile number.")
        return redirect(url_for("home") + "#grievance")

    data = {
        "type": "grievance",
        "name": name,
        "phone": phone,
        "category": category,
        "details": details,
        "created_at": datetime.now().isoformat()
    }

    # Replace with secure grievance database storage.
    print(data)

    flash("Your complaint has been received.")

    return redirect(url_for("home") + "#grievance")


# ==========================================================
# CONTACT
# ==========================================================

@app.route("/contact", methods=["POST"])
def contact():

    name = clean(request.form.get("name"), 100)
    email = clean(request.form.get("email"), 120)
    phone = clean(request.form.get("phone"), 15)
    message = clean(request.form.get("message"), 1500)

    if not name or not email or not message:
        flash("Please complete all required fields.")
        return redirect(url_for("home") + "#contact")

    if not valid_email(email):
        flash("Please enter a valid email address.")
        return redirect(url_for("home") + "#contact")

    if phone and not valid_phone(phone):
        flash("Please enter a valid 10-digit mobile number.")
        return redirect(url_for("home") + "#contact")

    data = {
        "type": "general_enquiry",
        "name": name,
        "email": email,
        "phone": phone,
        "message": message,
        "created_at": datetime.now().isoformat()
    }

    # Replace with secure contact database storage.
    print(data)

    flash("Thank you. Your message has been received.")

    return redirect(url_for("home") + "#contact")


# ==========================================================
# PRIVACY POLICY
# ==========================================================

@app.route("/privacy")
def privacy():

    return render_template_string('''
    <div style="max-width:850px;margin:60px auto;
    padding:20px;font-family:Arial;line-height:1.8">

    <h1>Privacy Policy</h1>

    <p><strong>Sarvocch Microcare Foundation</strong></p>

    <p>We respect the privacy of individuals who contact
    our organisation through this website.</p>

    <h3>Information We Collect</h3>
    <p>Information voluntarily submitted through enquiry,
    contact and grievance forms may include names,
    contact information and enquiry details.</p>

    <h3>Use of Information</h3>
    <p>Information may be used to respond to enquiries,
    provide customer support and process grievances.</p>

    <h3>Data Protection</h3>
    <p>Appropriate organisational and technical measures
    should be implemented to protect personal information.</p>

    <h3>Contact</h3>
    <p>{{ email }}</p>

    <a href="/">Return to Home</a>
    </div>
    ''')


# ==========================================================
# TERMS AND CONDITIONS
# ==========================================================

@app.route("/terms")
def terms():

    return render_template_string('''
    <div style="max-width:850px;margin:60px auto;
    padding:20px;font-family:Arial;line-height:1.8">

    <h1>Terms and Conditions</h1>

    <p>Welcome to the website of
    {{ company_name }}.</p>

    <h3>Website Information</h3>
    <p>Website content is provided for general
    informational purposes.</p>

    <h3>Financial Enquiries</h3>
    <p>Submitting an online enquiry does not constitute
    a loan approval, sanction or commitment to disburse.</p>

    <h3>Product Information</h3>
    <p>Actual financial products, eligibility and terms
    are subject to approved company policies and
    applicable legal requirements.</p>

    <h3>Contact</h3>
    <p>{{ email }}</p>

    <a href="/">Return to Home</a>
    </div>
    ''')


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.route("/health")
def health():

    return {
        "status": "ok",
        "service": COMPANY_NAME,
        "time": datetime.now().isoformat()
    }


# ==========================================================
# 404
# ==========================================================

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("home"))


# ==========================================================
# APPLICATION START
# ==========================================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", "5110"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
