' VBScript to create JIRA Time Tracker Excel Workbook
' Run this script to automatically create the workbook with VBA modules

Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = True
objExcel.DisplayAlerts = False

' Create new workbook
Set objWorkbook = objExcel.Workbooks.Add

' Import VBA modules
Set objVBProject = objWorkbook.VBProject

' Add JiraApiModule
Set objModule1 = objVBProject.VBComponents.Add(1) ' vbext_ct_StdModule
objModule1.Name = "JiraApiModule"

' Read and insert JiraApiModule code
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.OpenTextFile("JiraApiModule.bas", 1)
strCode = objFile.ReadAll
objFile.Close
objModule1.CodeModule.AddFromString strCode

' Add WorksheetSetup module
Set objModule2 = objVBProject.VBComponents.Add(1) ' vbext_ct_StdModule
objModule2.Name = "WorksheetSetup"

' Read and insert WorksheetSetup code
Set objFile = objFSO.OpenTextFile("WorksheetSetup.bas", 1)
strCode = objFile.ReadAll
objFile.Close
objModule2.CodeModule.AddFromString strCode

' Run worksheet setup
objExcel.Run "SetupWorksheets"

' Save as macro-enabled workbook
strFileName = objFSO.GetParentFolderName(WScript.ScriptFullName) & "\JiraTimeTracker.xlsm"
objWorkbook.SaveAs strFileName, 52 ' xlOpenXMLWorkbookMacroEnabled

WScript.Echo "JIRA Time Tracker workbook created successfully: " & strFileName

objExcel.DisplayAlerts = True
' objExcel.Quit ' Uncomment to close Excel automatically
