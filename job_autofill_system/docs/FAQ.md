# ❓ Frequently Asked Questions (FAQ)

## General Questions

### Q: What is the Job Application Autofill Extension?
**A:** It's a browser extension that automatically fills out job application forms using your pre-configured personal information, work experience, education, and skills. It works across major job sites like LinkedIn, Indeed, and company career pages.

### Q: Is this extension free to use?
**A:** Yes, the extension is completely free. There are no premium features, subscriptions, or hidden costs.

### Q: Which browsers are supported?
**A:** Currently supports:
- ✅ **Google Chrome** (version 88+)
- ✅ **Microsoft Edge** (version 88+)
- 🔄 **Firefox support** (coming soon)
- 🔄 **Safari support** (under consideration)

### Q: Is my personal data safe?
**A:** Absolutely! Your data is:
- 🔒 **Stored locally** on your computer only
- 🚫 **Never sent to external servers**
- 🔐 **Encrypted** when stored
- 🗑️ **Completely deletable** by you at any time

---

## Installation & Setup

### Q: How do I install the extension?
**A:** Follow these steps:
1. Download the extension package
2. Open Chrome/Edge extensions page (`chrome://extensions/`)
3. Enable "Developer mode"
4. Click "Load unpacked" and select the extension folder
5. Complete setup by adding your personal information

*Detailed instructions: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)*

### Q: The extension icon doesn't appear in my toolbar. What should I do?
**A:** Try these solutions:
1. **Pin the extension**: Click the puzzle piece icon (🧩) → find "Job Autofill" → click pin (📌)
2. **Refresh extensions page**: Press F5 on `chrome://extensions/`
3. **Restart browser**: Close all windows and reopen
4. **Check Developer Mode**: Ensure it's enabled in extensions settings

### Q: How much information do I need to provide?
**A:** **Minimum required**:
- Full name, email, phone number
- Current address
- At least one work experience entry
- Basic education information

**Recommended for best results**:
- Complete work history (last 10 years)
- All relevant skills
- Professional profiles (LinkedIn, GitHub)
- Resume and cover letter files

### Q: Can I import my information from LinkedIn?
**A:** Yes! You can:
1. **Export your LinkedIn data** (Settings → Get a copy of your data)
2. **Import in extension**: Documents tab → Import from LinkedIn
3. **Review imported data** and make any necessary adjustments

---

## Using the Extension

### Q: How do I fill out a job application?
**A:** Three easy methods:
1. **Automatic**: Visit job site → extension detects forms → click "Fill Form"
2. **Keyboard shortcut**: Press `Ctrl+Shift+F` (or `Cmd+Shift+F` on Mac)
3. **Manual**: Right-click individual fields → select "Fill with..."

### Q: Which job sites does it work on?
**A:** **Fully supported** (90%+ success rate):
- LinkedIn (Easy Apply)
- Indeed
- Glassdoor
- Monster
- ZipRecruiter

**Well supported** (70%+ success rate):
- Workday-based systems
- Greenhouse
- Lever
- BambooHR
- Most company career pages

