#!/usr/bin/env python3
"""
Build script to generate complete HTML pages for GitHub Pages deployment.
Combines base template with page content and inlines CSS.
"""

import os
import re

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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

    # Landing pages
    ('pages/landing/quote.html', 'quote.html', 'Get a Free Quote', 'Request a free pallet racking quote from Rack Storage Solutions.'),
    ('pages/landing/used-rack-inventory.html', 'used-rack-inventory.html', 'Used Rack Inventory', 'Check available used pallet rack inventory.'),
    ('pages/landing/warehouse-design-consultation.html', 'warehouse-design-consultation.html', 'Free Design Consultation', 'Book a free warehouse design consultation.'),
    ('pages/landing/permitting-services.html', 'permitting-services.html', 'Permitting Services', 'Pallet rack permitting services.'),
    ('pages/landing/warehouse-relocation-quote.html', 'warehouse-relocation-quote.html', 'Relocation Quote', 'Get a warehouse relocation quote.'),

    # Thank you pages
    ('pages/thank-you/quote.html', 'thank-you/quote.html', 'Thank You', 'Thank you for your quote request.'),
    ('pages/thank-you/contact.html', 'thank-you/contact.html', 'Thank You', 'Thank you for contacting us.'),
    ('pages/thank-you/consultation.html', 'thank-you/consultation.html', 'Consultation Scheduled', 'Your consultation has been scheduled.'),
    ('pages/thank-you/download.html', 'thank-you/download.html', 'Download Ready', 'Your download is ready.'),
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

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{{{PAGE_TITLE}}}} | Rack Storage Solutions">
  <meta property="og:description" content="{{{{META_DESCRIPTION}}}}">
  <meta property="og:image" content="https://storage.googleapis.com/msgsndr/7FWz2v6LvpUoGO3qQ2Xb/media/695b0f593ccdd60d510ce6a3.png">

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
        <div class="header__cta hidden lg:block">
          <a href="/rs-solutions-website/contact.html" class="btn btn--primary">Get a Quote</a>
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
          <p class="footer__tagline">Your trusted partner for warehouse storage solutions. Serving businesses nationwide.</p>
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
          </ul>
        </div>
        <div>
          <h3 class="footer__heading">Contact Us</h3>
          <div class="footer__contact-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
            <a href="tel:+18337772257" style="color: inherit;">(833) 777-2257</a>
          </div>
          <div style="margin-top: 1rem;">
            <a href="/rs-solutions-website/contact.html" class="btn btn--primary btn--full">Request a Quote</a>
          </div>
        </div>
      </div>
      <div class="footer__bottom">
        <p class="footer__copyright">&copy; 2025 Rack Storage Solutions. All rights reserved.</p>
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

    # Read CSS
    css_content = read_file(CSS_FILE)
    print(f"Loaded CSS: {len(css_content)} characters")

    # Get template
    template = get_template(css_content)

    # Build all pages
    print("\nBuilding pages:")
    success = 0
    failed = 0

    for source, output, title, desc in PAGES:
        if build_page(template, source, output, title, desc, css_content):
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
