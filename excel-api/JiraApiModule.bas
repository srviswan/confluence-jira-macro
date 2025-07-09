Attribute VB_Name = "JiraApiModule"
'========================================================================
' JIRA Time Tracking Excel Macro
' Connects to JIRA API and fetches time logged data for specific weeks
' Aggregates by Feature Link and Assignee
'========================================================================

Option Explicit

' API Configuration Constants
Private Const JIRA_API_VERSION As String = "2"
Private Const MAX_RESULTS As Integer = 1000

' Data Types
Type JiraConfig
    BaseUrl As String
    Username As String
    ApiToken As String
    DefaultJQL As String
End Type

Type TimeEntry
    IssueKey As String
    IssueSummary As String
    Assignee As String
    FeatureLink As String
    TimeSpent As Double
    DateLogged As Date
    Author As String
    WorkDescription As String
End Type

Type FeatureAssigneeSummary
    FeatureLink As String
    Assignee As String
    TotalHours As Double
    IssueCount As Integer
End Type

'========================================================================
' MAIN FUNCTIONS
'========================================================================

Sub FetchJiraTimeData()
    '
    ' Main function to fetch JIRA time tracking data
    '
    On Error GoTo ErrorHandler
    
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    
    ' Clear previous results
    Call ClearResults
    
    ' Get configuration from Excel
    Dim config As JiraConfig
    If Not LoadConfiguration(config) Then
        MsgBox "Please configure JIRA connection settings in the Config sheet", vbCritical
        Exit Sub
    End If
    
    ' Get date range from Excel
    Dim startDate As Date, endDate As Date
    If Not GetDateRange(startDate, endDate) Then
        MsgBox "Please specify valid start and end dates", vbCritical
        Exit Sub
    End If
    
    ' Show progress
    UpdateStatus "Connecting to JIRA..."
    
    ' Test connection
    If Not TestJiraConnection(config) Then
        MsgBox "Failed to connect to JIRA. Please check your configuration.", vbCritical
        Exit Sub
    End If
    
    UpdateStatus "Fetching time tracking data..."
    
    ' Fetch worklog data
    Dim timeEntries() As TimeEntry
    Dim entryCount As Integer
    entryCount = FetchTimeEntries(config, startDate, endDate, timeEntries)
    
    If entryCount = 0 Then
        MsgBox "No time entries found for the specified date range", vbInformation
        Exit Sub
    End If
    
    UpdateStatus "Processing " & entryCount & " time entries..."
    
    ' Write raw data to Excel
    Call WriteRawDataToExcel(timeEntries, entryCount)
    
    ' Create aggregated summary
    Dim summaries() As FeatureAssigneeSummary
    Dim summaryCount As Integer
    summaryCount = CreateAggregatedSummary(timeEntries, entryCount, summaries)
    
    ' Write summary to Excel
    Call WriteSummaryToExcel(summaries, summaryCount)
    
    ' Create charts and formatting
    Call FormatWorksheets
    Call CreateSummaryChart
    
    UpdateStatus "Complete! Processed " & entryCount & " time entries"
    
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    
    MsgBox "JIRA time tracking data successfully imported!" & vbCrLf & _
           "Entries: " & entryCount & vbCrLf & _
           "Date Range: " & Format(startDate, "mm/dd/yyyy") & " - " & Format(endDate, "mm/dd/yyyy"), _
           vbInformation, "Import Complete"
    
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    Application.Calculation = xlCalculationAutomatic
    UpdateStatus "Error occurred: " & Err.Description
    MsgBox "Error: " & Err.Description, vbCritical
End Sub

'========================================================================
' CONFIGURATION FUNCTIONS
'========================================================================

