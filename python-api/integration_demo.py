#!/usr/bin/env python3
"""
Integration Demo for JIRA Data Aggregator
Demonstrates real-world scenarios without requiring actual JIRA connection
"""

import pandas as pd
from datetime import datetime, timedelta
import json
import sys
import os

def simulate_jira_data():
    """Create simulated JIRA data for demonstration"""
    
    # Simulate typical JIRA issue structure
    simulated_issues = [
        {
            'key': 'PROJ-101',
            'fields': {
                'summary': 'User Authentication System',
                'status': {'name': 'In Progress'},
                'assignee': {'displayName': 'John Doe'},
                'priority': {'name': 'High'},
                'issuetype': {'name': 'Epic'},
                'created': '2024-01-15T09:00:00.000+0000',
                'updated': '2024-01-20T15:30:00.000+0000',
                'timeoriginalestimate': 144000,  # 40 hours in seconds
                'timeestimate': 72000,           # 20 hours remaining
                'timespent': 72000,              # 20 hours spent
                'customfield_10014': 'PROJ-100',  # Epic link
                'issuelinks': []
            }
        },
        {
            'key': 'PROJ-102',
            'fields': {
                'summary': 'Login Form Implementation',
                'status': {'name': 'Done'},
                'assignee': {'displayName': 'Jane Smith'},
                'priority': {'name': 'Medium'},
                'issuetype': {'name': 'Story'},
                'created': '2024-01-16T10:00:00.000+0000',
                'updated': '2024-01-19T16:00:00.000+0000',
                'timeoriginalestimate': 28800,   # 8 hours
                'timeestimate': 0,               # 0 hours remaining
                'timespent': 32400,              # 9 hours spent (overtime)
                'customfield_10014': 'PROJ-101',  # Links to authentication epic
                'issuelinks': []
            }
        },
        {
            'key': 'PROJ-103',
            'fields': {
                'summary': 'Password Reset Feature',
                'status': {'name': 'In Progress'},
                'assignee': {'displayName': 'John Doe'},
                'priority': {'name': 'Medium'},
                'issuetype': {'name': 'Story'},
                'created': '2024-01-17T11:00:00.000+0000',
                'updated': '2024-01-21T14:00:00.000+0000',
                'timeoriginalestimate': 21600,   # 6 hours
                'timeestimate': 10800,           # 3 hours remaining
                'timespent': 10800,              # 3 hours spent
                'customfield_10014': 'PROJ-101',  # Links to authentication epic
                'issuelinks': []
            }
        },
        {
            'key': 'PROJ-201',
            'fields': {
                'summary': 'Payment Integration',
                'status': {'name': 'To Do'},
                'assignee': {'displayName': 'Bob Wilson'},
                'priority': {'name': 'High'},
                'issuetype': {'name': 'Epic'},
                'created': '2024-01-18T12:00:00.000+0000',
                'updated': '2024-01-18T12:00:00.000+0000',
                'timeoriginalestimate': 180000,  # 50 hours
                'timeestimate': 180000,          # 50 hours remaining
                'timespent': 0,                  # 0 hours spent
                'customfield_10014': None,       # No parent epic
                'issuelinks': []
            }
        },
        {
            'key': 'PROJ-202',
            'fields': {
                'summary': 'Stripe Integration Setup',
                'status': {'name': 'In Progress'},
                'assignee': {'displayName': 'Alice Johnson'},
                'priority': {'name': 'High'},
                'issuetype': {'name': 'Story'},
                'created': '2024-01-19T13:00:00.000+0000',
                'updated': '2024-01-22T10:00:00.000+0000',
                'timeoriginalestimate': 36000,   # 10 hours
                'timeestimate': 21600,           # 6 hours remaining
                'timespent': 14400,              # 4 hours spent
                'customfield_10014': 'PROJ-201', # Links to payment epic
                'issuelinks': []
            }
        },
        {
            'key': 'PROJ-104',
            'fields': {
                'summary': 'OAuth Implementation',
                'status': {'name': 'To Do'},
                'assignee': None,  # Unassigned
                'priority': {'name': 'Low'},
                'issuetype': {'name': 'Story'},
                'created': '2024-01-20T14:00:00.000+0000',
                'updated': '2024-01-20T14:00:00.000+0000',
                'timeoriginalestimate': 43200,   # 12 hours
                'timeestimate': 43200,           # 12 hours remaining
                'timespent': 0,                  # 0 hours spent
                'customfield_10014': 'PROJ-101', # Links to authentication epic
                'issuelinks': []
            }
        }
    ]
    
    return simulated_issues

