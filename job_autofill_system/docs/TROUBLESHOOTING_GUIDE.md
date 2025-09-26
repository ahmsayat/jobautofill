# 🔧 Troubleshooting Guide - Job Application Autofill Extension

## Quick Fixes (Try These First!)

### 🚨 **Extension Not Working At All**
1. **Refresh the page** (`F5` or `Cmd+R`)
2. **Check if extension is enabled** in `chrome://extensions/`
3. **Click the extension icon** to verify it's responding
4. **Restart your browser** completely

### 🚨 **Forms Not Being Detected**
1. **Wait 2-3 seconds** after page loads
2. **Scroll down** to ensure all form fields are visible
3. **Try clicking in a form field** to trigger detection
4. **Check if site is supported** (see supported sites list)

### 🚨 **Data Not Filling Correctly**
1. **Verify your data setup** in extension popup
2. **Check field mapping** for the specific site
3. **Try manual field selection** (right-click → "Fill this field")
4. **Clear and retry** the autofill process

## Common Issues & Detailed Solutions

### Issue #1: "Extension Icon Missing from Toolbar"

#### Symptoms:
- Extension installed but icon not visible
- Can't access extension popup

#### Solutions:
1. **Check Extensions Page**:
   - Go to `chrome://extensions/`
   - Verify "Job Application Autofill" is listed and enabled
   - If disabled, click the toggle to enable

2. **Pin the Extension**:
   - Click puzzle piece icon (🧩) in toolbar
   - Find "Job Application Autofill"
   - Click pin icon (📌) to make it always visible

3. **Browser Restart**:
   - Close ALL browser windows
   - Restart browser completely
   - Check toolbar again

---

### Issue #2: "Forms Detected But Fields Not Filling"

#### Symptoms:
- Extension recognizes the form
- Fields highlighted but data doesn't appear
- Success message shows but fields remain empty

#### Diagnostic Steps:
1. **Check Data Setup**:
   ```
   Extension Popup → Personal Info Tab
   Verify all required fields have data
   ```

2. **Field Mapping Issue**:
   ```
   Right-click on specific field → Inspect element
   Check if field has unusual attributes
   ```

3. **Site-Specific Problems**:
   ```
   Try on a different job site
   If works elsewhere, it's a site-specific issue
   ```

#### Solutions:
1. **Manual Field Selection**:
   - Right-click on any form field
   - Select "Fill this field with..." from context menu
   - Choose appropriate data type

2. **Custom Field Mapping**:
   - Open extension popup
   - Go to "Settings" → "Field Mappings"
   - Add custom mapping for problematic fields

3. **Update Field Selectors**:
   ```
   Settings → Advanced → Update Selectors
   This refreshes field detection rules
   ```

---

### Issue #3: "Extension Slows Down Browser"

#### Symptoms:
- Pages load slowly when extension is active
- Browser becomes unresponsive
- High CPU usage

#### Solutions:
1. **Reduce Scan Frequency**:
   ```
   Settings → Performance → Scan Interval
   Change from "Aggressive" to "Normal" or "Conservative"
   ```

2. **Disable Auto-Detection**:
   ```
   Settings → General → Auto-detect forms
   Turn off and use manual activation only
   ```

3. **Limit Active Sites**:
   ```
   Settings → Site Management → Active Sites
   Disable extension on non-job sites
   ```

---

### Issue #4: "File Uploads Not Working"

#### Symptoms:
- Resume/cover letter files not uploading
- File input fields remain empty
- Error messages about file access

#### Solutions:
1. **Check File Permissions**:
   - Ensure files are not in restricted folders
   - Move files to Desktop or Documents
   - Re-upload files in extension settings

2. **File Format Issues**:
   - Supported formats: PDF, DOC, DOCX, TXT
   - File size limit: 5MB maximum
   - Avoid special characters in filename

3. **Browser File Access**:
   ```
   Chrome Settings → Privacy and Security → Site Settings
   → Additional permissions → File System Access
   Ensure enabled for job sites
   ```

---

### Issue #5: "Wrong Information Being Filled"

#### Symptoms:
- Incorrect data appears in fields
- Information from wrong section used
- Outdated information being filled

#### Solutions:
1. **Update Your Data**:
   ```
   Extension Popup → Edit all sections
   Verify current information is entered
   Save changes
   ```

2. **Clear Cache**:
   ```
   Settings → Advanced → Clear Cache
   This refreshes stored field mappings
   ```

3. **Field Priority Settings**:
   ```
   Settings → Data Priority
   Adjust which information takes precedence
   ```

