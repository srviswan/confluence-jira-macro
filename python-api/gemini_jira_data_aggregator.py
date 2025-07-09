import pandas as pd
from datetime import datetime, timedelta
from jira import JIRA # Make sure to install this: pip install jira

# --- JIRA API Configuration ---
# IMPORTANT: Replace with your Jira instance details and credentials
JIRA_SERVER = 'YOUR_JIRA_INSTANCE_URL' # e.g., 'https://yourcompany.atlassian.net'
JIRA_USERNAME = 'YOUR_JIRA_USERNAME'   # e.g., 'your.email@example.com'
JIRA_API_TOKEN = 'YOUR_JIRA_API_TOKEN' # Generate this in your Jira account settings

def fetch_jira_worklogs(jql_query, max_results=1000):
    """
    Fetches worklog data from Jira based on a JQL query.
    """
    try:
        # Authenticate with Jira
        jira_options = {'server': JIRA_SERVER}
        jira = JIRA(options=jira_options, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))
        print(f"Successfully connected to Jira server: {JIRA_SERVER}")

        # Search for issues using the provided JQL query
        # We need to expand 'worklog' to get the time logged details
        issues = jira.search_issues(jql_query, expand='changelog,worklog', maxResults=max_results)
        print(f"Found {len(issues)} issues matching the JQL query.")

        all_worklog_data = []

        for issue in issues:
            # Extract Feature Link (assuming it's the issue key or a custom field)
            # For simplicity, we'll use issue.key as 'Feature Link'.
            # If 'Feature Link' is a custom field, you'd access it like issue.fields.customfield_XXXXX
            feature_link = issue.key

            # Extract Assignee
            assignee_name = issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'

            # Iterate through worklogs for each issue
            for worklog in issue.fields.worklog.worklogs:
                # Jira stores time spent in seconds
                time_spent_seconds = worklog.timeSpentSeconds
                time_logged_hours = round(time_spent_seconds / 3600, 2) # Convert seconds to hours

                # Worklog creation date
                worklog_date = datetime.strptime(worklog.started[:10], '%Y-%m-%d') # Extract YYYY-MM-DD

                all_worklog_data.append({
                    'Date': worklog_date.strftime('%Y-%m-%d'),
                    'Feature Link': feature_link,
                    'Assignee': assignee_name,
                    'Time Logged (Hours)': time_logged_hours
                })
        print("Worklog data extracted from Jira issues.")
        return pd.DataFrame(all_worklog_data)

    except Exception as e:
        print(f"An error occurred while fetching data from Jira: {e}")
        return pd.DataFrame() # Return an empty DataFrame on error

def analyze_time_tracking(df):
    """
    Performs time tracking analysis, grouping by Feature Link and Assignee,
    and summing time logged on a weekly basis.
    """
    if df.empty:
        print("No data to analyze. Please check your Jira connection or JQL query.")
        return pd.DataFrame()

    # Convert 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])

    # Create a 'Week Start' column to group by week
    # This sets the date to the beginning of the week (Monday)
    df['Week Start'] = df['Date'].apply(lambda x: x - timedelta(days=x.weekday()))

    # Group by 'Feature Link', 'Assignee', and 'Week Start', then sum 'Time Logged'
    grouped_df = df.groupby(['Feature Link', 'Assignee', 'Week Start'])['Time Logged (Hours)'].sum().reset_index()

    # Sort the results for better readability
    grouped_df = grouped_df.sort_values(by=['Feature Link', 'Assignee', 'Week Start'])

    return grouped_df

def export_to_excel(df, filename="TimeTrackingAnalysis_Jira.xlsx"):
    """
    Exports the DataFrame to an Excel file with proper formatting.
    """
    if df.empty:
        print("No data to export to Excel.")
        return

    try:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
            # Write the DataFrame to a specific sheet
            df.to_excel(writer, sheet_name='Weekly Time Analysis', index=False)

            # Get the xlsxwriter workbook and worksheet objects.
            workbook = writer.book
            worksheet = writer.sheets['Weekly Time Analysis']

            # Add some formatting
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC', # Light green background
                'border': 1
            })

            # Apply header format to the first row (headers)
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)

            # Set column widths for better readability
            worksheet.set_column('A:A', 20) # Feature Link (increased width)
            worksheet.set_column('B:B', 20) # Assignee (increased width)
            worksheet.set_column('C:C', 15) # Week Start
            worksheet.set_column('D:D', 20) # Time Logged (Hours)

        print(f"Successfully created '{filename}'")
    except Exception as e:
        print(f"An error occurred while exporting to Excel: {e}")

if __name__ == "__main__":
    # --- JQL Query ---
    # Define your JQL query to fetch the relevant issues.
    # Examples:
    # "project = 'MyProject' AND worklogDate >= '2024-01-01'"
    # "assignee in ('user1', 'user2') AND status = 'Done' AND updated >= '-4w'"
    # "issuetype = Story AND statusCategory = 'Done'"
    JQL_QUERY = "project = 'YOUR_PROJECT_KEY' AND worklogDate >= '2024-01-01' ORDER BY updated DESC"

    # 1. Fetch data from Jira
    print("Fetching time tracking data from Jira...")
    jira_data_df = fetch_jira_worklogs(JQL_QUERY)
    if not jira_data_df.empty:
        print("Data fetched successfully from Jira.")
        # print(jira_data_df.head()) # Uncomment to see the raw Jira data

        # 2. Analyze the data
        print("Analyzing time tracking data...")
        analyzed_df = analyze_time_tracking(jira_data_df)
        print("Analysis complete.")
        # print(analyzed_df.head()) # Uncomment to see the analyzed data

        # 3. Export to Excel
        print("Exporting analyzed data to Excel...")
        export_to_excel(analyzed_df, "TimeTrackingAnalysis_Jira.xlsx")
        print("Process finished.")
    else:
        print("No data retrieved from Jira. Excel file will not be generated.")