def simulate_aggregation_process():
    """Simulate the aggregation process with demo data"""
    print("🔄 SIMULATING JIRA DATA AGGREGATION PROCESS")
    print("=" * 60)
    
    # Get simulated data
    issues = simulate_jira_data()
    print(f"📊 Fetched {len(issues)} issues from JIRA (simulated)")
    
    # Process issues similar to the real aggregator
    processed_data = []
    
    for issue in issues:
        fields = issue.get('fields', {})
        
        # Extract assignee
        assignee = fields.get('assignee')
        assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
        
        # Extract time tracking (convert seconds to hours)
        estimated_hours = (fields.get('timeoriginalestimate', 0) or 0) / 3600
        remaining_hours = (fields.get('timeestimate', 0) or 0) / 3600
        spent_hours = (fields.get('timespent', 0) or 0) / 3600
        
        # Extract feature link
        feature_link = fields.get('customfield_10014', 'No Feature Link')
        if not feature_link:
            feature_link = 'No Feature Link'
        
        processed_data.append({
            'Issue Key': issue.get('key'),
            'Summary': fields.get('summary', ''),
            'Assignee': assignee_name,
            'Feature Link': feature_link,
            'Estimated Hours': estimated_hours,
            'Remaining Hours': remaining_hours,
            'Spent Hours': spent_hours,
            'Status': fields.get('status', {}).get('name', ''),
            'Priority': fields.get('priority', {}).get('name', ''),
            'Issue Type': fields.get('issuetype', {}).get('name', '')
        })
    
    # Create DataFrame
    df = pd.DataFrame(processed_data)
    
    print("\n📋 DETAILED ISSUE DATA:")
    print("-" * 40)
    for _, row in df.iterrows():
        print(f"🎫 {row['Issue Key']}: {row['Summary'][:40]}...")
        print(f"   👤 {row['Assignee']} | 🔗 {row['Feature Link']}")
        print(f"   ⏱️  Est: {row['Estimated Hours']:.1f}h | Rem: {row['Remaining Hours']:.1f}h | Spent: {row['Spent Hours']:.1f}h")
        print()
    
    # Create aggregated summary
    summary_df = df.groupby(['Feature Link', 'Assignee']).agg({
        'Estimated Hours': 'sum',
        'Remaining Hours': 'sum', 
        'Spent Hours': 'sum',
        'Issue Key': 'count'
    }).round(2)
    
    summary_df.rename(columns={'Issue Key': 'Issue Count'}, inplace=True)
    summary_df['Completion %'] = (
        (summary_df['Spent Hours'] / summary_df['Estimated Hours'] * 100)
        .fillna(0)
        .round(1)
    )
    summary_df = summary_df.reset_index()
    
    return df, summary_df

def print_aggregated_summary(summary_df):
    """Print the aggregated summary similar to the real aggregator"""
    print("\n" + "="*80)
    print("SIMULATED JIRA ISSUE SUMMARY - GROUPED BY FEATURE LINK AND ASSIGNEE")
    print("="*80)
    
    for feature_link in summary_df['Feature Link'].unique():
        feature_data = summary_df[summary_df['Feature Link'] == feature_link]
        
        print(f"\n📋 Feature: {feature_link}")
        print("-" * 60)
        
        for _, row in feature_data.iterrows():
            print(f"  👤 {row['Assignee']:<20} | "
                  f"Estimated: {row['Estimated Hours']:>6.1f}h | "
                  f"Remaining: {row['Remaining Hours']:>6.1f}h | "
                  f"Spent: {row['Spent Hours']:>6.1f}h | "
                  f"Issues: {row['Issue Count']:>3} | "
                  f"Complete: {row['Completion %']:>5.1f}%")
        
        # Feature totals
        feature_totals = feature_data.sum(numeric_only=True)
        completion_pct = (feature_totals['Spent Hours'] / feature_totals['Estimated Hours'] * 100) if feature_totals['Estimated Hours'] > 0 else 0
        
        print(f"  {'TOTAL':<20} | "
              f"Estimated: {feature_totals['Estimated Hours']:>6.1f}h | "
              f"Remaining: {feature_totals['Remaining Hours']:>6.1f}h | "
              f"Spent: {feature_totals['Spent Hours']:>6.1f}h | "
              f"Issues: {feature_totals['Issue Count']:>3} | "
              f"Complete: {completion_pct:>5.1f}%")
    
    # Grand totals
    grand_totals = summary_df.sum(numeric_only=True)
    grand_completion = (grand_totals['Spent Hours'] / grand_totals['Estimated Hours'] * 100) if grand_totals['Estimated Hours'] > 0 else 0
    
    print("\n" + "="*80)
    print("GRAND TOTALS")
    print("="*80)
    print(f"Total Estimated Hours: {grand_totals['Estimated Hours']:.1f}")
    print(f"Total Remaining Hours: {grand_totals['Remaining Hours']:.1f}")
    print(f"Total Spent Hours: {grand_totals['Spent Hours']:.1f}")
    print(f"Total Issues: {grand_totals['Issue Count']}")
    print(f"Overall Completion: {grand_completion:.1f}%")

