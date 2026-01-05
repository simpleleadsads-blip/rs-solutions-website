/**
 * ============================================
 * RACK STORAGE SOLUTIONS - ATTRIBUTION TRACKING
 * ============================================
 *
 * This script handles:
 * - UTM parameter capture and storage
 * - Click ID tracking (gclid, fbclid, msclkid)
 * - Landing page and referrer tracking
 * - Traffic type classification
 * - Hidden form field population
 * - Cross-session attribution (90-day cookie)
 *
 * GHL Compatible | No External Dependencies
 */

(function() {
  'use strict';

  // ===========================================
  // CONFIGURATION
  // ===========================================

  var RS_ATTRIBUTION = {
    // Cookie settings
    cookiePrefix: 'rs_',
    cookieExpiry: 7776000, // 90 days in seconds
    cookiePath: '/',
    cookieSameSite: 'Lax',

    // UTM parameters to track
    utmParams: [
      'utm_source',
      'utm_medium',
      'utm_campaign',
      'utm_content',
      'utm_term'
    ],

    // Click IDs to track
    clickIds: [
      'gclid',    // Google Ads
      'fbclid',   // Facebook/Meta
      'msclkid',  // Microsoft Ads
      'li_fat_id' // LinkedIn
    ],

    // Additional tracking params
    additionalParams: [
      'landing_page',
      'first_referrer',
      'traffic_type',
      'service_interest'
    ]
  };

  // ===========================================
  // UTILITY FUNCTIONS
  // ===========================================

  /**
   * Get URL parameter value
   */
  function getUrlParam(param) {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param) || '';
  }

  /**
   * Set cookie with proper encoding
   */
  function setCookie(name, value, expiry) {
    if (!value) return;

    var cookieString = RS_ATTRIBUTION.cookiePrefix + name + '=' +
                       encodeURIComponent(value) +
                       '; max-age=' + (expiry || RS_ATTRIBUTION.cookieExpiry) +
                       '; path=' + RS_ATTRIBUTION.cookiePath +
                       '; SameSite=' + RS_ATTRIBUTION.cookieSameSite;

    document.cookie = cookieString;
  }

  /**
   * Get cookie value
   */
  function getCookie(name) {
    var fullName = RS_ATTRIBUTION.cookiePrefix + name + '=';
    var cookies = document.cookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.indexOf(fullName) === 0) {
        return decodeURIComponent(cookie.substring(fullName.length));
      }
    }
    return '';
  }

  /**
   * Check if cookie exists
   */
  function hasCookie(name) {
    return getCookie(name) !== '';
  }

  /**
   * Determine traffic type based on source/medium
   */
  function determineTrafficType(source, medium) {
    source = (source || '').toLowerCase();
    medium = (medium || '').toLowerCase();

    // Check for click IDs first
    if (getUrlParam('gclid')) return 'paid_search_google';
    if (getUrlParam('fbclid')) return 'paid_social_meta';
    if (getUrlParam('msclkid')) return 'paid_search_microsoft';

    // Check medium
    if (medium === 'cpc' || medium === 'ppc' || medium === 'paid') {
      return 'paid_search';
    }
    if (medium === 'paid_social' || medium === 'paidsocial') {
      return 'paid_social';
    }
    if (medium === 'email') {
      return 'email';
    }
    if (medium === 'social' || medium === 'organic_social') {
      return 'organic_social';
    }
    if (medium === 'referral') {
      return 'referral';
    }
    if (medium === 'organic') {
      return 'organic_search';
    }

    // Check source for common patterns
    if (source === 'google' || source === 'bing' || source === 'yahoo' || source === 'duckduckgo') {
      return 'organic_search';
    }
    if (source === 'facebook' || source === 'instagram' || source === 'linkedin' || source === 'twitter') {
      return medium === 'cpc' ? 'paid_social' : 'organic_social';
    }

    // Check referrer
    var referrer = document.referrer;
    if (!referrer || referrer.indexOf(window.location.hostname) > -1) {
      return 'direct';
    }

    // Check if referrer is a search engine
    var searchEngines = ['google.', 'bing.', 'yahoo.', 'duckduckgo.', 'baidu.'];
    for (var i = 0; i < searchEngines.length; i++) {
      if (referrer.indexOf(searchEngines[i]) > -1) {
        return 'organic_search';
      }
    }

    return 'referral';
  }

  /**
   * Extract service interest from URL path
   */
  function getServiceInterest() {
    var path = window.location.pathname.toLowerCase();

    var serviceMap = {
      'pallet-racking': 'pallet_racking',
      'heavy-duty': 'pallet_racking',
      'used-rack': 'used_rack',
      'used-pallet': 'used_rack',
      'warehouse-design': 'warehouse_design',
      'layout': 'warehouse_design',
      'shelving': 'shelving_systems',
      'installation': 'installation',
      'teardown': 'installation',
      'relocation': 'relocation',
      'permitting': 'permitting',
      'engineering': 'permitting',
      'safety': 'safety_inspections',
      'inspection': 'safety_inspections'
    };

    for (var key in serviceMap) {
      if (path.indexOf(key) > -1) {
        return serviceMap[key];
      }
    }

    return '';
  }

  // ===========================================
  // MAIN TRACKING FUNCTIONS
  // ===========================================

  /**
   * Capture and store all attribution data
   */
  function captureAttribution() {
    // Capture UTM parameters
    RS_ATTRIBUTION.utmParams.forEach(function(param) {
      var value = getUrlParam(param);
      if (value) {
        setCookie(param, value);
      }
    });

    // Capture click IDs
    RS_ATTRIBUTION.clickIds.forEach(function(param) {
      var value = getUrlParam(param);
      if (value) {
        setCookie(param, value);
      }
    });

    // Capture landing page (only on first visit)
    if (!hasCookie('landing_page')) {
      setCookie('landing_page', window.location.pathname + window.location.search);
    }

    // Capture first referrer (only on first visit)
    if (!hasCookie('first_referrer') && document.referrer) {
      // Don't store if referrer is same domain
      if (document.referrer.indexOf(window.location.hostname) === -1) {
        setCookie('first_referrer', document.referrer);
      }
    }

    // Determine and store traffic type
    var source = getUrlParam('utm_source') || getCookie('utm_source');
    var medium = getUrlParam('utm_medium') || getCookie('utm_medium');
    var trafficType = determineTrafficType(source, medium);

    if (trafficType && !hasCookie('traffic_type')) {
      setCookie('traffic_type', trafficType);
    }

    // Update service interest based on current page
    var serviceInterest = getServiceInterest();
    if (serviceInterest) {
      setCookie('service_interest', serviceInterest);
    }
  }

  /**
   * Get all attribution data as object
   */
  function getAttributionData() {
    var data = {};

    // Get UTM parameters
    RS_ATTRIBUTION.utmParams.forEach(function(param) {
      data[param] = getCookie(param);
    });

    // Get click IDs
    RS_ATTRIBUTION.clickIds.forEach(function(param) {
      data[param] = getCookie(param);
    });

    // Get additional params
    RS_ATTRIBUTION.additionalParams.forEach(function(param) {
      data[param] = getCookie(param);
    });

    // Add current page as conversion page
    data.conversion_page = window.location.pathname;

    return data;
  }

  /**
   * Populate hidden form fields with attribution data
   */
  function populateFormFields() {
    var data = getAttributionData();

    // Find all forms on the page
    var forms = document.querySelectorAll('form');

    forms.forEach(function(form) {
      // Check for hidden fields matching our tracking params
      for (var key in data) {
        if (data[key]) {
          var field = form.querySelector('input[name="' + key + '"], input[name="' + RS_ATTRIBUTION.cookiePrefix + key + '"]');
          if (field) {
            field.value = data[key];
          }
        }
      }
    });
  }

  /**
   * Create hidden input elements for form
   * Call this function to add hidden fields to a specific form
   */
  function createHiddenFields(form) {
    if (!form) return;

    var allParams = RS_ATTRIBUTION.utmParams.concat(
      RS_ATTRIBUTION.clickIds,
      RS_ATTRIBUTION.additionalParams,
      ['conversion_page']
    );

    allParams.forEach(function(param) {
      // Check if field already exists
      if (!form.querySelector('input[name="' + param + '"]')) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = param;
        input.value = getCookie(param) || '';
        form.appendChild(input);
      }
    });

    // Update conversion page to current
    var conversionField = form.querySelector('input[name="conversion_page"]');
    if (conversionField) {
      conversionField.value = window.location.pathname;
    }
  }

  // ===========================================
  // INITIALIZATION
  // ===========================================

  /**
   * Initialize attribution tracking
   */
  function init() {
    // Capture attribution on page load
    captureAttribution();

    // Populate form fields when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        populateFormFields();
      });
    } else {
      populateFormFields();
    }

    // Re-populate on any form that gets dynamically added
    // Use MutationObserver for GHL dynamic forms
    if (typeof MutationObserver !== 'undefined') {
      var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
          if (mutation.addedNodes.length) {
            mutation.addedNodes.forEach(function(node) {
              if (node.tagName === 'FORM') {
                createHiddenFields(node);
                populateFormFields();
              }
              if (node.querySelectorAll) {
                var forms = node.querySelectorAll('form');
                forms.forEach(function(form) {
                  createHiddenFields(form);
                  populateFormFields();
                });
              }
            });
          }
        });
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
    }
  }

  // ===========================================
  // PUBLIC API
  // ===========================================

  window.RSAttribution = {
    init: init,
    capture: captureAttribution,
    getData: getAttributionData,
    populateForms: populateFormFields,
    createHiddenFields: createHiddenFields,
    getCookie: getCookie,
    setCookie: setCookie
  };

  // Auto-initialize
  init();

})();
