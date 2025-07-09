Attribute VB_Name = "WorksheetSetup"
'========================================================================
' Worksheet Setup Module
' Creates and configures worksheets for JIRA Time Tracker
'========================================================================

Option Explicit

Sub SetupWorksheets()
    '
    ' Create and configure all required worksheets
    '
    Application.ScreenUpdating = False
    
    ' Create worksheets
    Call CreateConfigSheet
    Call CreateSettingsSheet
    Call CreateRawDataSheet
    Call CreateSummarySheet
    Call CreateDashboardSheet
    
    ' Set active sheet to Dashboard
    ThisWorkbook.Worksheets("Dashboard").Activate
    
    Application.ScreenUpdating = True
    
    MsgBox "JIRA Time Tracker workbook setup complete!" & vbCrLf & _
           "Please configure your JIRA settings in the Config sheet.", _
           vbInformation, "Setup Complete"
End Sub

Sub CreateConfigSheet()
    '
    ' Create configuration worksheet
    '
    On Error Resume Next
    Dim configSheet As Worksheet
    Set configSheet = ThisWorkbook.Worksheets("Config")
    
    If configSheet Is Nothing Then
        Set configSheet = ThisWorkbook.Worksheets.Add
        configSheet.Name = "Config"
    End If
    On Error GoTo 0
    
    ' Clear existing content
    configSheet.Cells.Clear
    
    ' Create configuration form
    With configSheet
        ' Title
        .Range("A1").Value = "JIRA API Configuration"
        .Range("A1").Font.Size = 16
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(68, 114, 196)
        .Range("A1").Font.Color = RGB(255, 255, 255)
        .Range("A1:B1").Merge
        
        ' Configuration fields
        .Range("A3").Value = "JIRA Base URL:"
        .Range("A4").Value = "Username:"
        .Range("A5").Value = "API Token:"
        .Range("A6").Value = "Default JQL (Optional):"
        
        ' Sample values
        .Range("B3").Value = "https://yourcompany.atlassian.net"
        .Range("B4").Value = "your.email@company.com"
        .Range("B5").Value = "your-api-token-here"
        .Range("B6").Value = "project = YourProject"
        
        ' Format input cells
        With .Range("B3:B6")
            .Interior.Color = RGB(255, 255, 204)  ' Light yellow
            .Borders.LineStyle = xlContinuous
        End With
        
        ' Instructions
        .Range("A8").Value = "Instructions:"
        .Range("A8").Font.Bold = True
        .Range("A9").Value = "1. Replace the sample values above with your actual JIRA details"
        .Range("A10").Value = "2. Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens"
        .Range("A11").Value = "3. Use JQL to filter specific projects or issue types (optional)"
        .Range("A12").Value = "4. Go to Settings sheet to configure date range"
        .Range("A13").Value = "5. Click 'Fetch JIRA Data' button on Dashboard to import time logs"
        
        ' Auto-fit columns
        .Columns.AutoFit
    End With
End Sub

Sub CreateSettingsSheet()
    '
    ' Create settings worksheet
    '
    On Error Resume Next
    Dim settingsSheet As Worksheet
    Set settingsSheet = ThisWorkbook.Worksheets("Settings")
    
    If settingsSheet Is Nothing Then
        Set settingsSheet = ThisWorkbook.Worksheets.Add
        settingsSheet.Name = "Settings"
    End If
    On Error GoTo 0
    
    ' Clear existing content
    settingsSheet.Cells.Clear
    
    With settingsSheet
        ' Title
        .Range("A1").Value = "Date Range Settings"
        .Range("A1").Font.Size = 16
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(68, 114, 196)
        .Range("A1").Font.Color = RGB(255, 255, 255)
        .Range("A1:B1").Merge
        
        ' Date range settings
        .Range("A3").Value = "Start Date:"
        .Range("A4").Value = "End Date:"
        
        ' Default to current week
        Dim today As Date
        today = Date
        Dim weekStart As Date
        Dim weekEnd As Date
        weekStart = today - Weekday(today, vbMonday) + 1
        weekEnd = weekStart + 6
        
        .Range("B3").Value = weekStart
        .Range("B4").Value = weekEnd
        
        ' Format date cells
        With .Range("B3:B4")
            .NumberFormat = "mm/dd/yyyy"
            .Interior.Color = RGB(255, 255, 204)  ' Light yellow
            .Borders.LineStyle = xlContinuous
        End With
        
        ' Quick date range buttons
        .Range("A6").Value = "Quick Date Ranges:"
        .Range("A6").Font.Bold = True
        
        ' Instructions
        .Range("A8").Value = "Instructions:"
        .Range("A8").Font.Bold = True
        .Range("A9").Value = "• Modify the dates above to specify the time period for time log import"
        .Range("A10").Value = "• The system will fetch all work logs recorded within this date range"
        .Range("A11").Value = "• Default is set to current week (Monday to Sunday)"
        
        .Columns.AutoFit
    End With
    
    ' Add quick date range buttons
    Call AddDateRangeButtons(settingsSheet)
