# Example Usage - Confluence JIRA Macro

This document provides practical examples of how to use the JIRA Issues Grid macro in various scenarios.

## Basic Examples

### 1. Simple Project Issues
Display all open issues from a specific project:
```
{jira-grid:jql=project = "DEMO" AND status != "Done"}
```

### 2. Personal Task List
Show issues assigned to the current user:
```
{jira-grid:jql=assignee = currentUser() AND status in ("To Do", "In Progress")|title=My Active Tasks}
```

### 3. Team Sprint Board
Display current sprint issues:
```
{jira-grid:jql=project = "TEAM" AND sprint in openSprints()|fields=key,summary,status,assignee,storyPoints|title=Current Sprint}
```

## Advanced Examples

### 4. High Priority Issues Dashboard
Show critical and high priority issues across multiple projects:
```
{jira-grid:jql=priority in ("Critical", "High") AND status != "Done" AND project in ("PROJ1", "PROJ2", "PROJ3")|fields=key,summary,status,assignee,priority,updated|maxResults=50|title=High Priority Issues}
```

### 5. Recently Updated Issues
Display issues updated in the last 7 days:
```
{jira-grid:jql=updated >= "-7d" AND project = "MYPROJECT"|fields=key,summary,status,assignee,updated,reporter|title=Recent Activity}
```

### 6. Bug Tracking Board
Show all open bugs with severity information:
```
{jira-grid:jql=issuetype = "Bug" AND status != "Done"|fields=key,summary,status,assignee,priority,components|title=Open Bugs}
```

### 7. Release Planning View
Display issues for a specific fix version:
```
{jira-grid:jql=fixVersion = "Release 2.0" AND project = "PRODUCT"|fields=key,summary,status,assignee,issuetype|title=Release 2.0 Issues}
```

### 8. Component-Specific Issues
Show issues for specific components:
```
{jira-grid:jql=component in ("Frontend", "Backend") AND status != "Done"|fields=key,summary,status,assignee,components|title=Development Issues}
```

## Specialized Use Cases

### 9. Executive Summary
High-level view for management:
```
{jira-grid:jql=project = "STRATEGIC" AND issuetype in ("Epic", "Story") AND status != "Done"|fields=key,summary,status,assignee,priority|maxResults=20|title=Strategic Initiatives}
```

### 10. Quality Assurance Board
Testing-focused view:
```
{jira-grid:jql=project = "QA" AND (status = "Ready for Testing" OR assignee in membersOf("qa-team"))|fields=key,summary,status,assignee,labels|title=QA Pipeline}
```

### 11. Overdue Issues Alert
Issues past their due date:
```
{jira-grid:jql=duedate < now() AND status != "Done"|fields=key,summary,status,assignee,duedate,priority|title=⚠️ Overdue Issues}
```

### 12. Customer Support Tickets
Support-focused dashboard:
```
{jira-grid:jql=project = "SUPPORT" AND status in ("Open", "In Progress", "Waiting for Customer")|fields=key,summary,status,assignee,priority,customer|title=Active Support Tickets}
```

## Filtered and Sorted Examples

### 13. Recently Created Issues
New issues requiring attention:
```
{jira-grid:jql=created >= "-3d" AND project = "NEWPROJ" ORDER BY created DESC|fields=key,summary,status,reporter,created|title=New Issues (Last 3 Days)}
```

### 14. Issues by Assignee
Group issues by team member:
```
{jira-grid:jql=project = "TEAM" AND assignee is not EMPTY ORDER BY assignee, priority DESC|fields=key,summary,status,assignee,priority|title=Team Workload}
```

### 15. Epic Progress Tracking
Track epic completion:
```
{jira-grid:jql=issuetype = "Epic" AND project = "PRODUCT" ORDER BY status|fields=key,summary,status,assignee,progress|title=Epic Progress}
```

## Custom Field Examples

### 16. With Story Points
Agile planning view:
```
{jira-grid:jql=project = "AGILE" AND sprint in openSprints()|fields=key,summary,status,assignee,storyPoints,timeSpent|title=Sprint Burndown}
```

