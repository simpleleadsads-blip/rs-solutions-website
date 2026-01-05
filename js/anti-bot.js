/**
 * RS Solutions - Anti-Bot Form Protection
 * Prevents automated form submissions from bots and click fraud
 */

(function() {
  'use strict';

  var RS_ANTI_BOT = {
    // Config
    MIN_FORM_TIME: 3000,      // Minimum 3 seconds to fill form (bots are instant)
    MAX_FORM_TIME: 1800000,   // Maximum 30 minutes (session timeout)
    HONEYPOT_FIELD: 'website_url',  // Hidden field name bots will fill

    // State
    pageLoadTime: Date.now(),
    mouseMovements: 0,
    keystrokes: 0,
    scrolled: false,

    init: function() {
      this.trackUserBehavior();
      this.setupForms();
    },

    // Track real human behavior
    trackUserBehavior: function() {
      var self = this;

      document.addEventListener('mousemove', function() {
        self.mouseMovements++;
      }, { passive: true });

      document.addEventListener('keydown', function() {
        self.keystrokes++;
      }, { passive: true });

      document.addEventListener('scroll', function() {
        self.scrolled = true;
      }, { passive: true, once: true });
    },

    // Setup all forms on the page
    setupForms: function() {
      var self = this;
      var forms = document.querySelectorAll('form');

      forms.forEach(function(form) {
        // Skip if already protected
        if (form.dataset.botProtected) return;
        form.dataset.botProtected = 'true';

        // Add honeypot field (hidden from humans, bots fill it)
        self.addHoneypot(form);

        // Add timing field
        self.addTimingField(form);

        // Add validation on submit
        form.addEventListener('submit', function(e) {
          if (!self.validateSubmission(form)) {
            e.preventDefault();
            e.stopPropagation();
            return false;
          }
        });
      });
    },

    // Add honeypot field - hidden via CSS, bots will fill it
    addHoneypot: function(form) {
      // Create container that looks like a real field but is hidden
      var container = document.createElement('div');
      container.style.cssText = 'position:absolute;left:-9999px;top:-9999px;height:0;width:0;overflow:hidden;';
      container.setAttribute('aria-hidden', 'true');

      // Label
      var label = document.createElement('label');
      label.textContent = 'Website URL';
      label.setAttribute('for', this.HONEYPOT_FIELD);

      // Input - bots see this as a normal field and fill it
      var input = document.createElement('input');
      input.type = 'text';
      input.name = this.HONEYPOT_FIELD;
      input.id = this.HONEYPOT_FIELD;
      input.tabIndex = -1;
      input.autocomplete = 'off';

      container.appendChild(label);
      container.appendChild(input);
      form.appendChild(container);
    },

    // Add timing field to track form fill time
    addTimingField: function(form) {
      var input = document.createElement('input');
      input.type = 'hidden';
      input.name = '_form_loaded';
      input.value = Date.now().toString();
      form.appendChild(input);
    },

    // Validate the submission
    validateSubmission: function(form) {
      var issues = [];

      // Check 1: Honeypot filled (bots fill hidden fields)
      var honeypot = form.querySelector('[name="' + this.HONEYPOT_FIELD + '"]');
      if (honeypot && honeypot.value.length > 0) {
        issues.push('honeypot');
        this.logBot('Honeypot filled');
        return false; // Immediate rejection
      }

      // Check 2: Time-based validation
      var loadedField = form.querySelector('[name="_form_loaded"]');
      if (loadedField) {
        var loadTime = parseInt(loadedField.value, 10);
        var fillTime = Date.now() - loadTime;

        if (fillTime < this.MIN_FORM_TIME) {
          issues.push('too_fast');
          this.logBot('Form filled too fast: ' + fillTime + 'ms');
          // Show error to user (might be legitimate fast typer)
          alert('Please take a moment to review your submission before sending.');
          return false;
        }

        if (fillTime > this.MAX_FORM_TIME) {
          issues.push('session_expired');
          // Don't block, just refresh the timestamp
          loadedField.value = Date.now().toString();
        }
      }

      // Check 3: No human interaction detected
      if (this.mouseMovements < 3 && this.keystrokes < 5) {
        issues.push('no_interaction');
        this.logBot('No human interaction detected');
        // Soft check - don't block but flag
      }

      // Check 4: JavaScript-only field (bots without JS won't have this)
      var jsCheck = document.createElement('input');
      jsCheck.type = 'hidden';
      jsCheck.name = '_js_verified';
      jsCheck.value = 'true';
      form.appendChild(jsCheck);

      return issues.length === 0 || !issues.includes('honeypot');
    },

    // Log suspected bot activity (could send to analytics)
    logBot: function(reason) {
      console.warn('[Anti-Bot] Suspected bot activity:', reason);

      // Send to GA4 as event
      if (typeof gtag !== 'undefined') {
        gtag('event', 'bot_detected', {
          'event_category': 'security',
          'event_label': reason
        });
      }
    }
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      RS_ANTI_BOT.init();
    });
  } else {
    RS_ANTI_BOT.init();
  }

  // Expose for debugging
  window.RS_ANTI_BOT = RS_ANTI_BOT;
})();
