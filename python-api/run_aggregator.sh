#!/bin/bash

# JIRA Data Aggregator - Batch Execution Script
# Makes it easy to run the aggregator with common configurations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}JIRA Data Aggregator - Batch Runner${NC}"
echo "=================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed${NC}"
    exit 1
fi

# Check if virtual environment should be created
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install/update requirements
echo -e "${YELLOW}Installing/updating requirements...${NC}"
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}Requirements installed${NC}"

# Check for configuration
if [ ! -f "config.json" ]; then
    if [ -f "config.json.template" ]; then
        echo -e "${YELLOW}Configuration file not found. Creating from template...${NC}"
        cp config.json.template config.json
        echo -e "${RED}Please edit config.json with your JIRA details before running${NC}"
        echo "Required fields:"
        echo "  - base_url: Your JIRA instance URL"
        echo "  - username: Your JIRA email"
        echo "  - api_token: Generate from JIRA Profile → Security → API tokens"
        exit 1
    else
        echo -e "${RED}No configuration found. Please create config.json${NC}"
        exit 1
    fi
fi

# Function to run with different options
run_aggregator() {
    local description="$1"
    local command="$2"
    
    echo -e "\n${BLUE}Running: $description${NC}"
    echo "Command: python $command"
    echo "---"
    
    if python $command; then
        echo -e "${GREEN}✓ Completed successfully${NC}"
    else
        echo -e "${RED}✗ Failed with error code $?${NC}"
        return 1
    fi
}

# Parse command line arguments
case "${1:-default}" in
    "test")
        echo -e "${YELLOW}Testing JIRA connection...${NC}"
        run_aggregator "Connection Test" "jira_data_aggregator.py --console-only --jql \"ORDER BY created DESC\""
        ;;
    
    "console")
        echo -e "${YELLOW}Running console-only mode...${NC}"
        run_aggregator "Console Output" "jira_data_aggregator.py --console-only"
        ;;
    
    "excel")
        timestamp=$(date +"%Y%m%d_%H%M%S")
        filename="jira_report_${timestamp}.xlsx"
        echo -e "${YELLOW}Generating Excel report: $filename${NC}"
        run_aggregator "Excel Report" "jira_data_aggregator.py --output \"$filename\""
        ;;
    
    "current-user")
        timestamp=$(date +"%Y%m%d_%H%M%S")
        filename="my_issues_${timestamp}.xlsx"
        echo -e "${YELLOW}Generating report for current user: $filename${NC}"
        run_aggregator "Current User Issues" "jira_data_aggregator.py --jql \"assignee = currentUser() AND status != Done\" --output \"$filename\""
        ;;
    
    "sprint")
        timestamp=$(date +"%Y%m%d_%H%M%S")
        filename="sprint_report_${timestamp}.xlsx"
        echo -e "${YELLOW}Generating current sprint report: $filename${NC}"
        run_aggregator "Sprint Report" "jira_data_aggregator.py --jql \"sprint in openSprints()\" --output \"$filename\""
        ;;
    
    "fields")
        echo -e "${YELLOW}Inspecting JIRA fields...${NC}"
        run_aggregator "Field Inspector" "field_inspector.py"
        ;;
    
    "examples")
        echo -e "${YELLOW}Running usage examples...${NC}"
        run_aggregator "Usage Examples" "example_usage.py"
        ;;
    
    "help")
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  test         - Test JIRA connection"
        echo "  console      - Run with console output only"
        echo "  excel        - Generate Excel report with timestamp"
        echo "  current-user - Generate report for current user's issues"
        echo "  sprint       - Generate report for current sprint"
        echo "  fields       - Inspect available JIRA fields"
        echo "  examples     - Show usage examples"
        echo "  help         - Show this help message"
        echo "  default      - Run standard aggregation (same as no arguments)"
        echo ""
        echo "Examples:"
        echo "  $0 test                    # Test connection"
        echo "  $0 console                 # Console output only"
        echo "  $0 excel                   # Generate Excel report"
        echo "  $0 current-user            # My issues report"
        ;;
    
    "default"|*)
        echo -e "${YELLOW}Running standard JIRA data aggregation...${NC}"
        run_aggregator "Standard Aggregation" "jira_data_aggregator.py"
        ;;
esac

echo -e "\n${GREEN}Script completed!${NC}"
