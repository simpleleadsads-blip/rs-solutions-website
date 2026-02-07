# RS Solutions Website - Functionality Audit & Testing Checklist

## Quick Summary

### Known Issues to Fix
1. **Meta Pixel ID** - Currently placeholder `XXXXXXXXXXXXXXX` in `/js/events.js:38`
2. **Forms not connected** - Forms have `action="#"` - need GHL webhook URLs
3. **Privacy Policy page** - Links exist but page may not be created
4. **Terms of Service page** - Links exist but page may not be created

---

## SECTION 1: Navigation Testing

### Desktop Navigation
- [ ] Logo links to homepage
- [ ] All main nav links work (Home, Services, Industries, About, FAQ)
- [ ] Services dropdown displays on hover
- [ ] All service dropdown links work (8 links)
- [ ] Industries dropdown displays on hover
- [ ] All industry dropdown links work (5 links)
- [ ] "Get a Quote" button links to contact page
- [ ] Language toggle shows "Español" in English mode
- [ ] Language toggle switches to Spanish properly
- [ ] Language toggle shows "English" in Spanish mode
- [ ] Language toggle switches back to English properly

### Mobile Navigation
- [ ] Hamburger menu icon visible on mobile
- [ ] Hamburger menu opens mobile nav
- [ ] All mobile nav links work
- [ ] Mobile nav closes when link clicked
- [ ] Body scroll locks when nav open
- [ ] "Get a Quote" button works in mobile nav
- [ ] Phone number button works in mobile nav

---

## SECTION 2: Form Testing

### Contact Form (/contact)
- [ ] All required fields show validation
- [ ] Form accepts valid input
- [ ] Anti-bot honeypot field is hidden
- [ ] Form blocks submission under 3 seconds (anti-bot)
- [ ] Form submits successfully
- [ ] Redirects to thank-you page
- [ ] Tracking events fire (check console/network)

### Quote Forms (Landing Pages)
- [ ] LP forms display correctly
- [ ] Required field validation works
- [ ] Service dropdown populates
- [ ] Hidden fields capture page URL
- [ ] Form submission works
- [ ] Tracking fires on submit

### Location Page Forms
- [ ] Form displays in sidebar
- [ ] All fields work
- [ ] Hidden location field populated
- [ ] Submission works

---

## SECTION 3: Click-to-Call Testing

### Phone Links
- [ ] Header phone number clickable
- [ ] Footer phone number clickable
- [ ] Mobile nav phone number clickable
- [ ] Hero CTA phone buttons work
- [ ] Landing page phone numbers work
- [ ] Phone clicks tracked in GA4 (check events)

### Phone Numbers to Verify
- Main: (833) 777-2257
- Sales: (407) 920-3747

---

## SECTION 4: FAQ Accordion Testing

### FAQ Pages
- [ ] FAQ items display collapsed by default
- [ ] Clicking question expands answer
- [ ] Clicking again collapses answer
- [ ] Only one FAQ open at a time
- [ ] FAQ animation smooth
- [ ] Works on mobile

