// Job Autofill Extension Content Script
class JobAutofillContentScript {
  constructor() {
    this.settings = {
      autoDetect: true,
      smartSuggestions: true
    };
    this.fieldMappings = new Map();
    this.detectedFields = [];
    
    this.initialize();
  }

  async initialize() {
    // Load settings
    try {
      const result = await chrome.storage.local.get(['settings']);
      this.settings = { ...this.settings, ...result.settings };
    } catch (error) {
      console.log('Failed to load settings:', error);
    }

    // Set up message listener
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message, sender, sendResponse);
      return true; // Keep message channel open for async responses
    });

    // Auto-detect forms if enabled
    if (this.settings.autoDetect) {
      this.detectFormsOnLoad();
    }

    // Monitor for dynamic form changes
    this.observeFormChanges();
  }

  handleMessage(message, sender, sendResponse) {
    switch (message.action) {
      case 'fillForm':
        this.fillForm(message.profileData).then(result => {
          sendResponse(result);
        });
        break;
      
      case 'detectFields':
        const fields = this.detectFormFields();
        sendResponse({ fields: fields });
        break;
      
      case 'extractFormData':
        const formData = this.extractFormData();
        sendResponse({ formData: formData });
        break;
      
      case 'updateSettings':
        this.settings = { ...this.settings, ...message.settings };
        sendResponse({ success: true });
        break;
      
      default:
        sendResponse({ error: 'Unknown action' });
    }
  }

  detectFormsOnLoad() {
    // Wait for page to be fully loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => {
        setTimeout(() => this.detectFormFields(), 1000);
      });
    } else {
      setTimeout(() => this.detectFormFields(), 1000);
    }
  }

  observeFormChanges() {
    const observer = new MutationObserver((mutations) => {
      let shouldRedetect = false;
      
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === 1) { // Element node
            if (node.tagName === 'FORM' || node.querySelector('form')) {
              shouldRedetect = true;
            }
          }
        });
      });

      if (shouldRedetect && this.settings.autoDetect) {
        setTimeout(() => this.detectFormFields(), 500);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  detectFormFields() {
    const forms = document.querySelectorAll('form');
    this.detectedFields = [];
    this.fieldMappings.clear();

    forms.forEach((form, formIndex) => {
      const fields = this.analyzeForm(form, formIndex);
      this.detectedFields.push(...fields);
    });

    // Also check for standalone input fields (not in forms)
    const standaloneInputs = document.querySelectorAll('input:not(form input), select:not(form select), textarea:not(form textarea)');
    standaloneInputs.forEach((input, index) => {
      const field = this.analyzeField(input, -1, index);
      if (field) {
        this.detectedFields.push(field);
      }
    });

    console.log(`Detected ${this.detectedFields.length} form fields`);
    return this.detectedFields;
  }

  analyzeForm(form, formIndex) {
    const fields = [];
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach((input, inputIndex) => {
      const field = this.analyzeField(input, formIndex, inputIndex);
      if (field) {
        fields.push(field);
      }
    });

    return fields;
  }

  analyzeField(input, formIndex, inputIndex) {
    // Skip hidden, submit, and button inputs
    if (input.type === 'hidden' || input.type === 'submit' || input.type === 'button') {
      return null;
    }

    const field = {
      element: input,
      formIndex,
      inputIndex,
      type: input.type || input.tagName.toLowerCase(),
      name: input.name || '',
      id: input.id || '',
      placeholder: input.placeholder || '',
      label: this.findFieldLabel(input),
      required: input.required || false,
      category: this.categorizeField(input)
    };

    // Create unique selector for the field
    field.selector = this.createFieldSelector(input);
    
    // Map field to data category
    this.fieldMappings.set(field.selector, field.category);

    return field;
  }

  findFieldLabel(input) {
    // Method 1: Associated label element
    if (input.id) {
      const label = document.querySelector(`label[for="${input.id}"]`);
      if (label) return label.textContent.trim();
    }

    // Method 2: Parent label
    const parentLabel = input.closest('label');
    if (parentLabel) {
      return parentLabel.textContent.replace(input.value || '', '').trim();
    }

    // Method 3: Previous sibling text
    let sibling = input.previousElementSibling;
    while (sibling) {
      if (sibling.tagName === 'LABEL' || sibling.textContent.trim()) {
        return sibling.textContent.trim();
      }
      sibling = sibling.previousElementSibling;
    }

    // Method 4: Closest text content
    const parent = input.parentElement;
    if (parent) {
      const text = parent.textContent.replace(input.value || '', '').trim();
      if (text.length < 100) return text;
    }

    return '';
  }

  categorizeField(input) {
    const text = (
      (input.name || '') + ' ' +
      (input.id || '') + ' ' +
      (input.placeholder || '') + ' ' +
      this.findFieldLabel(input)
    ).toLowerCase();

    // Personal Information
    if (/first.?name|fname|given.?name/.test(text)) return 'personalInfo.firstName';
    if (/last.?name|lname|family.?name|surname/.test(text)) return 'personalInfo.lastName';
    if (/full.?name|name(?!.*first|.*last)/.test(text) && !/company|organization/.test(text)) return 'personalInfo.fullName';
    if (/email|e-mail/.test(text)) return 'personalInfo.email';
    if (/phone|mobile|tel/.test(text)) return 'personalInfo.phone';
    if (/address.*line.?1|street|address(?!.*email)/.test(text)) return 'personalInfo.address.street';
    if (/address.*line.?2|apartment|apt|suite/.test(text)) return 'personalInfo.address.line2';
    if (/city/.test(text)) return 'personalInfo.address.city';
    if (/state|province/.test(text)) return 'personalInfo.address.state';
    if (/zip|postal/.test(text)) return 'personalInfo.address.zipCode';
    if (/country/.test(text)) return 'personalInfo.address.country';
    if (/linkedin/.test(text)) return 'personalInfo.linkedin';
    if (/website|portfolio|url/.test(text)) return 'personalInfo.website';

    // Work Experience
    if (/current.?company|employer|company.*name/.test(text)) return 'workExperience.currentCompany';
    if (/current.?title|job.?title|position/.test(text)) return 'workExperience.currentTitle';
    if (/years?.?experience|experience.*years?/.test(text)) return 'workExperience.yearsExperience';
    if (/salary|compensation|pay/.test(text)) return 'workExperience.salary';
    if (/start.?date|from.?date/.test(text)) return 'workExperience.startDate';
    if (/end.?date|to.?date/.test(text)) return 'workExperience.endDate';

    // Education
    if (/school|university|college|institution/.test(text)) return 'education.school';
    if (/degree|education/.test(text)) return 'education.degree';
    if (/major|field.?of.?study|study/.test(text)) return 'education.fieldOfStudy';
    if (/graduation|grad.?date/.test(text)) return 'education.graduationDate';
    if (/gpa/.test(text)) return 'education.gpa';

    // Skills
    if (/skill|competenc|proficienc/.test(text)) return 'skills.technical';
    if (/language/.test(text)) return 'skills.languages';
    if (/certification|certificate/.test(text)) return 'skills.certifications';

    // Application Specific
    if (/cover.?letter|motivation/.test(text)) return 'application.coverLetter';
    if (/why.*company|why.*interested/.test(text)) return 'application.whyCompany';
    if (/availability|start.?date/.test(text)) return 'application.availability';

    return 'unknown';
  }

  createFieldSelector(input) {
    // Create a robust selector for the field
    const parts = [];
    
    if (input.id) {
      parts.push(`#${input.id}`);
    } else if (input.name) {
      parts.push(`[name="${input.name}"]`);
    } else {
      // Fallback to position-based selector
      const form = input.closest('form');
      if (form) {
        const formInputs = Array.from(form.querySelectorAll('input, select, textarea'));
        const index = formInputs.indexOf(input);
        parts.push(`form:nth-of-type(${Array.from(document.querySelectorAll('form')).indexOf(form) + 1}) input:nth-of-type(${index + 1})`);
      } else {
        parts.push(input.tagName.toLowerCase());
      }
    }

    return parts.join('');
  }

  async fillForm(profileData) {
    if (!profileData) {
      throw new Error('No profile data provided');
    }

    let filledCount = 0;
    const errors = [];

    // Re-detect fields to ensure we have current form state
    this.detectFormFields();

    for (const field of this.detectedFields) {
      try {
        const value = this.getValueForField(field.category, profileData);
        if (value !== null && value !== undefined) {
          await this.fillField(field.element, value);
          filledCount++;
        }
      } catch (error) {
        errors.push(`Failed to fill ${field.category}: ${error.message}`);
      }
    }

    return {
      success: true,
      filledCount,
      totalFields: this.detectedFields.length,
      errors
    };
  }

  getValueForField(category, profileData) {
    const keys = category.split('.');
    let value = profileData;

    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return null;
      }
    }

    return value;
  }

  async fillField(element, value) {
    if (!element || value === null || value === undefined) {
      return;
    }

    // Focus the element
    element.focus();

    // Handle different input types
    switch (element.type) {
      case 'select-one':
      case 'select-multiple':
        this.selectOption(element, value);
        break;
      
      case 'checkbox':
        element.checked = Boolean(value);
        break;
      
      case 'radio':
        if (element.value === value) {
          element.checked = true;
        }
        break;
      
      case 'date':
        if (value instanceof Date) {
          element.value = value.toISOString().split('T')[0];
        } else if (typeof value === 'string') {
          const date = new Date(value);
          if (!isNaN(date.getTime())) {
            element.value = date.toISOString().split('T')[0];
          }
        }
        break;
      
      default:
        // Text inputs, textareas, etc.
        element.value = String(value);
        break;
    }

    // Trigger change events
    element.dispatchEvent(new Event('input', { bubbles: true }));
    element.dispatchEvent(new Event('change', { bubbles: true }));
    element.dispatchEvent(new Event('blur', { bubbles: true }));

    // Small delay to allow for any async validation
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  selectOption(selectElement, value) {
    const options = Array.from(selectElement.options);
    
    // Try exact match first
    let option = options.find(opt => opt.value === value || opt.text === value);
    
    // Try partial match
    if (!option) {
      const valueStr = String(value).toLowerCase();
      option = options.find(opt => 
        opt.value.toLowerCase().includes(valueStr) || 
        opt.text.toLowerCase().includes(valueStr)
      );
    }

    if (option) {
      option.selected = true;
    }
  }

  extractFormData() {
    const formData = {};
    
    this.detectFormFields();
    
    for (const field of this.detectedFields) {
      const value = this.getFieldValue(field.element);
      if (value !== null && value !== undefined && value !== '') {
        this.setNestedValue(formData, field.category, value);
      }
    }

    return formData;
  }

  getFieldValue(element) {
    switch (element.type) {
      case 'checkbox':
        return element.checked;
      
      case 'radio':
        return element.checked ? element.value : null;
      
      case 'select-one':
        return element.selectedOptions[0]?.value || null;
      
      case 'select-multiple':
        return Array.from(element.selectedOptions).map(opt => opt.value);
      
      default:
        return element.value || null;
    }
  }

  setNestedValue(obj, path, value) {
    const keys = path.split('.');
    let current = obj;
    
    for (let i = 0; i < keys.length - 1; i++) {
      const key = keys[i];
      if (!(key in current)) {
        current[key] = {};
      }
      current = current[key];
    }
    
    current[keys[keys.length - 1]] = value;
  }
}

// Initialize content script
if (typeof window !== 'undefined') {
  new JobAutofillContentScript();
}