*Full list: [USER_MANUAL.md - Supported Websites](USER_MANUAL.md#supported-websites)*

### Q: What if the extension doesn't work on a specific site?
**A:** Try these approaches:
1. **Manual field selection**: Right-click fields individually
2. **Custom field mapping**: Create mappings for new sites
3. **Report the site**: Help us add support via "Report Site" feature
4. **Copy-paste fallback**: Use extension popup as a reference

### Q: Can I use different resumes for different types of jobs?
**A:** Yes! You can:
- **Upload multiple resume versions** in Documents tab
- **Create job-specific profiles** for different career paths
- **Switch between profiles** based on the type of position
- **Use different cover letter templates** for various roles

---

## Troubleshooting

### Q: The extension fills some fields incorrectly. How do I fix this?
**A:** Several solutions:
1. **Update your data**: Check if information in extension is current
2. **Review field mappings**: Settings → Field Mappings → check site-specific rules
3. **Use manual selection**: Right-click problematic fields → choose correct data type
4. **Create custom mapping**: Add site-specific field rules

*Detailed help: [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)*

### Q: The extension makes my browser slow. What can I do?
**A:** Optimize performance:
1. **Reduce scan frequency**: Settings → Performance → set to "Conservative"
2. **Disable auto-detection**: Only activate manually when needed
3. **Limit active sites**: Disable extension on non-job sites
4. **Clear cache**: Settings → Advanced → Clear Cache

### Q: File uploads (resume/cover letter) don't work. Why?
**A:** Common causes and fixes:
1. **File location**: Move files to easily accessible folders (Desktop/Documents)
2. **File format**: Use PDF, DOC, or DOCX (avoid TXT or images)
3. **File size**: Keep under 5MB
4. **Browser permissions**: Check if site has file access permissions

### Q: I accidentally deleted my data. Can I recover it?
**A:** Recovery options:
1. **Recent backup**: Import from your most recent data export
2. **Browser sync**: Check if browser synced extension data
3. **Re-import**: Import from LinkedIn, resume, or other sources
4. **Manual re-entry**: Unfortunately, if no backup exists, you'll need to re-enter

---

## Features & Functionality

### Q: Can the extension automatically submit applications for me?
**A:** **No, and here's why**:
- 🚫 **Not recommended**: Each application needs personal review
- 🚫 **Legal concerns**: Some sites prohibit automated submissions
- 🚫 **Quality control**: You should verify information for each specific role

The extension **fills forms only** - you maintain complete control over submission.

### Q: Does the extension work with multi-page applications?
**A:** **Yes**, with some limitations:
- ✅ **Workday systems**: Handles multi-step flows well
- ✅ **Standard progressions**: Works with typical next/continue buttons
- 🔶 **Complex flows**: May need manual intervention on some steps
- 🔄 **Improving**: Multi-page support continuously enhanced

### Q: Can I customize which fields get filled?
**A:** **Absolutely**! You have full control:
- **Field-level control**: Choose which types of information to fill
- **Site-specific rules**: Different settings for different job sites
- **Quick fill vs. full fill**: Options for basic or comprehensive filling
- **Manual override**: Always option to fill individual fields manually

### Q: How does the extension handle dropdown menus and selection fields?
**A:** **Smart matching**:
- **Text matching**: Looks for closest text matches in dropdowns
- **Experience levels**: Maps years of experience to appropriate ranges
- **Education levels**: Matches degree types to dropdown options
- **Location**: Matches city/state to available options
- **Fallback**: Highlights unmatched fields for manual selection

---

## Privacy & Security

### Q: What data does the extension collect?
**A:** **Only what you provide**:
- ✅ **Personal info**: Only what you enter in the extension
- ✅ **Usage statistics**: Anonymous performance data (optional)
- 🚫 **No browsing history**: Doesn't track your web activity
- 🚫 **No external transmission**: Data never leaves your computer

### Q: Can employers see that I used an autofill extension?
**A:** **No**:
- 🚫 **No detection possible**: Forms receive data normally
- 🚫 **No special markers**: Filled data is indistinguishable from manual entry
- 🚫 **No tracking**: No way for sites to detect autofill usage
- ✅ **Standard behavior**: Mimics normal form filling patterns

### Q: What happens if I uninstall the extension?
**A:** **Your choice**:
- 🗑️ **Complete removal**: All data deleted from browser
- 💾 **Export first**: Save your data before uninstalling
- 🔄 **Easy reinstall**: Import saved data if you reinstall later
- 📱 **No external storage**: No cloud data to worry about

---

## Advanced Features

### Q: Can I create custom field mappings for unsupported sites?
**A:** **Yes!** Advanced users can:
1. **Analyze form fields** using browser developer tools
2. **Create custom mappings** in Settings → Field Mappings
3. **Test and refine** mappings for accuracy
4. **Share with community** to help others

*Guide: [FIELD_MAPPING_GUIDE.md](FIELD_MAPPING_GUIDE.md)*

### Q: Is there an API or integration with other tools?
**A:** **Currently**:
- 🚫 **No public API**: Focus on standalone functionality
- ✅ **Export/Import**: JSON format for data portability
- 🔄 **Considering**: Integrations with job search tracking tools
- 💡 **Suggestions welcome**: Open to feature requests

### Q: Can I use the extension for other types of forms?
**A:** **Designed for job applications**, but can work with:
- ✅ **Contact forms**: Basic personal information fields
- ✅ **Registration forms**: Name, email, address fields
- 🔶 **Survey forms**: Limited usefulness
- 🚫 **Financial forms**: Not recommended for security reasons

---

## Performance & Optimization

### Q: How fast should the extension work?
**A:** **Typical performance**:
- ⚡ **Form detection**: 2-3 seconds after page load
- ⚡ **Field filling**: 1-2 seconds for complete form
- ⚡ **File uploads**: 3-5 seconds depending on file size
- 🐌 **If slower**: Check troubleshooting guide for optimization

### Q: Does the extension work offline?
**A:** **Partially**:
- ✅ **Data access**: Your information available offline
- ✅ **Extension UI**: Popup works without internet
- 🚫 **Job site access**: Need internet to visit job sites
- 🚫 **File uploads**: Require online connection

### Q: How many applications can I fill per day?
**A:** **No limits**:
- ∞ **Unlimited usage**: Fill as many applications as you want
- ⚡ **No rate limiting**: Extension doesn't restrict frequency
- 🎯 **Site limits**: Individual job sites may have their own restrictions
- 🎯 **Quality focus**: Recommend quality over quantity

---

## Getting Help

### Q: Where can I find more detailed help?
**A:** **Comprehensive documentation**:
- 📖 **User Manual**: [USER_MANUAL.md](USER_MANUAL.md) - Complete feature guide
- 🔧 **Troubleshooting**: [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md) - Fix common issues
- ⚙️ **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md) - Initial configuration help
- 🎯 **Field Mapping**: [FIELD_MAPPING_GUIDE.md](FIELD_MAPPING_GUIDE.md) - Advanced customization