End Sub

Sub CreateRawDataSheet()
    '
    ' Create raw data worksheet
    '
    On Error Resume Next
    Dim dataSheet As Worksheet
    Set dataSheet = ThisWorkbook.Worksheets("Raw Data")
    
    If dataSheet Is Nothing Then
        Set dataSheet = ThisWorkbook.Worksheets.Add
        dataSheet.Name = "Raw Data"
    End If
    On Error GoTo 0
    
    dataSheet.Cells.Clear
    
    With dataSheet
        ' Title
        .Range("A1").Value = "Raw Time Log Data"
        .Range("A1").Font.Size = 14
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(68, 114, 196)
        .Range("A1").Font.Color = RGB(255, 255, 255)
        .Range("A1:H1").Merge
        
        ' Placeholder message
        .Range("A3").Value = "Click 'Fetch JIRA Data' on the Dashboard to populate this sheet with time log data."
        .Range("A3").Font.Italic = True
        .Range("A3").Font.Color = RGB(128, 128, 128)
        
        .Columns.AutoFit
    End With
End Sub

Sub CreateSummarySheet()
    '
    ' Create summary worksheet
    '
    On Error Resume Next
    Dim summarySheet As Worksheet
    Set summarySheet = ThisWorkbook.Worksheets("Summary")
    
    If summarySheet Is Nothing Then
        Set summarySheet = ThisWorkbook.Worksheets.Add
        summarySheet.Name = "Summary"
    End If
    On Error GoTo 0
    
    summarySheet.Cells.Clear
    
    With summarySheet
        ' Title
        .Range("A1").Value = "Time Summary by Feature & Assignee"
        .Range("A1").Font.Size = 14
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(68, 114, 196)
        .Range("A1").Font.Color = RGB(255, 255, 255)
        .Range("A1:D1").Merge
        
        ' Placeholder message
        .Range("A3").Value = "Summary data will appear here after importing JIRA time logs."
        .Range("A3").Font.Italic = True
        .Range("A3").Font.Color = RGB(128, 128, 128)
        
        .Columns.AutoFit
    End With
End Sub

Sub CreateDashboardSheet()
    '
    ' Create main dashboard worksheet
    '
    On Error Resume Next
    Dim dashSheet As Worksheet
    Set dashSheet = ThisWorkbook.Worksheets("Dashboard")
    
    If dashSheet Is Nothing Then
        Set dashSheet = ThisWorkbook.Worksheets.Add
        dashSheet.Name = "Dashboard"
    End If
    On Error GoTo 0
    
    dashSheet.Cells.Clear
    
    With dashSheet
        ' Main title
        .Range("A1").Value = "JIRA Time Tracker Dashboard"
        .Range("A1").Font.Size = 20
        .Range("A1").Font.Bold = True
        .Range("A1").Interior.Color = RGB(68, 114, 196)
        .Range("A1").Font.Color = RGB(255, 255, 255)
        .Range("A1:F1").Merge
        
        ' Description
        .Range("A3").Value = "Import and analyze JIRA time tracking data by feature and assignee"
        .Range("A3").Font.Size = 12
        .Range("A3").Font.Italic = True
        .Range("A3:F3").Merge
        
        ' Setup instructions
        .Range("A5").Value = "Setup Instructions:"
        .Range("A5").Font.Bold = True
        .Range("A5").Font.Size = 14
        
        .Range("A6").Value = "1. Configure JIRA connection in 'Config' sheet"
        .Range("A7").Value = "2. Set date range in 'Settings' sheet"
        .Range("A8").Value = "3. Click 'Fetch JIRA Data' button below"
        .Range("A9").Value = "4. View results in 'Raw Data' and 'Summary' sheets"
        
        ' Status area
        .Range("A12").Value = "Status:"
        .Range("A12").Font.Bold = True
        .Range("B12").Value = "Ready to import data"
        .Range("B12").Interior.Color = RGB(204, 255, 204)  ' Light green
        
        .Columns.AutoFit
    End With
    
    ' Add main action button
    Call AddFetchDataButton(dashSheet)
    
    ' Add navigation buttons
    Call AddNavigationButtons(dashSheet)