### 17. With Custom Fields
Include organization-specific fields:
```
{jira-grid:jql=project = "CUSTOM"|fields=key,summary,status,assignee,customfield_10001,customfield_10002|title=Custom Tracking}
```

Note: Replace `customfield_XXXXX` with your actual custom field IDs.

## Multi-Project Examples

### 18. Cross-Project Dependencies
Track dependencies across projects:
```
{jira-grid:jql=project in ("PROJ1", "PROJ2", "PROJ3") AND status = "Blocked"|fields=key,summary,status,assignee,project|title=Blocked Issues}
```

### 19. Portfolio View
High-level portfolio tracking:
```
{jira-grid:jql=project in projectsLeadByUser(currentUser()) AND issuetype = "Epic"|fields=key,summary,status,project,assignee|title=My Portfolio}
```

### 20. Cross-Team Collaboration
Issues involving multiple teams:
```
{jira-grid:jql=labels in ("cross-team", "collaboration") AND status != "Done"|fields=key,summary,status,assignee,labels,project|title=Cross-Team Issues}
```

## Time-Based Filters

### 21. This Week's Work
Current week focus:
```
{jira-grid:jql=assignee = currentUser() AND updated >= startOfWeek() AND updated <= endOfWeek()|fields=key,summary,status,updated|title=This Week's Activity}
```

### 22. Monthly Report
Month-to-date progress:
```
{jira-grid:jql=project = "MONTHLY" AND created >= startOfMonth()|fields=key,summary,status,created,assignee|title=This Month's Issues}
```

### 23. Quarterly Planning
Quarterly milestone tracking:
```
{jira-grid:jql=project = "PLANNING" AND fixVersion in unreleasedVersions() AND duedate <= "2024-03-31"|fields=key,summary,status,fixVersion,duedate|title=Q1 Deliverables}
```

## Integration Examples

### 24. Confluence Page Integration
Link to related Confluence content:
```
{jira-grid:jql=project = "DOCS" AND labels = "confluence-linked"|fields=key,summary,status,assignee,labels|title=Documentation Issues}
```

### 25. Git Integration
Development tracking:
```
{jira-grid:jql=project = "DEV" AND status in ("In Progress", "Code Review")|fields=key,summary,status,assignee,branch|title=Development Pipeline}
```

## Performance Considerations

### Large Datasets
For projects with many issues, use pagination and filtering:
```
{jira-grid:jql=project = "LARGE" AND updated >= "-30d"|maxResults=100|title=Recent Activity (Large Project)}
```

### Complex Queries
Break down complex queries into focused views:
```
{jira-grid:jql=project = "COMPLEX" AND priority = "High" AND status != "Done"|maxResults=25|title=High Priority Items}
```

## Tips for Effective Usage

1. **Start Simple**: Begin with basic JQL and add complexity gradually
2. **Test Queries**: Always test JQL in JIRA's issue search first
3. **Use Meaningful Titles**: Make it clear what each grid shows
4. **Limit Results**: Use `maxResults` to prevent performance issues
5. **Choose Relevant Fields**: Only display fields that add value
6. **Regular Updates**: Keep queries current with project changes
7. **User Permissions**: Ensure viewers have access to the queried projects

## JQL Reference

### Common Functions
- `currentUser()` - Current logged-in user
- `membersOf("group-name")` - Members of a group
- `now()` - Current date/time
- `startOfWeek()`, `endOfWeek()` - Week boundaries
- `startOfMonth()`, `endOfMonth()` - Month boundaries

### Common Operators
- `=`, `!=` - Equals, not equals
- `IN`, `NOT IN` - List membership
- `~` - Contains (text search)
- `>=`, `<=` - Greater/less than or equal
- `IS EMPTY`, `IS NOT EMPTY` - Null checks
- `ORDER BY` - Sorting

### Date Formats
- `"2024-01-15"` - Specific date
- `"-7d"` - 7 days ago
- `"1w"` - 1 week from now
- `now()` - Current timestamp

Remember to adjust project keys, field names, and values according to your JIRA configuration.
