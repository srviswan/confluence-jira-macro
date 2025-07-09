#!/usr/bin/env python3
"""
Excel Data Aggregator for JIRA Issues
Processes JIRA data from Excel files and creates aggregated summaries
Similar functionality to jira_data_aggregator.py but works with Excel input
"""

import pandas as pd
import argparse
import json
import os
import sys
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import warnings

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)

@dataclass
class ExcelIssueSummary:
    """Data structure for Excel issue summary"""
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
    completion_percent: float

class ExcelDataAggregator:
    """Aggregates JIRA issue data from Excel files"""
    
    def __init__(self, excel_file: str, sheet_name: Optional[str] = None):
        """
        Initialize with Excel file path
        
        Args:
            excel_file: Path to Excel file containing JIRA data
            sheet_name: Specific sheet name to read (optional)
        """
        self.excel_file = excel_file
        self.sheet_name = sheet_name
        self.raw_data = None
        self.processed_issues = []
        
    def load_excel_data(self) -> pd.DataFrame:
        """Load data from Excel file"""
        try:
            if not os.path.exists(self.excel_file):
                raise FileNotFoundError(f"Excel file not found: {self.excel_file}")
            
            print(f"📊 Loading data from: {self.excel_file}")
            
            # Try to read the Excel file
            if self.sheet_name:
                df = pd.read_excel(self.excel_file, sheet_name=self.sheet_name)
                print(f"📋 Reading sheet: {self.sheet_name}")
            else:
                # Read first sheet or all sheets
                excel_file = pd.ExcelFile(self.excel_file)
                sheet_names = excel_file.sheet_names
                print(f"📋 Available sheets: {', '.join(sheet_names)}")
                
                # Use first sheet by default
                df = pd.read_excel(self.excel_file, sheet_name=sheet_names[0])
                print(f"📋 Using sheet: {sheet_names[0]}")
            
            print(f"📊 Loaded {len(df)} rows with {len(df.columns)} columns")
            return df
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            raise
    
    def detect_column_mappings(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Automatically detect column mappings from Excel headers
        Handles various common column naming conventions
        """
        columns = [col.lower().strip() for col in df.columns]
        
        # Common column name patterns
        mapping_patterns = {
            'key': ['key', 'issue key', 'ticket', 'jira key', 'issue id', 'id'],
            'summary': ['summary', 'title', 'description', 'issue summary', 'subject'],
            'assignee': ['assignee', 'assigned to', 'owner', 'developer', 'responsible'],
            'status': ['status', 'state', 'current status', 'issue status'],
            'priority': ['priority', 'importance', 'urgency'],
            'issue_type': ['issue type', 'type', 'issuetype', 'category', 'kind'],
            'estimated_hours': [
                'estimated hours', 'original estimate', 'estimate', 'planned hours',
                'time estimate', 'estimated time', 'original time estimate', 'effort estimate'
            ],
            'remaining_hours': [
                'remaining hours', 'remaining estimate', 'time remaining', 'hours remaining',
                'remaining time', 'time left', 'remaining effort'
            ],
            'spent_hours': [
                'spent hours', 'time spent', 'logged time', 'hours spent', 'actual time',
                'work logged', 'time logged', 'hours logged'
            ],
            'feature_link': [
                'feature link', 'epic link', 'parent', 'epic', 'feature', 'epic key',
                'parent epic', 'parent key', 'feature key', 'linked epic'
            ]
        }
        
        detected_mapping = {}
        
        for field, patterns in mapping_patterns.items():
            for pattern in patterns:
                matches = [col for col in columns if pattern in col.lower()]
                if matches:
                    # Use the first match, preferring exact matches
                    exact_matches = [col for col in matches if col == pattern]
                    if exact_matches:
                        detected_mapping[field] = df.columns[columns.index(exact_matches[0])]
                    else:
                        detected_mapping[field] = df.columns[columns.index(matches[0])]
                    break
        
        return detected_mapping
    
    def print_column_mapping(self, mapping: Dict[str, str], df: pd.DataFrame):
        """Print detected column mappings for user verification"""
        print("\n🔍 DETECTED COLUMN MAPPINGS:")
        print("-" * 50)
        
        available_columns = list(df.columns)
        
        for field, column in mapping.items():
            print(f"  {field.replace('_', ' ').title():<20} → {column}")
        
        # Show unmapped columns
        mapped_columns = set(mapping.values())
        unmapped = [col for col in available_columns if col not in mapped_columns]
        
        if unmapped:
            print(f"\n📋 Unmapped columns: {', '.join(unmapped)}")
        
        print("-" * 50)
    
    def process_excel_data(self) -> List[ExcelIssueSummary]:
        """Process Excel data into issue summaries"""
        
        # Load data
        df = self.load_excel_data()
        
        # Detect column mappings
        mapping = self.detect_column_mappings(df)
        self.print_column_mapping(mapping, df)
        
        # Validate required columns
        required_fields = ['key', 'summary']
        missing_required = [field for field in required_fields if field not in mapping]
        
        if missing_required:
            print(f"❌ Missing required columns: {missing_required}")
            print("Available columns:", list(df.columns))
            raise ValueError(f"Required columns not found: {missing_required}")
        
        print(f"\n🔄 Processing {len(df)} issues...")
        
        processed_issues = []
        
        for idx, row in df.iterrows():
            try:
                # Extract basic fields
                key = str(row.get(mapping.get('key', ''), f'ISSUE-{idx+1}')).strip()
                summary = str(row.get(mapping.get('summary', ''), 'No Summary')).strip()
                
                # Extract assignee
                assignee = row.get(mapping.get('assignee', ''), 'Unassigned')
                if pd.isna(assignee) or str(assignee).strip() == '':
                    assignee = 'Unassigned'
                else:
                    assignee = str(assignee).strip()
                
                # Extract feature link
                feature_link = row.get(mapping.get('feature_link', ''), 'No Feature Link')
                if pd.isna(feature_link) or str(feature_link).strip() == '':
                    feature_link = 'No Feature Link'
                else:
                    feature_link = str(feature_link).strip()
                
                # Extract time tracking (handle various formats)
                estimated_hours = self._parse_time_value(row.get(mapping.get('estimated_hours', ''), 0))
                remaining_hours = self._parse_time_value(row.get(mapping.get('remaining_hours', ''), 0))
                spent_hours = self._parse_time_value(row.get(mapping.get('spent_hours', ''), 0))
                
                # Calculate completion percentage
                completion_percent = 0.0
                if estimated_hours > 0:
                    completion_percent = (spent_hours / estimated_hours) * 100
                
                # Extract other fields
                status = str(row.get(mapping.get('status', ''), 'Unknown')).strip()
                priority = str(row.get(mapping.get('priority', ''), 'Medium')).strip()
                issue_type = str(row.get(mapping.get('issue_type', ''), 'Story')).strip()
                
                # Create issue summary
                issue_summary = ExcelIssueSummary(
                    key=key,
                    summary=summary,
                    assignee=assignee,
                    feature_link=feature_link,
                    estimated_hours=estimated_hours,
                    remaining_hours=remaining_hours,
                    spent_hours=spent_hours,
                    status=status,
                    priority=priority,
                    issue_type=issue_type,
                    completion_percent=completion_percent
                )
                
                processed_issues.append(issue_summary)
                
            except Exception as e:
                print(f"⚠️  Warning: Error processing row {idx+1}: {e}")
                continue
        
        print(f"✅ Successfully processed {len(processed_issues)} issues")
        self.processed_issues = processed_issues
        return processed_issues
    
    def _parse_time_value(self, value) -> float:
        """Parse time value from various formats (hours, seconds, text)"""
        if pd.isna(value) or value == '' or value is None:
            return 0.0
        
        try:
            # If it's already a number, assume it's hours
            if isinstance(value, (int, float)):
                return float(value)
            
            # Convert string to number
            str_value = str(value).strip().lower()
            
            # Handle empty or 'null' values
            if str_value in ['', 'null', 'none', 'n/a', '-']:
                return 0.0
            
            # Parse time formats
            if 'h' in str_value:
                # Format like "8h", "8.5h", "8 hours"
                return float(str_value.replace('h', '').replace('hours', '').replace('hour', '').strip())
            elif 'd' in str_value:
                # Format like "1d", "1.5d" (assume 8 hours per day)
                return float(str_value.replace('d', '').replace('days', '').replace('day', '').strip()) * 8
            elif 'w' in str_value:
                # Format like "1w" (assume 40 hours per week)
                return float(str_value.replace('w', '').replace('weeks', '').replace('week', '').strip()) * 40
            elif ':' in str_value:
                # Format like "8:30" (hours:minutes)
                parts = str_value.split(':')
                hours = float(parts[0])
                minutes = float(parts[1]) / 60 if len(parts) > 1 else 0
                return hours + minutes
            else:
                # Try to parse as plain number
                return float(str_value)
                
        except (ValueError, TypeError):
            # If parsing fails, return 0
            return 0.0
    
    def create_aggregated_summary(self) -> pd.DataFrame:
        """Create aggregated summary grouped by feature link and assignee"""
        
        if not self.processed_issues:
            raise ValueError("No processed issues available. Run process_excel_data() first.")
        
        # Convert to DataFrame for easier aggregation
        data = []
        for issue in self.processed_issues:
            data.append({
                'Feature Link': issue.feature_link,
                'Assignee': issue.assignee,
                'Estimated Hours': issue.estimated_hours,
                'Remaining Hours': issue.remaining_hours,
                'Spent Hours': issue.spent_hours,
                'Issue Key': issue.key,
                'Status': issue.status,
                'Priority': issue.priority,
                'Issue Type': issue.issue_type
            })
        
        df = pd.DataFrame(data)
        
        # Group by Feature Link and Assignee
        summary_df = df.groupby(['Feature Link', 'Assignee']).agg({
            'Estimated Hours': 'sum',
            'Remaining Hours': 'sum',
            'Spent Hours': 'sum',
            'Issue Key': 'count'
        }).round(2)
        
        summary_df.rename(columns={'Issue Key': 'Issue Count'}, inplace=True)
        
        # Calculate completion percentages
        summary_df['Completion %'] = (
            (summary_df['Spent Hours'] / summary_df['Estimated Hours'] * 100)
            .fillna(0)
            .round(1)
        )
        
        summary_df = summary_df.reset_index()
        return summary_df
    
    def print_console_summary(self, summary_df: pd.DataFrame):
        """Print formatted summary to console"""
        
        print("\n" + "="*80)
        print("EXCEL JIRA ISSUE SUMMARY - GROUPED BY FEATURE LINK AND ASSIGNEE")
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
        
        # Show top contributors
        print(f"\n🏆 TOP CONTRIBUTORS:")
        print("-" * 30)
        assignee_totals = summary_df.groupby('Assignee').sum(numeric_only=True).sort_values('Spent Hours', ascending=False)
        for assignee, totals in assignee_totals.head(5).iterrows():
            print(f"  👤 {assignee:<20} | Spent: {totals['Spent Hours']:>6.1f}h | Issues: {totals['Issue Count']:>3}")
    
    def export_to_excel(self, output_file: str):
        """Export aggregated data to Excel with multiple sheets"""
        
        if not self.processed_issues:
            raise ValueError("No processed issues available. Run process_excel_data() first.")
        
        print(f"\n📊 Exporting to Excel: {output_file}")
        
        # Create detailed DataFrame
        detailed_data = []
        for issue in self.processed_issues:
            detailed_data.append({
                'Issue Key': issue.key,
                'Summary': issue.summary,
                'Assignee': issue.assignee,
                'Feature Link': issue.feature_link,
                'Estimated Hours': issue.estimated_hours,
                'Remaining Hours': issue.remaining_hours,
                'Spent Hours': issue.spent_hours,
                'Completion %': issue.completion_percent,
                'Status': issue.status,
                'Priority': issue.priority,
                'Issue Type': issue.issue_type
            })
        
        detailed_df = pd.DataFrame(detailed_data)
        summary_df = self.create_aggregated_summary()
        
        # Create additional summary views
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
        
        # Write to Excel with multiple sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name='Summary by Feature & Assignee', index=False)
            detailed_df.to_excel(writer, sheet_name='Detailed Issues', index=False)
            feature_summary.to_excel(writer, sheet_name='Summary by Feature')
            assignee_summary.to_excel(writer, sheet_name='Summary by Assignee')
        
        print(f"✅ Excel export completed with 4 sheets")
        
        # Show file info
        file_size = os.path.getsize(output_file)
        print(f"📁 File size: {file_size:,} bytes")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Excel Data Aggregator for JIRA Issues',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python excel_data_aggregator.py issues.xlsx
  python excel_data_aggregator.py issues.xlsx --sheet "JIRA Export"
  python excel_data_aggregator.py issues.xlsx --output report.xlsx
  python excel_data_aggregator.py issues.xlsx --console-only
        """
    )
    
    parser.add_argument('excel_file', help='Path to Excel file containing JIRA data')
    parser.add_argument('--sheet', '-s', help='Specific sheet name to read')
    parser.add_argument('--output', '-o', help='Output Excel filename')
    parser.add_argument('--console-only', action='store_true', help='Only print to console, no Excel export')
    
    args = parser.parse_args()
    
    try:
        # Initialize aggregator
        aggregator = ExcelDataAggregator(args.excel_file, args.sheet)
        
        # Process data
        issues = aggregator.process_excel_data()
        
        if not issues:
            print("❌ No issues found in Excel file")
            return
        
        # Create summary
        summary_df = aggregator.create_aggregated_summary()
        
        # Print console output
        aggregator.print_console_summary(summary_df)
        
        # Export to Excel if requested
        if not args.console_only:
            if args.output:
                output_file = args.output
            else:
                base_name = os.path.splitext(os.path.basename(args.excel_file))[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"{base_name}_aggregated_{timestamp}.xlsx"
            
            aggregator.export_to_excel(output_file)
        
        print(f"\n🎉 Processing completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
