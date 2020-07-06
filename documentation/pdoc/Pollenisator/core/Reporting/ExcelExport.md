Module Pollenisator.core.Reporting.ExcelExport
==============================================

Functions
---------

    
`addDefectsRecap(workbook, defectDicts)`
:   Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.

    
`addDefectsReport(workbook)`
:   Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.

    
`addGlobalStatus(workbook)`
:   Add a global status reporting sheet to the given workbook.
    
    Args:
        workbook: The workbook to add the created sheet into.

    
`addNotesReport(workbook)`
:   Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.

    
`addReport(workbook)`
:   Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.

    
`exportExcel(defectsDict, outname=None)`
:   Export a given database calendar name to an excel reporting file.
    
    Args:
        dbName: The database name to be reported in the excel file.