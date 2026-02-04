#!/usr/bin/env python3
"""
Build script to generate complete HTML pages for GitHub Pages deployment.
Combines base template with page content and inlines CSS.
"""

import os
import re
import json

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load image configuration
IMAGE_CONFIG_FILE = os.path.join(BASE_DIR, 'image-config.json')
IMAGE_MAP = {}
if os.path.exists(IMAGE_CONFIG_FILE):
    with open(IMAGE_CONFIG_FILE, 'r') as f:
        config = json.load(f)
        IMAGE_MAP = config.get('images', {})
PAGES_DIR = os.path.join(BASE_DIR, 'pages')
CSS_FILE = os.path.join(BASE_DIR, 'css', 'brand.css')
OUTPUT_DIR = os.path.join(BASE_DIR, 'docs')  # GitHub Pages serves from /docs

# Page configurations: (source_file, output_path, title, description)
PAGES = [
    # Core pages
    ('pages/core/home.html', 'index.html', 'Warehouse Storage Solutions | Pallet Racking Nationwide', 'Get quality pallet racking, warehouse design, installation, and relocation services nationwide. New and used rack available. Free quotes from Rack Storage Solutions.'),
    ('pages/core/about.html', 'about.html', 'About Us', 'Learn about Rack Storage Solutions - your trusted partner for warehouse storage solutions nationwide.'),
    ('pages/core/contact.html', 'contact.html', 'Contact Us | Get a Free Quote', 'Contact Rack Storage Solutions for a free quote on pallet racking, warehouse design, and installation services.'),
    ('pages/core/services-hub.html', 'services.html', 'Our Services', 'Explore our full range of warehouse storage services including pallet racking, design, installation, and relocation.'),
    ('pages/core/nationwide-service.html', 'nationwide-service.html', 'Nationwide Service', 'Rack Storage Solutions serves all 50 states with warehouse storage solutions.'),

    # Service pages
    ('pages/services/heavy-duty-pallet-racking.html', 'services/heavy-duty-pallet-racking.html', 'Heavy Duty Pallet Racking', 'Heavy duty pallet racking systems for warehouses. Selective, drive-in, push-back, and more.'),
    ('pages/services/used-pallet-rack.html', 'services/used-pallet-rack.html', 'Used Pallet Rack', 'Quality used pallet rack at 40-60% savings. Inspected and graded inventory available.'),
    ('pages/services/warehouse-design-layout.html', 'services/warehouse-design-layout.html', 'Warehouse Design & Layout', 'Custom warehouse design and layout services to maximize your storage space.'),
    ('pages/services/shelving-systems.html', 'services/shelving-systems.html', 'Shelving Systems', 'Industrial shelving systems for parts, cartons, and hand-pick operations.'),
    ('pages/services/warehouse-installation-teardown.html', 'services/warehouse-installation-teardown.html', 'Installation & Teardown', 'Professional warehouse racking installation and teardown services.'),
    ('pages/services/warehouse-relocation.html', 'services/warehouse-relocation.html', 'Warehouse Relocation', 'Complete warehouse relocation services including teardown, transport, and reinstallation.'),
    ('pages/services/permitting-engineering.html', 'services/permitting-engineering.html', 'Permitting & Engineering', 'Pallet rack permitting and engineering services. PE-stamped drawings available.'),
    ('pages/services/rack-safety-inspections.html', 'services/rack-safety-inspections.html', 'Rack Safety Inspections', 'Professional rack safety inspections to keep your warehouse compliant and safe.'),

    # New service pages
    ('pages/services/garage-storage.html', 'garage-storage.html', 'Garage Storage Solutions', 'Garage storage and organization solutions. Heavy-duty garage racking and shelving.'),
    ('pages/services/lockers.html', 'lockers.html', 'Industrial Lockers', 'Industrial and employee lockers for warehouses and facilities.'),
    ('pages/services/lift-equipment.html', 'lift-equipment.html', 'Lift Equipment', 'Warehouse lift equipment and material handling solutions.'),
    ('pages/services/warehouse-safety.html', 'warehouse-safety.html', 'Warehouse Safety', 'Warehouse safety products and solutions.'),
    ('pages/services/containment-fencing.html', 'containment-fencing.html', 'Containment Fencing', 'Warehouse containment fencing and security caging.'),
    ('pages/services/rack-protection.html', 'rack-protection.html', 'Rack Protection', 'Pallet rack protection products - column guards, end-of-aisle guards, and more.'),
    ('pages/services/labeling-services.html', 'labeling-services.html', 'Labeling Services', 'Warehouse labeling and signage services.'),

    # Industry pages
    ('pages/industries/3pl-logistics.html', 'industries/3pl-logistics.html', '3PL & Logistics', 'Warehouse storage solutions for 3PL and logistics operations.'),
    ('pages/industries/manufacturing.html', 'industries/manufacturing.html', 'Manufacturing', 'Industrial storage solutions for manufacturing facilities.'),
    ('pages/industries/ecommerce.html', 'industries/ecommerce.html', 'E-Commerce', 'Warehouse solutions for e-commerce fulfillment centers.'),
    ('pages/industries/cold-storage.html', 'industries/cold-storage.html', 'Cold Storage', 'Cold storage racking solutions for freezer and cooler environments.'),
    ('pages/industries/retail.html', 'industries/retail.html', 'Retail', 'Storage solutions for retail distribution centers.'),

    # Authority pages
    ('pages/authority/faq-hub.html', 'resources/faq.html', 'Frequently Asked Questions', 'Common questions about pallet racking, installation, and warehouse storage.'),
    ('pages/authority/how-it-works.html', 'resources/how-it-works.html', 'How It Works', 'Learn about our process from consultation to installation.'),
    ('pages/authority/glossary.html', 'resources/glossary.html', 'Warehouse Glossary', 'Warehouse and racking terminology explained.'),
    ('pages/authority/safety-compliance.html', 'resources/safety-compliance.html', 'Safety & Compliance', 'Rack safety standards and compliance information.'),
    ('pages/authority/industries-hub.html', 'industries.html', 'Industries We Serve', 'Warehouse storage solutions for various industries.'),

    # Resource pages
    ('pages/resources/new-vs-used-pallet-rack.html', 'resources/new-vs-used-pallet-rack.html', 'New vs Used Pallet Rack', 'Compare new and used pallet rack options.'),
    ('pages/resources/racking-types-comparison.html', 'resources/racking-types-comparison.html', 'Racking Types Comparison', 'Compare different types of pallet racking systems.'),
    ('pages/resources/when-you-need-permits.html', 'resources/when-you-need-permits.html', 'When You Need Permits', 'Guide to pallet rack permitting requirements.'),

    # Landing pages (existing)
    ('pages/landing/quote.html', 'quote.html', 'Get a Free Quote', 'Request a free pallet racking quote from Rack Storage Solutions.'),
    ('pages/landing/used-rack-inventory.html', 'used-rack-inventory.html', 'Used Rack Inventory', 'Check available used pallet rack inventory.'),
    ('pages/landing/warehouse-design-consultation.html', 'warehouse-design-consultation.html', 'Free Design Consultation', 'Book a free warehouse design consultation.'),
    ('pages/landing/permitting-services.html', 'permitting-services.html', 'Permitting Services', 'Pallet rack permitting services.'),
    ('pages/landing/warehouse-relocation-quote.html', 'warehouse-relocation-quote.html', 'Relocation Quote', 'Get a warehouse relocation quote.'),

    # NEW Landing Pages (/lp/)
    ('pages/lp/pallet-rack.html', 'lp/pallet-rack.html', 'Pallet Rack | Free Quote', 'Get a free quote on pallet racking systems. New and used rack available.'),
    ('pages/lp/used-pallet-rack.html', 'lp/used-pallet-rack.html', 'Used Pallet Rack | Save 40-60%', 'Quality used pallet rack at 40-60% savings. Free quote.'),
    ('pages/lp/warehouse-racking.html', 'lp/warehouse-racking.html', 'Warehouse Racking | Free Quote', 'Warehouse racking solutions. Design, supply, and installation.'),
    ('pages/lp/heavy-duty-rack.html', 'lp/heavy-duty-rack.html', 'Heavy Duty Rack | Industrial Racking', 'Heavy duty industrial racking for warehouses.'),
    ('pages/lp/garage-storage.html', 'lp/garage-storage.html', 'Garage Storage | Free Quote', 'Garage storage and organization solutions.'),
    ('pages/lp/shelving.html', 'lp/shelving.html', 'Industrial Shelving | Free Quote', 'Industrial shelving systems for warehouses.'),
    ('pages/lp/warehouse-design.html', 'lp/warehouse-design.html', 'Warehouse Design | Free Consultation', 'Free warehouse design consultation.'),
    ('pages/lp/warehouse-relocation.html', 'lp/warehouse-relocation.html', 'Warehouse Relocation | Get Quote', 'Complete warehouse relocation services.'),
    ('pages/lp/rack-installation.html', 'lp/rack-installation.html', 'Rack Installation | Professional Install', 'Professional pallet rack installation services.'),
    ('pages/lp/local-pickup.html', 'lp/local-pickup.html', 'Local Pickup | Orlando FL', 'Local pickup available in Orlando, FL area.'),

    # Geo-targeted Landing Pages
    ('pages/lp/pallet-rack-orlando.html', 'lp/pallet-rack-orlando.html', 'Pallet Rack Orlando FL', 'Pallet racking in Orlando, Florida. Local service and installation.'),
    ('pages/lp/pallet-rack-tampa.html', 'lp/pallet-rack-tampa.html', 'Pallet Rack Tampa FL', 'Pallet racking in Tampa, Florida. Local service and installation.'),
    ('pages/lp/pallet-rack-jacksonville.html', 'lp/pallet-rack-jacksonville.html', 'Pallet Rack Jacksonville FL', 'Pallet racking in Jacksonville, Florida. Local service and installation.'),
    ('pages/lp/pallet-rack-atlanta.html', 'lp/pallet-rack-atlanta.html', 'Pallet Rack Atlanta GA', 'Pallet racking in Atlanta, Georgia. Local service and installation.'),
    ('pages/lp/pallet-rack-miami.html', 'lp/pallet-rack-miami.html', 'Pallet Rack Miami FL', 'Pallet racking in Miami, Florida. Local service and installation.'),

    # Location Pages
    ('pages/locations/orlando-fl.html', 'locations/orlando-fl.html', 'Pallet Racking Orlando FL', 'Pallet racking and warehouse storage in Orlando, Florida.'),
    ('pages/locations/tampa-fl.html', 'locations/tampa-fl.html', 'Pallet Racking Tampa FL', 'Pallet racking and warehouse storage in Tampa, Florida.'),
    ('pages/locations/jacksonville-fl.html', 'locations/jacksonville-fl.html', 'Pallet Racking Jacksonville FL', 'Pallet racking and warehouse storage in Jacksonville, Florida.'),
    ('pages/locations/miami-fl.html', 'locations/miami-fl.html', 'Pallet Racking Miami FL', 'Pallet racking and warehouse storage in Miami, Florida.'),
    ('pages/locations/atlanta-ga.html', 'locations/atlanta-ga.html', 'Pallet Racking Atlanta GA', 'Pallet racking and warehouse storage in Atlanta, Georgia.'),
    ('pages/locations/savannah-ga.html', 'locations/savannah-ga.html', 'Pallet Racking Savannah GA', 'Pallet racking and warehouse storage in Savannah, Georgia.'),
    ('pages/locations/charlotte-nc.html', 'locations/charlotte-nc.html', 'Pallet Racking Charlotte NC', 'Pallet racking and warehouse storage in Charlotte, North Carolina.'),
    ('pages/locations/nashville-tn.html', 'locations/nashville-tn.html', 'Pallet Racking Nashville TN', 'Pallet racking and warehouse storage in Nashville, Tennessee.'),
    ('pages/locations/birmingham-al.html', 'locations/birmingham-al.html', 'Pallet Racking Birmingham AL', 'Pallet racking and warehouse storage in Birmingham, Alabama.'),
    ('pages/locations/memphis-tn.html', 'locations/memphis-tn.html', 'Pallet Racking Memphis TN', 'Pallet racking and warehouse storage in Memphis, Tennessee.'),
    ('pages/locations/columbia-sc.html', 'locations/columbia-sc.html', 'Pallet Racking Columbia SC', 'Pallet racking and warehouse storage in Columbia, South Carolina.'),
    ('pages/locations/charleston-sc.html', 'locations/charleston-sc.html', 'Pallet Racking Charleston SC', 'Pallet racking and warehouse storage in Charleston, South Carolina.'),
    ('pages/locations/richmond-va.html', 'locations/richmond-va.html', 'Pallet Racking Richmond VA', 'Pallet racking and warehouse storage in Richmond, Virginia.'),
    ('pages/locations/raleigh-nc.html', 'locations/raleigh-nc.html', 'Pallet Racking Raleigh NC', 'Pallet racking and warehouse storage in Raleigh, North Carolina.'),
    ('pages/locations/new-orleans-la.html', 'locations/new-orleans-la.html', 'Pallet Racking New Orleans LA', 'Pallet racking and warehouse storage in New Orleans, Louisiana.'),

    # Careers page
    ('pages/core/careers.html', 'careers.html', 'Careers', 'Join the Rack Storage Solutions team. View current job openings.'),

    # Thank you pages
    ('pages/thank-you/quote.html', 'thank-you/quote.html', 'Thank You', 'Thank you for your quote request.'),
    ('pages/thank-you/contact.html', 'thank-you/contact.html', 'Thank You', 'Thank you for contacting us.'),
    ('pages/thank-you/consultation.html', 'thank-you/consultation.html', 'Consultation Scheduled', 'Your consultation has been scheduled.'),
    ('pages/thank-you/download.html', 'thank-you/download.html', 'Download Ready', 'Your download is ready.'),
]

