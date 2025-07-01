# Setup Instructions for Confluence JIRA Macro

## Overview
This guide will help you set up the JIRA Issues Grid macro in your Confluence instance.

## Options for Space Admins (Limited Privileges)

**If you're a Space Admin without Confluence Administrator access, you have several alternatives:**

### Option A: HTML Macro (Most Common)
If your Confluence instance has the HTML Macro enabled:
1. Edit any page in your space
2. Add the **HTML Macro** (+ → Other macros → Formatting → HTML)
3. Copy the content from `jira-macro.html`
4. Update the configuration section with your JIRA details
5. Save the page

### Option B: Source Editor Method
For Confluence Server/Data Center:
1. Edit a page and switch to **Source Editor** mode
2. Copy the entire content from `jira-macro.html`
3. Paste directly into the source editor
4. Update configuration variables
5. Switch back to visual editor and save

### Option C: Iframe Embedding
If you can host the HTML file externally:
1. Host `jira-macro.html` on your web server or cloud storage
2. Use Confluence's **Iframe Macro** to embed it
3. Configure the iframe source URL
4. Set appropriate width/height dimensions

### Option D: Request Admin Assistance
Ask your Confluence Administrator to:
1. Create a User Macro using `user-macro-template.vm`
2. Make it available to your space
3. Provide you with usage instructions

### Option E: Third-Party Apps
Explore Atlassian Marketplace for:
- **Better Excel Exporter** - May support JIRA integration
- **Table Filter and Charts** - Advanced table functionality
- **Custom HTML** - Enhanced HTML embedding capabilities

---

## Method 1: Confluence User Macro (Requires Admin Access)

### Prerequisites
- Confluence Administrator access
- JIRA instance with REST API access
- JIRA API token for authentication

### Step 1: Generate JIRA API Token
1. Log in to your JIRA instance
2. Go to **Profile** → **Personal Access Tokens** (or **Security** → **API tokens** in older versions)
3. Create a new API token
4. Copy and save the token securely

### Step 2: Create User Macro in Confluence
1. Go to **Confluence Administration** (⚙️ → General Configuration)
2. Navigate to **User Macros** (under Configuration section)
3. Click **Create a User Macro**
4. Fill in the macro details:
   - **Macro Name**: `jira-grid`
   - **Macro Title**: `JIRA Issues Grid`
   - **Description**: `Display JIRA issues in a responsive grid format using JQL queries`
   - **Categories**: `External Content`
   - **Icon URL**: `/download/resources/confluence.extra.jira/images/icons/jira-16.png`

### Step 3: Configure Macro Parameters
Add the following parameters to your macro:

| Parameter Name | Type | Required | Default Value | Description |
|----------------|------|----------|---------------|-------------|
| `jql` | String | Yes | - | JQL query to execute |
| `fields` | String | No | `key,summary,status,assignee,priority` | Comma-separated field list |
| `maxResults` | String | No | `25` | Maximum number of results |
| `title` | String | No | `JIRA Issues` | Custom title for the grid |
| `baseUrl` | String | No | - | JIRA base URL (if different) |
| `username` | String | No | - | JIRA username |
| `apiToken` | String | No | - | JIRA API token |

### Step 4: Add Macro Template
1. In the **Template** section, copy and paste the content from `user-macro-template.vm`
2. Click **Save**

### Step 5: Use the Macro
1. Edit any Confluence page
2. Add the macro using one of these methods:
   - Type `{jira-grid` and select from the autocomplete
   - Use the macro browser (+ → Other macros → External Content → JIRA Issues Grid)

## Method 2: Direct HTML Implementation

### For Confluence Cloud
1. Install the **HTML Macro** app from Atlassian Marketplace
2. Create a new page or edit an existing one
3. Add the HTML macro
4. Copy the content from `jira-macro.html`
5. Update the configuration section with your JIRA details
6. Save the page

### For Confluence Server/Data Center
1. Edit a page in **Source Editor** mode
2. Copy the content from `jira-macro.html`
3. Update the configuration section
4. Save the page

## Configuration Examples

### Basic Usage
```
{jira-grid:jql=project = "MYPROJECT" AND status != "Done"}
```

### Advanced Usage with Custom Fields
```
{jira-grid:jql=assignee = currentUser() AND status in ("In Progress", "To Do")|fields=key,summary,status,assignee,priority,updated|maxResults=50|title=My Active Issues}
```

### With Authentication
```
{jira-grid:jql=project = "DEMO"|username=user@company.com|apiToken=your-api-token|baseUrl=https://company.atlassian.net}
```

## Security Considerations

### API Token Security
- **Never hardcode API tokens** in the macro parameters on public pages
- Use Confluence's **User Macros** feature which allows server-side parameter processing
- Consider using **Service Account** credentials for shared macros
- Regularly rotate API tokens

### CORS Configuration
- Ensure your JIRA instance allows requests from your Confluence domain
- Configure CORS headers in JIRA if needed:
  ```
  Access-Control-Allow-Origin: https://your-confluence-domain.com
  Access-Control-Allow-Methods: GET, POST, OPTIONS
  Access-Control-Allow-Headers: Authorization, Content-Type
  ```

### Authentication Options
1. **User API Tokens**: Each user provides their own credentials
2. **Service Account**: Single service account for all requests
3. **OAuth**: More secure but complex setup
4. **App Links**: Use Confluence-JIRA application links (if available)

## Troubleshooting

### Common Issues

#### 1. Authentication Errors
**Error**: "Failed to authenticate with JIRA"
**Solutions**:
- Verify API token is correct and not expired
- Check username format (usually email address)
- Ensure user has permission to access the queried projects

#### 2. CORS Errors
**Error**: "Cross-origin request blocked"
**Solutions**:
- Configure CORS headers in JIRA
- Use server-side proxy if needed
- Check browser console for specific CORS errors

#### 3. JQL Syntax Errors
**Error**: "Invalid JQL query"
**Solutions**:
- Test JQL in JIRA's Issues search
- Check field names and syntax
- Escape special characters properly

#### 4. No Results Displayed
**Possible Causes**:
- JQL query returns no results
- User doesn't have permission to view issues
- Field names are incorrect
- Network connectivity issues

### Debugging Steps

1. **Check Browser Console**: Look for JavaScript errors or network failures
2. **Test JQL Directly**: Run the JQL query in JIRA to verify it works
3. **Verify Permissions**: Ensure the user can see the projects/issues
4. **Test API Endpoint**: Use tools like Postman to test the JIRA REST API directly
5. **Check Network Tab**: Look for HTTP errors in browser developer tools

## Advanced Customization

### Custom Styling
- Modify the CSS in the macro template
- Use Confluence's theme customization
- Add custom CSS through space or site administration

### Additional Fields
- Add new field mappings to `FIELD_DISPLAY_NAMES`
- Implement custom field rendering in `renderFieldValue()`
- Update the default fields list as needed

### Performance Optimization
- Use pagination for large result sets
- Implement caching for frequently accessed data
- Consider server-side filtering for better performance

## Support and Maintenance

### Regular Tasks
- Monitor API token expiration
- Update field mappings when JIRA schema changes
- Review and update JQL queries as needed
- Check for Confluence/JIRA API updates

### Version Compatibility
- Test macro after Confluence/JIRA upgrades
- Update API endpoints if deprecated
- Monitor for changes in authentication methods

For additional support, consult your Confluence and JIRA documentation or contact your system administrator.
