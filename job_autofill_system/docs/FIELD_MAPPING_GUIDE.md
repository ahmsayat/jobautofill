# 🎯 Field Mapping Customization Guide

## Overview
This guide explains how to customize field mappings for new websites and troubleshoot field detection issues. Perfect for when the extension doesn't work perfectly on a new job site.

## Understanding Field Detection

### How the Extension Identifies Fields

The extension uses multiple methods to identify form fields:

1. **Label Text Analysis**: Matches field labels to data types
2. **Input Attributes**: Uses `name`, `id`, `placeholder` attributes  
3. **Context Clues**: Analyzes surrounding text and form structure
4. **Pattern Recognition**: Looks for common field patterns
5. **Site-Specific Rules**: Uses known mappings for popular sites

### Field Detection Priority
```
1. Exact attribute match (name="firstName")
2. Label text match ("First Name:")
3. Placeholder text match ("Enter your first name")
4. Context analysis (field near "Name" heading)
5. Fallback patterns (first text input in section)
```

## Creating Custom Field Mappings

### When You Need Custom Mappings
- ✅ Extension doesn't detect fields on a specific site
- ✅ Wrong information being filled in fields
- ✅ New job site not yet supported
- ✅ Company uses custom application system

### Step-by-Step Custom Mapping

#### 1. Identify the Problem Field
1. **Right-click** on the problematic form field
2. Select **"Inspect Element"** (or press `F12`)
3. **Note these attributes**:
   ```html
   <input name="applicant_first_name" 
          id="fname" 
          placeholder="Your first name"
          class="form-control">
   ```

#### 2. Open Field Mapping Settings
1. Click the **extension icon**
2. Go to **Settings** → **Field Mappings**
3. Click **"Add Custom Mapping"**

#### 3. Create the Mapping
Fill out the custom mapping form:

```
Site Domain: careers.company.com
Field Selector: input[name="applicant_first_name"]
Data Type: firstName
Description: First name field on Company careers page
```

#### 4. Test the Mapping
1. **Reload** the job application page
2. **Try autofill** again
3. **Verify** the field fills correctly

### Advanced Field Selectors

#### CSS Selector Examples
```css
/* By name attribute */
input[name="first_name"]

/* By ID */
#firstName

/* By class and type */
input.form-input[type="text"]

/* By placeholder */
input[placeholder*="first name"]

/* Multiple possibilities */
input[name="fname"], input[id="firstName"], input[placeholder*="first name"]

/* Complex selectors */
.personal-info input[data-field="first-name"]
```

#### XPath Selectors (Advanced)
```xpath
// By text content
//label[contains(text(), 'First Name')]/following-sibling::input

// By position
//form//input[1]

// By attributes
//input[@data-testid='first-name']
```

## Site-Specific Mapping Examples

### Example 1: Workday-Based Systems

#### Common Field Patterns:
```javascript
// Workday typically uses these patterns
{
  "firstName": "input[data-automation-id*='firstName']",
  "lastName": "input[data-automation-id*='lastName']", 
  "email": "input[data-automation-id*='email']",
  "phone": "input[data-automation-id*='phone']"
}
```

#### Creating Workday Mapping:
1. **Site Pattern**: `*.myworkdayjobs.com`
2. **Field Mapping**:
   ```json
   {
     "siteName": "Workday Jobs",
     "domain": "*.myworkdayjobs.com", 
     "fields": {
       "firstName": {
         "selectors": [
           "input[data-automation-id*='firstName']",
           "input[aria-label*='First Name']"
         ]
       }
     }
   }
   ```

### Example 2: Greenhouse Systems

#### Common Patterns:
```javascript
// Greenhouse uses these selectors
{
  "firstName": "#first_name",
  "lastName": "#last_name",
  "email": "#email", 
  "phone": "#phone",
  "resume": "input[name='resume']"
}
```

#### Creating Greenhouse Mapping:
```json
{
  "siteName": "Greenhouse",
  "domain": "boards.greenhouse.io",
  "fields": {
    "firstName": {
      "selectors": ["#first_name", "input[name='first_name']"]
    },
    "lastName": {
      "selectors": ["#last_name", "input[name='last_name']"] 
    }
  }
}
```

### Example 3: Custom Company Sites

#### Analyzing Unknown Sites:
1. **Look for patterns** in field names/IDs
2. **Check form structure** 
3. **Test different selectors**
4. **Create comprehensive mapping**

#### Example Custom Site:
```json
{
  "siteName": "TechCorp Careers",  
  "domain": "careers.techcorp.com",
  "waitTime": 2000,
  "fields": {
    "firstName": {
      "selectors": [
        "input.candidate-first-name",
        "#applicant_fname"
      ]
    },
    "experience": {
      "selectors": ["textarea[name='work_experience']"],
      "fillMethod": "replace"
    }
  }
}
```

## Advanced Mapping Features

### Conditional Field Mapping

#### Different Fields Based on Job Type:
```json
{
  "conditions": {
    "engineering": {
      "githubProfile": {
        "selectors": ["input[name='github_url']"],
        "required": true
      }
    },
    "sales": {
      "salesExperience": {
        "selectors": ["textarea[name='sales_exp']"],
        "required": true
      }
    }
  }
}
```

### Multi-Step Form Handling