# Landing page configurations (use LP template)
LP_PAGES = [
    ('pages/lp/pallet-rack.html', 'lp/pallet-rack.html', 'Pallet Rack | Free Quote', 'Get a free quote on pallet racking systems. New and used rack available.'),
    ('pages/lp/used-pallet-rack.html', 'lp/used-pallet-rack.html', 'Used Pallet Rack | Save 40-60%', 'Quality used pallet rack at 40-60% savings. Free quote.'),
    ('pages/lp/warehouse-racking.html', 'lp/warehouse-racking.html', 'Warehouse Racking | Free Quote', 'Warehouse racking solutions. Design, supply, and installation.'),
    ('pages/lp/heavy-duty-rack.html', 'lp/heavy-duty-rack.html', 'Heavy Duty Rack | Industrial Racking', 'Heavy duty industrial racking for warehouses.'),
    ('pages/lp/garage-storage.html', 'lp/garage-storage.html', 'Garage Storage | Free Quote', 'Garage storage and organization solutions.'),
    ('pages/lp/shelving.html', 'lp/shelving.html', 'Industrial Shelving | Free Quote', 'Industrial shelving systems for warehouses.'),
    ('pages/lp/warehouse-design.html', 'lp/warehouse-design.html', 'Warehouse Design | Free Consultation', 'Free warehouse design consultation.'),
    ('pages/lp/warehouse-relocation.html', 'lp/warehouse-relocation.html', 'Warehouse Relocation | Get Quote', 'Complete warehouse relocation services.'),
    ('pages/lp/rack-installation.html', 'lp/rack-installation.html', 'Rack Installation | Professional Install', 'Professional pallet rack installation services.'),
    ('pages/lp/local-pickup.html', 'lp/local-pickup.html', 'Local Pickup | Orlando FL', 'Local pickup available in Orlando, FL area.'),
    ('pages/lp/pallet-rack-orlando.html', 'lp/pallet-rack-orlando.html', 'Pallet Rack Orlando FL', 'Pallet racking in Orlando, Florida. Local service and installation.'),
    ('pages/lp/pallet-rack-tampa.html', 'lp/pallet-rack-tampa.html', 'Pallet Rack Tampa FL', 'Pallet racking in Tampa, Florida. Local service and installation.'),
    ('pages/lp/pallet-rack-jacksonville.html', 'lp/pallet-rack-jacksonville.html', 'Pallet Rack Jacksonville FL', 'Pallet racking in Jacksonville, Florida. Local service and installation.'),
    ('pages/lp/pallet-rack-atlanta.html', 'lp/pallet-rack-atlanta.html', 'Pallet Rack Atlanta GA', 'Pallet racking in Atlanta, Georgia. Local service and installation.'),
    ('pages/lp/pallet-rack-miami.html', 'lp/pallet-rack-miami.html', 'Pallet Rack Miami FL', 'Pallet racking in Miami, Florida. Local service and installation.'),
]

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def get_template(css_content):
    """Generate the complete HTML template with inlined CSS."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{{{PAGE_TITLE}}}} | Rack Storage Solutions</title>
  <meta name="description" content="{{{{META_DESCRIPTION}}}}">
  <link rel="canonical" href="https://simpleleadsads-blip.github.io/rs-solutions-website/{{{{CANONICAL_PATH}}}}">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/rs-solutions-website/favicon.png">
  <link rel="apple-touch-icon" href="/rs-solutions-website/favicon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{{{PAGE_TITLE}}}} | Rack Storage Solutions">
  <meta property="og:description" content="{{{{META_DESCRIPTION}}}}">
  <meta property="og:image" content="https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png">

  <!-- Geo Meta Tags -->
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="Longwood">
  <meta name="geo.position" content="28.7028;-81.3586">
  <meta name="ICBM" content="28.7028, -81.3586">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Google Analytics 4 + Google Ads -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XHZ0XZW8L3"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XHZ0XZW8L3');
    gtag('config', 'AW-17500834233');
  </script>

  <!-- LocalBusiness Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Rack Storage Solutions",
    "image": "https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png",
    "telephone": "+1-833-777-2257",
    "email": "Sales@IneedRacks.com",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "1687 Timocuan Way Unit 113",
      "addressLocality": "Longwood",
      "addressRegion": "FL",
      "postalCode": "32750",
      "addressCountry": "US"
    }},
    "geo": {{
      "@type": "GeoCoordinates",
      "latitude": 28.7028,
      "longitude": -81.3586
    }},
    "url": "https://www.rackstoragesolutions.com",
    "priceRange": "$$",
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "47"
    }},
    "sameAs": [
      "https://youtube.com/racksdirect",
      "https://instagram.com/Racksdirect",
      "https://facebook.com/racksdirect"
    ]
  }}
  </script>

  <style>
{css_content}
  </style>
</head>
<body>
  <a href="#main-content" class="sr-only">Skip to main content</a>

  <!-- Header -->
  <header class="header">
    <div class="container">
      <div class="header__inner">
        <a href="/rs-solutions-website/" class="header__logo">
          <img src="https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png" alt="Rack Storage Solutions" width="200" height="50">
        </a>
        <nav class="nav">
          <a href="/rs-solutions-website/" class="nav__link">Home</a>
          <div class="nav__dropdown">
            <a href="/rs-solutions-website/services.html" class="nav__link">Services</a>
            <div class="nav__dropdown-menu">
              <a href="/rs-solutions-website/services/heavy-duty-pallet-racking.html" class="nav__dropdown-link">Pallet Racking</a>
              <a href="/rs-solutions-website/services/used-pallet-rack.html" class="nav__dropdown-link">Used Rack</a>
              <a href="/rs-solutions-website/services/warehouse-design-layout.html" class="nav__dropdown-link">Warehouse Design</a>
              <a href="/rs-solutions-website/services/shelving-systems.html" class="nav__dropdown-link">Shelving</a>
              <a href="/rs-solutions-website/services/warehouse-installation-teardown.html" class="nav__dropdown-link">Installation</a>
              <a href="/rs-solutions-website/services/warehouse-relocation.html" class="nav__dropdown-link">Relocation</a>
              <a href="/rs-solutions-website/services/permitting-engineering.html" class="nav__dropdown-link">Permitting</a>
              <a href="/rs-solutions-website/services/rack-safety-inspections.html" class="nav__dropdown-link">Safety Inspections</a>
            </div>
          </div>
          <div class="nav__dropdown">
            <a href="/rs-solutions-website/industries.html" class="nav__link">Industries</a>
            <div class="nav__dropdown-menu">
              <a href="/rs-solutions-website/industries/3pl-logistics.html" class="nav__dropdown-link">3PL & Logistics</a>
              <a href="/rs-solutions-website/industries/manufacturing.html" class="nav__dropdown-link">Manufacturing</a>
              <a href="/rs-solutions-website/industries/ecommerce.html" class="nav__dropdown-link">E-Commerce</a>
              <a href="/rs-solutions-website/industries/cold-storage.html" class="nav__dropdown-link">Cold Storage</a>
              <a href="/rs-solutions-website/industries/retail.html" class="nav__dropdown-link">Retail</a>
            </div>
          </div>
          <a href="/rs-solutions-website/about.html" class="nav__link">About</a>
          <a href="/rs-solutions-website/resources/faq.html" class="nav__link">FAQ</a>
        </nav>
        <div class="header__actions">
          <button id="lang-toggle" class="header__lang-toggle" aria-label="Switch language">
            <span class="lang-toggle__en">Español</span>
            <span class="lang-toggle__es" style="display:none;">English</span>
          </button>
          <div id="google_translate_element" style="display:none;"></div>
          <a href="/rs-solutions-website/contact.html" class="btn btn--primary hidden lg:block">Get a Quote</a>
        </div>
        <button class="nav-toggle" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>

  <!-- Mobile Nav -->
  <nav class="mobile-nav" id="mobile-nav">
    <a href="/rs-solutions-website/" class="mobile-nav__link">Home</a>
    <a href="/rs-solutions-website/services.html" class="mobile-nav__link">Services</a>
    <a href="/rs-solutions-website/industries.html" class="mobile-nav__link">Industries</a>
    <a href="/rs-solutions-website/about.html" class="mobile-nav__link">About</a>
    <a href="/rs-solutions-website/resources/faq.html" class="mobile-nav__link">FAQ</a>
    <a href="/rs-solutions-website/contact.html" class="mobile-nav__link">Contact</a>
    <div style="padding-top: 1.5rem;">
      <a href="/rs-solutions-website/contact.html" class="btn btn--primary btn--full">Get a Quote</a>
    </div>
    <div style="padding-top: 1rem;">
      <a href="tel:+18337772257" class="btn btn--secondary btn--full">Call (833) 777-2257</a>
    </div>
    <div style="padding-top: 0.5rem;">
      <a href="tel:+14079203747" class="btn btn--ghost btn--full">Sales: (407) 920-3747</a>
    </div>
  </nav>

  <!-- Main Content -->
  <main id="main-content">
{{{{PAGE_CONTENT}}}}
  </main>

  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div class="footer__brand">
          <img src="https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png" alt="Rack Storage Solutions" class="footer__logo" width="180" height="45">
          <p class="footer__tagline">Your trusted partner for warehouse storage solutions. Serving businesses nationwide from Longwood, Florida.</p>
          <div style="margin-top: var(--space-4);">
            <a href="https://youtube.com/racksdirect" target="_blank" rel="noopener" style="color: var(--primary-red); margin-right: var(--space-3);" aria-label="YouTube">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2c-.3-1-1-1.8-2-2.1C19.6 3.5 12 3.5 12 3.5s-7.6 0-9.5.5c-1 .3-1.7 1.1-2 2.1C0 8.2 0 12 0 12s0 3.8.5 5.8c.3 1 1 1.8 2 2.1 1.9.5 9.5.5 9.5.5s7.6 0 9.5-.5c1-.3 1.7-1.1 2-2.1.5-2 .5-5.8.5-5.8s0-3.8-.5-5.8zM9.5 15.5v-7l6.4 3.5-6.4 3.5z"/></svg>
            </a>
            <a href="https://instagram.com/Racksdirect" target="_blank" rel="noopener" style="color: var(--primary-red); margin-right: var(--space-3);" aria-label="Instagram">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.2.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.2.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2-.1-1.2-.1-1.6-.1-4.8s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4 1.2-.1 1.6-.1 4.8-.1M12 0C8.7 0 8.3 0 7.1.1 5.8.1 4.9.3 4.1.6c-.8.3-1.5.7-2.2 1.4C1.2 2.6.8 3.3.5 4.1c-.3.8-.5 1.7-.5 3 0 1.2 0 1.6 0 4.9s0 3.7.1 4.9c.1 1.3.3 2.2.6 3 .3.8.7 1.5 1.4 2.2.7.7 1.4 1.1 2.2 1.4.8.3 1.7.5 3 .6 1.2 0 1.6.1 4.9.1s3.7 0 4.9-.1c1.3-.1 2.2-.3 3-.6.8-.3 1.5-.7 2.2-1.4.7-.7 1.1-1.4 1.4-2.2.3-.8.5-1.7.6-3 0-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.1-1.3-.3-2.2-.6-3-.3-.8-.7-1.5-1.4-2.2-.7-.7-1.4-1.1-2.2-1.4-.8-.3-1.7-.5-3-.6C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-10.9a1.4 1.4 0 1 0 0 2.8 1.4 1.4 0 0 0 0-2.8z"/></svg>
            </a>
            <a href="https://facebook.com/racksdirect" target="_blank" rel="noopener" style="color: var(--primary-red);" aria-label="Facebook">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12c0-6.6-5.4-12-12-12S0 5.4 0 12c0 6 4.4 11 10.1 11.9v-8.4H7.1V12h3v-2.7c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v2.9h-1.5c-1.5 0-2 .9-2 1.9V12h3.3l-.5 3.5h-2.8v8.4C19.6 23 24 18 24 12z"/></svg>
            </a>
          </div>
        </div>
        <div>
          <h3 class="footer__heading">Services</h3>
          <ul class="footer__links">
            <li><a href="/rs-solutions-website/services/heavy-duty-pallet-racking.html" class="footer__link">Pallet Racking</a></li>
            <li><a href="/rs-solutions-website/services/used-pallet-rack.html" class="footer__link">Used Rack</a></li>
            <li><a href="/rs-solutions-website/services/warehouse-design-layout.html" class="footer__link">Warehouse Design</a></li>
            <li><a href="/rs-solutions-website/services/warehouse-installation-teardown.html" class="footer__link">Installation</a></li>
            <li><a href="/rs-solutions-website/services/warehouse-relocation.html" class="footer__link">Relocation</a></li>
          </ul>
        </div>
        <div>
          <h3 class="footer__heading">Company</h3>
          <ul class="footer__links">
            <li><a href="/rs-solutions-website/about.html" class="footer__link">About Us</a></li>
            <li><a href="/rs-solutions-website/industries.html" class="footer__link">Industries</a></li>
            <li><a href="/rs-solutions-website/resources/faq.html" class="footer__link">FAQ</a></li>
            <li><a href="/rs-solutions-website/contact.html" class="footer__link">Contact</a></li>
            <li><a href="/rs-solutions-website/careers.html" class="footer__link">Careers</a></li>
          </ul>
        </div>
        <div>
          <h3 class="footer__heading">Contact Us</h3>
          <div class="footer__contact-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <a href="tel:+18337772257" style="color: inherit;">(833) 777-2257</a><br>
              <small style="color: rgba(255,255,255,0.5);">Toll-Free</small>
            </div>
          </div>
          <div class="footer__contact-item" style="margin-top: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <div>
              <a href="tel:+14079203747" style="color: inherit;">(407) 920-3747</a><br>
              <small style="color: rgba(255,255,255,0.5);">Sales Direct</small>
            </div>
          </div>
          <div class="footer__contact-item" style="margin-top: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            <a href="mailto:Sales@IneedRacks.com" style="color: inherit;">Sales@IneedRacks.com</a>
          </div>
          <div class="footer__contact-item" style="margin-top: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <span>1687 Timocuan Way #113<br>Longwood, FL 32750</span>
          </div>
          <div style="margin-top: 1rem;">
            <a href="/rs-solutions-website/contact.html" class="btn btn--primary btn--full">Request a Quote</a>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <p class="footer__copyright">&copy; 2025 Rack Storage Solutions. All rights reserved.</p>
        <div class="footer__legal">
          <a href="/rs-solutions-website/privacy-policy.html">Privacy Policy</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    (function() {{
      var toggle = document.querySelector('.nav-toggle');
      var mobileNav = document.querySelector('.mobile-nav');
      if (toggle && mobileNav) {{
        toggle.addEventListener('click', function() {{
          var isOpen = mobileNav.classList.toggle('mobile-nav--open');
          toggle.setAttribute('aria-expanded', isOpen);
          document.body.style.overflow = isOpen ? 'hidden' : '';
        }});
      }}
      // FAQ Accordion
      var faqItems = document.querySelectorAll('.faq__item');
      faqItems.forEach(function(item) {{
        var question = item.querySelector('.faq__question');
        if (question) {{
          question.addEventListener('click', function() {{
            faqItems.forEach(function(other) {{
              if (other !== item) other.classList.remove('faq__item--open');
            }});
            item.classList.toggle('faq__item--open');
          }});
        }}
      }});
    }})();
  </script>

  <!-- Anti-Bot Form Protection -->
  <script>
  (function(){{
    'use strict';
    var RS_ANTI_BOT={{
      MIN_FORM_TIME:3000,
      MAX_FORM_TIME:1800000,
      HONEYPOT_FIELD:'website_url',
      pageLoadTime:Date.now(),
      mouseMovements:0,
      keystrokes:0,
      init:function(){{
        var self=this;
        document.addEventListener('mousemove',function(){{self.mouseMovements++}},{{passive:true}});
        document.addEventListener('keydown',function(){{self.keystrokes++}},{{passive:true}});
        this.setupForms();
      }},
      setupForms:function(){{
        var self=this;
        document.querySelectorAll('form').forEach(function(form){{
          if(form.dataset.botProtected)return;
          form.dataset.botProtected='true';
          // Honeypot
          var hp=document.createElement('div');
          hp.style.cssText='position:absolute;left:-9999px;top:-9999px;height:0;width:0;overflow:hidden;';
          hp.innerHTML='<label>Website URL</label><input type="text" name="'+self.HONEYPOT_FIELD+'" tabindex="-1" autocomplete="off">';
          form.appendChild(hp);
          // Timing
          var tf=document.createElement('input');
          tf.type='hidden';tf.name='_form_loaded';tf.value=Date.now().toString();
          form.appendChild(tf);
          // Validate
          form.addEventListener('submit',function(e){{
            var honeypot=form.querySelector('[name="'+self.HONEYPOT_FIELD+'"]');
            if(honeypot&&honeypot.value.length>0){{
              e.preventDefault();
              if(typeof gtag!=='undefined')gtag('event','bot_detected',{{'event_category':'security','event_label':'honeypot'}});
              return false;
            }}
            var lf=form.querySelector('[name="_form_loaded"]');
            if(lf){{
              var ft=Date.now()-parseInt(lf.value,10);
              if(ft<self.MIN_FORM_TIME){{
                e.preventDefault();
                alert('Please take a moment to review your submission.');
                return false;
              }}
            }}
            var js=document.createElement('input');
            js.type='hidden';js.name='_js_verified';js.value='true';
            form.appendChild(js);
          }});
        }});
      }}
    }};
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){{RS_ANTI_BOT.init()}});
    else RS_ANTI_BOT.init();
  }})();
  </script>

  <!-- Attribution Tracking -->
  <script src="/rs-solutions-website/js/attribution.js"></script>

  <!-- Event Tracking -->
  <script src="/rs-solutions-website/js/events.js"></script>

  <!-- Language Toggle -->
  <script type="text/javascript">
    function googleTranslateElementInit() {{
      new google.translate.TranslateElement({{
        pageLanguage: 'en',
        includedLanguages: 'es',
        autoDisplay: false
      }}, 'google_translate_element');
    }}

    (function() {{
      // Check if currently translated to Spanish
      function isSpanish() {{
        var googtrans = document.cookie.match(/googtrans=([^;]+)/);
        return googtrans && googtrans[1].includes('/es');
      }}

      // Update toggle button display
      function updateToggleDisplay() {{
        var enLabel = document.querySelector('.lang-toggle__en');
        var esLabel = document.querySelector('.lang-toggle__es');
        if (enLabel && esLabel) {{
          if (isSpanish()) {{
            enLabel.style.display = 'none';
            esLabel.style.display = 'inline';
          }} else {{
            enLabel.style.display = 'inline';
            esLabel.style.display = 'none';
          }}
        }}
      }}

      // Switch to English
      function switchToEnglish() {{
        // Clear Google Translate cookies
        document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + window.location.hostname;
        document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=' + window.location.hostname;
        // Reload without hash
        window.location.href = window.location.pathname + window.location.search;
      }}

      // Switch to Spanish
      function switchToSpanish() {{
        // Set cookie and trigger Google Translate
        document.cookie = 'googtrans=/en/es; path=/;';
        // Find and click the Spanish option in Google Translate
        var select = document.querySelector('.goog-te-combo');
        if (select) {{
          select.value = 'es';
          select.dispatchEvent(new Event('change'));
        }} else {{
          // If widget not ready, set cookie and reload
          window.location.reload();
        }}
      }}

      // Initialize on DOM ready
      document.addEventListener('DOMContentLoaded', function() {{
        updateToggleDisplay();

        var toggle = document.getElementById('lang-toggle');
        if (toggle) {{
          toggle.addEventListener('click', function() {{
            if (isSpanish()) {{
              switchToEnglish();
            }} else {{
              switchToSpanish();
            }}
          }});
        }}
      }});

      // Also update after a short delay (for Google Translate to load)
      setTimeout(updateToggleDisplay, 1000);
    }})();
  </script>
  <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</body>
</html>'''

def get_lp_template(css_content):
    """Generate the landing page template with minimal header/footer."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{{{PAGE_TITLE}}}} | Rack Storage Solutions</title>
  <meta name="description" content="{{{{META_DESCRIPTION}}}}">
  <link rel="canonical" href="https://simpleleadsads-blip.github.io/rs-solutions-website/{{{{CANONICAL_PATH}}}}">

  <!-- Favicon -->
  <link rel="icon" type="image/png" href="/rs-solutions-website/favicon.png">
  <link rel="apple-touch-icon" href="/rs-solutions-website/favicon.png">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{{{PAGE_TITLE}}}} | Rack Storage Solutions">
  <meta property="og:description" content="{{{{META_DESCRIPTION}}}}">
  <meta property="og:image" content="https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png">

  <!-- Geo Meta Tags -->
  <meta name="geo.region" content="US-FL">
  <meta name="geo.placename" content="Longwood">
  <meta name="geo.position" content="28.7028;-81.3586">
  <meta name="ICBM" content="28.7028, -81.3586">

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <!-- Google Analytics 4 + Google Ads -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XHZ0XZW8L3"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-XHZ0XZW8L3');
    gtag('config', 'AW-17500834233');
  </script>

  <!-- LocalBusiness Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "Rack Storage Solutions",
    "image": "https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png",
    "telephone": "+1-833-777-2257",
    "email": "Sales@IneedRacks.com",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "1687 Timocuan Way Unit 113",
      "addressLocality": "Longwood",
      "addressRegion": "FL",
      "postalCode": "32750",
      "addressCountry": "US"
    }},
    "geo": {{
      "@type": "GeoCoordinates",
      "latitude": 28.7028,
      "longitude": -81.3586
    }},
    "url": "https://www.rackstoragesolutions.com",
    "priceRange": "$$",
    "aggregateRating": {{
      "@type": "AggregateRating",
      "ratingValue": "4.9",
      "reviewCount": "47"
    }},
    "sameAs": [
      "https://youtube.com/racksdirect",
      "https://instagram.com/Racksdirect",
      "https://facebook.com/racksdirect"
    ]
  }}
  </script>

  <style>
{css_content}

