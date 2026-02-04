# Rack Storage Solutions - Website Specification

## Overview
Complete website specification for Rack Storage Solutions, a nationwide warehouse storage provider based in Longwood, FL.

---

## Brand Colors

```css
:root {
  /* Primary - Red Brand */
  --primary-red: #E63946;
  --primary-red-hover: #C5303C;
  --primary-red-light: rgba(230, 57, 70, 0.1);

  /* Neutrals */
  --black: #000000;
  --white: #FFFFFF;
  --dark-gray: #333333;
  --medium-gray: #666666;
  --light-gray: #F5F5F5;
  --border-gray: #E0E0E0;
}
```

---

## Contact Information

```
Company: Rack Storage Solutions
Address: 1687 Timocuan Way Unit 113, Longwood, FL 32750
Geo Coordinates: 28.7028, -81.3586

Phone Numbers:
- Sales: (407) 920-3747
- Toll-Free: (833) 777-2257
- Spanish Line: (833) 777-2257

Email Addresses:
- Sales@IneedRacks.com
- Matt@Racks-R-Us.com
- Info@IneedRacks.com

Social Media:
- YouTube: youtube.com/racksdirect
- Instagram: instagram.com/Racksdirect
- Facebook: facebook.com/racksdirect

Google Business: https://share.google/kUeKg45Ts1cGdDkrX
```

---

## Site Architecture

### Core Pages
- `/` - Home
- `/about` - About Us
- `/contact` - Contact
- `/services` - Services Hub
- `/industries` - Industries Hub
- `/nationwide-service` - Nationwide Coverage
- `/careers` - Careers

### Service Pages (`/services/`)
- `/services/heavy-duty-pallet-racking`
- `/services/used-pallet-rack`
- `/services/warehouse-design-layout`
- `/services/shelving-systems`
- `/services/warehouse-installation-teardown`
- `/services/warehouse-relocation`
- `/services/permitting-engineering`
- `/services/rack-safety-inspections`
- `/garage-storage` (NEW)
- `/lockers` (NEW)
- `/lift-equipment` (NEW)
- `/warehouse-safety` (NEW)
- `/containment-fencing` (NEW)
- `/rack-protection` (NEW)
- `/labeling-services` (NEW)

### Industry Pages (`/industries/`)
- `/industries/3pl-logistics`
- `/industries/manufacturing`
- `/industries/ecommerce`
- `/industries/cold-storage`
- `/industries/retail`

### Landing Pages (`/lp/`)

#### Service Landing Pages
- `/lp/pallet-rack`
- `/lp/used-pallet-rack`
- `/lp/warehouse-racking`
- `/lp/heavy-duty-rack`
- `/lp/garage-storage`
- `/lp/shelving`
- `/lp/warehouse-design`
- `/lp/warehouse-relocation`
- `/lp/rack-installation`
- `/lp/local-pickup`

#### Geo-Targeted Landing Pages
- `/lp/pallet-rack-orlando`
- `/lp/pallet-rack-tampa`
- `/lp/pallet-rack-jacksonville`
- `/lp/pallet-rack-atlanta`
- `/lp/pallet-rack-miami`

### Location Pages (`/locations/`)
- `/locations/orlando-fl`
- `/locations/tampa-fl`
- `/locations/jacksonville-fl`
- `/locations/miami-fl`
- `/locations/atlanta-ga`
- `/locations/savannah-ga`
- `/locations/charlotte-nc`
- `/locations/nashville-tn`
- `/locations/birmingham-al`
- `/locations/memphis-tn`
- `/locations/columbia-sc`
- `/locations/charleston-sc`
- `/locations/richmond-va`
- `/locations/raleigh-nc`
- `/locations/new-orleans-la`

### Resource Pages
- `/resources/faq`
- `/resources/how-it-works`
- `/resources/glossary`
- `/resources/safety-compliance`
- `/resources/new-vs-used-pallet-rack`
- `/resources/racking-types-comparison`
- `/resources/when-you-need-permits`
- `/resources/calculator` (NEW - Interactive)

### Thank You Pages
- `/thank-you/quote`
- `/thank-you/contact`
- `/thank-you/consultation`
- `/thank-you/download`

---

## Landing Page Template Structure

Landing pages use a minimal, conversion-focused layout:

```
[HEADER - Minimal]
- Logo (left)
- Phone number with click-to-call (right)
- NO navigation menu

[HERO SECTION]
- Headline with keyword
- Sub-headline addressing pain point
- Hero image
- Primary CTA button
- Trust badges (4.9 stars, etc.)

[SOCIAL PROOF STRIP]
- Star rating: 4.9/5
- Reviews: 47 reviews
- Customers served: 5,000+
- Service area: Nationwide

[BENEFITS SECTION]
- 3-4 key benefits with icons

[FORM SECTION]
- Above the fold on desktop
- Sticky on mobile
- Multi-step or single form

[TESTIMONIALS]
- 2-3 customer testimonials
- Name, title, company

[FAQ SECTION]
- 4-6 FAQs with FAQPage schema markup

[FINAL CTA SECTION]
- Phone number prominent
- Form repeat

[FOOTER - Minimal]
- Company info, phone, address
- Privacy policy link only
```

