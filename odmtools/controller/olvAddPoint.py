"""
    Object List View Control used in Add Point Form
"""
import wx

from datetime import datetime
from odmtools.common import x_mark_16, star_16, star_32, x_mark_32, check_mark_3_16, check_mark_3_32
from odmtools.controller.logicCellEdit import CellEdit

__author__ = 'Jacob'

from odmtools.lib.ObjectListView import FastObjectListView, ColumnDefn

# # Specific Settings
NO_DATA_VALUE = -9999


class Points(object):
    """

    """

    def __init__(self, dataValue="-9999", valueAccuracy="NULL", time="00:00:00",
                 date="", utcOffSet="NULL", dateTimeUTC="NULL", offSetValue="NULL",
                 offSetType="NULL", censorCode="NULL", qualifierCode="NULL",
                 qualifierDesc="NULL",
                 labSampleCode="NULL"):
        self.dataValue = dataValue
        self.valueAccuracy = valueAccuracy
        self.time = str(time)
        self.date = datetime.now().date()
        self.utcOffSet = utcOffSet
        self.dateTimeUTC = dateTimeUTC
        self.offSetValue = offSetValue
        self.offSetType = offSetType
        self.censorCode = censorCode
        self.qualifierCode = qualifierCode
        self.qualifierDesc = qualifierDesc
        self.labSampleCode = labSampleCode

        ## determines whether a row is in correct format or now
        self.isCorrect = True



class OLVAddPoint(FastObjectListView):
    """

    """
    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        self.serviceManager = kwargs.pop("serviceManager")
        self.recordService = kwargs.pop("recordService")

        FastObjectListView.__init__(self, *args, **kwargs)

        cellEdit = CellEdit(self.serviceManager, self.recordService)

        # # Custom Image Getters
        self.imgGetterDataValue = cellEdit.imgGetterDataValue
        self.imgGetterCensorCode = cellEdit.imgGetterCensorCode
        self.imgGetterUTCOffset = cellEdit.imgGetterUTCOFFset
        self.imgGetterValueAcc = cellEdit.imgGetterValueAcc

        ## Custom Value Getters
        self.valueGetterValueAcc = cellEdit.valueGetterValueAccuracy

        ## Custom Value Setters
        ## Sets the value, can modify rules for setting value
        self.valueSetterDataValue = cellEdit.valueSetterDataValue
        self.valueSetterUTCOffset = cellEdit.valueSetterUTCOffset

        ## Custom String Converters
        ## Changes how the string will appear in the cell after editing
        self.localtime2Str = cellEdit.strConverterLocalTime
        self.str2DataValue = cellEdit.strConverterDataValue

        ## Custom CellEditors
        self.timeEditor = cellEdit.localTimeEditor
        self.censorEditor = cellEdit.censorCodeEditor
        self.labSampleEditor = cellEdit.labSampleCodeEditor

        self.SetEmptyListMsg("Add points either by csv or by adding a new row")
        self.AddNamedImages("error", x_mark_16.GetBitmap(), x_mark_32.GetBitmap())
        self.AddNamedImages("star", star_16.GetBitmap(), star_32.GetBitmap())
        self.AddNamedImages("check", check_mark_3_16.GetBitmap(), check_mark_3_32.GetBitmap())


        self.buildOlv()

        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 239, 255)
        self.cellEditMode = self.CELLEDIT_DOUBLECLICK

    def buildOlv(self):
        columns = [
            ColumnDefn("", "left", -1, valueSetter=self.emptyCol),
            ColumnDefn("DataValue", "left", -1, minimumWidth=100,
                       valueGetter='dataValue',
                       valueSetter=self.valueSetterDataValue,
                       imageGetter=self.imgGetterDataValue,
                       stringConverter=self.str2DataValue,
                       headerImage="star"),
            ColumnDefn("Date", "left", -1,  minimumWidth=85,
                       valueGetter="date",
                       headerImage="star"),
            ColumnDefn("Time", "left", -1, valueGetter="time", minimumWidth=75,
                       cellEditorCreator=self.timeEditor,
                       stringConverter=self.localtime2Str,
                       headerImage="star"),
            ColumnDefn("UTCOffset", "left", -1, minimumWidth=100,
                       valueGetter="utcOffSet",
                       valueSetter=self.valueSetterUTCOffset,
                       imageGetter=self.imgGetterUTCOffset,
                       headerImage="star"),
            ColumnDefn("CensorCode", "left", -1, valueGetter="censorCode", minimumWidth=110,
                       cellEditorCreator=self.censorEditor,
                       imageGetter=self.imgGetterCensorCode,
                       headerImage="star"),
            ColumnDefn("ValueAccuracy", "left", -1, valueGetter="valueAccuracy", minimumWidth=100,
                       imageGetter=self.imgGetterValueAcc,
                       ),
            ColumnDefn("OffsetValue", "left", -1, valueGetter="offSetValue", minimumWidth=100),
            ColumnDefn("OffsetType", "left", -1, valueGetter="offSetType", minimumWidth=100),
            ColumnDefn("QualifierCode", "left", -1, valueGetter="qualifierCode", minimumWidth=100),
            ColumnDefn("QualifierDesc", "left", -1, valueGetter="qualifierDesc", minimumWidth=150),
            ColumnDefn("LabSampleCode", "left", -1, valueGetter="labSampleCode", minimumWidth=100,
                       cellEditorCreator=self.labSampleEditor)
        ]

        self.SetColumns(columns)
        self.SetObjects(None)

    def sampleRow(self):
        return Points()

    def emptyCol(self):
        return " "