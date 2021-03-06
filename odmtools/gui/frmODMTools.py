#!/usr/bin/env

'''
this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(this_file))
sys.path.insert(0, directory)
'''

import wx
import sys
import os
import logging
import mnuRibbon
from odmtools.controller.frmSeriesSelector import FrmSeriesSelector
from odmtools.gui.frmConsole import ODMConsole
import pnlPlot
import pnlDataTable
import wx.lib.agw.aui as aui
import wx.py.crust
import wx.stc
from odmtools.common import gtk_execute
from odmtools.lib.Appdirs.appdirs import user_config_dir
from wx.lib.pubsub import pub as Publisher
from odmtools.odmservices import ServiceManager
from pnlScript import pnlScript
from odmtools.common.logger import LoggerTool
from odmtools.controller import frmDBConfig
from odmtools.controller.frmAbout import  frmAbout


def create(parent):
    return frmODMToolsMain(parent)
[
    wxID_ODMTOOLS, wxID_ODMTOOLSCHECKLISTBOX2, wxID_ODMTOOLSCOMBOBOX1,
    wxID_ODMTOOLSCOMBOBOX2, wxID_ODMTOOLSCOMBOBOX4, wxID_ODMTOOLSCOMBOBOX5,
    wxID_ODMTOOLSGRID1, wxID_ODMTOOLSPANEL1, wxID_ODMTOOLSPANEL2,
    wxID_ODMTOOLSTOOLBAR1, wxID_PNLSELECTOR, wxID_TXTPYTHONSCRIPT,
    wxID_TXTPYTHONCONSOLE,
] = [wx.NewId() for _init_ctrls in range(13)]

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)