---

## Form Configuration

### Initial Form (Visible Fields)
| Field | Type | Required |
|-------|------|----------|
| Name | text | Yes |
| Phone | tel | Yes |
| Email | email | Yes |
| What do you need? | dropdown | Yes |

### "What do you need?" Options
- Pallet Racking (New)
- Used Pallet Rack
- Warehouse Design & Layout
- Shelving Systems
- Installation / Teardown
- Warehouse Relocation
- Permitting & Engineering
- Rack Safety Inspection
- Garage Storage
- Other / General Inquiry

### Step 2 / Optional Fields
| Field | Type | Required |
|-------|------|----------|
| Company Name | text | No |
| Warehouse Size (sq ft) | dropdown | No |
| Timeline | dropdown | No |
| Zip Code | text | No |
| Message/Details | textarea | No |

### Warehouse Size Options
- Under 5,000 sq ft
- 5,000 - 10,000 sq ft
- 10,000 - 25,000 sq ft
- 25,000 - 50,000 sq ft
- 50,000 - 100,000 sq ft
- Over 100,000 sq ft

### Timeline Options
- ASAP / Urgent
- Within 1 month
- 1-3 months
- 3-6 months
- Just planning / researching

### Hidden Attribution Fields
- utm_source
- utm_medium
- utm_campaign
- utm_content
- utm_term
- gclid
- fbclid
- landing_page
- first_referrer
- traffic_type
- conversion_page

---

## Tracking Configuration

### Current (Keep)
- GA4: `G-XHZ0XZW8L3`
- Google Ads: `AW-17500834233`

### Scripts to Activate
- `/js/attribution.js` - UTM & click ID tracking
- `/js/events.js` - Conversion events
- `/js/anti-bot.js` - Form protection

### To Add
- GTM Container (need ID)
- Meta Pixel (need ID from client)

### Data Layer Events
```javascript
// Lead submission
dataLayer.push({
  'event': 'generate_lead',
  'form_type': 'quote_request',
  'service_interest': 'pallet_racking',
  'utm_source': '...',
  'utm_medium': '...'
});

// Phone click
dataLayer.push({
  'event': 'click',
  'event_category': 'engagement',
  'event_label': 'phone_call'
});
```

---

## SEO / Schema Requirements

### Meta Tags (All Pages)
```html
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Longwood">
<meta name="geo.position" content="28.7028;-81.3586">
<meta name="ICBM" content="28.7028, -81.3586">
```

### LocalBusiness Schema
```json
{
  "@type": "LocalBusiness",
  "name": "Rack Storage Solutions",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "1687 Timocuan Way Unit 113",
    "addressLocality": "Longwood",
    "addressRegion": "FL",
    "postalCode": "32750",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 28.7028,
    "longitude": -81.3586
  },
  "telephone": "+1-833-777-2257",
  "priceRange": "$$",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "47"
  }
}
```

### Organization Schema (sameAs)
```json
{
  "sameAs": [
    "https://youtube.com/racksdirect",
    "https://instagram.com/Racksdirect",
    "https://facebook.com/racksdirect"
  ]
}
```

### FAQPage Schema
Every page with FAQs must include FAQPage schema markup.

---

## Spanish Translation

Add Google Translate widget to header:
```html
<div id="google_translate_element" class="header__translate">
  <span>Español</span>
</div>
<script type="text/javascript">
  function googleTranslateElementInit() {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'es',
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
  }
</script>
<script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
```

---

## Outstanding Items (Client Input Needed)

1. **Meta Pixel ID** - Currently placeholder `XXXXXXXXXXXXXXX`
2. **GTM Container ID** - Create new or use existing?
3. **GHL Webhook URLs** - For form submissions
4. **Team photos** - For about page updates
5. **Testimonial content** - Names/companies for LP testimonials

---

## File Structure

```
/
├── build.py                    # Build script
├── PROJECT-SPEC.md             # This file
├── css/
│   └── brand.css               # All styles
├── js/
│   ├── attribution.js          # UTM tracking
│   ├── events.js               # Event tracking
│   └── anti-bot.js             # Bot protection
├── config/
│   └── form-configurations.json
├── schema/
│   ├── organization.json
│   ├── website.json
│   └── ...
├── templates/
│   ├── base-template.html      # Main site template
│   ├── lp-template.html        # Landing page template (NEW)
│   └── location-template.html  # Location page template (NEW)
├── pages/
│   ├── core/                   # Home, about, contact, etc.
│   ├── services/               # Service pages
│   ├── industries/             # Industry pages
│   ├── landing/                # Existing landing pages
│   ├── lp/                     # NEW landing pages
│   ├── locations/              # NEW location pages
│   ├── authority/              # FAQ, glossary, etc.
│   ├── resources/              # Guides, comparisons
│   └── thank-you/              # Confirmation pages
└── docs/                       # Built output (GitHub Pages)
```

---

## Build Commands

```bash
# Build all pages
python3 build.py

# Deploy (via GitHub Pages from /docs)
git add . && git commit -m "Update site" && git push
```

---

*Last Updated: February 2026*