End Sub

Sub AddFetchDataButton(ws As Worksheet)
    '
    ' Add the main Fetch Data button
    '
    Dim btn As Button
    Set btn = ws.Buttons.Add(150, 250, 200, 40)
    
    With btn
        .Caption = "🔄 Fetch JIRA Data"
        .Font.Size = 12
        .Font.Bold = True
        .OnAction = "FetchJiraTimeData"
    End With
End Sub

Sub AddNavigationButtons(ws As Worksheet)
    '
    ' Add navigation buttons
    '
    Dim configBtn As Button
    Set configBtn = ws.Buttons.Add(50, 320, 100, 30)
    With configBtn
        .Caption = "⚙️ Config"
        .OnAction = "ShowConfigSheet"
    End With
    
    Dim settingsBtn As Button
    Set settingsBtn = ws.Buttons.Add(160, 320, 100, 30)
    With settingsBtn
        .Caption = "📅 Settings"
        .OnAction = "ShowSettingsSheet"
    End With
    
    Dim rawDataBtn As Button
    Set rawDataBtn = ws.Buttons.Add(270, 320, 100, 30)
    With rawDataBtn
        .Caption = "📊 Raw Data"
        .OnAction = "ShowRawDataSheet"
    End With
    
    Dim summaryBtn As Button
    Set summaryBtn = ws.Buttons.Add(380, 320, 100, 30)
    With summaryBtn
        .Caption = "📈 Summary"
        .OnAction = "ShowSummarySheet"
    End With
End Sub

Sub AddDateRangeButtons(ws As Worksheet)
    '
    ' Add quick date range selection buttons
    '
    Dim thisWeekBtn As Button
    Set thisWeekBtn = ws.Buttons.Add(50, 150, 80, 25)
    With thisWeekBtn
        .Caption = "This Week"
        .OnAction = "SetThisWeek"
    End With
    
    Dim lastWeekBtn As Button
    Set lastWeekBtn = ws.Buttons.Add(140, 150, 80, 25)
    With lastWeekBtn
        .Caption = "Last Week"
        .OnAction = "SetLastWeek"
    End With
    
    Dim thisMonthBtn As Button
    Set thisMonthBtn = ws.Buttons.Add(230, 150, 80, 25)
    With thisMonthBtn
        .Caption = "This Month"
        .OnAction = "SetThisMonth"
    End With
End Sub

'========================================================================
' NAVIGATION FUNCTIONS
'========================================================================

Sub ShowConfigSheet()
    ThisWorkbook.Worksheets("Config").Activate
End Sub

Sub ShowSettingsSheet()
    ThisWorkbook.Worksheets("Settings").Activate
End Sub

Sub ShowRawDataSheet()
    ThisWorkbook.Worksheets("Raw Data").Activate
End Sub

Sub ShowSummarySheet()
    ThisWorkbook.Worksheets("Summary").Activate
End Sub

'========================================================================
' DATE RANGE HELPER FUNCTIONS
'========================================================================

Sub SetThisWeek()
    Dim today As Date
    today = Date
    Dim weekStart As Date
    weekStart = today - Weekday(today, vbMonday) + 1
    
    With ThisWorkbook.Worksheets("Settings")
        .Range("B3").Value = weekStart
        .Range("B4").Value = weekStart + 6
    End With
    
    MsgBox "Date range set to this week", vbInformation
End Sub

Sub SetLastWeek()
    Dim today As Date
    today = Date
    Dim lastWeekStart As Date
    lastWeekStart = today - Weekday(today, vbMonday) + 1 - 7
    
    With ThisWorkbook.Worksheets("Settings")
        .Range("B3").Value = lastWeekStart
        .Range("B4").Value = lastWeekStart + 6
    End With
    
    MsgBox "Date range set to last week", vbInformation
End Sub

Sub SetThisMonth()
    Dim today As Date
    today = Date
    Dim monthStart As Date
    Dim monthEnd As Date
    monthStart = DateSerial(Year(today), Month(today), 1)
    monthEnd = DateSerial(Year(today), Month(today) + 1, 0)
    
    With ThisWorkbook.Worksheets("Settings")
        .Range("B3").Value = monthStart
        .Range("B4").Value = monthEnd
    End With
    
    MsgBox "Date range set to this month", vbInformation
End Sub