### Q: How do I report bugs or request features?
**A:** **Multiple channels**:
1. **Extension feedback**: Use "Report Issue" button in extension
2. **GitHub Issues**: Submit detailed bug reports
3. **Community forums**: Discuss with other users
4. **Email support**: For complex technical issues

### Q: Is there a community of users I can connect with?
**A:** **Yes!** Join the community:
- 💬 **GitHub Discussions**: Share tips and ask questions
- 📱 **User forums**: Connect with other job seekers
- 🎓 **Best practices**: Learn from experienced users
- 🤝 **Success stories**: Share your job search wins

### Q: How often is the extension updated?
**A:** **Regular updates**:
- 🔄 **Monthly**: Bug fixes and minor improvements
- 🚀 **Quarterly**: New features and major site support additions
- 🎯 **As needed**: Critical fixes and urgent site updates
- 📢 **Notifications**: Update announcements in extension

---

## Quick Help Reference

### 🚨 **Emergency Fixes**
- **Extension not working**: Refresh page, restart browser
- **Wrong data filling**: Check extension settings, update information
- **Site not supported**: Try manual field selection, report site issue
- **Performance issues**: Clear cache, reduce scan frequency

### ⌨️ **Essential Shortcuts**
- **Fill form**: `Ctrl+Shift+F` (Windows) / `Cmd+Shift+F` (Mac)
- **Quick fill**: `Ctrl+Shift+Q` (Windows) / `Cmd+Shift+Q` (Mac)
- **Settings**: `Ctrl+Shift+S` (Windows) / `Cmd+Shift+S` (Mac)

### 📚 **Quick Links**
- **Setup**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Problems**: [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md)
- **Advanced**: [FIELD_MAPPING_GUIDE.md](FIELD_MAPPING_GUIDE.md)
- **Complete manual**: [USER_MANUAL.md](USER_MANUAL.md)

---

**❓ Still have questions?** Check the detailed guides above, or use the "Contact Support" feature in the extension for personalized help!