Function LoadConfiguration(ByRef config As JiraConfig) As Boolean
    '
    ' Load JIRA configuration from Config worksheet
    '
    On Error GoTo ConfigError
    
    Dim configSheet As Worksheet
    Set configSheet = ThisWorkbook.Worksheets("Config")
    
    config.BaseUrl = Trim(configSheet.Range("B2").Value)
    config.Username = Trim(configSheet.Range("B3").Value)
    config.ApiToken = Trim(configSheet.Range("B4").Value)
    config.DefaultJQL = Trim(configSheet.Range("B5").Value)
    
    ' Validate required fields
    If config.BaseUrl = "" Or config.Username = "" Or config.ApiToken = "" Then
        LoadConfiguration = False
        Exit Function
    End If
    
    ' Ensure base URL format
    If Right(config.BaseUrl, 1) = "/" Then
        config.BaseUrl = Left(config.BaseUrl, Len(config.BaseUrl) - 1)
    End If
    
    LoadConfiguration = True
    Exit Function
    
ConfigError:
    LoadConfiguration = False
End Function

Function GetDateRange(ByRef startDate As Date, ByRef endDate As Date) As Boolean
    '
    ' Get date range from Settings worksheet
    '
    On Error GoTo DateError
    
    Dim settingsSheet As Worksheet
    Set settingsSheet = ThisWorkbook.Worksheets("Settings")
    
    startDate = settingsSheet.Range("B2").Value
    endDate = settingsSheet.Range("B3").Value
    
    ' Validate dates
    If Not IsDate(startDate) Or Not IsDate(endDate) Then
        GetDateRange = False
        Exit Function
    End If
    
    If startDate > endDate Then
        GetDateRange = False
        Exit Function
    End If
    
    GetDateRange = True
    Exit Function
    
DateError:
    GetDateRange = False
End Function

'========================================================================
' JIRA API FUNCTIONS
'========================================================================

Function TestJiraConnection(config As JiraConfig) As Boolean
    '
    ' Test connection to JIRA API
    '
    On Error GoTo ConnectionError
    
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    Dim url As String
    url = config.BaseUrl & "/rest/api/" & JIRA_API_VERSION & "/myself"
    
    http.Open "GET", url, False
    http.setRequestHeader "Authorization", "Basic " & EncodeBase64(config.Username & ":" & config.ApiToken)
    http.setRequestHeader "Content-Type", "application/json"
    http.Send
    
    TestJiraConnection = (http.Status = 200)
    Exit Function
    
ConnectionError:
    TestJiraConnection = False
End Function

Function FetchTimeEntries(config As JiraConfig, startDate As Date, endDate As Date, ByRef timeEntries() As TimeEntry) As Integer
    '
    ' Fetch time entries from JIRA for the specified date range
    '
    On Error GoTo FetchError
    
    ' Build JQL query for issues updated in date range
    Dim jql As String
    jql = "worklogDate >= '" & Format(startDate, "yyyy-mm-dd") & "' AND worklogDate <= '" & Format(endDate, "yyyy-mm-dd") & "'"
    
    ' Add additional JQL if specified
    If config.DefaultJQL <> "" Then
        jql = "(" & config.DefaultJQL & ") AND " & jql
    End If
    
    ' Fetch issues
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    Dim url As String
    url = config.BaseUrl & "/rest/api/" & JIRA_API_VERSION & "/search"
    url = url & "?jql=" & URLEncode(jql)
    url = url & "&fields=key,summary,assignee,customfield_10014,worklog"
    url = url & "&maxResults=" & MAX_RESULTS
    url = url & "&expand=changelog"
    
    http.Open "GET", url, False
    http.setRequestHeader "Authorization", "Basic " & EncodeBase64(config.Username & ":" & config.ApiToken)
    http.setRequestHeader "Content-Type", "application/json"
    http.Send
    
    If http.Status <> 200 Then
        MsgBox "JIRA API Error: " & http.Status & " - " & http.responseText, vbCritical
        FetchTimeEntries = 0
        Exit Function
    End If
    
    ' Parse JSON response
    Dim json As Object
    Set json = ParseJson(http.responseText)
    
    Dim issues As Object
    Set issues = json("issues")
    
    ' Process each issue's worklog
    ReDim timeEntries(1 To MAX_RESULTS)
    Dim entryCount As Integer
    entryCount = 0
    
    Dim i As Integer
    For i = 0 To issues.Count - 1
        Dim issue As Object
        Set issue = issues(i)
        
        entryCount = ProcessIssueWorklogs(issue, startDate, endDate, timeEntries, entryCount)
    Next i
    
    ' Resize array to actual count
    If entryCount > 0 Then
        ReDim Preserve timeEntries(1 To entryCount)
    End If
    
    FetchTimeEntries = entryCount
    Exit Function
    
