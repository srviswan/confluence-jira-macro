#!/usr/bin/env python3
"""
JIRA Field Inspector
Utility to discover available fields in your JIRA instance
"""

import requests
import json
import sys
from jira_data_aggregator import JiraConfig

class JiraFieldInspector:
    """Utility class to inspect JIRA fields and custom fields"""
    
    def __init__(self, config: JiraConfig):
        self.config = config
        self.session = requests.Session()
        self.session.auth = (config.username, config.api_token)
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def get_all_fields(self):
        """Get all available fields in JIRA instance"""
        url = f"{self.config.base_url}/rest/api/3/field"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching fields: {e}")
            return []
    
    def get_sample_issue_fields(self, jql: str = None):
        """Get fields from a sample issue to see actual data structure"""
        if jql is None:
            jql = "ORDER BY created DESC"
        
        url = f"{self.config.base_url}/rest/api/3/search"
        params = {
            'jql': jql,
            'maxResults': 1,
            'fields': '*all'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('issues'):
                return data['issues'][0].get('fields', {})
            return {}
        except requests.RequestException as e:
            print(f"Error fetching sample issue: {e}")
            return {}
    
    def print_field_summary(self):
        """Print a summary of all available fields"""
        print("JIRA Field Inspector")
        print("=" * 50)
        
        # Get all field definitions
        all_fields = self.get_all_fields()
        if not all_fields:
            print("No fields found or connection failed")
            return
        
        print(f"\nTotal Fields Available: {len(all_fields)}")
        print("\nField Categories:")
        
        # Categorize fields
        system_fields = []
        custom_fields = []
        
        for field in all_fields:
            if field['id'].startswith('customfield_'):
                custom_fields.append(field)
            else:
                system_fields.append(field)
        
        print(f"  - System Fields: {len(system_fields)}")
        print(f"  - Custom Fields: {len(custom_fields)}")
        
        # Print system fields
        print("\n📋 SYSTEM FIELDS")
        print("-" * 40)
        for field in sorted(system_fields, key=lambda x: x['name']):
            print(f"  {field['id']:<25} | {field['name']}")
        
        # Print custom fields  
        if custom_fields:
            print("\n🔧 CUSTOM FIELDS")
            print("-" * 40)
            for field in sorted(custom_fields, key=lambda x: x['name']):
                field_type = field.get('schema', {}).get('type', 'unknown')
                print(f"  {field['id']:<25} | {field['name']} ({field_type})")
        
        # Show time tracking related fields
        print("\n⏱️  TIME TRACKING FIELDS")
        print("-" * 40)
        time_fields = [
            'timeoriginalestimate', 'timeestimate', 'timespent', 
            'aggregatetimeoriginalestimate', 'aggregatetimeestimate', 'aggregatetimespent'
        ]
        
        for field in all_fields:
            if field['id'] in time_fields:
                print(f"  {field['id']:<25} | {field['name']}")
        
        # Show epic/feature link fields
        print("\n🔗 EPIC/FEATURE LINK FIELDS")
        print("-" * 40)
        epic_keywords = ['epic', 'parent', 'feature', 'initiative']
        
        for field in all_fields:
            field_name_lower = field['name'].lower()
            if any(keyword in field_name_lower for keyword in epic_keywords):
                print(f"  {field['id']:<25} | {field['name']}")
    
    def print_sample_issue_structure(self, jql: str = None):
        """Print the structure of a sample issue"""
        print("\n" + "=" * 50)
        print("SAMPLE ISSUE FIELD STRUCTURE")
        print("=" * 50)
        
        sample_fields = self.get_sample_issue_fields(jql)
        if not sample_fields:
            print("No sample issue found")
            return
        
        def print_field_value(key, value, indent=0):
            """Recursively print field structure"""
            prefix = "  " * indent
            
            if isinstance(value, dict):
                if value:  # Non-empty dict
                    print(f"{prefix}{key}:")
                    for sub_key, sub_value in value.items():
                        print_field_value(sub_key, sub_value, indent + 1)
                else:
                    print(f"{prefix}{key}: {{}}")
            elif isinstance(value, list):
                if value:  # Non-empty list
                    print(f"{prefix}{key}: [{len(value)} items]")
                    if len(value) <= 3:  # Show first few items
                        for i, item in enumerate(value):
                            print_field_value(f"[{i}]", item, indent + 1)
                else:
                    print(f"{prefix}{key}: []")
            else:
                # Truncate long values
                str_value = str(value)
                if len(str_value) > 100:
                    str_value = str_value[:100] + "..."
                print(f"{prefix}{key}: {str_value}")
        
        # Print key fields first
        key_fields = ['key', 'summary', 'status', 'assignee', 'issuetype', 'priority']
        
        print("🔑 KEY FIELDS:")
        for field in key_fields:
            if field in sample_fields:
                print_field_value(field, sample_fields[field])
        
        print("\n⏱️  TIME TRACKING FIELDS:")
        time_fields = [
            'timeoriginalestimate', 'timeestimate', 'timespent',
            'aggregatetimeoriginalestimate', 'aggregatetimeestimate', 'aggregatetimespent',
            'timetracking'
        ]
        for field in time_fields:
            if field in sample_fields:
                print_field_value(field, sample_fields[field])
        
        print("\n🔗 LINK FIELDS:")
        link_fields = ['issuelinks', 'subtasks', 'parent']
        custom_link_fields = [k for k in sample_fields.keys() 
                             if k.startswith('customfield_') and 
                             any(word in sample_fields[k].__class__.__name__.lower() 
                                 if hasattr(sample_fields[k], '__class__') else False
                                 for word in ['link', 'epic', 'parent'])]
        
        for field in link_fields + custom_link_fields:
            if field in sample_fields:
                print_field_value(field, sample_fields[field])
        
        print(f"\n📊 TOTAL FIELDS IN SAMPLE: {len(sample_fields)}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='JIRA Field Inspector')
    parser.add_argument('--config', '-c', help='Configuration file path', default='config.json')
    parser.add_argument('--sample-jql', help='JQL query to get sample issue')
    parser.add_argument('--use-env', action='store_true', help='Use environment variables')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        if args.use_env:
            config = JiraConfig.from_env()
        else:
            config = JiraConfig.from_file(args.config)
        
        inspector = JiraFieldInspector(config)
        
        # Print field summary
        inspector.print_field_summary()
        
        # Print sample issue structure
        inspector.print_sample_issue_structure(args.sample_jql)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
