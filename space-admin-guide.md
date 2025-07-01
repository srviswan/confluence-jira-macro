# Space Admin Guide - JIRA Macro Deployment

**For Confluence Space Admins without full Administrator privileges**

## 🎯 Your Available Options

As a Space Admin, you can't create User Macros, but you have several effective alternatives to deploy the JIRA Issues Grid in your space.

## ✅ Option 1: HTML Macro (Recommended)

### Prerequisites
- HTML Macro must be enabled in your Confluence instance
- Space Admin permissions in your target space
- JIRA API token (see [API Token Setup](#api-token-setup))

### Step-by-Step Instructions

1. **Test First**: Open `demo.html` locally to verify your JIRA connection works

2. **Edit Your Page**:
   - Navigate to the page where you want the JIRA grid
   - Click **Edit**

3. **Add HTML Macro**:
   - Click **+** (Insert more content)
   - Search for "HTML" or navigate to **Other macros** → **Formatting** → **HTML**
   - Select the **HTML Macro**

4. **Configure the Macro**:
   - Copy the entire content from `jira-macro.html`
   - Paste into the HTML macro editor
   - Update the configuration section (around line 15-25):

```javascript
const config = {
    baseUrl: 'https://your-company.atlassian.net',  // Your JIRA URL
    username: 'your-email@company.com',             // Your email
    apiToken: 'your-api-token-here',                // Your API token
    jql: 'project = "YOUR_PROJECT" AND status != "Done"',
    fields: ['key', 'summary', 'status', 'assignee', 'priority'],
    maxResults: 25,
    title: 'My JIRA Issues'
};
```

5. **Save and Test**:
   - Click **Save** on the HTML macro
   - **Save** the page
   - Verify the grid loads correctly

### HTML Macro Limitations
- Configuration is hardcoded in each page
- Updates require editing each page individually
- No parameter-based configuration
- May have script execution restrictions in some Confluence versions

## ✅ Option 2: Source Editor Method

### For Confluence Server/Data Center

1. **Edit Page**: Navigate to your target page and click **Edit**

2. **Switch to Source Editor**:
   - Look for **Source** or **<>** button in the editor toolbar
   - Click to switch to source/HTML view

3. **Insert Code**:
   - Copy the entire content from `jira-macro.html`
   - Paste at the desired location in the source editor
   - Update the configuration variables

4. **Return to Visual Editor**:
   - Switch back to the visual editor
   - Save the page

### Source Editor Benefits
- Direct HTML insertion
- Full control over styling and behavior
- Works in most Confluence versions
- No macro dependencies

## ✅ Option 3: Iframe Embedding

### If You Can Host Files Externally

1. **Host the HTML File**:
   - Upload `jira-macro.html` to your web server, cloud storage, or GitHub Pages
   - Update the configuration in the hosted file
   - Ensure the URL is accessible from your Confluence instance

2. **Add Iframe Macro**:
   - Edit your Confluence page
   - Add **Iframe Macro** (+ → Other macros → Media → Iframe)
   - Configure the iframe:
     - **URL**: Your hosted HTML file URL
     - **Width**: 100%
     - **Height**: 600px (adjust as needed)

3. **Test Access**:
   - Save the page
   - Verify the iframe loads and displays correctly
   - Check for CORS issues (see [Troubleshooting](#troubleshooting))

### Iframe Hosting Options
- **GitHub Pages**: Create a repository and enable Pages
- **Company Web Server**: Upload to your organization's server
- **Cloud Storage**: AWS S3, Google Cloud Storage (with static hosting)
- **CDN Services**: jsDelivr, unpkg (for public repositories)

## ✅ Option 4: Request Administrator Help

### Prepare Your Request

Create a formal request to your Confluence Administrator including:

1. **Business Justification**:
   - Explain the business value of JIRA integration
   - Mention improved productivity and visibility
   - Reference specific use cases for your team

2. **Technical Details**:
   - Provide the `user-macro-template.vm` file
   - Include setup instructions
   - Mention security considerations

3. **Sample Request Email**:

```
Subject: Request: Create JIRA Issues Grid User Macro

Hi [Admin Name],

I'd like to request the creation of a User Macro to display JIRA issues within our Confluence space. This would significantly improve our team's ability to track project progress and share status updates.

Benefits:
- Real-time JIRA data in Confluence pages
- Customizable queries for different teams/projects
- Responsive design for mobile and desktop
- Secure API token authentication

I have prepared all the technical details and can provide:
- Complete macro template (Velocity)
- Setup instructions
- Security documentation
- Usage examples

Would you be available for a brief meeting to discuss implementation?

Best regards,
[Your Name]
```

## 🔐 API Token Setup

### Generate JIRA API Token

1. **Log into JIRA**:
   - Go to your JIRA instance
   - Click on your profile picture → **Account settings**

2. **Create Token**:
   - Navigate to **Security** → **API tokens**
   - Click **Create API token**
   - Give it a descriptive name (e.g., "Confluence JIRA Macro")
   - **Copy and save the token securely**

3. **Test Authentication**:
   - Use the interactive demo (`demo.html`) to verify the token works
   - Test with your actual JQL queries

### Security Best Practices

- **Use Service Account**: Consider creating a dedicated JIRA user for the macro
- **Limit Permissions**: Ensure the account only has necessary project access
- **Regular Rotation**: Rotate API tokens periodically
- **Secure Storage**: Never commit tokens to version control

## 🔧 Configuration Examples

### Personal Dashboard
```javascript
const config = {
    baseUrl: 'https://company.atlassian.net',
    username: 'service-account@company.com',
    apiToken: 'your-token-here',
    jql: 'assignee = currentUser() AND status != "Done"',
    fields: ['key', 'summary', 'status', 'priority', 'updated'],
    title: 'My Active Issues'
};
```

### Team Sprint Board
```javascript
const config = {
    baseUrl: 'https://company.atlassian.net',
    username: 'service-account@company.com',
    apiToken: 'your-token-here',
    jql: 'project = "TEAMPROJ" AND sprint in openSprints()',
    fields: ['key', 'summary', 'status', 'assignee', 'storyPoints'],
    title: 'Current Sprint Issues'
};
```

### High Priority Alerts
```javascript
const config = {
    baseUrl: 'https://company.atlassian.net',
    username: 'service-account@company.com',
    apiToken: 'your-token-here',
    jql: 'priority in ("Critical", "High") AND status != "Done"',
    fields: ['key', 'summary', 'status', 'assignee', 'priority'],
    title: '🔥 High Priority Issues',
    maxResults: 50
};
```

## 🛠️ Troubleshooting

### Common Space Admin Issues

#### HTML Macro Not Available
**Problem**: Can't find HTML Macro in the macro list
**Solutions**:
- Check if HTML Macro is enabled by your admin
- Try "HTML Include" or "Custom HTML" macros
- Use Source Editor method instead
- Request admin to enable HTML Macro

#### Script Execution Blocked
**Problem**: JavaScript doesn't execute in HTML Macro
**Solutions**:
- Use Iframe embedding method
- Request admin to adjust Content Security Policy
- Try Source Editor insertion
- Consider third-party apps

#### CORS Errors with Iframe
**Problem**: Cross-origin request blocked when using iframe
**Solutions**:
- Host file on same domain as Confluence
- Configure CORS headers on your hosting server
- Use a CORS proxy service
- Request JIRA admin to update CORS settings

#### Authentication Issues
**Problem**: API authentication fails
**Solutions**:
- Verify API token is correct and not expired
- Check username format (usually email address)
- Test with demo.html first
- Ensure user has project access permissions

### Testing Strategy

1. **Start with Demo**: Always test `demo.html` locally first
2. **Validate Connection**: Use the "Test Connection" feature
3. **Simple JQL First**: Start with basic queries like `project = "TEST"`
4. **Gradual Complexity**: Add filters and fields incrementally
5. **Error Monitoring**: Check browser console for detailed errors

## 📋 Deployment Checklist

### Before Deployment
- [ ] API token generated and tested
- [ ] JQL query validated in JIRA
- [ ] demo.html tested locally
- [ ] Configuration variables updated
- [ ] Security permissions verified

### During Deployment
- [ ] HTML Macro added successfully
- [ ] Configuration copied correctly
- [ ] Page saved without errors
- [ ] Grid displays data correctly
- [ ] Search and filtering work

### After Deployment
- [ ] Team trained on usage
- [ ] Documentation created for your space
- [ ] Regular token rotation scheduled
- [ ] Feedback collected from users
- [ ] Additional pages planned

## 🚀 Next Steps

1. **Choose Your Method**: Select the deployment option that works for your environment
2. **Test Thoroughly**: Use the demo to validate your setup
3. **Start Simple**: Begin with basic JQL queries and expand gradually
4. **Document for Team**: Create space-specific documentation
5. **Gather Feedback**: Collect user feedback and iterate

## 📞 Getting Help

If you encounter issues:
1. **Check Browser Console**: Look for JavaScript errors
2. **Validate JQL**: Test queries directly in JIRA
3. **Review Permissions**: Ensure proper JIRA project access
4. **Test with Demo**: Use `demo.html` to isolate issues
5. **Contact Admin**: Request assistance for macro creation or troubleshooting

---

**Remember**: As a Space Admin, you have significant flexibility within your space. Choose the method that best fits your technical comfort level and organizational constraints.