FetchError:
    FetchTimeEntries = 0
    MsgBox "Error fetching time entries: " & Err.Description, vbCritical
End Function

Function ProcessIssueWorklogs(issue As Object, startDate As Date, endDate As Date, ByRef timeEntries() As TimeEntry, currentCount As Integer) As Integer
    '
    ' Process worklog entries for a single issue
    '
    On Error GoTo ProcessError
    
    Dim newCount As Integer
    newCount = currentCount
    
    ' Get issue details
    Dim issueKey As String
    Dim issueSummary As String
    Dim assignee As String
    Dim featureLink As String
    
    issueKey = issue("key")
    issueSummary = issue("fields")("summary")
    
    ' Get assignee
    If Not IsNull(issue("fields")("assignee")) Then
        assignee = issue("fields")("assignee")("displayName")
    Else
        assignee = "Unassigned"
    End If
    
    ' Get feature link (Epic Link - customfield_10014)
    If Not IsNull(issue("fields")("customfield_10014")) Then
        featureLink = issue("fields")("customfield_10014")
    Else
        featureLink = "No Feature Link"
    End If
    
    ' Process worklog entries
    If Not IsNull(issue("fields")("worklog")) Then
        Dim worklogs As Object
        Set worklogs = issue("fields")("worklog")("worklogs")
        
        Dim j As Integer
        For j = 0 To worklogs.Count - 1
            Dim worklog As Object
            Set worklog = worklogs(j)
            
            ' Parse worklog date
            Dim worklogDate As Date
            worklogDate = ParseJiraDate(worklog("started"))
            
            ' Check if worklog is in our date range
            If worklogDate >= startDate And worklogDate <= endDate Then
                newCount = newCount + 1
                
                ' Create time entry
                timeEntries(newCount).IssueKey = issueKey
                timeEntries(newCount).IssueSummary = issueSummary
                timeEntries(newCount).Assignee = assignee
                timeEntries(newCount).FeatureLink = featureLink
                timeEntries(newCount).TimeSpent = worklog("timeSpentSeconds") / 3600 ' Convert to hours
                timeEntries(newCount).DateLogged = worklogDate
                timeEntries(newCount).Author = worklog("author")("displayName")
                
                If Not IsNull(worklog("comment")) Then
                    timeEntries(newCount).WorkDescription = worklog("comment")
                Else
                    timeEntries(newCount).WorkDescription = ""
                End If
            End If
        Next j
    End If
    
    ProcessIssueWorklogs = newCount
    Exit Function
    
ProcessError:
    ProcessIssueWorklogs = currentCount
End Function

'========================================================================
' DATA PROCESSING FUNCTIONS
'========================================================================

Function CreateAggregatedSummary(timeEntries() As TimeEntry, entryCount As Integer, ByRef summaries() As FeatureAssigneeSummary) As Integer
    '
    ' Create aggregated summary by Feature Link and Assignee
    '
    On Error GoTo SummaryError
    
    ' Use Collection to group unique combinations
    Dim groups As New Collection
    Dim groupKey As String
    
    Dim i As Integer
    For i = 1 To entryCount
        groupKey = timeEntries(i).FeatureLink & "|" & timeEntries(i).Assignee
        
        On Error Resume Next
        Dim existingGroup As FeatureAssigneeSummary
        existingGroup = groups(groupKey)
        
        If Err.Number = 0 Then
            ' Group exists, add to totals
            existingGroup.TotalHours = existingGroup.TotalHours + timeEntries(i).TimeSpent
            existingGroup.IssueCount = existingGroup.IssueCount + 1
            groups.Remove groupKey
            groups.Add existingGroup, groupKey
        Else
            ' New group
            Dim newGroup As FeatureAssigneeSummary
            newGroup.FeatureLink = timeEntries(i).FeatureLink
            newGroup.Assignee = timeEntries(i).Assignee
            newGroup.TotalHours = timeEntries(i).TimeSpent
            newGroup.IssueCount = 1
            groups.Add newGroup, groupKey
        End If
        On Error GoTo SummaryError
    Next i
    
    ' Convert Collection to Array
    ReDim summaries(1 To groups.Count)
    For i = 1 To groups.Count
        summaries(i) = groups(i)
    Next i
    
    CreateAggregatedSummary = groups.Count
    Exit Function
    