---

### Issue #6: "Extension Works on Some Sites But Not Others"

#### Symptoms:
- Perfect on LinkedIn, fails on company sites
- Works on Indeed but not on Greenhouse
- Inconsistent behavior across platforms

#### Diagnostic Information:
Check our **Supported Sites List**:

**✅ Fully Supported:**
- LinkedIn (Easy Apply)
- Indeed
- Glassdoor
- Monster
- ZipRecruiter

**🔶 Partially Supported:**
- Workday (some companies)
- Greenhouse (most implementations)
- Lever (basic fields)
- BambooHR (standard forms)

**❌ Known Issues:**
- Heavy JavaScript-based forms
- Sites with CAPTCHA requirements
- Multi-page applications without standard navigation

#### Solutions:
1. **Site-Specific Fixes**:
   - Check if site has known workarounds
   - Look for updated field mappings
   - Try different timing settings

2. **Manual Override**:
   - Use keyboard shortcuts (`Ctrl+Shift+F`)
   - Right-click context menu for individual fields
   - Copy-paste mode for difficult forms

3. **Report New Sites**:
   - Use "Report Site Issue" in extension
   - Provide URL and description of problems
   - Help us add support for new platforms

## Advanced Troubleshooting

### Developer Console Debugging

#### Enable Debug Mode:
1. **Extension Settings** → **Advanced** → **Debug Mode: ON**
2. **Open Developer Console**: `F12` or `Cmd+Option+I`
3. **Look for extension messages** in Console tab

#### Common Debug Messages:
```
"Form detected: 5 fields found" - ✅ Good
"No matching fields for: firstName" - ❌ Field mapping issue  
"Permission denied for file access" - ❌ File permission problem
"Rate limit exceeded" - ❌ Too many rapid requests
```

### Reset Extension to Defaults

#### Complete Reset Process:
1. **Backup Your Data**:
   ```
   Extension Popup → Settings → Export Data
   Save the JSON file somewhere safe
   ```

2. **Reset Extension**:
   ```
   Settings → Advanced → Reset All Settings
   Confirm reset when prompted
   ```

3. **Restore Data**:
   ```
   Settings → Import Data
   Select your backup JSON file
   ```

### Manual Field Mapping

#### For Persistent Field Issues:
1. **Identify Problem Fields**:
   - Right-click → Inspect Element
   - Note the field's `name`, `id`, and `placeholder` attributes

2. **Add Custom Mapping**:
   ```
   Extension Settings → Field Mappings → Add Custom
   Site: [website domain]
   Field Selector: [CSS selector]
   Data Type: [personal info type]
   ```

3. **Test Custom Mapping**:
   - Reload the page
   - Try autofill again
   - Verify field fills correctly

## Performance Optimization

### Speed Up Extension Performance

#### Optimize Settings:
```
✅ Scan Interval: Normal (not Aggressive)
✅ Auto-detection: Only on job sites
✅ Animation: Reduced or disabled
✅ Debug Mode: OFF (unless troubleshooting)
```

#### Browser Optimization:
- Keep extensions to minimum needed
- Close unnecessary tabs
- Clear browser cache regularly
- Update browser to latest version

## Getting Additional Help

### Contact Support Channels

#### Before Contacting Support:
1. ✅ Try all solutions in this guide
2. ✅ Check FAQ for common questions
3. ✅ Test on multiple websites
4. ✅ Note your browser version and OS

#### Include This Information:
```
Browser: Chrome/Edge [version number]
Operating System: Windows/Mac/Linux [version]
Extension Version: [found in chrome://extensions/]
Problem Site: [specific URL]
Error Messages: [exact text if any]
Steps to Reproduce: [detailed steps]
```

#### Support Options:
- **📧 Email**: Create issue in project repository
- **📖 Documentation**: Check USER_MANUAL.md
- **🐛 Bug Report**: Use extension's "Report Issue" feature
- **💬 Community**: Check project discussions

### Emergency Workarounds

#### If Extension Completely Fails:
1. **Copy-Paste Method**:
   - Keep extension popup open
   - Copy information from extension
   - Paste manually into forms

2. **Text File Backup**:
   - Export your data to text file
   - Keep it open while applying
   - Manual copy-paste as needed

3. **Browser Bookmarks**:
   - Create bookmarks with auto-text
   - Use browser's built-in form filling
   - Temporary solution until fixed

---

**💡 Pro Tip**: Most issues resolve with a simple page refresh and ensuring your data is properly set up in the extension. When in doubt, start with the "Quick Fixes" section!