### Pages with FAQs
- /resources/faq
- All service pages (/services/*)
- All location pages (/locations/*)
- All landing pages (/lp/*)

---

## SECTION 5: Tracking & Analytics

### Google Analytics 4 (G-XHZ0XZW8L3)
- [ ] GA4 script loads on all pages
- [ ] Page views tracked
- [ ] Scroll depth events fire (25%, 50%, 75%, 90%)
- [ ] Time on page events fire (30s, 60s, 120s, 300s)
- [ ] Phone click events fire
- [ ] Form submission events fire

### Google Ads (AW-17500834233)
- [ ] Google Ads tag loads
- [ ] Conversion events fire on thank-you pages

### Meta Pixel (NOT CONFIGURED)
- [ ] **ACTION NEEDED:** Add real Meta Pixel ID to events.js
- Current placeholder: `XXXXXXXXXXXXXXX`

### Attribution Tracking
- [ ] UTM parameters captured to cookies
- [ ] Landing page stored in cookie
- [ ] Referrer captured
- [ ] Attribution data passed with form submissions

---

## SECTION 6: Thank-You Pages

### Thank-You Page URLs
- [ ] /thank-you/quote - loads correctly
- [ ] /thank-you/contact - loads correctly
- [ ] /thank-you/consultation - loads correctly
- [ ] /thank-you/download - loads correctly

### Thank-You Page Tracking
- [ ] Conversion event fires on page load
- [ ] Google Ads conversion tracked
- [ ] GA4 event tracked

---

## SECTION 7: Page-Specific Testing

### Homepage
- [ ] Hero section displays correctly
- [ ] Hero CTA buttons work
- [ ] Trust badges visible
- [ ] Services section displays
- [ ] All service cards link correctly
- [ ] Testimonials display (if present)
- [ ] CTA section displays
- [ ] Footer displays correctly

### Service Pages (15 pages)
Test at least one from each category:
- [ ] /services/heavy-duty-pallet-racking
- [ ] /services/used-pallet-rack
- [ ] /services/warehouse-design-layout
- [ ] /garage-storage (new service page)
- [ ] /lift-equipment (new service page)

Check for each:
- [ ] Hero image loads
- [ ] Breadcrumbs show correct path
- [ ] Content sections display
- [ ] FAQ accordion works
- [ ] Schema markup present (view source)

### Landing Pages (15 pages)
Test at least:
- [ ] /lp/pallet-rack (main LP)
- [ ] /lp/pallet-rack-orlando (geo LP)
- [ ] /lp/garage-storage

Check for each:
- [ ] Minimal header (logo + phone only)
- [ ] Hero displays
- [ ] Trust badges visible
- [ ] Form displays and works
- [ ] Social proof section
- [ ] FAQ section
- [ ] Minimal footer
- [ ] No main navigation (by design)

### Location Pages (15 pages)
Test at least:
- [ ] /locations/orlando-fl
- [ ] /locations/atlanta-ga
- [ ] /locations/miami-fl

Check for each:
- [ ] City name in H1
- [ ] Local schema markup
- [ ] Areas served section
- [ ] Industries section (localized)
- [ ] FAQ section (localized)
- [ ] Contact form in sidebar
- [ ] Correct phone numbers

### Careers Page
- [ ] /careers loads correctly
- [ ] Benefits section displays
- [ ] Open positions listed (or placeholder)
- [ ] Application form/contact info present

---

## SECTION 8: SEO & Schema Testing

### Schema Markup (Use Google Rich Results Test)
- [ ] Homepage - Organization schema
- [ ] Service pages - Service schema
- [ ] Location pages - LocalBusiness schema
- [ ] FAQ pages - FAQPage schema

### Meta Tags
Check using View Source or SEO extension:
- [ ] Title tags present and unique
- [ ] Meta descriptions present
- [ ] Open Graph tags present
- [ ] Canonical URLs correct

### Technical SEO
- [ ] All images have alt text
- [ ] Heading hierarchy correct (H1 > H2 > H3)
- [ ] Internal links use relative paths
- [ ] No broken links (use link checker)

---

## SECTION 9: Performance Testing

### Page Speed (Use Google PageSpeed Insights)
- [ ] Mobile score > 70
- [ ] Desktop score > 80
- [ ] Largest Contentful Paint < 2.5s
- [ ] First Input Delay < 100ms
- [ ] Cumulative Layout Shift < 0.1

### Image Optimization
- [ ] Images lazy load below fold
- [ ] Hero images eager load
- [ ] Images have width/height attributes
- [ ] Images compressed appropriately

---

## SECTION 10: Cross-Browser Testing

### Browsers to Test
- [ ] Chrome (latest)
- [ ] Safari (latest)
- [ ] Firefox (latest)
- [ ] Edge (latest)
- [ ] Safari iOS
- [ ] Chrome Android

### Devices to Test
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)
- [ ] Large mobile (414x896)

---

## SECTION 11: Accessibility Testing

### Basic Accessibility
- [ ] Skip to content link works
- [ ] All images have alt text
- [ ] Form labels present
- [ ] Color contrast sufficient
- [ ] Focus indicators visible
- [ ] Keyboard navigation works

### Screen Reader
- [ ] Page structure logical
- [ ] Landmarks present (header, main, footer)
- [ ] Links have descriptive text
- [ ] Form error messages announced

---

## ACTION ITEMS

### High Priority (Before Launch)
1. [ ] Add real Meta Pixel ID to events.js
2. [ ] Connect forms to GHL webhooks
3. [ ] Create privacy policy page
4. [ ] Create terms of service page
5. [ ] Test all forms end-to-end
6. [ ] Verify thank-you page redirects work

### Medium Priority
1. [ ] Replace Pexels stock images with custom photography
2. [ ] Add real customer testimonials
3. [ ] Set up Google Search Console
4. [ ] Submit sitemap to Google

### Low Priority
1. [ ] Add structured data testing to CI/CD
2. [ ] Set up uptime monitoring
3. [ ] Configure CDN for images
4. [ ] Implement image lazy loading for all pages

---

## Testing Tools

### Recommended Tools
- **Google PageSpeed Insights** - Performance testing
- **Google Rich Results Test** - Schema validation
- **Google Search Console** - SEO issues
- **WAVE Browser Extension** - Accessibility
- **Lighthouse** - Comprehensive audit
- **BrowserStack** - Cross-browser testing
- **Screaming Frog** - Link checking & SEO crawl

### Browser DevTools
- **Network tab** - Check script loading, API calls
- **Console** - Check for JS errors
- **Elements** - Inspect markup
- **Application** - Check cookies, storage

---

## Notes

_Use this space for testing notes and observations:_

```
Date: ___________
Tester: ___________

Observations:


Issues Found:


```