SummaryError:
    CreateAggregatedSummary = 0
End Function

'========================================================================
' EXCEL OUTPUT FUNCTIONS
'========================================================================

Sub WriteRawDataToExcel(timeEntries() As TimeEntry, entryCount As Integer)
    '
    ' Write raw time entry data to Excel worksheet
    '
    On Error GoTo WriteError
    
    Dim dataSheet As Worksheet
    Set dataSheet = ThisWorkbook.Worksheets("Raw Data")
    
    ' Clear existing data
    dataSheet.Cells.Clear
    
    ' Write headers
    dataSheet.Range("A1").Value = "Issue Key"
    dataSheet.Range("B1").Value = "Issue Summary"
    dataSheet.Range("C1").Value = "Assignee"
    dataSheet.Range("D1").Value = "Feature Link"
    dataSheet.Range("E1").Value = "Hours Logged"
    dataSheet.Range("F1").Value = "Date Logged"
    dataSheet.Range("G1").Value = "Author"
    dataSheet.Range("H1").Value = "Work Description"
    
    ' Format headers
    With dataSheet.Range("A1:H1")
        .Font.Bold = True
        .Interior.Color = RGB(68, 114, 196)
        .Font.Color = RGB(255, 255, 255)
    End With
    
    ' Write data
    Dim i As Integer
    For i = 1 To entryCount
        dataSheet.Cells(i + 1, 1).Value = timeEntries(i).IssueKey
        dataSheet.Cells(i + 1, 2).Value = timeEntries(i).IssueSummary
        dataSheet.Cells(i + 1, 3).Value = timeEntries(i).Assignee
        dataSheet.Cells(i + 1, 4).Value = timeEntries(i).FeatureLink
        dataSheet.Cells(i + 1, 5).Value = timeEntries(i).TimeSpent
        dataSheet.Cells(i + 1, 6).Value = timeEntries(i).DateLogged
        dataSheet.Cells(i + 1, 7).Value = timeEntries(i).Author
        dataSheet.Cells(i + 1, 8).Value = timeEntries(i).WorkDescription
    Next i
    
    ' Auto-fit columns
    dataSheet.Columns.AutoFit
    
    Exit Sub
    
WriteError:
    MsgBox "Error writing raw data: " & Err.Description, vbCritical
End Sub

Sub WriteSummaryToExcel(summaries() As FeatureAssigneeSummary, summaryCount As Integer)
    '
    ' Write aggregated summary to Excel worksheet
    '
    On Error GoTo WriteSummaryError
    
    Dim summarySheet As Worksheet
    Set summarySheet = ThisWorkbook.Worksheets("Summary")
    
    ' Clear existing data
    summarySheet.Cells.Clear
    
    ' Write headers
    summarySheet.Range("A1").Value = "Feature Link"
    summarySheet.Range("B1").Value = "Assignee"
    summarySheet.Range("C1").Value = "Total Hours"
    summarySheet.Range("D1").Value = "Issue Count"
    
    ' Format headers
    With summarySheet.Range("A1:D1")
        .Font.Bold = True
        .Interior.Color = RGB(68, 114, 196)
        .Font.Color = RGB(255, 255, 255)
    End With
    
    ' Write data
    Dim i As Integer
    For i = 1 To summaryCount
        summarySheet.Cells(i + 1, 1).Value = summaries(i).FeatureLink
        summarySheet.Cells(i + 1, 2).Value = summaries(i).Assignee
        summarySheet.Cells(i + 1, 3).Value = summaries(i).TotalHours
        summarySheet.Cells(i + 1, 4).Value = summaries(i).IssueCount
    Next i
    
    ' Auto-fit columns
    summarySheet.Columns.AutoFit
    
    Exit Sub
    
