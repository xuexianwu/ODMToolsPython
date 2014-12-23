"""Subclass of frmDataFilters, which is generated by wxFormBuilder."""

from datetime import datetime

import wx
from wx.lib.pubsub import pub as Publisher


# # Enable logging
import logging
from odmtools.common.logger import LoggerTool
from odmtools.view import clsDataFilters

tool = LoggerTool()
logger = tool.setupLogger(__name__, __name__ + '.log', 'w', logging.DEBUG)
# #




# Implementing frmDataFilters
class frmDataFilter(clsDataFilters.clsDataFilters):
    def __init__(self, parent, series):
        self.is_applied = False
        self.recordService = series
        clsDataFilters.clsDataFilters.__init__(self, parent)

        self.chkToggleFilterSelection.SetValue(self.recordService.get_toggle())
        self.setDates()


    def onCheckBox(self, event):
        self.recordService.filter_from_previous(self.chkToggleFilterSelection.GetValue())

    def onSetFocus(self, event):
        logger.debug("event id : %s" % repr(event.Id))

        # DateRange
        if event.Id in (self.dpAfter.Id, self.dpBefore.Id, self.tpBefore.Id, self.tpAfter.Id, self.sbAfter.Id, self.sbBefore.Id):
            self.rbDate.SetValue(True)
        # Data Gaps
        elif event.Id in (self.txtGapsVal.Id, self.cbGapTime.Id):
            self.rbDataGaps.SetValue(True)
        #Value Threshold
        elif event.Id in (self.txtThreshValLT.Id, self.txtThreshValGT.Id ):
            self.rbThreshold.SetValue(True)
        #value change threshold
        elif event.Id in (self.txtVChangeLT.Id, self.txtVChangeGT.Id):
            self.rbVChangeThresh.SetValue(True)

        event.Skip()


    def onBtnClearButton(self, event):
        self.setDates()
        self.txtThreshValGT.Clear()
        self.txtThreshValLT.Clear()
        self.txtGapsVal.Clear()
        self.cbGapTime.SetStringSelection("second")
        # self.txtVChangeThresh.Clear()
        self.txtVChangeLT.Clear()
        self.txtVChangeGT.Clear()
        self.recordService.reset_filter()
        self.chkToggleFilterSelection.SetValue(False)

        event.Skip()


    def onBtnOKButton(self, event):


        if not self.is_applied:
            self.onBtnApplyButton(event)
        if self.chkToggleFilterSelection.GetValue():
            self.recordService.filter_from_previous(False)
        event.Skip()
        self.Close()


    def onBtnCancelButton(self, event):
        if self.chkToggleFilterSelection.GetValue():
            self.recordService.filter_from_previous(False)
        event.Skip()
        self.Close()


    def onBtnApplyButton(self, event):
        self.is_applied = True
        if self.rbThreshold.GetValue():
            gt = self.txtThreshValGT.GetValue()
            lt = self.txtThreshValLT.GetValue()

            '''

            if gt and lt:
                self.recordService.filter_value({'gt': float(gt), 'lt': float(lt)}, ['>', '<'])
            elif gt:
                self.recordService.filter_value({'gt': float(gt)}, ['>'])
            elif lt:
                self.recordService.filter_value({'lt': float(lt)}, ['<'])

            '''

            if self.txtThreshValGT.GetValue():
                self.recordService.filter_value(float(gt), '>')
            if self.txtThreshValLT.GetValue():
                self.recordService.filter_value(float(lt), '<')

        elif self.rbDataGaps.GetValue():
            if self.txtGapsVal.GetValue():
                self.recordService.data_gaps(float(self.txtGapsVal.GetValue()), self.cbGapTime.GetValue())

        elif self.rbDate.GetValue():
            dateAfter = self.dpAfter.GetValue()
            timeAfter = self.tpAfter.GetValue(as_wxDateTime=True)
            dateBefore = self.dpBefore.GetValue()
            timeBefore = self.tpBefore.GetValue(as_wxDateTime=True)


            # convert to datetime.datetime from wxdatetime time
            dtDateAfter = _wxdate2pydate(dateAfter, timeAfter)
            dtDateBefore = _wxdate2pydate(dateBefore, timeBefore)
            self.recordService.filter_date(dtDateBefore, dtDateAfter)

        elif self.rbVChangeThresh.GetValue():
            if self.txtVChangeGT.GetValue():
                self.recordService.value_change_threshold(float(self.txtVChangeGT.GetValue()), '>')
            elif self.txtVChangeLT.GetValue():
                self.recordService.value_change_threshold(float(self.txtVChangeLT.GetValue()), '<')

        event.Skip()


    def setDates(self):
        dateAfter = self.recordService.get_series_points()[0][2]
        dateBefore = self.recordService.get_series_points()[-1][2]

        formattedDateAfter = _pydate2wxdate(dateAfter)
        formattedDateBefore = _pydate2wxdate(dateBefore)

        self.dpAfter.SetRange(formattedDateAfter, formattedDateBefore)
        self.dpBefore.SetRange(formattedDateAfter, formattedDateBefore)
        self.dpAfter.SetValue(formattedDateAfter)
        self.tpBefore.SetValue(wx.DateTimeFromHMS(hour=23, minute=59, second=59))
        self.dpBefore.SetValue(formattedDateBefore)


def _pydate2wxdate(date):
    import datetime

    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTimeFromDMY(*dmy)


def _wxdate2pydate(date, time):
    import datetime

    assert isinstance(date, wx.DateTime)
    assert isinstance(time, wx.DateTime)
    if date.IsValid() and time.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        hms = map(int, time.FormatISOTime().split(':'))
        return datetime.datetime(*(ymd + hms))
    else:
        return None