#### For Applications with Multiple Pages:
```json
{
  "multiStep": true,
  "steps": [
    {
      "stepId": 1,
      "url": "*step1*",
      "fields": ["firstName", "lastName", "email"]
    },
    {
      "stepId": 2, 
      "url": "*step2*",
      "fields": ["experience", "education"]
    }
  ]
}
```

### Dynamic Content Handling

#### For JavaScript-Heavy Sites:
```json
{
  "waitForElement": "input[name='firstName']",
  "maxWaitTime": 5000,
  "retryAttempts": 3,
  "dynamicContent": true
}
```

## Testing Your Custom Mappings

### Testing Checklist
- [ ] All required fields are mapped
- [ ] Test on multiple job postings from same site  
- [ ] Verify data fills correctly
- [ ] Check for any JavaScript errors
- [ ] Test edge cases (optional fields, dropdowns)

### Debug Mode Testing
1. **Enable Debug Mode**:
   ```
   Settings → Advanced → Debug Mode: ON
   ```

2. **Open Browser Console** (`F12`)

3. **Look for Debug Messages**:
   ```
   ✅ "Custom mapping found for careers.company.com"
   ✅ "Field mapped: firstName → input[name='fname']"
   ❌ "Mapping failed: selector not found"  
   ❌ "Timeout waiting for element"
   ```

### Validation Tools

#### Test Field Detection:
```javascript
// Run in browser console to test selectors
document.querySelector("input[name='firstName']");  // Should return element
document.querySelectorAll("input[type='text']");   // See all text inputs
```

#### Extension Debug Commands:
```javascript
// Available when debug mode enabled
JobAutofill.testMapping('firstName');
JobAutofill.analyzeForm();
JobAutofill.validateSelectors();
```

## Sharing Custom Mappings

### Export Your Mappings
1. **Settings** → **Field Mappings** → **Export Custom Mappings**
2. **Save JSON file** with your custom mappings
3. **Share with community** via GitHub issues

### Import Community Mappings
1. **Download mapping file** from community
2. **Settings** → **Field Mappings** → **Import Mappings**
3. **Select JSON file** to import
4. **Test on target site**

### Contributing Back
Help improve the extension by:
- ✅ Sharing mappings for new sites
- ✅ Reporting issues with existing mappings  
- ✅ Suggesting improvements
- ✅ Testing beta mapping updates

## Common Mapping Patterns

### Standard Field Types
```javascript
// Personal Information
"firstName": ["#fname", "input[name*='first']", "[placeholder*='first name']"]
"lastName": ["#lname", "input[name*='last']", "[placeholder*='last name']"]  
"email": ["#email", "input[type='email']", "[name*='email']"]
"phone": ["#phone", "input[type='tel']", "[name*='phone']"]

// Address Fields  
"address": ["#address", "[name*='street']", "[placeholder*='address']"]
"city": ["#city", "[name*='city']"]
"state": ["#state", "[name*='state']", "select[name*='state']"]
"zipCode": ["#zip", "[name*='zip']", "[name*='postal']"]

// Work Authorization
"workAuth": ["[name*='authorized']", "[name*='eligible']"]
"visa": ["[name*='visa']", "[name*='sponsorship']"]
```

### File Upload Fields
```javascript
"resume": [
  "input[type='file'][name*='resume']",
  "input[type='file'][accept*='.pdf']", 
  ".file-upload input[type='file']"
]

"coverLetter": [
  "input[type='file'][name*='cover']",
  "input[type='file'][name*='letter']"
]
```

### Dropdown/Select Fields
```javascript
"experience": [
  "select[name*='experience']",
  "select[name*='years']"
]

"education": [
  "select[name*='education']",
  "select[name*='degree']"
]
```

## Troubleshooting Mappings

### Common Issues

#### ❌ Selector Not Found
**Problem**: Element exists but selector doesn't match
**Solution**: 
- Check for typos in selector
- Use browser inspector to verify attributes
- Try more general selector

#### ❌ Element Found But Won't Fill  
**Problem**: Field detected but data doesn't appear
**Solution**:
- Check if field is disabled/readonly
- Try different fill method (type vs value)
- Add wait time for dynamic content

#### ❌ Mapping Works Sometimes
**Problem**: Inconsistent behavior
**Solution**:
- Add multiple selector options
- Increase wait times  
- Use more specific selectors

### Advanced Debugging

#### Manual Testing Commands:
```javascript
// Test if element exists
console.log(document.querySelector('#firstName'));

// Test filling element
document.querySelector('#firstName').value = 'Test Name';

// Trigger events (sometimes required)
document.querySelector('#firstName').dispatchEvent(new Event('input'));
```

## Best Practices

### Mapping Guidelines
- ✅ **Use specific selectors** when possible
- ✅ **Provide fallback options** for robustness  
- ✅ **Test thoroughly** before sharing
- ✅ **Document your mappings** clearly
- ✅ **Keep mappings updated** as sites change

### Performance Tips
- ✅ Avoid overly complex selectors
- ✅ Use efficient CSS selectors over XPath
- ✅ Set appropriate wait times
- ✅ Limit number of retry attempts

---

**🎯 Pro Tip**: Start with simple mappings and gradually add complexity. Most sites follow standard patterns, so begin with common field selectors before creating custom ones!