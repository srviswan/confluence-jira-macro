# Confluence JIRA Macro

A comprehensive JavaScript-based Confluence macro that integrates with JIRA REST API to display issues in a responsive, sortable grid format with advanced filtering and customization options.

## Features

- **JQL Query Support**: Execute custom JQL queries to filter issues
- **Responsive Grid**: Mobile-friendly table with sortable columns
- **Real-time Search**: Filter displayed issues with instant search
- **Customizable Fields**: Configure which JIRA fields to display
- **Status Badges**: Color-coded status indicators
- **Pagination Support**: Handle large result sets efficiently
- **Error Handling**: User-friendly error messages and loading states
- **Secure Authentication**: Basic auth with API tokens
- **Interactive Demo**: Test the macro before deployment
- **Multiple Deployment Options**: User macro, HTML macro, or standalone
- **Python API**: Advanced data aggregation and time tracking analysis

## Project Structure

```
confluence-jira-macro/
├── README.md                      # Main documentation
├── config.js                      # Configuration settings
├── jira-macro.css                # Styling for the grid
├── jira-macro.js                 # Core JavaScript functionality
├── jira-macro.html               # Standalone HTML version
├── user-macro-template.vm        # Confluence User Macro template
├── setup-instructions.md         # Detailed setup guide
├── example-usage.md              # Usage examples and JQL queries
├── demo.html                     # Interactive demo page
└── python-api/                   # Python-based data aggregation
    ├── jira_data_aggregator.py   # Main aggregation script
    ├── field_inspector.py        # JIRA field discovery utility
    ├── example_usage.py          # Usage examples
    ├── config.json.template      # Configuration template
    ├── requirements.txt          # Python dependencies
    ├── run_aggregator.sh         # Batch execution script
    └── README.md                 # Python API documentation
```

## Quick Start

### Option 1: Confluence User Macro (Recommended)
1. Follow the detailed instructions in `setup-instructions.md`
2. Copy the Velocity template from `user-macro-template.vm`
3. Create a new User Macro in Confluence Administration
4. Configure macro parameters and use in any page

### Option 2: Interactive Demo
1. Open `demo.html` in your browser
2. Configure your JIRA connection details
3. Test different scenarios and JQL queries
4. Copy the working configuration for production use

### Option 3: Direct HTML Embedding
1. Use `jira-macro.html` for simple HTML macro embedding
2. Update configuration section with your JIRA details
3. Paste into Confluence HTML macro or page source

### Option 4: Python API (Advanced Analytics)

**NEW!** The Python API provides advanced data aggregation and time tracking analysis capabilities:

#### Key Features:
- **Time Tracking Aggregation**: Summarizes estimated, remaining, and spent hours
- **Multi-Level Grouping**: Groups by Feature Link (Epic) and Assignee
- **Progress Analysis**: Calculates completion percentages and project health
- **Excel Reports**: Generates comprehensive reports with multiple sheets
- **Batch Processing**: Handles large datasets efficiently
- **Field Discovery**: Utility to inspect available JIRA fields

#### Quick Start:
```bash
cd python-api
./run_aggregator.sh help          # Show available options
./run_aggregator.sh test          # Test JIRA connection
./run_aggregator.sh console       # View summary in console
./run_aggregator.sh excel         # Generate Excel report
```

#### Use Cases:
- **Project Managers**: Track progress across features and team members
- **Scrum Masters**: Generate sprint and team velocity reports
- **Stakeholders**: Get executive summaries with completion metrics
- **Resource Planning**: Analyze workload distribution and capacity

See `python-api/README.md` for detailed documentation and examples.

## Configuration

Update the configuration in `config.js` or directly in the HTML:

```javascript
const JIRA_CONFIG = {
    baseUrl: 'https://your-domain.atlassian.net',
    username: 'your-email@domain.com',
    apiToken: 'your-api-token',
    defaultJQL: 'project IS NOT EMPTY AND status != "Done"',
    maxResults: 25,
    fields: ['key', 'summary', 'status', 'assignee', 'priority']
};
```

