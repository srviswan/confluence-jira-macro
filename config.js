/**
 * JIRA Configuration for Confluence Macro
 */
const JIRA_CONFIG = {
    // JIRA instance base URL (replace with your domain)
    baseUrl: 'https://your-domain.atlassian.net',
    
    // Authentication (use API token for security)
    username: 'your-email@domain.com',
    apiToken: 'your-api-token', // Generate from JIRA Profile → Security → API tokens
    
    // Default settings
    defaultJql: 'project = "YOUR_PROJECT" AND status != "Done"',
    defaultMaxResults: 25,
    defaultFields: ['key', 'summary', 'status', 'assignee', 'priority', 'updated'],
    
    // API endpoints
    searchEndpoint: '/rest/api/3/search',
    
    // Display options
    dateFormat: 'YYYY-MM-DD',
    truncateLength: 100,
    
    // Error messages
    errorMessages: {
        authentication: 'Failed to authenticate with JIRA. Please check your credentials.',
        network: 'Network error occurred. Please check your connection.',
        jql: 'Invalid JQL query. Please check your syntax.',
        general: 'An error occurred while fetching JIRA data.'
    }
};

// Field display names mapping
const FIELD_DISPLAY_NAMES = {
    'key': 'Issue Key',
    'summary': 'Summary',
    'status': 'Status',
    'assignee': 'Assignee',
    'priority': 'Priority',
    'updated': 'Updated',
    'created': 'Created',
    'reporter': 'Reporter',
    'issuetype': 'Issue Type',
    'project': 'Project',
    'fixVersions': 'Fix Version',
    'labels': 'Labels',
    'components': 'Components'
};

// Status color mapping
const STATUS_COLORS = {
    'To Do': '#42526E',
    'In Progress': '#0052CC',
    'Done': '#00875A',
    'Closed': '#00875A',
    'Open': '#DE350B',
    'Resolved': '#00875A',
    'Reopened': '#DE350B'
};

// Priority color mapping
const PRIORITY_COLORS = {
    'Highest': '#CD1316',
    'High': '#EA7D24',
    'Medium': '#E2B203',
    'Low': '#57A55A',
    'Lowest': '#8993A4'
};
