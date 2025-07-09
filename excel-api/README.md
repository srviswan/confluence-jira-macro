# JIRA Time Tracker Excel Macro

A powerful Excel VBA solution that connects directly to JIRA API to fetch and analyze time tracking data by feature and assignee for specific weeks.

## 🚀 **Key Features**

### **JIRA API Integration**
- **Direct API Connection**: Connects to JIRA Cloud/Server via REST API
- **Authentication**: Secure Basic Auth with username/API token
- **Custom JQL Support**: Filter data with custom JIRA Query Language
- **Automatic Pagination**: Handles large datasets efficiently

### **Time Tracking Analysis**
- **Weekly Time Logs**: Fetch time entries for specific date ranges
- **Feature Grouping**: Aggregate by Epic Link/Feature Link automatically  
- **Assignee Analysis**: Group and summarize by team member
- **Multi-dimensional Views**: Raw data + aggregated summaries

### **Excel-Native Experience**
- **User-Friendly Interface**: Dashboard with configuration forms and buttons
- **Multiple Worksheets**: Organized data across Config, Settings, Raw Data, and Summary sheets
- **Interactive Controls**: Quick date range selection (This Week, Last Week, This Month)
- **Automatic Formatting**: Professional charts and formatted tables

### **Business Intelligence**
- **Time Investment Analysis**: See where team time is being spent
- **Feature Progress Tracking**: Monitor progress across epics/features
- **Resource Allocation**: Understand team member workload distribution
- **Historical Reporting**: Analyze any date range for retrospectives

## 📋 **Requirements**

- **Microsoft Excel** with VBA support (Excel 2010 or later)
- **JIRA Cloud** or **JIRA Server** with REST API access
- **API Token** for authentication (for JIRA Cloud)
- **Internet Connection** for API calls

## 🛠️ **Installation**

### **Step 1: Enable Excel Macros**
1. Open Excel
2. Go to `File` → `Options` → `Trust Center` → `Trust Center Settings`
3. Select `Macro Settings` 
4. Choose `Enable all macros` (or `Disable with notification`)
5. Click `OK`

### **Step 2: Import VBA Code**
1. Press `Alt + F11` to open VBA Editor
2. In the Project Explorer, right-click on your workbook
3. Select `Insert` → `Module`
4. Copy and paste the contents of `JiraApiModule.bas`
5. Insert another module and paste `WorksheetSetup.bas`
6. Save the workbook as `.xlsm` (macro-enabled)

### **Step 3: Setup Worksheets**
1. In VBA Editor, press `F5` or go to `Run` → `Run Sub/UserForm`
2. Select `SetupWorksheets` and click `Run`
3. This creates all required worksheets with proper formatting

## ⚙️ **Configuration**

### **1. JIRA API Configuration**
Navigate to the **Config** sheet and fill in:

| Field | Description | Example |
|-------|-------------|---------|
| **JIRA Base URL** | Your JIRA instance URL | `https://yourcompany.atlassian.net` |
| **Username** | Your JIRA username/email | `john.doe@company.com` |
| **API Token** | JIRA API token | `ATATTxxxxxxxxxx` |
| **Default JQL** | Optional filter query | `project = "MyProject" AND assignee != empty` |

