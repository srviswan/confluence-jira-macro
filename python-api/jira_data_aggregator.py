#!/usr/bin/env python3
"""
JIRA Data Aggregator - Python Implementation
Fetches data via REST API and creates summaries grouped by feature link and assignee
"""

import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import sys
import argparse
from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
from urllib.parse import quote
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class JiraConfig:
    """Configuration for JIRA API connection"""
    base_url: str
    username: str
    api_token: str
    default_jql: str = 'project IS NOT EMPTY AND status != "Done"'
    max_results: int = 1000
    
    @classmethod
    def from_file(cls, config_path: str = 'config.json'):
        """Load configuration from JSON file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file {config_path} not found")
        
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        return cls(**config_data)
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        return cls(
            base_url=os.getenv('JIRA_BASE_URL', ''),
            username=os.getenv('JIRA_USERNAME', ''),
            api_token=os.getenv('JIRA_API_TOKEN', ''),
            default_jql=os.getenv('JIRA_DEFAULT_JQL', 'project IS NOT EMPTY AND status != "Done"'),
            max_results=int(os.getenv('JIRA_MAX_RESULTS', '1000'))
        )

@dataclass
class IssueSummary:
    """Data structure for issue summary metrics"""
    key: str
    summary: str
    assignee: str
    feature_link: str
    estimated_hours: float
    remaining_hours: float
    spent_hours: float
    status: str
    priority: str
    issue_type: str
    created: str
    updated: str

class JiraDataAggregator:
    """Main class for fetching and aggregating JIRA data"""
    
    def __init__(self, config: JiraConfig):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.username, config.api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
    def test_connection(self) -> bool:
        """Test JIRA API connection"""
        try:
            url = f"{self.config.base_url}/rest/api/3/myself"
            response = self.session.get(url)
            response.raise_for_status()
            logger.info("JIRA connection successful")
            return True
        except requests.RequestException as e:
            logger.error(f"JIRA connection failed: {e}")
            return False
    
    def fetch_issues(self, jql: Optional[str] = None, additional_fields: List[str] = None) -> List[Dict[str, Any]]:
        """Fetch issues from JIRA using JQL query"""
        if jql is None:
            jql = self.config.default_jql
            
        # Essential fields for time tracking and grouping
        base_fields = [
            'key', 'summary', 'status', 'assignee', 'priority', 'issuetype',
            'created', 'updated', 'timetracking', 'timeoriginalestimate',
            'timeestimate', 'timespent', 'aggregatetimeoriginalestimate',
            'aggregatetimeestimate', 'aggregatetimespent', 'issuelinks',
            'customfield_10014'  # Epic Link (commonly used for feature links)
        ]
        
        if additional_fields:
            base_fields.extend(additional_fields)
        
        fields = ','.join(set(base_fields))
        
        url = f"{self.config.base_url}/rest/api/3/search"
        
        all_issues = []
        start_at = 0
        max_results = min(self.config.max_results, 100)  # JIRA API limit per request
        
        while True:
            params = {
                'jql': jql,
                'fields': fields,
                'maxResults': max_results,
                'startAt': start_at
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                issues = data.get('issues', [])
                
                if not issues:
                    break
                    
                all_issues.extend(issues)
                
                if len(issues) < max_results:
                    break
                    
                start_at += max_results
                logger.info(f"Fetched {len(all_issues)} issues so far...")
                
            except requests.RequestException as e:
                logger.error(f"Error fetching issues: {e}")
                break
                
        logger.info(f"Total issues fetched: {len(all_issues)}")
        return all_issues
    
    def extract_issue_summary(self, issue: Dict[str, Any]) -> IssueSummary:
        """Extract summary data from JIRA issue"""
        fields = issue.get('fields', {})
        
        # Extract assignee
        assignee = fields.get('assignee')
        assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
        
        # Extract time tracking information
        time_tracking = fields.get('timetracking', {})
        
        # Time values in seconds, convert to hours
        estimated_seconds = (
            fields.get('timeoriginalestimate', 0) or 
            fields.get('aggregatetimeoriginalestimate', 0) or 0
        )
        remaining_seconds = (
            fields.get('timeestimate', 0) or 
            fields.get('aggregatetimeestimate', 0) or 0
        )
        spent_seconds = (
            fields.get('timespent', 0) or 
            fields.get('aggregatetimespent', 0) or 0
        )
        
        # Convert seconds to hours
        estimated_hours = estimated_seconds / 3600 if estimated_seconds else 0
        remaining_hours = remaining_seconds / 3600 if remaining_seconds else 0
        spent_hours = spent_seconds / 3600 if spent_seconds else 0
        
        # Extract feature link (Epic Link or related issues)
        feature_link = self._extract_feature_link(fields)
        
        return IssueSummary(
            key=issue.get('key', ''),
            summary=fields.get('summary', ''),
            assignee=assignee_name,
            feature_link=feature_link,
            estimated_hours=estimated_hours,
            remaining_hours=remaining_hours,
            spent_hours=spent_hours,
            status=fields.get('status', {}).get('name', ''),
            priority=fields.get('priority', {}).get('name', ''),
            issue_type=fields.get('issuetype', {}).get('name', ''),
            created=fields.get('created', ''),
            updated=fields.get('updated', '')
        )
    
    def _extract_feature_link(self, fields: Dict[str, Any]) -> str:
        """Extract feature link from various JIRA fields"""
        # Try Epic Link first (customfield_10014 is common)
        epic_link = fields.get('customfield_10014')
        if epic_link:
            return epic_link
            
        # Try issue links for features/epics
        issue_links = fields.get('issuelinks', [])
        for link in issue_links:
            if link.get('type', {}).get('name', '').lower() in ['epic-story', 'feature-story', 'relates']:
                # Check inward link
                inward_issue = link.get('inwardIssue')
                if inward_issue:
                    issue_type = inward_issue.get('fields', {}).get('issuetype', {}).get('name', '').lower()
                    if 'epic' in issue_type or 'feature' in issue_type:
                        return inward_issue.get('key', '')
                
                # Check outward link
                outward_issue = link.get('outwardIssue')
                if outward_issue:
                    issue_type = outward_issue.get('fields', {}).get('issuetype', {}).get('name', '').lower()
                    if 'epic' in issue_type or 'feature' in issue_type:
                        return outward_issue.get('key', '')
        
        return 'No Feature Link'
    
    def create_summary_report(self, issues: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create aggregated summary report grouped by feature link and assignee"""
        issue_summaries = [self.extract_issue_summary(issue) for issue in issues]
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                'Issue Key': summary.key,
                'Summary': summary.summary,
                'Assignee': summary.assignee,
                'Feature Link': summary.feature_link,
                'Estimated Hours': summary.estimated_hours,
                'Remaining Hours': summary.remaining_hours,
                'Spent Hours': summary.spent_hours,
                'Status': summary.status,
                'Priority': summary.priority,
                'Issue Type': summary.issue_type,
                'Created': summary.created,
                'Updated': summary.updated
            }
            for summary in issue_summaries
        ])
        
        return df
    
    def create_aggregated_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create aggregated summary grouped by Feature Link and Assignee"""
        # Group by Feature Link and Assignee
        grouped = df.groupby(['Feature Link', 'Assignee']).agg({
            'Estimated Hours': 'sum',
            'Remaining Hours': 'sum',
            'Spent Hours': 'sum',
            'Issue Key': 'count'  # Count of issues
        }).round(2)
        
        # Rename the count column
        grouped.rename(columns={'Issue Key': 'Issue Count'}, inplace=True)
        
        # Calculate completion percentage
        grouped['Completion %'] = (
            (grouped['Spent Hours'] / grouped['Estimated Hours'] * 100)
            .fillna(0)
            .round(1)
        )
        
        # Reset index to make Feature Link and Assignee regular columns
        grouped = grouped.reset_index()
        
        return grouped
    
    def export_to_excel(self, detailed_df: pd.DataFrame, summary_df: pd.DataFrame, filename: str = None):
        """Export detailed and summary data to Excel with multiple sheets"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"jira_summary_{timestamp}.xlsx"
        
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
        
        logger.info(f"Data exported to {filename}")
        
    def print_summary_console(self, summary_df: pd.DataFrame):
        """Print summary to console in a formatted way"""
        print("\n" + "="*80)
        print("JIRA ISSUE SUMMARY - GROUPED BY FEATURE LINK AND ASSIGNEE")
        print("="*80)
        
        for feature_link in summary_df['Feature Link'].unique():
            feature_data = summary_df[summary_df['Feature Link'] == feature_link]
            
            print(f"\n📋 Feature: {feature_link}")
            print("-" * 60)
            
            for _, row in feature_data.iterrows():
                print(f"  👤 {row['Assignee']:<25} | "
                      f"Estimated: {row['Estimated Hours']:>6.1f}h | "
                      f"Remaining: {row['Remaining Hours']:>6.1f}h | "
                      f"Spent: {row['Spent Hours']:>6.1f}h | "
                      f"Issues: {row['Issue Count']:>3} | "
                      f"Complete: {row['Completion %']:>5.1f}%")
            
            # Feature totals
            feature_totals = feature_data.sum(numeric_only=True)
            completion_pct = (feature_totals['Spent Hours'] / feature_totals['Estimated Hours'] * 100) if feature_totals['Estimated Hours'] > 0 else 0
            
            print(f"  {'TOTAL':<25} | "
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

def main():
    """Main function to execute the JIRA data aggregation"""
    parser = argparse.ArgumentParser(description='JIRA Data Aggregator')
    parser.add_argument('--config', '-c', help='Configuration file path', default='config.json')
    parser.add_argument('--jql', '-j', help='JQL query to filter issues')
    parser.add_argument('--output', '-o', help='Output Excel filename')
    parser.add_argument('--console-only', action='store_true', help='Only print to console, no Excel export')
    parser.add_argument('--use-env', action='store_true', help='Use environment variables for configuration')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        if args.use_env:
            config = JiraConfig.from_env()
        else:
            config = JiraConfig.from_file(args.config)
        
        # Validate configuration
        if not all([config.base_url, config.username, config.api_token]):
            logger.error("Missing required configuration. Please provide base_url, username, and api_token")
            sys.exit(1)
        
        # Initialize aggregator
        aggregator = JiraDataAggregator(config)
        
        # Test connection
        if not aggregator.test_connection():
            logger.error("Failed to connect to JIRA. Please check your configuration.")
            sys.exit(1)
        
        # Fetch issues
        logger.info("Fetching JIRA issues...")
        jql_query = args.jql if args.jql else config.default_jql
        issues = aggregator.fetch_issues(jql_query)
        
        if not issues:
            logger.warning("No issues found matching the query")
            return
        
        # Create detailed summary
        detailed_df = aggregator.create_summary_report(issues)
        
        # Create aggregated summary
        summary_df = aggregator.create_aggregated_summary(detailed_df)
        
        # Print to console
        aggregator.print_summary_console(summary_df)
        
        # Export to Excel unless console-only mode
        if not args.console_only:
            aggregator.export_to_excel(detailed_df, summary_df, args.output)
        
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