def demonstrate_excel_export(detailed_df, summary_df):
    """Demonstrate Excel export functionality"""
    print("\n" + "="*60)
    print("📊 EXCEL EXPORT SIMULATION")
    print("="*60)
    
    filename = f"demo_jira_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Summary sheet
            summary_df.to_excel(writer, sheet_name='Summary by Feature & Assignee', index=False)
            
            # Detailed issues sheet
            detailed_df.to_excel(writer, sheet_name='Detailed Issues', index=False)
            
            # Feature-only summary
            feature_summary = detailed_df.groupby('Feature Link').agg({
                'Estimated Hours': 'sum',
                'Remaining Hours': 'sum',
                'Spent Hours': 'sum',
                'Issue Key': 'count'
            }).round(2)
            feature_summary.rename(columns={'Issue Key': 'Issue Count'}, inplace=True)
            feature_summary['Completion %'] = (
                (feature_summary['Spent Hours'] / feature_summary['Estimated Hours'] * 100)
                .fillna(0)
                .round(1)
            )
            feature_summary.to_excel(writer, sheet_name='Summary by Feature')
            
            # Assignee-only summary
            assignee_summary = detailed_df.groupby('Assignee').agg({
                'Estimated Hours': 'sum',
                'Remaining Hours': 'sum',
                'Spent Hours': 'sum',
                'Issue Key': 'count'
            }).round(2)
            assignee_summary.rename(columns={'Issue Key': 'Issue Count'}, inplace=True)
            assignee_summary['Completion %'] = (
                (assignee_summary['Spent Hours'] / assignee_summary['Estimated Hours'] * 100)
                .fillna(0)
                .round(1)
            )
            assignee_summary.to_excel(writer, sheet_name='Summary by Assignee')
        
        print(f"✅ Excel report generated: {filename}")
        print(f"📋 4 sheets created:")
        print(f"   1. Summary by Feature & Assignee")
        print(f"   2. Detailed Issues") 
        print(f"   3. Summary by Feature")
        print(f"   4. Summary by Assignee")
        
        # Show file size
        file_size = os.path.getsize(filename)
        print(f"📁 File size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Excel export failed: {e}")

def show_real_world_scenarios():
    """Show real-world usage scenarios"""
    print("\n" + "="*60)
    print("🌍 REAL-WORLD USAGE SCENARIOS")
    print("="*60)
    
    scenarios = [
        {
            "title": "Daily Standup Report",
            "description": "Generate current sprint progress for team standup",
            "command": "python jira_data_aggregator.py --jql \"sprint in openSprints()\" --console-only",
            "frequency": "Daily"
        },
        {
            "title": "Weekly Manager Report", 
            "description": "Executive summary with completion metrics",
            "command": "python jira_data_aggregator.py --output \"weekly_$(date +%Y%m%d).xlsx\"",
            "frequency": "Weekly"
        },
        {
            "title": "Individual Developer Report",
            "description": "Personal task tracking and time analysis",
            "command": "python jira_data_aggregator.py --jql \"assignee = currentUser()\" --console-only",
            "frequency": "As needed"
        },
        {
            "title": "Feature Progress Analysis",
            "description": "Deep dive into specific epic or feature development",
            "command": "python jira_data_aggregator.py --jql \"\\\"Epic Link\\\" = PROJ-123\"",
            "frequency": "Per feature cycle"
        },
        {
            "title": "Resource Capacity Planning",
            "description": "Analyze team workload and remaining capacity",
            "command": "python jira_data_aggregator.py --jql \"remainingEstimate > 0\"",
            "frequency": "Sprint planning"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. 🎯 {scenario['title']}")
        print(f"   📝 {scenario['description']}")
        print(f"   💻 {scenario['command']}")
        print(f"   🔄 Frequency: {scenario['frequency']}")

def main():
    """Main demonstration function"""
    print("🚀 JIRA DATA AGGREGATOR - INTEGRATION DEMO")
    print("=" * 60)
    print("This demo simulates the Python API functionality without requiring")
    print("a real JIRA connection. It shows how the aggregation works with")
    print("realistic project data.")
    print()
    
    # Simulate the aggregation process
    detailed_df, summary_df = simulate_aggregation_process()
    
    # Print aggregated summary
    print_aggregated_summary(summary_df)
    
    # Demonstrate Excel export
    if len(sys.argv) > 1 and sys.argv[1] == '--excel':
        demonstrate_excel_export(detailed_df, summary_df)
    
    # Show real-world scenarios
    show_real_world_scenarios()
    
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETED!")
    print("="*60)
    print("To use with real JIRA data:")
    print("1. Update config.json with your JIRA credentials")
    print("2. Run: python jira_data_aggregator.py --console-only")
    print("3. Or use: ./run_aggregator.sh test")
    print()
    print("For more examples: python example_usage.py")

if __name__ == "__main__":
    main()