/* LP-specific styles */
.lp-header {{
  background: var(--white);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}}
.lp-header__inner {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4) 0;
}}
.lp-header__phone {{
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-weight: var(--font-semibold);
  color: var(--primary-red);
  font-size: var(--text-lg);
}}
.lp-header__phone svg {{
  width: 20px;
  height: 20px;
}}
.lp-footer {{
  background: var(--dark-gray);
  color: var(--white);
  padding: var(--space-8) 0;
  text-align: center;
}}
.lp-footer a {{
  color: rgba(255,255,255,0.7);
}}
.lp-footer a:hover {{
  color: var(--white);
}}
.social-proof-strip {{
  background: var(--light-gray);
  padding: var(--space-4) 0;
}}
.social-proof-strip__inner {{
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--space-6);
}}
.social-proof-item {{
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  color: var(--medium-gray);
}}
.social-proof-item strong {{
  color: var(--dark-gray);
}}
.sticky-form {{
  position: sticky;
  top: 80px;
}}
@media (max-width: 1023px) {{
  .sticky-form {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--white);
    box-shadow: 0 -4px 12px rgba(0,0,0,0.15);
    padding: var(--space-4);
    z-index: 99;
  }}
}}
  </style>
</head>
<body>
  <!-- LP Header - Minimal -->
  <header class="lp-header">
    <div class="container">
      <div class="lp-header__inner">
        <a href="/rs-solutions-website/" class="header__logo">
          <img src="https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png" alt="Rack Storage Solutions" width="180" height="45">
        </a>
        <a href="tel:+18337772257" class="lp-header__phone">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          (833) 777-2257
        </a>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main id="main-content">
{{{{PAGE_CONTENT}}}}
  </main>

  <!-- LP Footer - Minimal -->
  <footer class="lp-footer">
    <div class="container">
      <p style="margin-bottom: var(--space-4);">
        <strong>Rack Storage Solutions</strong><br>
        1687 Timocuan Way #113, Longwood, FL 32750<br>
        <a href="tel:+18337772257">(833) 777-2257</a> | <a href="mailto:Sales@IneedRacks.com">Sales@IneedRacks.com</a>
      </p>
      <p style="font-size: var(--text-sm); color: rgba(255,255,255,0.5);">
        &copy; 2025 Rack Storage Solutions. All rights reserved. | <a href="/rs-solutions-website/privacy-policy.html">Privacy Policy</a>
      </p>
    </div>
  </footer>

  <script>
    // FAQ Accordion
    (function() {{
      var faqItems = document.querySelectorAll('.faq__item');
      faqItems.forEach(function(item) {{
        var question = item.querySelector('.faq__question');
        if (question) {{
          question.addEventListener('click', function() {{
            faqItems.forEach(function(other) {{
              if (other !== item) other.classList.remove('faq__item--open');
            }});
            item.classList.toggle('faq__item--open');
          }});
        }}
      }});
    }})();
  </script>

  <!-- Anti-Bot Form Protection -->
  <script>
  (function(){{
    'use strict';
    var RS_ANTI_BOT={{
      MIN_FORM_TIME:3000,
      HONEYPOT_FIELD:'website_url',
      init:function(){{
        var self=this;
        document.addEventListener('mousemove',function(){{}},{{passive:true}});
        this.setupForms();
      }},
      setupForms:function(){{
        var self=this;
        document.querySelectorAll('form').forEach(function(form){{
          if(form.dataset.botProtected)return;
          form.dataset.botProtected='true';
          var hp=document.createElement('div');
          hp.style.cssText='position:absolute;left:-9999px;';
          hp.innerHTML='<input type="text" name="'+self.HONEYPOT_FIELD+'" tabindex="-1" autocomplete="off">';
          form.appendChild(hp);
          var tf=document.createElement('input');
          tf.type='hidden';tf.name='_form_loaded';tf.value=Date.now().toString();
          form.appendChild(tf);
          form.addEventListener('submit',function(e){{
            var honeypot=form.querySelector('[name="'+self.HONEYPOT_FIELD+'"]');
            if(honeypot&&honeypot.value.length>0){{e.preventDefault();return false;}}
            var lf=form.querySelector('[name="_form_loaded"]');
            if(lf&&(Date.now()-parseInt(lf.value,10))<self.MIN_FORM_TIME){{
              e.preventDefault();alert('Please take a moment to review.');return false;
            }}
          }});
        }});
      }}
    }};
    if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){{RS_ANTI_BOT.init()}});
    else RS_ANTI_BOT.init();
  }})();
  </script>

  <!-- Attribution Tracking -->
  <script src="/rs-solutions-website/js/attribution.js"></script>

  <!-- Event Tracking -->
  <script src="/rs-solutions-website/js/events.js"></script>