### **2. Get JIRA API Token**
1. Go to [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click `Create API token`
3. Enter a label (e.g., "Excel Time Tracker")
4. Copy the generated token to Excel Config sheet

### **3. Date Range Settings**
Navigate to the **Settings** sheet:
- **Start Date**: First day of the period to analyze
- **End Date**: Last day of the period to analyze
- Use quick buttons: `This Week`, `Last Week`, `This Month`

## 🎯 **Usage**

### **Basic Workflow**
1. **Configure**: Set up JIRA connection in Config sheet
2. **Set Dates**: Choose date range in Settings sheet  
3. **Import**: Click `🔄 Fetch JIRA Data` on Dashboard
4. **Analyze**: Review results in Raw Data and Summary sheets

### **Data Import Process**
1. **API Connection**: Tests connection to JIRA
2. **Query Construction**: Builds JQL query with date filters
3. **Data Fetching**: Retrieves issues and worklog entries
4. **Processing**: Extracts time logs within date range
5. **Aggregation**: Groups by Feature Link and Assignee
6. **Output**: Populates Excel sheets with formatted data

### **Understanding the Output**

#### **Raw Data Sheet**
- **Issue Key**: JIRA ticket identifier (e.g., PROJ-123)
- **Issue Summary**: Ticket title/description
- **Assignee**: Person who logged the time
- **Feature Link**: Epic or parent issue (for grouping)
- **Hours Logged**: Time spent in decimal hours
- **Date Logged**: When the work was performed
- **Author**: Who logged the time entry
- **Work Description**: Comments about the work done

#### **Summary Sheet**
- **Feature Link**: Epic/Feature grouping
- **Assignee**: Team member name
- **Total Hours**: Sum of time logged for this combination
- **Issue Count**: Number of tickets worked on

## 📊 **Business Use Cases**

### **Project Management**
- **Sprint Retrospectives**: Analyze time spent during sprint periods
- **Feature Progress**: Track development effort across epics
- **Capacity Planning**: Understand team member availability and workload

### **Resource Management**
- **Team Utilization**: See how team members are spending time
- **Cross-Feature Work**: Identify people working across multiple features
- **Bottleneck Identification**: Find features requiring excessive time

### **Stakeholder Reporting**
- **Executive Summaries**: High-level time investment by feature
- **Client Billing**: Detailed time tracking for consulting/services
- **Budget Analysis**: Compare planned vs. actual effort

## 🔧 **Customization**

### **Custom Fields**
To use different Epic/Feature link fields:
1. Open `JiraApiModule.bas` in VBA Editor
2. Find the line: `customfield_10014` (Epic Link field)
3. Replace with your custom field ID
4. Save and test

### **Additional JQL Filters**
Common JQL examples for Default JQL field:
```sql
-- Specific project only
project = "MYPROJECT"

-- Exclude certain issue types
project = "MYPROJECT" AND issuetype != "Sub-task"

-- Specific assignees only
project = "MYPROJECT" AND assignee in ("john.doe", "jane.smith")

-- Include resolved issues
project = "MYPROJECT" AND status in ("Done", "Closed", "Resolved")
```

### **Date Range Modifications**
To add custom date range buttons:
1. Edit `WorksheetSetup.bas`
2. Add new button in `AddDateRangeButtons` function
3. Create corresponding date calculation function

## 🐛 **Troubleshooting**

### **Common Issues**

#### **"Authentication Failed"**
- ✅ Verify JIRA Base URL (no trailing slash)
- ✅ Check username/email is correct
- ✅ Ensure API token is valid and copied completely
- ✅ Test access in browser: `https://yourjira.com/rest/api/2/myself`

#### **"No Data Returned"**
- ✅ Verify date range includes working days
- ✅ Check if JQL query is too restrictive
- ✅ Ensure issues have worklog entries in date range
- ✅ Test JQL in JIRA web interface first

#### **"Script Timeout"**
- ✅ Reduce date range (try 1 week at a time)
- ✅ Add more specific JQL filters
- ✅ Check internet connection stability

#### **"Permission Denied"**
- ✅ Ensure user has permission to view time logs
- ✅ Check project-level permissions in JIRA
- ✅ Verify API token has correct scopes

### **Advanced Debugging**
1. Press `Ctrl + G` in VBA Editor to open Immediate Window
2. Add debug statements: `Debug.Print variable_name`
3. Check JIRA API responses for error details
4. Test individual functions separately

## 🔒 **Security Best Practices**

### **API Token Management**
- 🔐 Never share your API token
- 🔐 Store tokens securely (consider environment variables)
- 🔐 Regularly rotate API tokens (every 90 days)
- 🔐 Use minimal required permissions

### **Network Security**
- 🛡️ Use HTTPS URLs only
- 🛡️ Verify SSL certificates
- 🛡️ Consider VPN for internal JIRA instances
- 🛡️ Monitor API usage logs

## 📈 **Performance Tips**

### **Optimize API Calls**
- **Narrow Date Ranges**: Start with 1-2 weeks for testing
- **Specific JQL**: Use project filters to reduce data volume
- **Field Selection**: Only fetch required fields
- **Pagination**: Let the system handle large datasets automatically

### **Excel Performance**
- **Disable Screen Updates**: Automatic during processing
- **Calculation Mode**: Temporarily set to manual
- **Close Other Applications**: Free up system resources
- **Regular Saves**: Save workbook after successful imports

## 🔄 **Version History**

### **Version 1.0** (Initial Release)
- ✅ JIRA API integration with Basic Auth
- ✅ Time log fetching for date ranges
- ✅ Feature and assignee aggregation
- ✅ Multi-sheet Excel output
- ✅ Dashboard interface with buttons
- ✅ Quick date range selection

### **Planned Enhancements**
- 📅 OAuth 2.0 authentication support
- 📅 Custom field mapping interface  
- 📅 Advanced charting and visualizations
- 📅 Export to PowerPoint reports
- 📅 Scheduled/automated imports
- 📅 Multi-project aggregation

## 🤝 **Contributing**

### **Reporting Issues**
1. Check existing documentation first
2. Test with minimal configuration
3. Provide error messages and steps to reproduce
4. Include JIRA version and Excel version

### **Feature Requests**
1. Describe the business use case
2. Provide examples of expected output
3. Consider backward compatibility
4. Suggest implementation approach

## 📞 **Support**

### **Documentation**
- **This README**: Comprehensive setup and usage guide
- **Code Comments**: Detailed inline documentation in VBA modules
- **Example Configurations**: Sample JQL queries and settings

### **Self-Help**
1. **Test Connection**: Use JIRA web interface to verify credentials
2. **Simplify Query**: Start with basic JQL, add complexity gradually
3. **Check Permissions**: Ensure JIRA user can view time logs
4. **Review Logs**: Use VBA Debug.Print for detailed troubleshooting

---

## 🎉 **Getting Started**

Ready to start tracking your team's JIRA time investment?

1. **Download** the VBA files from this repository
2. **Follow** the installation steps above  
3. **Configure** your JIRA connection
4. **Import** your first week of data
5. **Analyze** the results and insights

Transform your JIRA time tracking data into actionable business intelligence with this powerful Excel solution!

---

*Built for teams who need advanced JIRA time tracking analysis without leaving Excel*
