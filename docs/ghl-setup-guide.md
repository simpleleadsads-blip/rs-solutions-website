# Go High Level Setup Guide for Rack Storage Solutions

This document provides step-by-step instructions for configuring Go High Level (GHL) to work with the Rack Storage Solutions website.

---

## Table of Contents

1. [Custom Fields Setup](#custom-fields-setup)
2. [Tag Taxonomy](#tag-taxonomy)
3. [Pipeline Configuration](#pipeline-configuration)
4. [Form Setup](#form-setup)
5. [Attribution Tracking Integration](#attribution-tracking-integration)
6. [Automation Workflows](#automation-workflows)

---

## Custom Fields Setup

Create the following custom fields in GHL under **Settings > Custom Fields > Contacts**.

### Attribution Fields (Group: Attribution)

| Field Name | Label | Type | Notes |
|------------|-------|------|-------|
| `utm_source` | UTM Source | Text | google, facebook, bing, etc. |
| `utm_medium` | UTM Medium | Text | cpc, organic, email, etc. |
| `utm_campaign` | UTM Campaign | Text | Campaign name |
| `utm_content` | UTM Content | Text | Ad variation |
| `utm_term` | UTM Term | Text | Keyword |
| `gclid` | Google Click ID | Text | Auto-captured from Google Ads |
| `fbclid` | Facebook Click ID | Text | Auto-captured from Meta ads |
| `landing_page` | Landing Page | Text | First page visited |
| `first_referrer` | First Referrer | Text | Referring domain |
| `traffic_type` | Traffic Type | Dropdown | See options below |
| `conversion_page` | Conversion Page | Text | Page where conversion occurred |

**Traffic Type Options:**
- direct
- organic_search
- paid_search_google
- paid_search_microsoft
- paid_social_meta
- organic_social
- email
- referral

### Sales Fields (Group: Sales)

| Field Name | Label | Type | Options |
|------------|-------|------|---------|
| `service_interest` | Service Interest | Dropdown | pallet_racking, used_rack, warehouse_design, shelving, installation, relocation, permitting, safety_inspection, other |
| `timeline` | Project Timeline | Dropdown | asap, 1_month, 1_3_months, 3_6_months, planning |
| `consultation_type` | Consultation Type | Dropdown | new_warehouse, expansion, optimization, relocation, other |

### Engagement Fields (Group: Engagement)

| Field Name | Label | Type | Notes |
|------------|-------|------|-------|
| `downloaded_resource` | Downloaded Resource | Text | Name of downloaded spec sheet/guide |

### Contact Preferences (Group: Contact Preferences)

| Field Name | Label | Type | Options |
|------------|-------|------|---------|
| `preferred_time` | Preferred Contact Time | Dropdown | morning, afternoon |

---

## Tag Taxonomy

Create the following tags in GHL under **Settings > Tags**.

### Lead Source Tags
- `organic`
- `paid_search`
- `paid_social`
- `referral`
- `direct`

### Service Tags
- `pallet_racking`
- `used_rack`
- `warehouse_design`
- `shelving`
- `installation`
- `relocation`
- `permitting`
- `safety_inspection`

### Engagement Tags
- `quote_request`
- `contact`
- `download`
- `consultation`
- `phone_call`

### Status Tags
- `new_lead`
- `contacted`
- `qualified`
- `quoted`
- `won`
- `lost`

### Industry Tags
- `3pl`
- `manufacturing`
- `ecommerce`
- `cold_storage`
- `retail`
- `other`

---

## Pipeline Configuration

Create a pipeline called **"New Leads"** with the following stages:

| Stage Order | Stage Name | Stage Color |
|-------------|------------|-------------|
| 1 | New Lead | Blue |
| 2 | Contacted | Yellow |
| 3 | Qualified | Orange |
| 4 | Quote Sent | Purple |
| 5 | Negotiating | Pink |
| 6 | Won | Green |
| 7 | Lost | Red |

### Stage Triggers (Optional Automations)
- **New Lead**: Auto-assign to sales rep, send internal notification
- **Contacted**: Start follow-up sequence if no response in 48 hours
- **Quote Sent**: Send quote follow-up email after 3 days
- **Won**: Move to customer pipeline, trigger onboarding

---

## Form Setup

### Form 1: Quote Request Form

**Form Name:** Quote Request Form
**Redirect URL:** /thank-you/quote

**Visible Fields:**
1. First Name (required) → contact.first_name
2. Last Name (required) → contact.last_name
3. Email (required) → contact.email
4. Phone (required) → contact.phone
5. Company Name → contact.company_name
6. What do you need? (dropdown, required) → contact.service_interest
7. Project Details (textarea) → contact.notes
8. Project Timeline (dropdown) → contact.timeline

**Hidden Fields (auto-populated by JavaScript):**
- utm_source → contact.utm_source
- utm_medium → contact.utm_medium
- utm_campaign → contact.utm_campaign
- utm_content → contact.utm_content
- utm_term → contact.utm_term
- gclid → contact.gclid
- fbclid → contact.fbclid
- landing_page → contact.landing_page
- first_referrer → contact.first_referrer
- traffic_type → contact.traffic_type
- conversion_page → contact.conversion_page

**Auto Tags:** quote_request, lead
**Pipeline:** New Leads
**Stage:** New Lead

---

### Form 2: Contact Form

**Form Name:** Contact Form
**Redirect URL:** /thank-you/contact

**Visible Fields:**
1. First Name (required) → contact.first_name
2. Last Name (required) → contact.last_name
3. Email (required) → contact.email
4. Phone (required) → contact.phone
5. Company Name → contact.company_name
6. Message (textarea, required) → contact.notes

**Hidden Fields:** Same as Quote Request Form

**Auto Tags:** contact, lead
**Pipeline:** New Leads
**Stage:** New Lead

---

### Form 3: Spec Sheet Download Form

**Form Name:** Spec Sheet Download Form
**Redirect URL:** /thank-you/download

**Visible Fields:**
1. First Name (required) → contact.first_name
2. Last Name (required) → contact.last_name
3. Work Email (required) → contact.email
4. Company Name (required) → contact.company_name

**Hidden Fields:**
- resource_name → contact.downloaded_resource
- Plus all attribution fields

**Auto Tags:** download, spec_sheet, lead
**Pipeline:** New Leads
**Stage:** Downloaded Resource

---

### Form 4: Consultation Booking Form

**Form Name:** Consultation Booking Form
**Redirect URL:** /thank-you/consultation

**Visible Fields:**
1. First Name (required) → contact.first_name
2. Last Name (required) → contact.last_name
3. Email (required) → contact.email
4. Phone (required) → contact.phone
5. Company Name (required) → contact.company_name
6. What would you like to discuss? (dropdown, required) → contact.consultation_type
7. Preferred Contact Time (dropdown) → contact.preferred_time

**Hidden Fields:** Same as Quote Request Form

**Auto Tags:** consultation, appointment, lead
**Pipeline:** New Leads
**Stage:** Consultation Booked

---

## Attribution Tracking Integration

### How It Works

The website includes JavaScript files (`/js/attribution.js` and `/js/events.js`) that:

1. **Capture UTM parameters and click IDs** on first visit
2. **Store them in cookies** for 90 days
3. **Auto-populate hidden form fields** when forms are loaded
4. **Fire conversion events** to GA4, Google Ads, and Meta Pixel

### Required Setup

#### 1. Add JavaScript to GHL Site Header

In GHL, go to **Sites > [Your Site] > Settings > Tracking Code** and add:

```html
<!-- Attribution Tracking -->
<script src="/js/attribution.js"></script>
<script src="/js/events.js"></script>
```

Or embed the code directly from the provided files.

#### 2. Configure Google Analytics 4

Add your GA4 Measurement ID to the events.js file:

```javascript
// In events.js, update the GA4 config
gtag('config', 'G-XXXXXXXXXX'); // Replace with your GA4 ID
```

#### 3. Configure Google Ads Conversion Tracking

Add your Google Ads conversion IDs:

```javascript
// In events.js, update conversion IDs
'google_ads': {
  'conversion_id': 'AW-XXXXXXXXXX', // Your conversion ID
  'conversion_label': 'XXXXXXXXXX'   // Your conversion label
}
```

#### 4. Configure Meta Pixel

Add your Meta Pixel ID:

```javascript
// In events.js, update Pixel ID
fbq('init', 'XXXXXXXXXXXXXXX'); // Your Pixel ID
```

### Form Integration

GHL forms use dynamic loading. The attribution.js file includes a MutationObserver that watches for GHL form elements and auto-populates hidden fields.

**Important:** Ensure your GHL forms include hidden fields with the correct `name` attributes that match the JavaScript (see Hidden Fields in form configurations above).

---

## Automation Workflows

### Recommended Workflows

#### 1. New Lead Notification
**Trigger:** Contact added to pipeline stage "New Lead"
**Actions:**
- Send internal email notification to sales team
- Send Slack/SMS alert (optional)
- Create task: "Follow up with new lead" (due: 1 hour)

#### 2. Quote Request Auto-Response
**Trigger:** Form submitted (Quote Request Form)
**Actions:**
- Wait 2 minutes
- Send email: "We received your quote request"
- Add tag: quote_request

#### 3. Contact Follow-Up Sequence
**Trigger:** Contact in stage "Contacted" for 48 hours with no activity
**Actions:**
- Send follow-up email
- Wait 3 days
- If no response, send second follow-up
- Wait 5 days
- If no response, create task for phone call

#### 4. Quote Follow-Up
**Trigger:** Contact in stage "Quote Sent" for 3 days
**Actions:**
- Send email: "Did you have questions about your quote?"
- Wait 5 days
- If no response, send second follow-up
- Create task: "Quote follow-up call needed"

#### 5. Won Deal Celebration
**Trigger:** Contact moved to stage "Won"
**Actions:**
- Send internal notification
- Remove from all nurture sequences
- Add to customer list
- Trigger onboarding workflow (optional)

---

## Testing Checklist

Before going live, verify:

- [ ] All custom fields created and mapped correctly
- [ ] All tags created
- [ ] Pipeline and stages configured
- [ ] Each form submits successfully
- [ ] Forms redirect to correct thank-you pages
- [ ] Hidden fields populate with attribution data
- [ ] Leads appear in correct pipeline stage
- [ ] Tags apply automatically
- [ ] Conversion events fire in GA4
- [ ] Google Ads conversions track
- [ ] Meta Pixel fires Lead event
- [ ] Automation workflows trigger correctly

### Test Procedure

1. Clear cookies and visit site with UTM parameters:
   `?utm_source=test&utm_medium=test&utm_campaign=test`
2. Browse a few pages
3. Submit each form type
4. Verify in GHL that:
   - Contact was created
   - All fields populated (including UTM data)
   - Correct tags applied
   - Appears in correct pipeline/stage
5. Check GA4 real-time for conversion event
6. Check Google Ads for conversion
7. Check Meta Events Manager for Lead event

---

## Support

For questions about this setup, contact your development team or refer to:
- [GHL Documentation](https://help.gohighlevel.com/)
- [GA4 Help](https://support.google.com/analytics)
- [Google Ads Help](https://support.google.com/google-ads)
- [Meta Business Help](https://www.facebook.com/business/help)
