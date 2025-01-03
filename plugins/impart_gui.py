# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class impartGUI
###########################################################################

class impartGUI ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"KiCad Importer", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.BORDER_DEFAULT )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText_librarypath2 = wx.StaticText( self, wx.ID_ANY, u"Console", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_librarypath2.Wrap( -1 )

        self.m_staticText_librarypath2.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer.Add( self.m_staticText_librarypath2, 0, wx.ALL, 5 )

        self.m_text = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_BESTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
        self.m_text.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_text.SetMinSize( wx.Size( -1,130 ) )

        bSizer.Add( self.m_text, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline11 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline11.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_staticline11.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.m_staticline11.Hide()

        bSizer.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticline12 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline12.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_staticline12.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

        bSizer.Add( self.m_staticline12, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Source of Import", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        self.m_staticText7.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer.Add( self.m_staticText7, 0, wx.ALL, 5 )

        m_radioBox_sourceChoices = [ u"SamacSys / Ultralibrarian / Octopart / SnapEDA (manually download zip file)", u"LCSC (key in LCSC part no.)" ]
        self.m_radioBox_source = wx.RadioBox( self, wx.ID_ANY, u"Source", wx.DefaultPosition, wx.DefaultSize, m_radioBox_sourceChoices, 1, wx.RA_SPECIFY_COLS )
        self.m_radioBox_source.SetSelection( 0 )
        self.m_radioBox_source.SetFont( wx.Font( 14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer.Add( self.m_radioBox_source, 0, wx.ALIGN_CENTER_HORIZONTAL, 0 )

        fgSizer2 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer2.AddGrowableCol( 1 )
        fgSizer2.AddGrowableRow( 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText_zipfileloc = wx.StaticText( self, wx.ID_ANY, u"Zip File Location", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_zipfileloc.Wrap( -1 )

        self.m_staticText_zipfileloc.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        fgSizer2.Add( self.m_staticText_zipfileloc, 0, wx.ALL, 5 )

        self.m_dirPicker_sourcepath = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"ZIP files (*.zip)|*.zip", wx.DefaultPosition, wx.Size( -1,-1 ), wx.FLP_DEFAULT_STYLE )
        self.m_dirPicker_sourcepath.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_dirPicker_sourcepath.SetMaxSize( wx.Size( -1,25 ) )

        fgSizer2.Add( self.m_dirPicker_sourcepath, 2, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText_lcscpartno = wx.StaticText( self, wx.ID_ANY, u"LCSC Part Number (e.g. C4030)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_lcscpartno.Wrap( -1 )

        self.m_staticText_lcscpartno.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        fgSizer2.Add( self.m_staticText_lcscpartno, 0, wx.ALL, 5 )

        self.m_textCtrl_lcsc_number = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_PROCESS_ENTER )
        self.m_textCtrl_lcsc_number.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_textCtrl_lcsc_number.SetMaxSize( wx.Size( -1,25 ) )

        fgSizer2.Add( self.m_textCtrl_lcsc_number, 2, wx.ALL|wx.EXPAND, 5 )


        bSizer.Add( fgSizer2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline121 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline121.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_staticline121.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

        bSizer.Add( self.m_staticline121, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText_sourcepath = wx.StaticText( self, wx.ID_ANY, u"Import Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_sourcepath.Wrap( -1 )

        self.m_staticText_sourcepath.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer.Add( self.m_staticText_sourcepath, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        fgSizer11 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer11.AddGrowableCol( 1 )
        fgSizer11.AddGrowableRow( 0 )
        fgSizer11.SetFlexibleDirection( wx.HORIZONTAL )
        fgSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_NONE )

        self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"Optional Prefix (e.g. \"MCU_Atmel\")", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )

        self.m_staticText13.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        fgSizer11.Add( self.m_staticText13, 0, wx.ALL, 5 )

        self.m_textCtrl_prefix = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl_prefix.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_textCtrl_prefix.SetMaxSize( wx.Size( -1,25 ) )

        fgSizer11.Add( self.m_textCtrl_prefix, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer.Add( fgSizer11, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL|wx.EXPAND, 5 )

        self.m_staticline1211 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline1211.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_staticline1211.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

        bSizer.Add( self.m_staticline1211, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText_sourcepath1 = wx.StaticText( self, wx.ID_ANY, u"Output Parameters", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_sourcepath1.Wrap( -1 )

        self.m_staticText_sourcepath1.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

        bSizer.Add( self.m_staticText_sourcepath1, 0, wx.ALL, 5 )

        self.m_overwrite = wx.CheckBox( self, wx.ID_ANY, u"Overwrite existing entry in library", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_overwrite.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer.Add( self.m_overwrite, 0, wx.ALL, 5 )

        fgSizer21 = wx.FlexGridSizer( 2, 2, 0, 0 )
        fgSizer21.AddGrowableCol( 1 )
        fgSizer21.AddGrowableRow( 0 )
        fgSizer21.SetFlexibleDirection( wx.BOTH )
        fgSizer21.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText_librarypath = wx.StaticText( self, wx.ID_ANY, u"Library location (same as ${KICAD_3RD_PARTY}):", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_librarypath.Wrap( -1 )

        self.m_staticText_librarypath.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        fgSizer21.Add( self.m_staticText_librarypath, 0, wx.ALL, 5 )

        self.m_dirPicker_librarypath = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( -1,-1 ), wx.DIRP_DEFAULT_STYLE )
        self.m_dirPicker_librarypath.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_dirPicker_librarypath.SetMinSize( wx.Size( 300,-1 ) )
        self.m_dirPicker_librarypath.SetMaxSize( wx.Size( -1,25 ) )

        fgSizer21.Add( self.m_dirPicker_librarypath, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText_librarypath1 = wx.StaticText( self, wx.ID_ANY, u"Library name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText_librarypath1.Wrap( -1 )

        self.m_staticText_librarypath1.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        fgSizer21.Add( self.m_staticText_librarypath1, 0, wx.ALL, 5 )

        self.m_textCtrl_libname = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl_libname.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_textCtrl_libname.SetMaxSize( wx.Size( -1,25 ) )

        fgSizer21.Add( self.m_textCtrl_libname, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer.Add( fgSizer21, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        self.m_staticline1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_staticline1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

        bSizer.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"There is no guarantee for faultless function. Use only at your own risk. Should there be any errors please write an issue.\nNecessary settings for the integration of the libraries can be found in the README:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        self.m_staticText5.Hide()
        self.m_staticText5.SetMinSize( wx.Size( -1,50 ) )

        bSizer.Add( self.m_staticText5, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5 )

        self.m_button_migrate = wx.Button( self, wx.ID_ANY, u"Migrate the libraries (highly recommended)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button_migrate.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.m_button_migrate.Hide()
        self.m_button_migrate.SetMaxSize( wx.Size( -1,150 ) )

        bSizer.Add( self.m_button_migrate, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button = wx.Button( self, wx.ID_ANY, u"Import!", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button.SetFont( wx.Font( 13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer.Add( self.m_button, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer )
        self.Layout()
        bSizer.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.on_close )
        self.m_radioBox_source.Bind( wx.EVT_RADIOBOX, self.RadioBoxPressed )
        self.m_dirPicker_librarypath.Bind( wx.EVT_DIRPICKER_CHANGED, self.DirChange )
        self.m_textCtrl_libname.Bind( wx.EVT_TEXT_ENTER, self.DirChange )
        self.m_button_migrate.Bind( wx.EVT_BUTTON, self.migrate_libs )
        self.m_button.Bind( wx.EVT_BUTTON, self.BottonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def on_close( self, event ):
        event.Skip()

    def RadioBoxPressed( self, event ):
        event.Skip()

    def DirChange( self, event ):
        event.Skip()


    def migrate_libs( self, event ):
        event.Skip()

    def BottonClick( self, event ):
        event.Skip()


