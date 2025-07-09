# JIRA Data Aggregator - Python API

A Python-based implementation for fetching JIRA data via REST API and creating comprehensive summaries grouped by feature link and assignee.

## Features

- 🔌 **REST API Integration**: Direct connection to JIRA Cloud/Server via REST API
- 📊 **Time Tracking Aggregation**: Summarizes estimated, remaining, and spent hours
- 🎯 **Multi-Level Grouping**: Groups data by Feature Link and Assignee
- 📈 **Progress Tracking**: Calculates completion percentages
- 📋 **Multiple Export Formats**: Console output and Excel reports
- 🔗 **Smart Feature Linking**: Automatically detects Epic Links and related issues
- ⚙️ **Flexible Configuration**: JSON config file or environment variables

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure JIRA Connection**:
   
   **Option A: Configuration File**
   ```bash
   cp config.json.template config.json
   # Edit config.json with your JIRA details
   ```
   
   **Option B: Environment Variables**
   ```bash
   export JIRA_BASE_URL="https://your-domain.atlassian.net"
   export JIRA_USERNAME="your-email@domain.com"
   export JIRA_API_TOKEN="your-api-token"
   export JIRA_DEFAULT_JQL="project = \"YOUR_PROJECT\" AND status != \"Done\""
   ```

## Configuration

### config.json Structure
```json
{
    "base_url": "https://your-domain.atlassian.net",
    "username": "your-email@domain.com",
    "api_token": "your-api-token",
    "default_jql": "project = \"YOUR_PROJECT\" AND status != \"Done\"",
    "max_results": 1000
}
```

### Getting JIRA API Token
1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Enter a label and click "Create"
4. Copy the generated token

## Usage

### Basic Usage
```bash
python jira_data_aggregator.py
```

### Advanced Usage
```bash
# Use custom JQL query
python jira_data_aggregator.py --jql "project = \"MYPROJ\" AND assignee = currentUser()"

# Custom output filename
python jira_data_aggregator.py --output "my_report.xlsx"

# Console output only (no Excel file)
python jira_data_aggregator.py --console-only

# Use environment variables instead of config file
python jira_data_aggregator.py --use-env

# Custom configuration file
python jira_data_aggregator.py --config "/path/to/my-config.json"
```

## Output Examples

### Console Output
```
================================================================================
JIRA ISSUE SUMMARY - GROUPED BY FEATURE LINK AND ASSIGNEE
================================================================================

📋 Feature: PROJ-123 (User Authentication)
------------------------------------------------------------
  👤 John Doe                  | Estimated:   40.0h | Remaining:   20.0h | Spent:   20.0h | Issues:   5 | Complete:  50.0%
  👤 Jane Smith                | Estimated:   30.0h | Remaining:   10.0h | Spent:   20.0h | Issues:   3 | Complete:  66.7%
  TOTAL                        | Estimated:   70.0h | Remaining:   30.0h | Spent:   40.0h | Issues:   8 | Complete:  57.1%

📋 Feature: PROJ-124 (Payment Integration)
------------------------------------------------------------
  👤 Bob Wilson                | Estimated:   25.0h | Remaining:   15.0h | Spent:   10.0h | Issues:   4 | Complete:  40.0%
  TOTAL                        | Estimated:   25.0h | Remaining:   15.0h | Spent:   10.0h | Issues:   4 | Complete:  40.0%

================================================================================
GRAND TOTALS
================================================================================
Total Estimated Hours: 95.0
Total Remaining Hours: 45.0
Total Spent Hours: 50.0
Total Issues: 12
Overall Completion: 52.6%
```

### Excel Output

The script generates an Excel file with 4 sheets:

1. **Summary by Feature & Assignee**: Main aggregated view
2. **Detailed Issues**: Individual issue details
3. **Summary by Feature**: Feature-level aggregation
4. **Summary by Assignee**: Assignee-level aggregation

## Data Fields

### Input Fields (from JIRA)
- Issue Key, Summary, Status, Assignee, Priority
- Time Tracking: Original Estimate, Remaining Estimate, Time Spent
- Feature Links: Epic Links, Issue Links
- Dates: Created, Updated

### Output Aggregations
- **Estimated Hours**: Total original time estimates
- **Remaining Hours**: Current remaining work estimates
- **Spent Hours**: Actual time logged
- **Issue Count**: Number of issues per group
- **Completion %**: Progress percentage (Spent/Estimated × 100)

## Feature Link Detection

The script automatically detects feature relationships through:

1. **Epic Link** (customfield_10014 - common field)
2. **Issue Links** with types: epic-story, feature-story, relates
3. **Issue Types**: Automatically identifies Epic/Feature issues in links

If no feature link is found, issues are grouped under "No Feature Link".

## Error Handling

- **Connection Testing**: Validates JIRA API connectivity
- **Authentication**: Clear error messages for credential issues
- **Rate Limiting**: Handles JIRA API pagination and limits
- **Data Validation**: Handles missing or malformed data gracefully

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `--config` | `-c` | Path to configuration file (default: config.json) |
| `--jql` | `-j` | Custom JQL query to filter issues |
| `--output` | `-o` | Custom Excel output filename |
| `--console-only` | | Print only to console, skip Excel export |
| `--use-env` | | Use environment variables instead of config file |

## Example JQL Queries

```bash
# Issues assigned to current user
--jql "assignee = currentUser() AND status != Done"

# Issues in specific sprint
--jql "project = MYPROJ AND sprint in openSprints()"

# Issues updated in last week
--jql "updated >= -1w AND project = MYPROJ"

# High priority issues
--jql "priority in (High, Highest) AND status != Done"

# Issues with time tracking
--jql "originalEstimate is not EMPTY AND project = MYPROJ"
```

## Integration with Existing JavaScript Macro

This Python implementation can complement the existing JavaScript/HTML JIRA macro by:

1. **Batch Processing**: Handle large datasets that might timeout in browsers
2. **Advanced Analytics**: Provide detailed time tracking and progress analysis
3. **Scheduled Reports**: Run via cron jobs for regular reporting
4. **Data Export**: Generate Excel reports for stakeholder distribution
5. **API Flexibility**: Access more JIRA fields and advanced filtering

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Verify API token is correct and not expired
   - Ensure username matches the token owner
   - Check if 2FA is properly configured

2. **Connection Errors**:
   - Verify JIRA base URL is correct
   - Check network connectivity and firewall settings
   - Ensure JIRA instance is accessible

3. **No Data Returned**:
   - Verify JQL query syntax
   - Check user permissions for queried projects
   - Ensure issues exist matching the criteria

4. **Missing Time Tracking Data**:
   - Verify time tracking is enabled in JIRA
   - Check if issues have time estimates logged
   - Confirm user permissions to view time tracking

### Debug Mode

Enable debug logging by modifying the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Development

To extend the functionality:

1. **Custom Fields**: Add custom field mappings in `extract_issue_summary()`
2. **New Aggregations**: Extend `create_aggregated_summary()` method
3. **Export Formats**: Add new export methods (CSV, JSON, etc.)
4. **Visualization**: Integrate with matplotlib/plotly for charts

## License

This project is part of the JIRA Confluence Macro suite and follows the same licensing terms.
