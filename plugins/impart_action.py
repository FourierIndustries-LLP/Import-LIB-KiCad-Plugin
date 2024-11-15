import pcbnew
import os.path
import wx
from time import sleep
from threading import Thread
import sys
import traceback
import importlib.util


"""
Comments for modifying the codebase for general purpose needs

Directory change calls a unified function called "DirChange". You can get the specific paths by directly referencing the pickers

backend_h.config.set_SRC_PATH(self.m_dirPicker_sourcepath.GetPath()). The source path is where this tool will look for zip files to import
backend_h.config.set_DEST_PATH(self.m_dirPicker_librarypath.GetPath()). The library path is where this tool will export all the files. 
    This directory must be the same as ${KICAD_3RD_PARTY} as defined in Preferences > Configure Paths

import_all() from KiCadImport.py is the main function responsible for importing a ZIP file, so modifications to prefixes etc has to modify that function.
In KiCadImport.py, remote_type.name will have to be replaced with the custom library name to make sure all of them goes into the same library of parts

The key import functions: import_footprint, import_dcm, import_lib, import_lib_new, import_model, which are all called by import_all()

TODO: found_model.name should be checked to see if it should be altered (since we get to define the model name in the GUI)

SnapEDA have a bad issue with not including the 3D model with the symbol+footprint combination and I will not add it in the GUI as an option

Ultralibrarian requires you to select 3D diagram AND Kicad format before this will import all the models, so be careful with those

The current non-volatile configuration file includes:
SRC_PATH: the source of the zip file's containing directory (now modified to the path to the zip file itself)
DEST_PATH: the library's path (aka the destination)

We should add the following config variables:
LIB_NAME: The name of the library, instead of naming our libraries as the source of the symbol/footprint. This is company specific

One of the issues when it comes to footprint naming is that some parts already use standardized footprints. For example, a QFN chip probably
already complies to a pre-installed QFN footprint. Footprint hunting might be more difficult when there's no prefix
"""


try:
    if __name__ == "__main__":
        from impart_gui import impartGUI
        from KiCadImport import import_lib
        from impart_helper_func import filehandler, config_handler, KiCad_Settings
        from impart_migration import find_old_lib_files, convert_lib_list
    else:
        # relative import is required in kicad
        from .impart_gui import impartGUI
        from .KiCadImport import import_lib
        from .impart_helper_func import filehandler, config_handler, KiCad_Settings
        from .impart_migration import find_old_lib_files, convert_lib_list
except Exception as e:
    print(e)
    print(traceback.format_exc())


EVT_UPDATE_ID = wx.NewIdRef()


def EVT_UPDATE(win, func):
    win.Connect(-1, -1, EVT_UPDATE_ID, func)


class ResultEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_UPDATE_ID)
        self.data = data


class PluginThread(Thread):
    def __init__(self, wxObject):
        Thread.__init__(self)
        self.wxObject = wxObject
        self.stopThread = False
        self.start()

    def run(self):
        lenStr = 0
        global backend_h
        while not self.stopThread:
            if lenStr != len(backend_h.print_buffer):
                self.report(backend_h.print_buffer)
                lenStr = len(backend_h.print_buffer)
            sleep(0.5)

    def report(self, status):
        wx.PostEvent(self.wxObject, ResultEvent(status))