class frmODMToolsMain(wx.Frame):
    """

    """
    def __init__(self, parent):
        size = self._obtainScreenResolution()
        wx.Frame.__init__(self, id=wxID_ODMTOOLS, name=u'ODMTools', parent=parent,
            size=size, style=wx.DEFAULT_FRAME_STYLE, title=u'ODM Tools')

        ## Obtain any existing database connections
        self.service_manager = ServiceManager()
        self.service_manager.extractConnectionInfo()
        self.record_service = None


        ## Initalize database
        self._init_database()
        self._init_ctrls()
        self.Refresh()

    def _obtainScreenResolution(self):
        """ Calculates the size of ODMTools

        :return wx.Size:
        """

        defaultSize = wx.Size(850, 800)
        defaultHeight, defaultWidth = defaultSize
        screenHeight, screenWidth = wx.GetDisplaySize()
        minimumAllowedSize = wx.Size(640, 480)

        '''
        if minimumAllowedSize >= wx.GetDisplaySize():
            logger.fatal("ODMTools cannot be displayed in this resolution: %s \n\tPlease use a larger resolution"
                         % wx.GetDisplaySize())
            print "minimumAllowedsize: ", minimumAllowedSize, "display: ", wx.GetDisplaySize()
            sys.exit(0)
        '''

        newSize = defaultSize
        ## Screen size is greater than ODMTools' default size
        if screenHeight > defaultHeight and screenWidth > defaultWidth:
            pass
        ## Screen size is smaller than ODMTools' default size
        elif screenHeight < defaultHeight and screenWidth < defaultWidth:
            newSize = wx.Size(screenHeight/1.5, screenWidth/1.5)
        elif screenHeight < defaultHeight:
            newSize = wx.Size(screenHeight/1.5, defaultWidth)
        elif screenWidth < defaultWidth:
            newSize = wx.Size(defaultHeight, screenWidth/1.5)

        logger.debug("ODMTools Window Size: %s" % newSize)
        return newSize


    #############Entire Form Sizers##########
    def _init_sizers(self):
        # generated method, don't edit
        self.s = wx.BoxSizer(wx.VERTICAL)
        self._init_s_Items(self.s)
        self.SetSizer(self.s)

    def _init_s_Items(self, parent):
        # generated method, don't edit
        parent.AddWindow(self._ribbon, 0, wx.EXPAND)
        parent.AddWindow(self.pnlDocking, 85, flag=wx.ALL | wx.EXPAND)

    def _init_database(self, quit_if_cancel=True):
        logger.debug("Loading Database...")

        while True:
            ## Database connection is valid, threfore proceed through the rest of the program
            if self.service_manager.is_valid_connection():
                service = None
                conn_dict = None

                service = self.createService()
                conn_dict = self.service_manager.get_current_conn_dict()

                if self.servicesValid(service):
                    self.service_manager.add_connection(conn_dict)
                    break

            db_config = frmDBConfig.frmDBConfig(None, self.service_manager, False)
            value = db_config.ShowModal()
            if value == wx.ID_CANCEL and quit_if_cancel:
                logger.fatal("ODMTools is now closing because there is no database connection.")
                sys.exit(0)
            elif not quit_if_cancel:
                return False

            newConnection = db_config.panel.getFieldValues()
            self.service_manager.set_current_conn_dict(newConnection)
            db_config.Destroy()

        conn_dict = self.service_manager.get_current_conn_dict()
        msg = '%s://%s@%s/%s' % (
            conn_dict['engine'], conn_dict['user'], conn_dict['address'], conn_dict['db']
        )
        logger.debug("...Connected to '%s'" % msg)

        return True


    def servicesValid(self, service, displayMsg=True):
        """

        :param displayMsg:
            Option to display a message box if there is an issue with a service. Default: True
        :return:
        """
        valid = True

        ## Test if Series Catalog is empty
        if not service.get_all_used_sites():
            if displayMsg:
                msg = wx.MessageDialog(None, 'Series Catalog cannot be empty. Please enter in a new database connection',
                                           'Series Catalog is empty', wx.OK | wx.ICON_ERROR )
                msg.ShowModal()
            valid = False

        # @TODO If Jeff runs into other issues with services not being available, we can simply test different services here
        #if not service.get_all_variables():
        #    valid = False

        return valid

    def on_about_request(self, event):
        frmAbout(self)

    def MacReopenApp(self):
        """Called when the doc icon is clicked, and ???"""

        try: # it's possible for this event to come when the frame is closed
            self.GetTopWindow().Raise()
        except:
            pass

    ###################### Frame ################
    def _init_ctrls(self):
        # generated method, don't edit
        logger.debug("Loading frame...")


        self.SetIcon(gtk_execute.getIcon())

        self.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL,
                             False, u'Tahoma'))

        ############### Ribbon ###################
        logger.debug("Loading Ribbon Menu...")
        self._ribbon = mnuRibbon.mnuRibbon(parent=self, id=wx.ID_ANY, name='ribbon')


        if sys.platform == 'darwin':
            self.menu_bar  = wx.MenuBar()
            self.help_menu = wx.Menu()

            self.help_menu.Append(wx.ID_ABOUT,   "&About ODMTools")
            self.menu_bar.Append(self.help_menu, "&Help")

            self.SetMenuBar(self.menu_bar)
            self.Bind(wx.EVT_MENU, self.on_about_request, id=wx.ID_ABOUT)

    #        self.menu_bar.SetAutoWindowMenu()


        ################ Docking Tools##############
        self.pnlDocking = wx.Panel(id=wxID_ODMTOOLSPANEL1, name='pnlDocking',
                                   parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        ############# Graph ###############
        logger.debug("Loading Plot ...")
        self.pnlPlot = pnlPlot.pnlPlot(id=wxID_ODMTOOLSPANEL1, name='pnlPlot',
                                       parent=self.pnlDocking, size=wx.Size(605, 458),
                                       style=wx.TAB_TRAVERSAL)

        ################ Series Selection Panel ##################
        logger.debug("Loading Series Selector ...")
        self.pnlSelector = FrmSeriesSelector(name=u'pnlSelector', parent=self.pnlDocking,
                                             size=wx.Size(770, 388), style=wx.TAB_TRAVERSAL, dbservice=self.sc,
                                             serviceManager=self.service_manager)

        ####################grid Table View##################
        logger.debug("Loading DataTable ...")
        self.dataTable = pnlDataTable.pnlDataTable(id=wxID_ODMTOOLSGRID1, name='dataTable',
                                                   parent=self.pnlDocking, size=wx.Size(376, 280),
                                                   style=0)

        ############# Script & Console ###############
        logger.debug("Loading Python Console ...")
        self.txtPythonConsole = ODMConsole(id=wxID_TXTPYTHONCONSOLE, parent=self.pnlDocking, size=wx.Size(200, 200) )
        wx.CallAfter(self._postStartup)

        self.txtPythonConsole.shell.run("import datetime", prompt=False, verbose=False)

        self.txtPythonConsole.shell.run("edit_service = app.TopWindow.record_service", prompt=False, verbose=False)
        #self.txtPythonConsole.shell.run("import datetime", prompt=False, verbose=False)

        logger.debug("Loading Python Script ...")
        self.txtPythonScript = pnlScript(id=wxID_TXTPYTHONSCRIPT, name=u'txtPython', parent=self,
                                         size=wx.Size(200, 200))

        ############ Docking ###################
        logger.debug("Loading AuiManager ...")
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow(self.pnlDocking)

        self._mgr.AddPane(self.pnlPlot, aui.AuiPaneInfo().CenterPane()
                          .Name("Plot").Caption("Plot").MaximizeButton(True).DestroyOnClose(False)

        )

        self._mgr.AddPane(self.dataTable, aui.AuiPaneInfo().Right().Name("Table").
                          Show(show=False).Caption('Table View').MinSize(wx.Size(200, 200)).Floatable().Movable().
                          Position(1).MinimizeButton(True).MaximizeButton(True).DestroyOnClose(False)

        )

        self._mgr.AddPane(self.pnlSelector, aui.AuiPaneInfo().Bottom().Name("Selector").MinSize(wx.Size(50, 200)).
                          Movable().Floatable().Position(0).MinimizeButton(True).MaximizeButton(True).CloseButton(True)
                          .DestroyOnClose(False)
        )

        self._mgr.AddPane(self.txtPythonScript, aui.AuiPaneInfo().Caption('Script').
                          Name("Script").Movable().Floatable().Right()
                          .MinimizeButton(True).MaximizeButton(True).FloatingSize(size=(400, 400))
                          .CloseButton(True).Float().FloatingPosition(pos=(self.Position))
                          .Hide().CloseButton(True).DestroyOnClose(False)
        )


        self._mgr.AddPane(self.txtPythonConsole, aui.AuiPaneInfo().Caption('Python Console').
                          Name("Console").FloatingSize(size=(300, 400)).MinimizeButton(
            True).Movable().Floatable().MaximizeButton(True).CloseButton(True).Float()
                          .FloatingPosition(pos=(self.Position)).Show(show=False).DestroyOnClose(False)
        )


        ## TODO Fix loadingDockingSettings as it doesn't load it correctly.
        #self.loadDockingSettings()

        self.refreshConnectionInfo()
        self._mgr.Update()
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.dataTable.toggleBindings()

        Publisher.subscribe(self.onDocking, ("adjust.Docking"))
        Publisher.subscribe(self.onPlotSelection, ("select.Plot"))
        Publisher.subscribe(self.onExecuteScript, ("execute.script"))
        Publisher.subscribe(self.onChangeDBConn, ("change.dbConfig"))
        Publisher.subscribe(self.onSetScriptTitle, ("script.title"))
        #.subscribe(self.onSetScriptTitle, ("script.title"))
        Publisher.subscribe(self.onClose, ("onClose"))
        Publisher.subscribe(self.addEdit, ("selectEdit"))
        Publisher.subscribe(self.stopEdit, ("stopEdit"))

        self._init_sizers()
        self._ribbon.Realize()
        logger.debug("System starting ...")

    def refreshConnectionInfo(self):
        """Updates the Series Selector Connection Information for the user"""

        conn_dict = self.service_manager.get_current_conn_dict()

        msg = 'Series: %s://%s@%s/%s' % (
            conn_dict['engine'], conn_dict['user'], conn_dict['address'], conn_dict['db']
        )

        self._mgr.GetPane('Selector').Caption(msg)
        self._mgr.RefreshCaptions()


    def onDocking(self, value):
        paneDetails = self._mgr.GetPane(self.pnlPlot)

        if value == "Table":
            paneDetails = self._mgr.GetPane(self.dataTable)
            self.dataTable.toggleBindings()

        elif value == "Selector":
            paneDetails = self._mgr.GetPane(self.pnlSelector)

        elif value == "Script":
            paneDetails = self._mgr.GetPane(self.txtPythonScript)

        elif value == "Console":
            paneDetails = self._mgr.GetPane(self.txtPythonConsole)
            self.txtPythonConsole.crust.OnSashDClick(event=None)

        if paneDetails.IsNotebookPage() or paneDetails.dock_direction == 0:
            paneDetails.FloatingPosition(pos=self.Position)
            paneDetails.Float()

        if paneDetails.IsShown():
            paneDetails.Show(show=False)
        else:
            paneDetails.Show(show=True)
        self._mgr.Update()

    def onPlotSelection(self, value):
        self.pnlPlot.selectPlot(value)

    def addPlot(self, memDB, seriesID):
        #Memory Database
        self.pnlPlot.addPlot(memDB, seriesID)
        Publisher.sendMessage("EnablePlotButton", plot=self.pnlPlot.getActivePlotID(), isActive=True)
        #self._ribbon.enableButtons(self.pnlPlot.getActivePlotID)

    def onSetScriptTitle(self, title):
        scriptPane = self._mgr.GetPane(self.txtPythonScript)
        scriptPane.Caption(title)
        if scriptPane.IsFloating():
            scriptPane.Restore()
        self._mgr.Update()

    def addEdit(self, event):
        isSelected, seriesID, memDB = self.pnlSelector.onReadyToEdit()

        if isSelected:
            self.record_service = self.service_manager.get_record_service(self.txtPythonScript, seriesID,
                                                                          connection=memDB.conn)
            self._ribbon.toggleEditButtons(True)
            self.pnlPlot.addEditPlot(memDB, seriesID, self.record_service)

            self.dataTable.init(memDB, self.record_service)

            # set record service for console
            Publisher.sendMessage("setEdit", isEdit=True)
            logger.debug("Enabling Edit")
            self.record_service.toggle_record(True)
            #self._mgr.GetPane(self.txtPythonScript).Show(show=True)


        else:
            logger.debug("disabling Edit")
            Publisher.sendMessage("setEdit", isEdit=False)
            self.record_service.toggle_record(True)
            #self._mgr.GetPane(self.txtPythonScript).Show(show=False)

        #self._mgr.Update()

        logger.debug("Recording? %s" % self.record_service._record)


            #self.record_service = None
        self.txtPythonConsole.shell.run("edit_service = app.TopWindow.record_service", prompt=False, verbose=False)
        self.txtPythonConsole.shell.run("series_service = edit_service.get_series_service()", prompt=False, verbose=False)

    def stopEdit(self, event):

        self.pnlSelector.stopEdit()
        self.dataTable.stopEdit()
        self.pnlPlot.stopEdit()
        Publisher.sendMessage("toggleEdit", checked=False)
        self.record_service = None
        self._ribbon.toggleEditButtons(False)


    def getRecordService(self):
        return self.record_service

    def onChangeDBConn(self, event):
        db_config = frmDBConfig.frmDBConfig(None, self.service_manager, False)
        value = db_config.ShowModal()
        if value == wx.ID_CANCEL:
            return

        newConnection = db_config.panel.getFieldValues()
        self.service_manager.set_current_conn_dict(newConnection)
        db_config.Destroy()

        if self._init_database(quit_if_cancel=False):
            if self._ribbon.getEditStatus():
                self.stopEdit(event=None)

            self.pnlSelector.resetDB(self.sc)
            self.refreshConnectionInfo()
            self.pnlPlot.clear()
            self.dataTable.clear()

    def createService(self, conn_dict=""):
        """

        :param conn_dict:
            Provides the ability to send in your own conn_dict instead
            of relying on reading one in from connection.config
        :return:
        """

        self.sc = self.service_manager.get_series_service(conn_dict=conn_dict)
        return self.sc

    def getServiceManager(self):
        return self.service_manager

    def toggleConsoleTools(self):
        self.txtPythonConsole.ToggleTools()

    def onExecuteScript(self, value):
        for i in ('red', 'blue', 'green', 'magenta', 'gold', 'cyan', 'brown', 'lime', 'purple', 'navy'):
            self.txtPythonScript('This is a test\n', i)

    def loadDockingSettings(self):
        #test if there is a perspective to load
        try:
            # TODO Fix resource_path to appdirs
            os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config')
            f = open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'r')
        except:
            # Create the file if it doesn't exist
            open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'w').close()
            f = open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'r')

        self._mgr.LoadPerspective(f.read(), True)

    def onClose(self, event):
        """
            Closes ODMTools Python
            Closes AUI Manager then closes MainWindow
        """
        # deinitialize the frame manager
        self.pnlPlot.Close()
        try:
            f = open(os.path.join(user_config_dir("ODMTools", "UCHIC"), 'ODMTools.config'), 'w')
            f.write(self._mgr.SavePerspective())
        except:
            print "error saving docking data"
        self._mgr.UnInit()

        # IMPORTANT! if wx.TaskBarIcons exist, it will keep mainloop running

        windowsRemaining = len(wx.GetTopLevelWindows())
        if windowsRemaining > 0:
            import wx.lib.agw.aui.framemanager as aui
            # logger.debug("Windows left to close: %d" % windowsRemaining)
            for item in wx.GetTopLevelWindows():
                #logger.debug("Windows %s" % item)
                if not isinstance(item, self.__class__):
                    if isinstance(item, aui.AuiFloatingFrame):
                        item.Destroy()
                    elif isinstance(item, aui.AuiSingleDockingGuide):
                        item.Destroy()
                    elif isinstance(item, aui.AuiDockingHintWindow):
                        item.Destroy()
                    elif isinstance(item, wx.Dialog):
                        item.Destroy()
                    item.Close()
        self.Destroy()

        wx.GetApp().ExitMainLoop()

    def _postStartup(self):
        """
            Called after MainLoop is initialized
                Hides Python Console Tools
        """
        if self.txtPythonConsole.ToolsShown():
            self.txtPythonConsole.ToggleTools()
