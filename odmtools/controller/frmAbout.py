__author__ = 'Stephanie'
import wx
from wx import AboutBox, AboutDialogInfo, ClientDC
from wx.lib.wordwrap import wordwrap


class frmAbout(wx.Dialog):
    def __init__(self, parent):
        self.parent = parent
        info = AboutDialogInfo()
        info.Name = "ODMTools"
        info.Version = "1.0.4"
        info.Copyright = "Copyright (c) 2013, Utah State University. All rights reserved."
        info.Description = wordwrap(
            "ODMTools is a python application for managing observational data using the Observations Data Model. "
            "ODMTools allows you to query, visualize, and edit data stored in an Observations Data Model (ODM) database."
            " ODMTools was originally developed as part of the CUAHSI Hydrologic Information System.",
            350, ClientDC(parent))
        info.WebSite = ("http://uchic.github.io/ODMToolsPython/", "ODMTools home page")
        info.Developers = ["Jeffery S. Horsburgh",
                           "Amber Spackman Jones",
                           "Stephanie L. Reeder",
                           "Jacob Meline",
                           "James Patton"]

        info.License = wordwrap(licenseText, 500, ClientDC(parent))

        # Then we call wx.AboutBox giving it that info object
        AboutBox(info)


        #self.ShowModal()



licenseText = "This material is copyright (c) 2013 Utah State University." \
              "\nIt is open and licensed under the New Berkeley Software Distribution (BSD) License. Full text of the license follows." \
              "\nCopyright (c) 2013, Utah State University. All rights reserved." \
              "\nRedistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:" \
              "\n    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer." \
              "\n    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution." \
              "\n    Neither the name of Utah State University nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission." \
              "\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. "

