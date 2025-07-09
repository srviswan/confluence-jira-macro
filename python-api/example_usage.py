#!/usr/bin/env python3
"""
Example usage of JIRA Data Aggregator
Demonstrates various ways to use the aggregator with sample configurations
"""

import os
import sys
from datetime import datetime
import json
from jira_data_aggregator import JiraConfig, JiraDataAggregator

def example_basic_usage():
    """Example of basic usage with configuration file"""
    print("=== Example 1: Basic Usage ===")
    
    # Create a sample configuration
    sample_config = {
        "base_url": "https://your-domain.atlassian.net",
        "username": "your-email@domain.com", 
        "api_token": "your-api-token",
        "default_jql": "project = \"DEMO\" AND status != \"Done\"",
        "max_results": 100
    }
    
    # Save sample config (for demonstration)
    with open('sample_config.json', 'w') as f:
        json.dump(sample_config, f, indent=2)
    
    print("Created sample_config.json - update with your JIRA details")
    print("Then run: python jira_data_aggregator.py --config sample_config.json")

def example_environment_variables():
    """Example of using environment variables"""
    print("\n=== Example 2: Environment Variables ===")
    
    print("Set these environment variables:")
    print("export JIRA_BASE_URL='https://your-domain.atlassian.net'")
    print("export JIRA_USERNAME='your-email@domain.com'")
    print("export JIRA_API_TOKEN='your-api-token'")
    print("export JIRA_DEFAULT_JQL='project = \"YOUR_PROJECT\" AND status != \"Done\"'")
    print()
    print("Then run: python jira_data_aggregator.py --use-env")

def example_custom_jql_queries():
    """Example of various JQL queries for different use cases"""
    print("\n=== Example 3: Custom JQL Queries ===")
    
    jql_examples = [
        {
            "description": "Issues assigned to current user",
            "jql": "assignee = currentUser() AND status != Done"
        },
        {
            "description": "Issues in current sprint",
            "jql": "project = MYPROJ AND sprint in openSprints()"
        },
        {
            "description": "High priority issues with time tracking",
            "jql": "priority in (High, Highest) AND originalEstimate is not EMPTY"
        },
        {
            "description": "Issues updated in last week",
            "jql": "updated >= -1w AND project = MYPROJ"
        },
        {
            "description": "Bugs in testing status",
            "jql": "issuetype = Bug AND status = \"In Testing\""
        },
        {
            "description": "Features with remaining work",
            "jql": "issuetype in (Epic, Story) AND remainingEstimate > 0"
        }
    ]
    
    print("Example JQL queries for different scenarios:")
    for i, example in enumerate(jql_examples, 1):
        print(f"\n{i}. {example['description']}:")
        print(f"   JQL: {example['jql']}")
        print(f"   Command: python jira_data_aggregator.py --jql \"{example['jql']}\"")

def example_output_formats():
    """Example of different output options"""
    print("\n=== Example 4: Output Options ===")
    
    commands = [
        {
            "description": "Console output only",
            "command": "python jira_data_aggregator.py --console-only"
        },
        {
            "description": "Save to custom Excel file",
            "command": "python jira_data_aggregator.py --output \"weekly_report.xlsx\""
        },
        {
            "description": "Generate timestamped report",
            "command": "python jira_data_aggregator.py --output \"report_$(date +%Y%m%d).xlsx\""
        }
    ]
    
    print("Different output format examples:")
    for i, cmd in enumerate(commands, 1):
        print(f"\n{i}. {cmd['description']}:")
        print(f"   {cmd['command']}")

def create_test_config():
    """Create a test configuration file with sample data"""
    print("\n=== Creating Test Configuration ===")
    
    test_config = {
        "base_url": "https://your-domain.atlassian.net",
        "username": "your-email@domain.com",
        "api_token": "your-api-token-here",
        "default_jql": "project in (\"TEST\", \"DEMO\") AND status != \"Done\" AND created >= -30d",
        "max_results": 500
    }
    
    config_file = "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(test_config, f, indent=2)
    
    print(f"Created {config_file}")
    print("Please update the configuration with your actual JIRA details:")
    print(f"  - base_url: Your JIRA instance URL")
    print(f"  - username: Your JIRA email address") 
    print(f"  - api_token: Generate from JIRA Profile → Security → API tokens")
    print(f"  - default_jql: Customize the JQL query for your projects")

def main():
    """Main function to run all examples"""
    print("JIRA Data Aggregator - Usage Examples")
    print("=" * 50)
    
    example_basic_usage()
    example_environment_variables() 
    example_custom_jql_queries()
    example_output_formats()
    create_test_config()
    
    print("\n" + "=" * 50)
    print("Next Steps:")
    print("1. Update configuration with your JIRA details")
    print("2. Install requirements: pip install -r requirements.txt")  
    print("3. Test connection: python jira_data_aggregator.py --console-only")
    print("4. Generate full report: python jira_data_aggregator.py")

if __name__ == "__main__":
    main()