class impart_backend:
    def __init__(self):
        path2config = os.path.join(os.path.dirname(__file__), "config.ini")
        self.config = config_handler(path2config)
        path_seting = pcbnew.SETTINGS_MANAGER().GetUserSettingsPath()
        self.KiCad_Settings = KiCad_Settings(path_seting)
        self.runThread = False
        self.autoImport = False
        self.overwriteImport = False
        self.import_old_format = False
        self.autoLib = False
        self.folderhandler = filehandler(".")
        self.print_buffer = ""
        self.importer = import_lib()
        self.importer.print = self.print2buffer

        def version_to_tuple(version_str):
            return tuple(map(int, version_str.split(".")))

        minVersion = "8.0.4"
        if version_to_tuple(pcbnew.Version()) < version_to_tuple(minVersion):
            self.print2buffer("[warn] KiCad Version: " + str(pcbnew.FullVersion()))
            self.print2buffer("Minimum required KiCad version is " + minVersion)
            self.print2buffer("The plugin may not function as intended.\n")

        if not self.config.config_is_set:
            self.print2buffer(
                "[warn] You have not yet selected a library save location. "
                + "Please select the location first (it should be the same as what you defined as the KICAD_3RD_PARTY path variable)"
            )

            additional_information = "If this plugin is being used for the first time, additional setup in KiCad is required\n"
            self.print2buffer(additional_information)

    def print2buffer(self, *args):
        for text in args:
            self.print_buffer = self.print_buffer + str(text) + "\n"

    def __find_new_file__(self, prefix=""):
        path = self.config.get_SRC_PATH()
        lib_name = self.config.get_LIB_NAME()

        if not os.path.isfile(path):
            return 0

        while True:
            try:
                (res,) = self.importer.import_all(
                    path,
                    overwrite_if_exists=self.overwriteImport,
                    import_old_format=self.import_old_format,
                    library_name=lib_name,
                    prefix=prefix,
                )
                self.print2buffer("[info] " + res)
            except AssertionError as e:
                self.print2buffer("[error] " + e)
            except Exception as e:
                self.print2buffer("[error] " + e)
                backend_h.print2buffer(f"Error: {e}")
                backend_h.print2buffer("Python version " + sys.version)
                print(traceback.format_exc())
            self.print2buffer("")
            if not self.runThread:
                break
            if not pcbnew.GetBoard():
                break
            sleep(1)

        # while True:
        #     newfilelist = self.folderhandler.GetNewFiles(path)
        #     for lib in newfilelist:
        #         try:
        #             (res,) = self.importer.import_all(
        #                 lib,
        #                 overwrite_if_exists=self.overwriteImport,
        #                 import_old_format=self.import_old_format,
        #             )
        #             self.print2buffer(res)
        #         except AssertionError as e:
        #             self.print2buffer(e)
        #         except Exception as e:
        #             self.print2buffer(e)
        #             backend_h.print2buffer(f"Error: {e}")
        #             backend_h.print2buffer("Python version " + sys.version)
        #             print(traceback.format_exc())
        #         self.print2buffer("")

        #     if not self.runThread:
        #         break
        #     if not pcbnew.GetBoard():
        #         # print("pcbnew close")
        #         break
        #     sleep(1)


backend_h = impart_backend()

# This function checks if the environment is correctly configured for this plugin
def check_setup_correctness(add_if_possible=True, prefix=""):
    LIB_NAME = backend_h.config.get_LIB_NAME()
    setting = backend_h.KiCad_Settings
    DEST_PATH = backend_h.config.get_DEST_PATH()

    # Check if KICAD_3RD_PARTY envvar already exists
    msg = "[info] "
    msg += setting.check_GlobalVar(DEST_PATH, add_if_possible)

    # The lines work but old libraries should not be added automatically
    # libname = os.path.join(DEST_PATH, name + ".lib")
    # if os.path.isfile(libname):
    #     msg += setting.check_symbollib(name + ".lib", add_if_possible)

    sym_dir = os.path.join(DEST_PATH, LIB_NAME + ".kicad_sym")
    sym_dir_old = os.path.join(DEST_PATH, LIB_NAME + "_kicad_sym.kicad_sym")
    sym_dir_convert = os.path.join(DEST_PATH, LIB_NAME + "_old_lib.kicad_sym")

    if os.path.isfile(sym_dir):
        libname = LIB_NAME + ".kicad_sym"
        msg += setting.check_symbollib(libname, add_if_possible, prefix)
    elif os.path.isfile(sym_dir_old):
        libname = LIB_NAME + "_kicad_sym.kicad_sym"
        msg += setting.check_symbollib(libname, add_if_possible, prefix)

    if os.path.isfile(sym_dir_convert):
        libname = LIB_NAME + "_old_lib.kicad_sym"
        msg += setting.check_symbollib(libname, add_if_possible, prefix)

    sym_dir = os.path.join(DEST_PATH, LIB_NAME + ".pretty")
    if os.path.isdir(sym_dir):
        msg += setting.check_footprintlib(LIB_NAME, add_if_possible, prefix)

    if msg == "[info] ":
        msg=""
    return msg


