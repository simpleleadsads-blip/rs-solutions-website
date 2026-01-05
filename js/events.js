/**
 * ============================================
 * RACK STORAGE SOLUTIONS - EVENT TRACKING
 * ============================================
 *
 * This script handles:
 * - Conversion event tracking
 * - GA4 event pushing
 * - Google Ads conversion tracking
 * - Meta (Facebook) Pixel events
 * - Custom event dispatching
 *
 * GHL Compatible | No External Dependencies
 */

(function() {
  'use strict';

  // ===========================================
  // CONFIGURATION
  // ===========================================

  var RS_EVENTS = {
    // Google Ads Conversion IDs
    googleAds: {
      conversionId: 'AW-17500834233', // Form Fill Conversion
      conversionLabels: {
        lead_submit: 'tWZPCIWe7NwbELmThplB',
        quote_request: 'tWZPCIWe7NwbELmThplB',
        contact_submit: 'tWZPCIWe7NwbELmThplB',
        download_submit: 'tWZPCIWe7NwbELmThplB',
        call_click: 'tWZPCIWe7NwbELmThplB',
        calendar_booked: 'tWZPCIWe7NwbELmThplB'
      }
    },

    // Meta Pixel ID (replace with actual value)
    metaPixelId: 'XXXXXXXXXXXXXXX', // Replace with actual Pixel ID

    // Debug mode (set to false in production)
    debug: false
  };

  // ===========================================
  // UTILITY FUNCTIONS
  // ===========================================

  /**
   * Log debug messages
   */
  function log(message, data) {
    if (RS_EVENTS.debug) {
      console.log('[RS Events]', message, data || '');
    }
  }

  /**
   * Get attribution data from cookies
   */
  function getAttributionData() {
    if (window.RSAttribution && typeof window.RSAttribution.getData === 'function') {
      return window.RSAttribution.getData();
    }
    return {};
  }

  /**
   * Check if Google Analytics 4 is loaded
   */
  function hasGA4() {
    return typeof gtag === 'function';
  }

  /**
   * Check if Google Ads gtag is loaded
   */
  function hasGoogleAds() {
    return typeof gtag === 'function';
  }

  /**
   * Check if Meta Pixel is loaded
   */
  function hasMetaPixel() {
    return typeof fbq === 'function';
  }

  // ===========================================
  // EVENT TRACKING FUNCTIONS
  // ===========================================

  /**
   * Track event in GA4
   */
  function trackGA4Event(eventName, eventParams) {
    if (!hasGA4()) {
      log('GA4 not loaded, skipping event:', eventName);
      return;
    }

    var params = Object.assign({}, eventParams, getAttributionData());

    gtag('event', eventName, params);
    log('GA4 event tracked:', { event: eventName, params: params });
  }

  /**
   * Track Google Ads conversion
   */
  function trackGoogleAdsConversion(eventType, value, currency) {
    if (!hasGoogleAds()) {
      log('Google Ads not loaded, skipping conversion:', eventType);
      return;
    }

    var label = RS_EVENTS.googleAds.conversionLabels[eventType];
    if (!label) {
      log('No conversion label found for:', eventType);
      return;
    }

    var conversionData = {
      'send_to': RS_EVENTS.googleAds.conversionId + '/' + label
    };

    if (value) {
      conversionData.value = value;
      conversionData.currency = currency || 'USD';
    }

    gtag('event', 'conversion', conversionData);
    log('Google Ads conversion tracked:', { eventType: eventType, data: conversionData });
  }

  /**
   * Track Meta Pixel event
   */
  function trackMetaEvent(eventName, eventParams) {
    if (!hasMetaPixel()) {
      log('Meta Pixel not loaded, skipping event:', eventName);
      return;
    }

    var params = Object.assign({}, eventParams, {
      content_category: 'Warehouse Storage Solutions'
    });

    fbq('track', eventName, params);
    log('Meta event tracked:', { event: eventName, params: params });
  }

  /**
   * Dispatch custom DOM event
   */
  function dispatchCustomEvent(eventName, detail) {
    var event = new CustomEvent('rs_' + eventName, {
      detail: Object.assign({}, detail, getAttributionData()),
      bubbles: true
    });
    document.dispatchEvent(event);
    log('Custom event dispatched:', 'rs_' + eventName);
  }

  // ===========================================
  // MAIN EVENT FUNCTIONS
  // ===========================================

  /**
   * Track lead submission
   */
  function trackLeadSubmit(formType, serviceInterest) {
    var eventName = 'lead_submit';
    var params = {
      form_type: formType || 'general',
      service_interest: serviceInterest || '',
      page_url: window.location.href,
      page_title: document.title
    };

    // GA4
    trackGA4Event('generate_lead', params);

    // Google Ads
    trackGoogleAdsConversion(eventName);

    // Meta - Lead event
    trackMetaEvent('Lead', {
      content_name: formType || 'Lead Form',
      content_category: serviceInterest || 'General'
    });

    // Custom event
    dispatchCustomEvent(eventName, params);
  }

  /**
   * Track quote request
   */
  function trackQuoteRequest(serviceType, estimatedValue) {
    var eventName = 'quote_request';
    var params = {
      service_type: serviceType || 'general',
      estimated_value: estimatedValue || 0,
      page_url: window.location.href
    };

    // GA4
    trackGA4Event('request_quote', params);

    // Google Ads with value
    trackGoogleAdsConversion(eventName, estimatedValue);

    // Meta - Lead event with higher intent
    trackMetaEvent('Lead', {
      content_name: 'Quote Request',
      content_category: serviceType || 'General',
      value: estimatedValue || 0,
      currency: 'USD'
    });

    // Custom event
    dispatchCustomEvent(eventName, params);
  }

  /**
   * Track contact form submission
   */
  function trackContactSubmit(inquiryType) {
    var eventName = 'contact_submit';
    var params = {
      inquiry_type: inquiryType || 'general',
      page_url: window.location.href
    };

    // GA4
    trackGA4Event('contact', params);

    // Google Ads
    trackGoogleAdsConversion(eventName);

    // Meta
    trackMetaEvent('Contact', {
      content_name: 'Contact Form',
      content_category: inquiryType || 'General'
    });

    // Custom event
    dispatchCustomEvent(eventName, params);
  }

  /**
   * Track spec sheet / resource download
   */
  function trackDownload(resourceName, resourceType) {
    var eventName = 'download_submit';
    var params = {
      resource_name: resourceName || '',
      resource_type: resourceType || 'spec_sheet',
      page_url: window.location.href
    };

    // GA4
    trackGA4Event('file_download', params);

    // Google Ads
    trackGoogleAdsConversion(eventName);

    // Meta - CompleteRegistration for gated content
    trackMetaEvent('CompleteRegistration', {
      content_name: resourceName || 'Resource Download',
      content_category: resourceType || 'Spec Sheet'
    });

    // Custom event
    dispatchCustomEvent(eventName, params);
  }

  /**
   * Track phone call click
   */
  function trackCallClick(phoneNumber) {
    var eventName = 'call_click';
    var params = {
      phone_number: phoneNumber || '',
      page_url: window.location.href,
      click_location: 'page'
    };

    // GA4
    trackGA4Event('click', {
      event_category: 'engagement',
      event_label: 'phone_call',
      phone_number: phoneNumber
    });

    // Google Ads
    trackGoogleAdsConversion(eventName);

    // Meta
    trackMetaEvent('Contact', {
      content_name: 'Phone Call Click',
      content_category: 'Phone'
    });

    // Custom event
    dispatchCustomEvent(eventName, params);
  }

  /**
   * Track calendar booking
   */
  function trackCalendarBooked(appointmentType, appointmentDate) {
    var eventName = 'calendar_booked';
    var params = {
      appointment_type: appointmentType || 'consultation',
      appointment_date: appointmentDate || '',
      page_url: window.location.href
    };

    // GA4
    trackGA4Event('schedule_appointment', params);

    // Google Ads
    trackGoogleAdsConversion(eventName);

    // Meta - Schedule event
    trackMetaEvent('Schedule', {
      content_name: appointmentType || 'Consultation',
      content_category: 'Appointment'
    });

    // Custom event
    dispatchCustomEvent(eventName, params);
  }

  /**
   * Track page engagement events
   */
  function trackEngagement(action, label, value) {
    var params = {
      event_category: 'engagement',
      event_label: label || '',
      value: value || 0,
      page_url: window.location.href
    };

    trackGA4Event(action, params);
    dispatchCustomEvent('engagement', params);
  }

  // ===========================================
  // SERVICE-SPECIFIC EVENT WRAPPERS
  // ===========================================

  /**
   * Track service-specific quote requests
   */
  var serviceQuotes = {
    palletRacking: function(value) {
      trackQuoteRequest('pallet_racking', value);
      trackGA4Event('quote_request_pallet_racking', { estimated_value: value });
    },
    usedRack: function(value) {
      trackQuoteRequest('used_rack', value);
      trackGA4Event('quote_request_used_rack', { estimated_value: value });
    },
    warehouseDesign: function(value) {
      trackQuoteRequest('warehouse_design', value);
      trackGA4Event('quote_request_warehouse_design', { estimated_value: value });
    },
    shelving: function(value) {
      trackQuoteRequest('shelving_systems', value);
      trackGA4Event('quote_request_shelving', { estimated_value: value });
    },
    installation: function(value) {
      trackQuoteRequest('installation', value);
      trackGA4Event('quote_request_installation', { estimated_value: value });
    },
    relocation: function(value) {
      trackQuoteRequest('relocation', value);
      trackGA4Event('quote_request_relocation', { estimated_value: value });
    },
    permitting: function(value) {
      trackQuoteRequest('permitting', value);
      trackGA4Event('quote_request_permitting', { estimated_value: value });
    },
    safetyInspection: function(value) {
      trackQuoteRequest('safety_inspection', value);
      trackGA4Event('quote_request_safety_inspection', { estimated_value: value });
    }
  };

  // ===========================================
  // AUTO-TRACKING SETUP
  // ===========================================

  /**
   * Set up automatic click tracking for phone links
   */
  function setupPhoneTracking() {
    document.addEventListener('click', function(e) {
      var target = e.target.closest('a[href^="tel:"]');
      if (target) {
        var phoneNumber = target.getAttribute('href').replace('tel:', '');
        trackCallClick(phoneNumber);
      }
    });
    log('Phone click tracking initialized');
  }

  /**
   * Set up scroll depth tracking
   */
  function setupScrollTracking() {
    var scrollThresholds = [25, 50, 75, 90];
    var triggered = {};

    window.addEventListener('scroll', function() {
      var scrollPercent = Math.round(
        (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
      );

      scrollThresholds.forEach(function(threshold) {
        if (scrollPercent >= threshold && !triggered[threshold]) {
          triggered[threshold] = true;
          trackEngagement('scroll', 'scroll_depth_' + threshold, threshold);
        }
      });
    }, { passive: true });

    log('Scroll tracking initialized');
  }

  /**
   * Set up time on page tracking
   */
  function setupTimeTracking() {
    var timeThresholds = [30, 60, 120, 300]; // seconds
    var startTime = Date.now();

    timeThresholds.forEach(function(seconds) {
      setTimeout(function() {
        trackEngagement('time_on_page', 'engaged_' + seconds + 's', seconds);
      }, seconds * 1000);
    });

    log('Time on page tracking initialized');
  }

  // ===========================================
  // THANK YOU PAGE DETECTION
  // ===========================================

  /**
   * Auto-fire events on thank you pages
   */
  function handleThankYouPage() {
    var path = window.location.pathname.toLowerCase();

    // Map thank you page paths to events
    var thankYouPages = {
      '/thank-you/quote': function() { trackQuoteRequest('general'); },
      '/thank-you/contact': function() { trackContactSubmit('general'); },
      '/thank-you/download': function() { trackDownload('spec_sheet', 'pdf'); },
      '/thank-you/consultation': function() { trackCalendarBooked('consultation'); },
      '/thank-you/pallet-racking': function() { serviceQuotes.palletRacking(); },
      '/thank-you/used-rack': function() { serviceQuotes.usedRack(); },
      '/thank-you/warehouse-design': function() { serviceQuotes.warehouseDesign(); },
      '/thank-you/relocation': function() { serviceQuotes.relocation(); },
      '/thank-you/permitting': function() { serviceQuotes.permitting(); }
    };

    for (var pagePath in thankYouPages) {
      if (path.indexOf(pagePath) > -1) {
        log('Thank you page detected:', pagePath);
        thankYouPages[pagePath]();
        break;
      }
    }
  }

  // ===========================================
  // INITIALIZATION
  // ===========================================

  /**
   * Initialize event tracking
   */
  function init() {
    // Set up automatic tracking
    setupPhoneTracking();
    setupScrollTracking();
    setupTimeTracking();

    // Check for thank you page
    handleThankYouPage();

    log('RS Events initialized');
  }

  // ===========================================
  // PUBLIC API
  // ===========================================

  window.RSEvents = {
    // Core tracking functions
    trackLeadSubmit: trackLeadSubmit,
    trackQuoteRequest: trackQuoteRequest,
    trackContactSubmit: trackContactSubmit,
    trackDownload: trackDownload,
    trackCallClick: trackCallClick,
    trackCalendarBooked: trackCalendarBooked,
    trackEngagement: trackEngagement,

    // Service-specific tracking
    serviceQuotes: serviceQuotes,

    // Utility
    init: init,
    log: log
  };

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();


/**
 * ============================================
 * USAGE EXAMPLES
 * ============================================
 *
 * // Track a general lead submission
 * RSEvents.trackLeadSubmit('contact_form', 'pallet_racking');
 *
 * // Track a quote request with estimated value
 * RSEvents.trackQuoteRequest('warehouse_design', 15000);
 *
 * // Track service-specific quote
 * RSEvents.serviceQuotes.palletRacking(25000);
 * RSEvents.serviceQuotes.usedRack(8000);
 *
 * // Track a download
 * RSEvents.trackDownload('Pallet Rack Spec Sheet', 'pdf');
 *
 * // Track consultation booking
 * RSEvents.trackCalendarBooked('warehouse_consultation', '2024-03-15');
 *
 * // Track custom engagement
 * RSEvents.trackEngagement('video_play', 'installation_overview', 1);
 */
