#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Fabien Barré for AlgoSecure
# Date: 11/07/2017
# Major version released: 09/2019
# @version: 1.0
"""
import tkinter as tk
import os
import argparse
import signal
import time
from core.Components.mongo import MongoCalendar
from core.Application.Appli import Appli
import AutoScanWorker as slave
from core.Models.Wave import Wave
from core.Models.Tool import Tool

class GracefulKiller:
    """
    Signal handler to shut down properly.

    Attributes:
        kill_now: a boolean that can checked to know that it's time to stop.
    """
    kill_now = False

    def __init__(self, app):
        """
        Constructor. Hook the signals SIGINT and SIGTERM to method exitGracefully

        Args:
            app: The appli object to stop
        """
        signal.signal(signal.SIGINT, self.exitGracefully)
        signal.signal(signal.SIGTERM, self.exitGracefully)
        # signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        self.app = app

    def exitGracefully(self, _signum, _frame):
        """
        Set the kill_now class attributes to True. Call the onClosing function of the application given at init.

        Args:
            signum: not used
            frame: not used
        """
        print('You pressed Ctrl+C!')
        self.app.onClosing()
        self.kill_now = True


#######################################
############## MAIN ###################
#######################################


def main():
    """Main function. Start pollenisator application
    """
    parser = argparse.ArgumentParser(
        description="Edit database stored in mongo database")
    parser.add_argument("--import", dest="importName",
                        action="store", nargs="?")
    parser.add_argument("--calendar", dest="calendarName", action="store")
    parser.add_argument("--exec", dest="execCmd", action="store")
    args, remainingArgs = parser.parse_known_args()
    if args.importName:
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.importDatabase(args.importName)
        return
    if args.execCmd and args.calendarName:
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.connectToDb(args.calendarName)
        cmdName = os.path.splitext(os.path.basename(args.execCmd.split(" ")[0]))[0]
        cmdName +="::"+str(time.time()).replace(" ","-")
        wave = Wave().initialize("Custom commands")
        wave.addInDb()
        tool = Tool()
        tool.initialize(cmdName, "Custom commands", "", None, None, None, "wave", args.execCmd+" "+(" ".join(remainingArgs)), dated="None", datef="None", scanner_ip="localhost")
        tool.updateInfos({"args":args.execCmd})
        res, iid = tool.addInDb()
        if res:
            slave.executeCommand(args.calendarName, str(iid), "auto-detect")
        return
    print("""
.__    ..              ,       
[__) _ || _ ._ * __ _.-+- _ ._.
|   (_)||(/,[ )|_) (_] | (_)[  
                               
""")
    root = tk.Tk()
    root.resizable(True, True)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, "icon/favicon.png")
    img = tk.PhotoImage(file=dir_path)
    root.iconphoto(True, img)

    root.minsize(width=400, height=400)
    root.resizable(True, True)
    root.title("Pollenisator")
    root.geometry("1220x830")
    gc = None
    app = Appli(root)
    try:
        root.protocol("WM_DELETE_WINDOW", app.onClosing)
        gc = GracefulKiller(app)
        root.mainloop()
        print("Exiting tkinter main loop")
    except tk.TclError:
        pass
    try:
        root.destroy()
        print("Destroying app window")
    except tk.TclError:
        pass
    app.onClosing()
    if gc is not None:
        gc.kill_now = True


if __name__ == '__main__':
    main()
