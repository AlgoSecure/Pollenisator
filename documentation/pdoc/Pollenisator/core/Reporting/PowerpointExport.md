Module Pollenisator.core.Reporting.PowerpointExport
===================================================

Functions
---------

    
`addSerieToChart(presentation, index_chart, serie_name, serie)`
:   

    
`copyShape(shape, idx)`
:   

    
`createReport(defects_dict, template, out_name, **kwargs)`
:   

    
`deleteShape(shape)`
:   

    
`delete_slide(presentation, index)`
:   

    
`duplicate_slide(pres, index)`
:   Duplicate the slide with the given index in pres.
    
    Adds slide to the end of the presentation

    
`findShapeContaining(document, slide_i, search)`
:   

    
`findSlideTableContaining(document, search)`
:   

    
`findTableInSlide(document, slide_i, search)`
:   

    
`findTextInDocument(document, search)`
:   Replace at a run level a text that will be searched in all the document paragraphs and tables.
        Args:
            document: the document object (opened pptx with at lease one paragraph or table inside)
            search: The string to search for that will be replaced. //!\ The search is done at a run level
        Return:
            The slide index where the text was found, None otherwise

    
`findTextInTable(tbl, search)`
:   

    
`findTextInTextFrame(shapeTextFrame, search)`
:   

    
`move_slide(presentation, old_index, new_index)`
:   

    
`replaceTextInChart(_chrt, _search, _replace)`
:   

    
`replaceTextInDocument(document, search, replace)`
:   Replace at a run level a text that will be searched in all the document paragraphs and tables.
        Args:
            document: the document object (opened pptx with at lease one paragraph or table inside)
            search: The string to search for that will be replaced. //!\ The search is done at a run level
            replace: The string to replace the search by.

    
`replaceTextInParagraph(paragraph, search, replace)`
:   Replace at a run level a text that will be searched in the given paragraph.
        Args:
            table: the table we want to replace a text inside
            search: The string to search for that will be replaced. //!\ The search is done at a run level
            replace: The string to replace the search by.
        Returns:
            Return None if nothing was found, the run where the string was replaced otherwise

    
`replaceTextInTable(tbl, search, replace)`
:   

    
`replaceTextInTextFrame(shapeTextFrame, search, replace)`
:   

    
`write_defect_from_input(result, document, table_d, slide_i, o_defect, count)`
:   

    
`write_each_defect(document, defects_dict)`
:   for each default
       Copy a table and a paragraph form the template marked with var_d_id and var_d_separator.
       replace the markers var_d_id var_d_separator var_d_id var_d_title var_d_ease var_d_impact var_d_description
    Then for each fixe of this default
        Copy a table form the template marked with var_c_id.
        replace the markers var_c_id var_d_separator var_c_title var_c_ease var_c_gain var_c_description
    
        Args:
            document: the document to search elements in
            defects_dict: the dictionary of defect gotten with the dedicated function getDefectDictFromExcel

    
`write_every_defect_fix(fixes, document, slide_i, count)`
:   

Classes
-------

`DummyProgressBar()`
:   

    ### Methods

    `update(self)`
    :