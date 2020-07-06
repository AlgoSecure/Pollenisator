import xlsxwriter
import os

def exportExcel(defectsDict, outname=None):
    """
    Export a given database calendar name to an excel reporting file.

    Args:
        dbName: The database name to be reported in the excel file.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    out_path = os.path.join(dir_path, "../../exports/", outname)
    workbook = xlsxwriter.Workbook(out_path)
    print("Created workbook at "+str(out_path))
    print("Adding global defect summary  2/5")
    addDefectsRecap(workbook, defectsDict)
    #print("Adding Notes report           3/5")
    #addNotesReport(workbook)
    #print("Adding Defect detailed report 4/5")
    #addDefectsReport(workbook)
    #print("Adding global report 5/5")
    #addReport(workbook)
    print("Saving...")
    workbook.close()

def addGlobalStatus(workbook):
    """
    Add a global status reporting sheet to the given workbook.
    
    Args:
        workbook: The workbook to add the created sheet into.
    """
    worksheet1 = workbook.add_worksheet("Status")
    colWave = 0
    colScope = 1
    colIp = 2
    colPort = 3
    colStatus = 4
    worksheet1.write(0, 0, "Wave")
    worksheet1.write(0, 1, "Scope")
    worksheet1.write(0, 2, "IP")
    worksheet1.write(0, 3, "Port")
    worksheet1.write(0, 4, "Status")
    # Create a format to use in the merged range.
    _ = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    ligne = 1
    mongoInstance = MongoCalendar.getInstance()
    waves = mongoInstance.find("waves", )
    for wave in waves:
        total = 0
        worksheet1.write(ligne, colWave, wave["wave"])
        agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"]}}, {"$count":"total"}])
        for elem in agg_res:
            total = elem["total"]
        agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "dated":{"$ne":"None"}, "datef":{"$ne":"None"}, "scanner_ip":{"$ne":"None"}}}, {"$count":"total"}])
        for elem in agg_res:
            done = elem["total"]
        if total > 0:
            worksheet1.write(ligne, colStatus, str(done)+"/"+str(total)+" ("+str(int((float(done)/float(total))*100))+"%)")
        ligne += 1
        
        scopes = mongoInstance.find("scopes", {"wave":wave["wave"]})
        for scope in scopes:
            worksheet1.write(ligne, colScope, scope["scope"])
            agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "scope":scope["scope"]}}, {"$count":"total"}])
            for elem in agg_res:
                total = elem["total"]
            agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "scope":scope["scope"], "dated":{"$ne":"None"}, "datef":{"$ne":"None"}, "scanner_ip":{"$ne":"None"}}}, {"$count":"total"}])
            for elem in agg_res:
                done = elem["total"]
            if total > 0:
                worksheet1.write(ligne, colStatus, str(done)+"/"+str(total)+" ("+str(int((float(done)/float(total))*100))+"%)")
            ligne += 1

            ips = mongoInstance.find("ips", {"wave":wave["wave"], "scope":scope["scope"]})
            for ip in ips:
                worksheet1.write(ligne, colIp, ip["ip"])
                agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"]}}, {"$count":"total"}])
                for elem in agg_res:
                    total = elem["total"]
                agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"], "dated":{"$ne":"None"}, "datef":{"$ne":"None"}, "scanner_ip":{"$ne":"None"}}}, {"$count":"total"}])
                for elem in agg_res:
                    done = elem["total"]
                if total > 0:
                    worksheet1.write(ligne, colStatus, str(done)+"/"+str(total)+" ("+str(int((float(done)/float(total))*100))+"%)")
                ligne += 1

                ports = mongoInstance.find("ports", {"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"]})
                for port in ports:
                    worksheet1.write(ligne, colPort, port["proto"]+"/"+port["port"])
                    agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"], "port":port["port"]}}, {"$count":"total"}])
                    for elem in agg_res:
                        total = elem["total"]
                    agg_res = mongoInstance.aggregate("tools", [{"$match":{"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"], "port":port["port"], "dated":{"$ne":"None"}, "datef":{"$ne":"None"}, "scanner_ip":{"$ne":"None"}}}, {"$count":"total"}])
                    for elem in agg_res:
                        done = elem["total"]
                    if total > 0:
                        worksheet1.write(ligne, colStatus, str(done)+"/"+str(total)+" ("+str(int((float(done)/float(total))*100))+"%)")
                    ligne += 1


def addNotesReport(workbook):
    """
    Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.
    """
    worksheet1 = workbook.add_worksheet("Notes")
    colWave = 0
    colScope = 1
    colIp = 2
    colPort = 3
    colStatus = 4
    worksheet1.write(0, 0, "Wave")
    worksheet1.write(0, 1, "Scope")
    worksheet1.write(0, 2, "IP")
    worksheet1.write(0, 3, "Port")
    worksheet1.write(0, 4, "Notes")
    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    merge_format_notes = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'green'})
    ligne = 1
    mongoInstance = MongoCalendar.getInstance()
    waves = mongoInstance.find("waves", )
    for wave in waves:
        waveLineStart = ligne
        ligne += 1
        scopes = mongoInstance.find("scopes", {"wave":wave["wave"]})
        for scope in scopes:
            scopeLineStart = ligne
            ligne += 1
            ips = mongoInstance.find("ips", {"wave":wave["wave"], "scope":scope["scope"]})
            for ip in ips:
                ipLineStart = ligne
                ligne += 1
                ports = mongoInstance.find("ports", {"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"]})
                for port in ports:
                    portLineStart = ligne
                    ligne += 1
                    worksheet1.write(portLineStart, colPort, port["proto"]+"/"+port["port"])
                    notes = port["service"]+"\n"
                    try:
                        notes += port["notes"]+"\n"
                    except:
                        pass
                    port_tools = mongoInstance.find("tools", {"lvl":"port", "wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"], "port":port["port"], "proto":port["proto"]})
                    for port_tool in port_tools:
                        try:
                            notes += "------------------------\n"+port_tool["name"]+":\n"+port_tool["notes"]+"\n"
                        except:
                            pass
                    worksheet1.write(portLineStart, colStatus, notes, merge_format_notes)
                ipLineEnd = ligne-1
                worksheet1.merge_range(ipLineStart, colIp, ipLineEnd, colIp, ip["ip"], merge_format)
                try:
                    notes = ip["notes"]
                except:
                    notes = "Nothing yet"
                ip_tools = mongoInstance.find("tools", {"lvl":"ip", "wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"]})
                for ip_tool in ip_tools:
                    try:
                        notes += "------------------------\n"+ip_tool["name"]+":\n"+ip_tool["notes"]+"\n"
                    except:
                        pass
                if notes.strip() != "":
                    worksheet1.merge_range(ipLineStart, colPort, ipLineStart, colStatus, notes, merge_format_notes)
            scopeLineEnd = ligne-1
            worksheet1.merge_range(scopeLineStart, colScope, scopeLineEnd, colScope, scope["scope"], merge_format)
            try:
                notes = scope["notes"]
            except:
                notes = "Nothing yet"
            scope_tools = mongoInstance.find("tools", {"lvl":"scope", "wave":wave["wave"], "scope":scope["scope"]})
            for scope_tool in scope_tools:
                try:
                    notes += "------------------------\n"+scope_tool["name"]+":\n"+scope_tool["notes"]+"\n"
                except:
                    pass
            if notes.strip() != "":
                worksheet1.merge_range(scopeLineStart, colIp, scopeLineStart, colStatus, notes, merge_format_notes)
        waveLineEnd = ligne-1
        worksheet1.merge_range(waveLineStart, colWave, waveLineEnd, colWave, wave["wave"], merge_format)

def addDefectsReport(workbook):
    """
    Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.
    """
    worksheet1 = workbook.add_worksheet("Security Defects")
    colTitle = 0
    colTarget = 1
    colNotes = 2
    worksheet1.write(0, colTitle, "Title")
    worksheet1.write(0, colTarget, "Vulnerable")
    worksheet1.write(0, colNotes, "Notes")
    # Create a format to use in the merged range.
    critical_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'black',
        'font_color': 'white'
    })
    major_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'red',
        'font_color': 'white'
    })
    important_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'orange',
        'font_color': 'white'
    })
    minor_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow',
        'font_color': 'black'
    })
    risk_formats = {"Critique":critical_risk_format, "Majeur":major_risk_format, "Important":important_risk_format, "Mineur":minor_risk_format}
    mongoInstance = MongoCalendar.getInstance()
    titles = mongoInstance.aggregate("defects", [{"$group":{"_id": "$title"}}])
    ligne = 1
    for title_id in titles:
        title = title_id["_id"] 
        defects = mongoInstance.find("defects", {"title":title})        
        defectLigneStart = ligne
        for defect in defects:
            
            target = defect["ip"]
            try:
                if defect["port"] is not None:
                    target+=":"+str(defect["port"])+" ("+str(defect["proto"])+")"
            except:
                pass
            worksheet1.write(ligne, colTarget, target)
            worksheet1.write(ligne, colNotes, defect["notes"])
            ligne += 1
        defectLigneEnd = ligne - 1
        if defectLigneEnd-defectLigneStart == 0:
            worksheet1.write(defectLigneStart, colTitle, title, risk_formats[defect["risk"]])
        else:
            worksheet1.merge_range(defectLigneStart, colTitle, defectLigneEnd, colTitle, title, risk_formats[defect["risk"]])
    #worksheet1.merge_range(waveLineStart, colWave, waveLineEnd, colWave, wave["wave"], merge_format)

def addDefectsRecap(workbook, defectDicts):
    """
    Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.
    """
    worksheet1 = workbook.add_worksheet("Report")
    ############ Number of security defects
    # Create a format to use in the merged range.
    critical_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'black',
        'font_color': 'white'
    })
    major_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'red',
        'font_color': 'white'
    })
    important_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'orange',
        'font_color': 'white'
    })
    minor_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow',
        'font_color': 'black'
    })
    strong_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#002060',
        'font_color': 'white'
    })
    medium_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#0070c0',
        'font_color': 'white'
    })
    QuickWin_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': '#00b0f0',
        'font_color': 'white'
    })
    important_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'orange',
        'font_color': 'white'
    })
    minor_risk_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow',
        'font_color': 'black'
    })
    border_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'white',
        'font_color': 'black'
    })
    risk_formats = {"Critique":critical_risk_format, "Majeur":major_risk_format, "Important":important_risk_format, "Mineur":minor_risk_format}
    fixes_formats = {"Quick Win":QuickWin_format, "Faible":QuickWin_format, "Modérée":medium_format, "Moyen":medium_format, "Fort":strong_format, "Envergure":strong_format}
    defects_dict = defectDicts
    impossible_to_connect = False
    worksheet1.write(0, 0, "Critique", risk_formats["Critique"])
    worksheet1.write(1, 0, str(len(defects_dict["Critique"].keys())), border_format)
    worksheet1.write(0, 1, "Majeur", risk_formats["Majeur"])
    worksheet1.write(1, 1, str(len(defects_dict["Majeur"].keys())), border_format)
    worksheet1.write(0, 2, "Important", risk_formats["Important"])
    worksheet1.write(1, 2, str(len(defects_dict["Important"].keys())), border_format)
    worksheet1.write(0, 3, "Mineur", risk_formats["Mineur"])
    worksheet1.write(1, 3, str(len(defects_dict["Mineur"].keys())), border_format)
    worksheet1.write(0, 4, "Total", border_format)
    worksheet1.write(1, 4, str(len(defects_dict["Mineur"].keys())+len(defects_dict["Important"].keys())+len(defects_dict["Majeur"].keys())+len(defects_dict["Critique"].keys())), border_format)

    ligne=3
    ligne_correctif = 3
    colID = 0
    colLibelle = 1
    colExploitation = 2
    colImpact = 3
    colType = 4
    colIdCorrectif = 6
    colLibelleCorrectif = 7
    colMOE = 8
    colGain = 9
    worksheet1.write(ligne, colID, "ID", border_format)
    worksheet1.write(ligne, colLibelle, "Libellé", border_format)
    worksheet1.write(ligne, colExploitation, "Exploitation", border_format)
    worksheet1.write(ligne, colImpact, "Impact", border_format)
    worksheet1.write(ligne, colType, "Type", border_format)
    worksheet1.write(ligne_correctif, colIdCorrectif, "ID", border_format)
    worksheet1.write(ligne_correctif, colLibelleCorrectif, "Libellé", border_format)
    worksheet1.write(ligne_correctif, colMOE, "Mise en oeuvre", border_format)
    worksheet1.write(ligne_correctif, colGain, "Gain en sécurité", border_format)
    ligne_correctif+=1
    criticity_list = ["Critique", "Majeur", "Important", "Mineur"]
    count_defect = 0
    for criticity in criticity_list:
        for title, defect_values in defects_dict[criticity].items():
            ligne+=1
            count_defect+=1
            format_criticity = risk_formats[criticity]
            worksheet1.write(ligne, colID, "D"+str(count_defect), format_criticity)
            worksheet1.write(ligne, colLibelle, title, format_criticity)
            worksheet1.write(ligne, colExploitation, defect_values["description"]["ease"], format_criticity)
            worksheet1.write(ligne, colImpact, defect_values["description"]["impact"], format_criticity)
            worksheet1.write(ligne, colType, ", ".join([x.strip() for x in defect_values["description"]["type"] if x.strip() != ""]), format_criticity)

def addReport(workbook):
    """
    Function triggered when a report is generated.
        Args:
            workbook:  a workbook object to write in.
    """
    worksheet1 = workbook.add_worksheet("Services")
    colWave = 0
    colScope = 1
    colIp = 2
    colPort = 3
    colStatus = 4
    worksheet1.write(0, 0, "Wave")
    worksheet1.write(0, 1, "Scope")
    worksheet1.write(0, 2, "IP")
    worksheet1.write(0, 3, "Port")
    worksheet1.write(0, 4, "Notes")
    # Create a format to use in the merged range.
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})
    merge_format_notes = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'green'})
    ligne = 1
    mongoInstance = MongoCalendar.getInstance()
    waves = mongoInstance.find("waves", )
    for wave in waves:
        waveLineStart = ligne
        ligne += 1
        scopes = mongoInstance.find("scopes", {"wave":wave["wave"]})
        for scope in scopes:
            scopeLineStart = ligne
            ligne += 1
            ips = mongoInstance.find("ips", {"wave":wave["wave"], "scope":scope["scope"]})
            for ip in ips:
                ipLineStart = ligne
                ligne += 1
                ports = mongoInstance.find("ports", {"wave":wave["wave"], "scope":scope["scope"], "ip":ip["ip"]})
                for port in ports:
                    portLineStart = ligne
                    ligne += 1
                    worksheet1.write(portLineStart, colPort, port["proto"]+"/"+port["port"])
                    notes = port["service"]
                    try:
                        notes += " / "+port["notes"]
                    except:
                        pass
                    worksheet1.write(portLineStart, colStatus, notes, merge_format_notes)
                ipLineEnd = ligne-1
                worksheet1.merge_range(ipLineStart, colIp, ipLineEnd, colIp, ip["ip"], merge_format)
                try:
                    notes = ip["notes"]
                except:
                    notes = "Nothing yet"
                if notes.strip() != "":
                    worksheet1.merge_range(ipLineStart, colPort, ipLineStart, colStatus, notes, merge_format_notes)
            scopeLineEnd = ligne-1
            worksheet1.merge_range(scopeLineStart, colScope, scopeLineEnd, colScope, scope["scope"], merge_format)
            try:
                notes = scope["notes"]
            except:
                notes = "Nothing yet"
            if notes.strip() != "":
                worksheet1.merge_range(scopeLineStart, colIp, scopeLineStart, colStatus, notes, merge_format_notes)
        waveLineEnd = ligne-1
        worksheet1.merge_range(waveLineStart, colWave, waveLineEnd, colWave, wave["wave"], merge_format)