## Usage Examples

See `example-usage.md` for comprehensive examples including:

### Basic Usage
```
{jira-grid:jql=project = "MYPROJECT" AND status != "Done"}
```

### Personal Dashboard
```
{jira-grid:jql=assignee = currentUser() AND status != "Done"|title=My Active Tasks}
```

### Team Sprint View
```
{jira-grid:jql=project = "TEAM" AND sprint in openSprints()|fields=key,summary,status,assignee,storyPoints|title=Current Sprint}
```

### High Priority Issues
```
{jira-grid:jql=priority in ("Critical", "High") AND status != "Done"|fields=key,summary,status,assignee,priority,updated|title=Urgent Items}
```

## Files Overview

### Core Files
- **`config.js`**: Central configuration for JIRA connection and display settings
- **`jira-macro.css`**: Complete styling including responsive design and themes
- **`jira-macro.js`**: Main JavaScript with API integration, sorting, and filtering
- **`jira-macro.html`**: Standalone version combining all components

### Templates and Setup
- **`user-macro-template.vm`**: Velocity template for Confluence User Macros
- **`setup-instructions.md`**: Step-by-step deployment guide with troubleshooting
- **`example-usage.md`**: 25+ real-world usage examples with JQL queries

### Testing and Demo
- **`demo.html`**: Interactive demo with scenario testing and connection validation

## Security

- Uses JIRA API tokens for secure authentication
- Supports both user-specific and service account credentials
- Configurable CORS settings for cross-domain requests
- No sensitive data stored in browser localStorage
- Detailed security considerations in setup instructions

## Browser Support

- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+
- Mobile browsers (responsive design)

## JIRA API Requirements

- JIRA Cloud, Server, or Data Center
- REST API v3 (v2 compatible)
- Valid user account with issue viewing permissions
- API token for authentication
- Appropriate CORS configuration for browser requests

## Deployment Options

1. **Confluence User Macro**: Full integration with parameter configuration
2. **HTML Macro**: Simple embedding with inline configuration
3. **Page Source**: Direct HTML insertion for advanced users
4. **Standalone Page**: Independent web page for testing or external use

## Advanced Features

- **Custom Field Support**: Display any JIRA field including custom fields
- **Multi-project Queries**: Cross-project issue aggregation
- **Time-based Filtering**: Recent updates, overdue items, etc.
- **Status Color Coding**: Configurable status badge colors
- **Responsive Tables**: Mobile-optimized display
- **Error Recovery**: Graceful handling of network and authentication errors

## Troubleshooting

See `setup-instructions.md` for detailed troubleshooting including:

### Common Issues
1. **Authentication Errors**: API token validation and user permissions
2. **CORS Errors**: Cross-origin configuration and proxy solutions
3. **Permission Errors**: Project access and field visibility
4. **JQL Syntax Errors**: Query validation and testing
5. **Display Issues**: Field mapping and custom field handling

### Debug Tools
- Interactive demo for connection testing
- Browser console logging
- Network request inspection
- JQL query validation

## Examples and Scenarios

The `example-usage.md` file contains 25+ practical examples:
- Personal task management
- Team dashboards
- Project tracking
- Bug management
- Release planning
- Executive reporting
- Support ticket tracking

## Getting Started

1. **Test First**: Use `demo.html` to validate your JIRA connection
2. **Choose Deployment**: Select User Macro for full integration
3. **Follow Setup Guide**: Use `setup-instructions.md` for step-by-step deployment
4. **Explore Examples**: Reference `example-usage.md` for inspiration
5. **Customize**: Modify CSS and configuration for your needs

## License

MIT License - feel free to modify and distribute.

## Support

For issues and feature requests:
1. Test with the interactive demo first
2. Check setup instructions and troubleshooting section
3. Verify JIRA API permissions and configuration
4. Review browser console for detailed error messages