</body>
</html>'''

def strip_comments_and_meta(content):
    """Remove HTML comments at the top of content files."""
    # Remove leading HTML comments
    content = re.sub(r'^<!--[\s\S]*?-->\s*', '', content, count=1)
    return content.strip()

def fix_internal_links(content):
    """Prefix internal links with /rs-solutions-website for GitHub Pages."""
    # Fix href="/..." links (but not href="/" alone or external links)
    content = re.sub(r'href="/([^"]+)"', r'href="/rs-solutions-website/\1"', content)
    # Fix href="/" (home link)
    content = re.sub(r'href="/"', r'href="/rs-solutions-website/"', content)
    # Add .html extension to internal links that don't have it (except anchors)
    content = re.sub(r'href="/rs-solutions-website/([^"#]+)(?<!\.html)"', r'href="/rs-solutions-website/\1.html"', content)
    return content

def replace_images(content):
    """Replace local image paths with CDN URLs from image-config.json."""
    def replace_image(match):
        img_path = match.group(1)
        # Look up in IMAGE_MAP
        if img_path in IMAGE_MAP:
            return f'src="{IMAGE_MAP[img_path]}"'
        # Try without leading slash
        if img_path.startswith('/'):
            img_path_no_slash = img_path[1:]
            if img_path_no_slash in IMAGE_MAP:
                return f'src="{IMAGE_MAP[img_path_no_slash]}"'
        # Return original if no match (will show broken image, easy to identify)
        return match.group(0)

    # Replace src="/images/..." patterns
    content = re.sub(r'src="/images/([^"]+)"', lambda m: replace_image_path(m.group(1)), content)
    return content

def replace_image_path(img_path):
    """Get the CDN URL for an image path."""
    if img_path in IMAGE_MAP:
        return f'src="{IMAGE_MAP[img_path]}"'
    # Fallback to a placeholder
    return f'src="https://images.pexels.com/photos/4483608/pexels-photo-4483608.jpeg?auto=compress&cs=tinysrgb&w=600&h=400&fit=crop"'

def build_page(template, source_path, output_path, title, description, css_content):
    """Build a single page."""
    source_full = os.path.join(BASE_DIR, source_path)
    output_full = os.path.join(OUTPUT_DIR, output_path)

    if not os.path.exists(source_full):
        print(f"  WARNING: Source not found: {source_path}")
        return False

    # Read and clean page content
    content = read_file(source_full)
    content = strip_comments_and_meta(content)
    content = fix_internal_links(content)
    content = replace_images(content)

    # Get canonical path (without .html for cleaner URLs)
    canonical = output_path.replace('.html', '') if output_path != 'index.html' else ''

    # Build the page
    html = template.replace('{{PAGE_TITLE}}', title)
    html = html.replace('{{META_DESCRIPTION}}', description)
    html = html.replace('{{CANONICAL_PATH}}', canonical)
    html = html.replace('{{PAGE_CONTENT}}', content)

    # Write output
    write_file(output_full, html)
    print(f"  Built: {output_path}")
    return True

def main():
    print("Building RS Solutions website for GitHub Pages...")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Create subdirectories
    for subdir in ['lp', 'locations', 'services', 'industries', 'resources', 'thank-you', 'js']:
        os.makedirs(os.path.join(OUTPUT_DIR, subdir), exist_ok=True)

    # Read CSS
    css_content = read_file(CSS_FILE)
    print(f"Loaded CSS: {len(css_content)} characters")

    # Get templates
    template = get_template(css_content)
    lp_template = get_lp_template(css_content)

    # Copy JS files to output
    js_dir = os.path.join(BASE_DIR, 'js')
    js_output_dir = os.path.join(OUTPUT_DIR, 'js')
    os.makedirs(js_output_dir, exist_ok=True)
    for js_file in ['attribution.js', 'events.js', 'anti-bot.js']:
        src = os.path.join(js_dir, js_file)
        dst = os.path.join(js_output_dir, js_file)
        if os.path.exists(src):
            content = read_file(src)
            write_file(dst, content)
            print(f"  Copied: js/{js_file}")

    # Build all pages
    print("\nBuilding pages:")
    success = 0
    failed = 0

    for source, output, title, desc in PAGES:
        # Determine which template to use
        if output.startswith('lp/'):
            use_template = lp_template
        else:
            use_template = template

        if build_page(use_template, source, output, title, desc, css_content):
            success += 1
        else:
            failed += 1

    print(f"\nBuild complete: {success} pages built, {failed} failed")
    print(f"\nTo deploy:")
    print(f"1. Go to GitHub repo settings")
    print(f"2. Pages > Source: Deploy from branch")
    print(f"3. Branch: main, folder: /docs")
    print(f"4. Save")

if __name__ == '__main__':
    main()