WriteSummaryError:
    MsgBox "Error writing summary: " & Err.Description, vbCritical
End Sub

'========================================================================
' UTILITY FUNCTIONS
'========================================================================

Function EncodeBase64(text As String) As String
    '
    ' Encode string to Base64 (simplified version)
    '
    Dim objXML As Object
    Dim objNode As Object
    
    Set objXML = CreateObject("MSXML2.DOMDocument")
    Set objNode = objXML.createElement("base64")
    
    objNode.dataType = "bin.base64"
    objNode.nodeTypedValue = StrConv(text, vbFromUnicode)
    EncodeBase64 = objNode.text
End Function

Function URLEncode(text As String) As String
    '
    ' Simple URL encoding
    '
    URLEncode = Replace(text, " ", "%20")
    URLEncode = Replace(URLEncode, "&", "%26")
    URLEncode = Replace(URLEncode, "=", "%3D")
    URLEncode = Replace(URLEncode, "+", "%2B")
End Function

Function ParseJiraDate(jiraDateStr As String) As Date
    '
    ' Parse JIRA date string (ISO format)
    '
    On Error GoTo DateParseError
    
    ' JIRA date format: 2024-01-15T09:00:00.000+0000
    Dim dateStr As String
    dateStr = Left(jiraDateStr, 19) ' Take only YYYY-MM-DDTHH:MM:SS part
    dateStr = Replace(dateStr, "T", " ")
    
    ParseJiraDate = CDate(dateStr)
    Exit Function
    
DateParseError:
    ParseJiraDate = Now()
End Function

Function ParseJson(jsonString As String) As Object
    '
    ' Parse JSON string (requires VBA-JSON library or ScriptControl)
    ' This is a simplified version - in practice, use a proper JSON parser
    '
    Set ParseJson = CreateObject("ScriptControl")
    ParseJson.Language = "JScript"
    Set ParseJson = ParseJson.Eval("(" + jsonString + ")")
End Function

Sub UpdateStatus(message As String)
    '
    ' Update status in the Excel status bar
    '
    Application.StatusBar = "JIRA Import: " & message
    DoEvents
End Sub

Sub ClearResults()
    '
    ' Clear previous results from worksheets
    '
    On Error Resume Next
    ThisWorkbook.Worksheets("Raw Data").Cells.Clear
    ThisWorkbook.Worksheets("Summary").Cells.Clear
    On Error GoTo 0
End Sub

Sub FormatWorksheets()
    '
    ' Apply formatting to worksheets
    '
    On Error Resume Next
    
    ' Format Raw Data sheet
    With ThisWorkbook.Worksheets("Raw Data")
        .Range("E:E").NumberFormat = "0.00"  ' Hours format
        .Range("F:F").NumberFormat = "mm/dd/yyyy"  ' Date format
    End With
    
    ' Format Summary sheet
    With ThisWorkbook.Worksheets("Summary")
        .Range("C:C").NumberFormat = "0.00"  ' Hours format
    End With
    
    On Error GoTo 0
End Sub

Sub CreateSummaryChart()
    '
    ' Create a chart from the summary data
    '
    On Error Resume Next
    
    Dim summarySheet As Worksheet
    Set summarySheet = ThisWorkbook.Worksheets("Summary")
    
    ' Create chart if data exists
    If summarySheet.Cells(2, 1).Value <> "" Then
        Dim chartRange As Range
        Set chartRange = summarySheet.Range("A1:C" & summarySheet.Cells(Rows.Count, 1).End(xlUp).Row)
        
        ' Add chart
        Dim chartObj As ChartObject
        Set chartObj = summarySheet.ChartObjects.Add(Left:=300, Width:=400, Top:=50, Height:=300)
        
        With chartObj.Chart
            .SetSourceData Source:=chartRange
            .ChartType = xlColumnClustered
            .HasTitle = True
            .ChartTitle.text = "Time Logged by Feature and Assignee"
        End With
    End If
    
    On Error GoTo 0
End Sub
