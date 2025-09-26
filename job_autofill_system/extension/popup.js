// Job Autofill Extension Popup JavaScript
class PopupController {
  constructor() {
    this.initializeEventListeners();
    this.loadSettings();
  }

  initializeEventListeners() {
    // Quick Actions
    document.getElementById('fillBtn').addEventListener('click', () => this.autoFillForm());
    document.getElementById('detectBtn').addEventListener('click', () => this.detectFormFields());

    document.getElementById("generateCoverLetter").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { action: "generateCoverLetter" },
      (response) => {
        if (response?.coverLetter) {
          console.log("Cover Letter:", response.coverLetter);
          alert("Cover letter generated! Check the form or console.");
        } else {
          alert("Failed: " + (response?.error || "Unknown error"));
        }
      }
    );
  });
});

    // Profile Management
    document.getElementById('loadProfileBtn').addEventListener('click', () => this.loadProfile());
    document.getElementById('saveProfileBtn').addEventListener('click', () => this.saveProfile());
    document.getElementById('exportBtn').addEventListener('click', () => this.exportProfile());

    // Settings
    document.getElementById('autoDetectToggle').addEventListener('change', (e) => this.updateSetting('autoDetect', e.target.checked));
    document.getElementById('smartSuggestionsToggle').addEventListener('change', (e) => this.updateSetting('smartSuggestions', e.target.checked));
    document.getElementById('settingsBtn').addEventListener('click', () => this.openAdvancedSettings());

    // Help & Support
    document.getElementById('helpBtn').addEventListener('click', () => this.openDocumentation());
    document.getElementById('troubleshootBtn').addEventListener('click', () => this.openTroubleshooting());
  }

  async autoFillForm() {
    try {
      this.showStatus('🔄 Filling form...', 'info');
      
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Get saved profile data
      const result = await chrome.storage.local.get(['userProfile']);
      if (!result.userProfile) {
        this.showStatus('❌ No profile data found. Please load your profile first.', 'error');
        return;
      }

      // Send fill command to content script
      await chrome.tabs.sendMessage(tab.id, {
        action: 'fillForm',
        profileData: result.userProfile
      });

      this.showStatus('✅ Form filled successfully!', 'success');
    } catch (error) {
      console.error('Auto-fill error:', error);
      this.showStatus('❌ Failed to fill form. Please try again.', 'error');
    }
  }

  async detectFormFields() {
    try {
      this.showStatus('🔍 Detecting form fields...', 'info');
      
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      const response = await chrome.tabs.sendMessage(tab.id, {
        action: 'detectFields'
      });

      if (response && response.fields) {
        this.showStatus(`✅ Found ${response.fields.length} form fields`, 'success');
        
        // Save detected fields for analysis
        await chrome.storage.local.set({ 
          lastDetectedFields: {
            url: tab.url,
            fields: response.fields,
            timestamp: Date.now()
          }
        });
      } else {
        this.showStatus('ℹ️ No form fields detected on this page', 'info');
      }
    } catch (error) {
      console.error('Field detection error:', error);
      this.showStatus('❌ Failed to detect fields', 'error');
    }
  }

  async loadProfile() {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.json';
    fileInput.addEventListener('change', async (event) => {
      const file = event.target.files[0];
      if (file) {
        try {
          const text = await file.text();
          const profileData = JSON.parse(text);
          
          // Validate profile structure
          if (this.validateProfile(profileData)) {
            await chrome.storage.local.set({ userProfile: profileData });
            this.showStatus('✅ Profile loaded successfully!', 'success');
          } else {
            this.showStatus('❌ Invalid profile format', 'error');
          }
        } catch (error) {
          this.showStatus('❌ Failed to load profile file', 'error');
        }
      }
    });
    fileInput.click();
  }

  async saveProfile() {
    try {
      const result = await chrome.storage.local.get(['userProfile']);
      if (!result.userProfile) {
        this.showStatus('❌ No profile data to save', 'error');
        return;
      }

      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Get current form data to update profile
      const response = await chrome.tabs.sendMessage(tab.id, {
        action: 'extractFormData'
      });

      if (response && response.formData) {
        // Merge with existing profile
        const updatedProfile = { ...result.userProfile, ...response.formData };
        await chrome.storage.local.set({ userProfile: updatedProfile });
        this.showStatus('✅ Profile updated with current form data!', 'success');
      } else {
        this.showStatus('ℹ️ No form data found to save', 'info');
      }
    } catch (error) {
      console.error('Save profile error:', error);
      this.showStatus('❌ Failed to save profile', 'error');
    }
  }

  async exportProfile() {
    try {
      const result = await chrome.storage.local.get(['userProfile']);
      if (!result.userProfile) {
        this.showStatus('❌ No profile data to export', 'error');
        return;
      }

      const dataBlob = new Blob([JSON.stringify(result.userProfile, null, 2)], {
        type: 'application/json'
      });
      
      const url = URL.createObjectURL(dataBlob);
      const downloadLink = document.createElement('a');
      downloadLink.href = url;
      downloadLink.download = `job_profile_${new Date().toISOString().split('T')[0]}.json`;
      downloadLink.click();
      
      URL.revokeObjectURL(url);
      this.showStatus('✅ Profile exported successfully!', 'success');
    } catch (error) {
      console.error('Export error:', error);
      this.showStatus('❌ Failed to export profile', 'error');
    }
  }

  async updateSetting(setting, value) {
    try {
      const result = await chrome.storage.local.get(['settings']);
      const settings = result.settings || {};
      settings[setting] = value;
      await chrome.storage.local.set({ settings });
      
      // Notify content scripts of setting changes
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      chrome.tabs.sendMessage(tab.id, {
        action: 'updateSettings',
        settings: settings
      }).catch(() => {}); // Ignore if no content script
      
    } catch (error) {
      console.error('Settings update error:', error);
    }
  }

  async loadSettings() {
    try {
      const result = await chrome.storage.local.get(['settings']);
      const settings = result.settings || {
        autoDetect: true,
        smartSuggestions: true
      };

      document.getElementById('autoDetectToggle').checked = settings.autoDetect;
      document.getElementById('smartSuggestionsToggle').checked = settings.smartSuggestions;
    } catch (error) {
      console.error('Load settings error:', error);
    }
  }

  validateProfile(profile) {
    // Basic validation of profile structure
    return profile && 
           typeof profile === 'object' && 
           (profile.personalInfo || profile.workExperience || profile.education);
  }

  showStatus(message, type) {
    const statusDiv = document.getElementById('status');
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.style.display = 'block';
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 3000);
  }

  openAdvancedSettings() {
    chrome.tabs.create({
      url: chrome.runtime.getURL('settings.html')
    });
  }

  openDocumentation() {
    chrome.tabs.create({
      url: 'https://github.com/ahmsayat/jobautofill/tree/main/job_autofill_system'
    });
  }

  openTroubleshooting() {
    chrome.tabs.create({
      url: 'https://github.com/ahmsayat/jobautofill/tree/main/job_autofill_system'
    });
  }
}

// Initialize popup controller when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new PopupController();
});