class impart_frontend(impartGUI):
    global backend_h

    def __init__(self, board, action):
        super(impart_frontend, self).__init__(None)
        self.board = board
        self.action = action

        # Set default values
        self.m_dirPicker_sourcepath.SetPath(backend_h.config.get_SRC_PATH())
        self.m_dirPicker_librarypath.SetPath(backend_h.config.get_DEST_PATH())
        self.m_textCtrl_libname.SetValue(backend_h.config.get_LIB_NAME())

        self.m_overwrite.SetValue(backend_h.overwriteImport)

        if backend_h.runThread:
            self.m_button.Label = "Automatic import / Press to stop"
        else:
            self.m_button.Label = "Import!"

        EVT_UPDATE(self, self.updateDisplay)
        self.Thread = PluginThread(self)  # only for text output

        self.test_migrate_possible()

    def updateDisplay(self, status):
        self.m_text.SetValue(status.data)
        self.m_text.SetInsertionPointEnd()
        # self.m_text.SetScrollPos(wx.VERTICAL, self.m_text.GetScrollRange(wx.VERTICAL))
        # self.m_text.SetInsertionPoint(-1)

    # def print(self, text):
    #     self.m_text.AppendText(str(text)+"\n")

    def on_close(self, event):
        if backend_h.runThread:
            dlg = wx.MessageDialog(
                None,
                "The automatic import process continues in the background. "
                + "If this is not desired, it must be stopped.\n"
                + "As soon as the PCB Editor window is closed, the import process also ends.",
                "WARNING: impart background process",
                wx.KILL_OK | wx.ICON_WARNING,
            )
            if dlg.ShowModal() != wx.ID_OK:
                return

        backend_h.overwriteImport = self.m_overwrite.IsChecked()
        # backend_h.runThread = False
        self.Thread.stopThread = True  # only for text output
        event.Skip()

    def BottonClick(self, event):
        # Save the library name and so first!
        backend_h.config.set_LIB_NAME(self.m_textCtrl_libname.GetValue())
        backend_h.config.set_PREFIX(self.m_textCtrl_prefix.GetValue())
        prefix = self.m_textCtrl_prefix.GetValue()
        if len(prefix) > 0 and prefix[-1] == '_':
            # strip _ character from the right side in case the user added it
            prefix = prefix[0:-1]
        # Check if user is importing from ZIP or LCSC part number
        selection = self.m_radioBox_source.GetSelection()  # 0=zip import, 1=lcsc
        # TODO: add prefix to part numbers
        if selection == 1:
            # pydantic
            pydantic_spec = importlib.util.find_spec("pydantic")
            found_pydantic = pydantic_spec is not None
            if found_pydantic:
                try:
                    from impart_easyeda import easyeda2kicad_wrapper
                    component_id = (
                        self.m_textCtrl_lcsc_number.GetValue().strip()
                    )  # example: "C2040"
                    overwrite = self.m_overwrite.IsChecked()
                    backend_h.print2buffer(
                        "[info] Attempting to import EasyEDA / LCSC Part# : " + component_id
                    )
                    base_folder = backend_h.config.get_DEST_PATH()
                    easyeda_import = easyeda2kicad_wrapper()
                    easyeda_import.print = backend_h.print2buffer
                    easyeda_import.full_import(
                        component_id,
                        base_folder,
                        overwrite,
                        str(self.m_textCtrl_libname.GetValue()),
                        prefix
                    )
                    event.Skip()
                except Exception as e:
                    backend_h.print2buffer(f"[error] {e}")
                    backend_h.print2buffer("Python version " + sys.version)
                    print(traceback.format_exc())
            else:
                backend_h.print2buffer("[error] the pydantic package is not installed! Please install it using the following commands:")
                backend_h.print2buffer("For macOS: /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/pip3.9 install pydantic")
                backend_h.print2buffer("For Windows (Local Installation): %LOCALAPPDATA%\Programs\KiCad\8.0\\bin\python.exe -m pip install pydantic")
                backend_h.print2buffer("For more information, see https://github.com/Steffen-W/Import-LIB-KiCad-Plugin/issues/23")
        else:
            backend_h.config.set_SRC_PATH(self.m_dirPicker_sourcepath.GetPath())
            backend_h.config.set_DEST_PATH(self.m_dirPicker_librarypath.GetPath())
            backend_h.importer.set_DEST_PATH(backend_h.config.get_DEST_PATH())

            backend_h.overwriteImport = self.m_overwrite.IsChecked()

            if backend_h.runThread:
                backend_h.runThread = False
                self.m_button.Label = "Import!"
                return

            backend_h.runThread = False
            # THIS IS WHERE THE ACTUAL ACTION TAKES PLACE
            if len(prefix) > 0:
                backend_h.__find_new_file__(prefix + '_')
            else:
                backend_h.__find_new_file__()
            
            self.m_button.Label = "Import!"

            # if backend_h.autoImport:
            #     backend_h.runThread = True
            #     self.m_button.Label = "Automatic import running / Press to stop"
            #     x = Thread(target=backend_h.__find_new_file__, args=[])
            #     x.start()

            add_if_possible = False  # TODO This variable appears to automatically add directories if it does not exist. We will need more experimentation on this
            msg = check_setup_correctness(add_if_possible, prefix)
            if msg:
                msg += "\n\n[warn] More information can be found in the README for the integration into KiCad.\n"
                msg += "github.com/Steffen-W/Import-LIB-KiCad-Plugin"
                msg += "\nSome configurations require a KiCad restart to be detected correctly."

                dlg = wx.MessageDialog(
                    None, msg, "WARNING", wx.KILL_OK | wx.ICON_WARNING
                )

                if dlg.ShowModal() != wx.ID_OK:
                    return

                backend_h.print2buffer("\n##############################\n")
                backend_h.print2buffer(msg)
                backend_h.print2buffer("\n##############################\n")
            event.Skip()

    def DirChange(self, event):
        backend_h.config.set_SRC_PATH(self.m_dirPicker_sourcepath.GetPath())
        backend_h.config.set_DEST_PATH(self.m_dirPicker_librarypath.GetPath())
        backend_h.config.set_LIB_NAME(self.m_textCtrl_libname.GetValue())
        backend_h.folderhandler.filelist = []
        # self.test_migrate_possible()
        event.Skip()

    def get_old_libfiles(self):
        libpath = self.m_dirPicker_librarypath.GetPath()
        LIB_NAME = backend_h.config.get_LIB_NAME()
        libs = [LIB_NAME]
        # libs = ["Octopart", "Samacsys", "UltraLibrarian", "Snapeda", "EasyEDA"]
        return find_old_lib_files(folder_path=libpath, libs=libs)

    def test_migrate_possible(self):
        libs2migrate = self.get_old_libfiles()
        conv = convert_lib_list(libs2migrate, drymode=True)

        if len(conv):
            self.m_button_migrate.Show()
        else:
            self.m_button_migrate.Hide()

    # def migrate_libs(self, event):
    #     libs2migrate = self.get_old_libfiles()

    #     conv = convert_lib_list(libs2migrate, drymode=True)

    #     def print2GUI(text):
    #         backend_h.print2buffer(text)

    #     if len(conv) <= 0:
    #         print2GUI("Error in migrate_libs()")
    #         return

    #     SymbolTable = backend_h.KiCad_Settings.get_sym_table()
    #     SymbolLibsUri = {lib["uri"]: lib for lib in SymbolTable}
    #     libRename = []

    #     def lib_entry(lib):
    #         return "${KICAD_3RD_PARTY}/" + lib

    #     msg = ""
    #     for line in conv:
    #         if line[1].endswith(".blk"):
    #             msg += "\n" + line[0] + " rename to " + line[1]
    #         else:
    #             msg += "\n" + line[0] + " convert to " + line[1]
    #             if lib_entry(line[0]) in SymbolLibsUri:
    #                 entry = SymbolLibsUri[lib_entry(line[0])]
    #                 tmp = {
    #                     "oldURI": entry["uri"],
    #                     "newURI": lib_entry(line[1]),
    #                     "name": entry["name"],
    #                 }
    #                 libRename.append(tmp)

    #     msg_lib = ""
    #     if len(libRename):
    #         msg_lib += "The following changes must be made to the list of imported Symbol libs:\n"

    #         for tmp in libRename:
    #             msg_lib += f"\n{tmp['name']} : {tmp['oldURI']} \n-> {tmp['newURI']}"

    #         msg_lib += "\n\n"
    #         msg_lib += "It is necessary to adjust the settings of the imported symbol libraries in KiCad."
    #         msg += "\n\n" + msg_lib

    #     msg += "\n\nBackup files are also created automatically. "
    #     msg += "These are named '*.blk'.\nShould the changes be applied?"

    #     dlg = wx.MessageDialog(
    #         None, msg, "WARNING", wx.KILL_OK | wx.ICON_WARNING | wx.CANCEL
    #     )
    #     if dlg.ShowModal() == wx.ID_OK:
    #         print2GUI("Converted libraries:")
    #         conv = convert_lib_list(libs2migrate, drymode=False)
    #         for line in conv:
    #             if line[1].endswith(".blk"):
    #                 print2GUI(line[0] + " rename to " + line[1])
    #             else:
    #                 print2GUI(line[0] + " convert to " + line[1])
    #     else:
    #         return

    #     if not len(msg_lib):
    #         return

    #     msg_dlg = "\nShould the change be made automatically? A restart of KiCad is then necessary to apply all changes."
    #     dlg2 = wx.MessageDialog(
    #         None, msg_lib + msg_dlg, "WARNING", wx.KILL_OK | wx.ICON_WARNING | wx.CANCEL
    #     )
    #     if dlg2.ShowModal() == wx.ID_OK:
    #         for tmp in libRename:
    #             print2GUI(f"\n{tmp['name']} : {tmp['oldURI']} \n-> {tmp['newURI']}")
    #             backend_h.KiCad_Settings.sym_table_change_entry(
    #                 tmp["oldURI"], tmp["newURI"]
    #             )
    #         print2GUI("\nA restart of KiCad is then necessary to apply all changes.")
    #     else:
    #         print2GUI(msg_lib)

    #     self.test_migrate_possible()  # When everything has worked, the button disappears
    #     event.Skip()


class ActionImpartPlugin(pcbnew.ActionPlugin):
    def defaults(self):
        self.set_LOGO(False)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)

    def set_LOGO(self, is_red):
        self.name = "KiCad Importer"
        self.category = "Import library files"
        self.description = (
            "Import library files from Octopart, Samacsys, Ultralibrarian and EasyEDA"
        )
        self.show_toolbar_button = True

        self.icon_file_name = os.path.join(
            os.path.dirname(__file__), "icon_small.png"
        )
        self.dark_icon_file_name = self.icon_file_name

    def Run(self):
        global backend_h
        board = pcbnew.GetBoard()
        Impart_h = impart_frontend(board, self)
        Impart_h.ShowModal()
        Impart_h.Destroy()
        self.set_LOGO(is_red=backend_h.runThread)  # not yet working


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="KiCad Plugin")
    Impart_t = impart_frontend(None, None)
    Impart_t.ShowModal()
    Impart_t.Destroy()
