// Job Autofill Extension Background Script (Service Worker)
class JobAutofillBackground {
  constructor() {
    this.initialize();
  }

  initialize() {
    // Set up installation handler
    chrome.runtime.onInstalled.addListener((details) => {
      this.handleInstallation(details);
    });

    // Set up message handlers
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message, sender, sendResponse);
      return true; // Keep message channel open for async responses
    });

    // Set up context menu
    this.setupContextMenu();

    // Set up tab update listeners
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      this.handleTabUpdate(tabId, changeInfo, tab);
    });

    // Set up keyboard shortcuts
    chrome.commands.onCommand.addListener((command) => {
      this.handleCommand(command);
    });
  }

  async handleInstallation(details) {
    console.log('Job Autofill Extension installed/updated:', details);

    // Initialize default settings
    const defaultSettings = {
      autoDetect: true,
      smartSuggestions: true,
      autoFillDelay: 1000,
      confirmBeforeFill: false,
      debugMode: false
    };

    try {
      const result = await chrome.storage.local.get(['settings']);
      if (!result.settings) {
        await chrome.storage.local.set({ settings: defaultSettings });
        console.log('Default settings initialized');
      }
    } catch (error) {
      console.error('Failed to initialize settings:', error);
    }

    // Show welcome notification on first install
    if (details.reason === 'install') {
      this.showWelcomeNotification();
    }
  }

  async handleMessage(message, sender, sendResponse) {
    try {
      switch (message.action) {
        case 'getSettings':
          const settings = await this.getSettings();
          sendResponse({ success: true, settings });
          break;

        case 'updateSettings':
          await this.updateSettings(message.settings);
          sendResponse({ success: true });
          break;

        case 'exportData':
          const exportData = await this.exportUserData();
          sendResponse({ success: true, data: exportData });
          break;

        case 'importData':
          await this.importUserData(message.data);
          sendResponse({ success: true });
          break;

        case 'clearData':
          await this.clearUserData();
          sendResponse({ success: true });
          break;

        case 'getStats':
          const stats = await this.getUsageStats();
          sendResponse({ success: true, stats });
          break;

        default:
          sendResponse({ success: false, error: 'Unknown action' });
      }
    } catch (error) {
      console.error('Background script error:', error);
      sendResponse({ success: false, error: error.message });
    }
  }

  setupContextMenu() {
    chrome.contextMenus.create({
      id: 'job-autofill-main',
      title: 'Job Autofill',
      contexts: ['page']
    });

    chrome.contextMenus.create({
      id: 'fill-form',
      parentId: 'job-autofill-main',
      title: 'Fill Current Form',
      contexts: ['page']
    });

    chrome.contextMenus.create({
      id: 'detect-fields',
      parentId: 'job-autofill-main',
      title: 'Detect Form Fields',
      contexts: ['page']
    });

    chrome.contextMenus.create({
      id: 'save-form-data',
      parentId: 'job-autofill-main',
      title: 'Save Form Data',
      contexts: ['page']
    });

    // Handle context menu clicks
    chrome.contextMenus.onClicked.addListener(async (info, tab) => {
      try {
        switch (info.menuItemId) {
          case 'fill-form':
            await this.fillFormInTab(tab.id);
            break;
          case 'detect-fields':
            await this.detectFieldsInTab(tab.id);
            break;
          case 'save-form-data':
            await this.saveFormDataFromTab(tab.id);
            break;
        }
      } catch (error) {
        console.error('Context menu action error:', error);
      }
    });
  }

  async handleTabUpdate(tabId, changeInfo, tab) {
    // Only act when page is completely loaded
    if (changeInfo.status !== 'complete') return;

    try {
      const settings = await this.getSettings();
      
      // Auto-detect forms on job sites if enabled
      if (settings.autoDetect && this.isJobSite(tab.url)) {
        setTimeout(() => {
          this.detectFieldsInTab(tabId);
        }, settings.autoFillDelay || 1000);
      }
    } catch (error) {
      console.error('Tab update handler error:', error);
    }
  }

  handleCommand(command) {
    switch (command) {
      case 'fill-current-form':
        this.fillCurrentPageForm();
        break;
      case 'detect-fields':
        this.detectCurrentPageFields();
        break;
      case 'toggle-autofill':
        this.toggleAutoFill();
        break;
    }
  }

  async getSettings() {
    try {
      const result = await chrome.storage.local.get(['settings']);
      return result.settings || {};
    } catch (error) {
      console.error('Failed to get settings:', error);
      return {};
    }
  }

  async updateSettings(newSettings) {
    try {
      const result = await chrome.storage.local.get(['settings']);
      const settings = { ...result.settings, ...newSettings };
      await chrome.storage.local.set({ settings });
      
      // Notify all content scripts of settings change
      const tabs = await chrome.tabs.query({});
      for (const tab of tabs) {
        try {
          await chrome.tabs.sendMessage(tab.id, {
            action: 'updateSettings',
            settings: settings
          });
        } catch (error) {
          // Ignore tabs that don't have content script
        }
      }
    } catch (error) {
      console.error('Failed to update settings:', error);
      throw error;
    }
  }

  async fillFormInTab(tabId) {
    try {
      // Get user profile
      const result = await chrome.storage.local.get(['userProfile']);
      if (!result.userProfile) {
        this.showNotification('No profile data found', 'Please load your profile first.');
        return;
      }

      // Send fill command to content script
      const response = await chrome.tabs.sendMessage(tabId, {
        action: 'fillForm',
        profileData: result.userProfile
      });

      if (response && response.success) {
        this.showNotification(
          'Form filled successfully!',
          `Filled ${response.filledCount} out of ${response.totalFields} fields.`
        );
        
        // Update usage stats
        await this.updateUsageStats('formsFilled');
      } else {
        this.showNotification('Fill failed', 'Unable to fill the form.');
      }
    } catch (error) {
      console.error('Fill form error:', error);
      this.showNotification('Error', 'Failed to fill form.');
    }
  }

  async detectFieldsInTab(tabId) {
    try {
      const response = await chrome.tabs.sendMessage(tabId, {
        action: 'detectFields'
      });

      if (response && response.fields) {
        console.log(`Detected ${response.fields.length} fields in tab ${tabId}`);
        
        // Store detection results
        await chrome.storage.local.set({
          [`detection_${tabId}`]: {
            fields: response.fields,
            timestamp: Date.now(),
            url: (await chrome.tabs.get(tabId)).url
          }
        });
        
        // Update usage stats
        await this.updateUsageStats('fieldsDetected', response.fields.length);
      }
    } catch (error) {
      console.error('Detect fields error:', error);
    }
  }

  async saveFormDataFromTab(tabId) {
    try {
      const response = await chrome.tabs.sendMessage(tabId, {
        action: 'extractFormData'
      });

      if (response && response.formData) {
        // Merge with existing profile
        const result = await chrome.storage.local.get(['userProfile']);
        const profile = result.userProfile || {};
        const updatedProfile = this.mergeProfiles(profile, response.formData);
        
        await chrome.storage.local.set({ userProfile: updatedProfile });
        
        this.showNotification(
          'Form data saved!',
          'Your profile has been updated with form data.'
        );
        
        // Update usage stats
        await this.updateUsageStats('dataSaved');
      }
    } catch (error) {
      console.error('Save form data error:', error);
      this.showNotification('Error', 'Failed to save form data.');
    }
  }

  async fillCurrentPageForm() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      await this.fillFormInTab(tab.id);
    } catch (error) {
      console.error('Fill current page error:', error);
    }
  }

  async detectCurrentPageFields() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      await this.detectFieldsInTab(tab.id);
    } catch (error) {
      console.error('Detect current page error:', error);
    }
  }

  async toggleAutoFill() {
    try {
      const settings = await this.getSettings();
      const newAutoDetect = !settings.autoDetect;
      
      await this.updateSettings({ autoDetect: newAutoDetect });
      
      this.showNotification(
        `Auto-fill ${newAutoDetect ? 'enabled' : 'disabled'}`,
        `Form detection is now ${newAutoDetect ? 'on' : 'off'}.`
      );
    } catch (error) {
      console.error('Toggle auto-fill error:', error);
    }
  }

  isJobSite(url) {
    const jobSiteDomains = [
      'linkedin.com',
      'indeed.com',
      'glassdoor.com',
      'monster.com',
      'careerbuilder.com',
      'ziprecruiter.com',
      'simplyhired.com',
      'dice.com',
      'workday.com',
      'greenhouse.io',
      'lever.co',
      'smartrecruiters.com',
      'bamboohr.com',
      'workable.com'
    ];

    return jobSiteDomains.some(domain => url && url.includes(domain));
  }

  async exportUserData() {
    try {
      const result = await chrome.storage.local.get(null);
      return {
        profile: result.userProfile,
        settings: result.settings,
        stats: result.usageStats,
        exportDate: new Date().toISOString()
      };
    } catch (error) {
      console.error('Export data error:', error);
      throw error;
    }
  }

  async importUserData(data) {
    try {
      const updates = {};
      
      if (data.profile) updates.userProfile = data.profile;
      if (data.settings) updates.settings = data.settings;
      if (data.stats) updates.usageStats = data.stats;
      
      await chrome.storage.local.set(updates);
    } catch (error) {
      console.error('Import data error:', error);
      throw error;
    }
  }

  async clearUserData() {
    try {
      await chrome.storage.local.clear();
      console.log('All user data cleared');
    } catch (error) {
      console.error('Clear data error:', error);
      throw error;
    }
  }

  async getUsageStats() {
    try {
      const result = await chrome.storage.local.get(['usageStats']);
      return result.usageStats || {
        formsFilled: 0,
        fieldsDetected: 0,
        dataSaved: 0,
        sessionsStarted: 0,
        lastUsed: null
      };
    } catch (error) {
      console.error('Get usage stats error:', error);
      return {};
    }
  }

  async updateUsageStats(action, value = 1) {
    try {
      const stats = await this.getUsageStats();
      
      if (action in stats) {
        stats[action] += value;
      }
      stats.lastUsed = new Date().toISOString();
      
      await chrome.storage.local.set({ usageStats: stats });
    } catch (error) {
      console.error('Update usage stats error:', error);
    }
  }

  mergeProfiles(existing, newData) {
    const merged = { ...existing };
    
    for (const [key, value] of Object.entries(newData)) {
      if (typeof value === 'object' && !Array.isArray(value) && value !== null) {
        merged[key] = { ...merged[key], ...value };
      } else {
        merged[key] = value;
      }
    }
    
    return merged;
  }

  showNotification(title, message) {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icon48.png',
      title: title,
      message: message
    });
  }

  showWelcomeNotification() {
    this.showNotification(
      'Job Autofill Extension Installed!',
      'Click the extension icon to get started with auto-filling job applications.'
    );
  }
}

// Initialize background script
new JobAutofillBackground();