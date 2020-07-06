Module Pollenisator.core.Reporting.WordExport
=============================================

Functions
---------

    
`add_hyperlink(paragraph, text, url, style)`
:   

    
`copy_format_manual(runA, runB)`
:   

    
`copy_table_after(table, paragraph, addParagraph=None, addPagebreak=False)`
:   Copy a table and insert it after a given paragraph
        Args:
            table: the table to move
            paragraph: the paragraph to put the table after.
        Optional Args:
            addParagraph: Add another paragraph after the new copied table. default is None.

    
`createReport(defects_dict, template, out_name, **kwargs)`
:   

    
`delete_paragraph(paragraph)`
:   Delete a paragraph.
        Args:
            paragraph: the paragraph object to delete.

    
`downloadImgData(url)`
:   

    
`fill_cell(cell, text, font_color=None, bg_color=None, bold=False)`
:   Fill a table's cell's background with a background color, a text and a font_color for this text
    Also sets the vertical alignement of every cell as centered.
        Args:
            cell: the cell we want to fill
            text: the text to be written inside the cell
        Optional Args:
            font_color: a new font color to use for this text at RGB format (docx rgb). Default is None
            bg_color: A backgroud color to use for the cell at hexa rgb format (FFFFFF is white) default is None.
                        The color is written in xml directly as python-docx does not give a function to do that.

    
`findParagraphContaining(document, search)`
:   Find the first paragraph in all the given document to contain the given search text.
        Args:
            document: the document object (opened word docx with at least one paragraph inside)
            search: The string to search for that will be replaced. //!\ The search is done at a paragraph level
        Returns:
            Return None if the text was not found, else, it returns the paragraph object where the text was found

    
`findRowContaining(document, search)`
:   Find the first row of a table in all the given document to contain the given search text.
        Args:
            document: the document object (opened word docx with at least table inside)
            search: The string to search for that will be replaced. //!\ The search is done at a paragraph level
        Returns:
            Return (None, None) if the text was not found, else, it returns the tuple (table object, table index in document)

    
`format_block_res_table(table_res, start_defect_line_on_res_table, nb_line_res_table)`
:   

    
`getParagraphs(document)`
:   Retourne un generateur pour tous les paragraphes du document.
    La page d'entête n'étant pas incluse dans documents.paragraphs.

    
`insertPageBreak(paragraph)`
:   

    
`insert_images_after(paragraph, pics)`
:   

    
`insert_paragraph_after(paragraph, text=None, style=None)`
:   Insert a new paragraph after the given paragraph.
        Args:
            paragraph: the paragraph object after which the new paragraph will be created
        
        Optional Args:
            text: a string of text to write in the new paragraph, Default = None
            style: a style to be applied on the new paragraph, Default = None
    
        Returns:
            Returns a paragraph object for the new added paragraph

    
`mardownCodeBlockToWordStyle(paragraph, styles, state)`
:   

    
`markdownArrayToWordList(document, paragraph, state)`
:   

    
`markdownCodeToWordStyle(paragraph, initialRun, style)`
:   

    
`markdownEmphasisToItalic(paragraph, initialRun)`
:   de _Man-in-the-Middle_ entre le serveur
     # Absence de support de TLS_FALLBACK_SCSV
    
    TLS_FALLBACK_SCSV est une option permettant de mitiger les attaques dites de downgrade (type POODLE), afin d’empêcher un attaquant de forcer l’utilisation d’un protocole vulnérable lorsque des protocoles plus récents et sécurisés sont disponibles.

    
`markdownHeaderToWordStyle(paragraph, run, style)`
:   

    
`markdownImgToInsertedImage(paragraph, initialRun)`
:   

    
`markdownLinkToHyperlink(paragraph, initialRun, styles)`
:   

    
`markdownStrikeThroughToStrike(paragraph, initialRun)`
:   

    
`markdownStrongEmphasisToBold(paragraph, initialRun)`
:   

    
`markdownToWordInDocument(document)`
:   

    
`markdownToWordInParagraph(document, paragraph, styles, state)`
:   

    
`markdownToWordInRun(paragraph, initialRun, styles)`
:   

    
`markdownUnorderedListToWordList(paragraph, style, state)`
:   

    
`move_table_after(table, paragraph)`
:   Move a given table after a given paragraph
        Args:
            table: the table to move
            paragraph: the paragraph to put the table after.

    
`populate_defect_summary_table(document, defects_dict)`
:   Fill a table found with a decorator var_dsum_colId in a line.
    This table will contains a summary of the defects given the excel.
    The template must have a table with var_dsum_colId, var_dsum_colTit, var_dsum_colEase, var_dsum_colImpact, var_dsum_colType
    The template must have another table next to the previous with var_csum_colId, var_csum_colTit, var_csum_colEase, var_csum_colGain
        Args:
            document: the document object (opened word docx with at least one paragraph inside)
            defects_dict: the dictionary of defect gotten in the getDefectDictFromExcel function

    
`populate_services_table(document, parent)`
:   

    
`remove_row(table, row)`
:   remove a given row inside a given table
        Args:
            table: the table we want to delete a row in
            row: the row to delete

    
`replaceTextInDocument(document, search, replace)`
:   Replace at a run level a text that will be searched in all the document paragraphs and tables.
        Args:
            document: the document object (opened word docx with at lease one paragraph or table inside)
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

    
`replaceTextInTable(table, search, replace)`
:   Replace at a run level a text that will be searched in the given table cells.
        Args:
            table: the table we want to replace a text inside
            search: The string to search for that will be replaced. //!\ The search is done at a run level
            replace: The string to replace the search by.
        Returns:
            Return None if nothing was found, (row's index, cell's index) otherwise

    
`set_cell_border(cell, **kwargs)`
:   Set cell`s border
    Usage:
    
    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        start={"sz": 24, "val": "dashed", "shadow": "true"},
        end={"sz": 12, "val": "dashed"},
    )

    
`set_hyperlink(paragraph, run, url, text, style)`
:   

    
`splitRunOnMarker(paragraph, run, regexToSearch, markerToRemove)`
:   

    
`split_run_in_three(paragraph, run, split_start, split_end)`
:   

    
`split_run_in_two(paragraph, run, split_index)`
:   

    
`write_defect_from_input(result, document, table_d, separator, o_defect, count)`
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

    
`write_every_defect_fix(fixes, document, last_defect_paragraph, count)`
:   

    
`write_res_table_defect_line(table_res, risks_font_colors, risks_bg_colors, count, o_defect)`
:   

    
`write_res_table_fix_line(table_res, risk_bg_color, id_correctif, fixe)`
:   

Classes
-------

`DummyProgressBar()`
:   

    ### Methods

    `update(self)`
    :