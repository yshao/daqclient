# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotterwidget.ui'
#
# Created: Sun Oct 19 16:38:46 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PlotterWidget(object):
    def setupUi(self, PlotterWidget):
        PlotterWidget.setObjectName(_fromUtf8("PlotterWidget"))
        PlotterWidget.resize(450, 369)
        self.gridLayout = QtGui.QGridLayout(PlotterWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.inTitle = QtGui.QLineEdit(PlotterWidget)
        self.inTitle.setObjectName(_fromUtf8("inTitle"))
        self.gridLayout.addWidget(self.inTitle, 1, 2, 1, 1)
        self.inDataSource = QtGui.QPushButton(PlotterWidget)
        self.inDataSource.setObjectName(_fromUtf8("inDataSource"))
        self.gridLayout.addWidget(self.inDataSource, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(PlotterWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.ycol_QLabel = QtGui.QLabel(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ycol_QLabel.sizePolicy().hasHeightForWidth())
        self.ycol_QLabel.setSizePolicy(sizePolicy)
        self.ycol_QLabel.setMinimumSize(QtCore.QSize(92, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.ycol_QLabel.setFont(font)
        self.ycol_QLabel.setObjectName(_fromUtf8("ycol_QLabel"))
        self.gridLayout.addWidget(self.ycol_QLabel, 3, 1, 1, 1)
        self.xcol_QLabel = QtGui.QLabel(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xcol_QLabel.sizePolicy().hasHeightForWidth())
        self.xcol_QLabel.setSizePolicy(sizePolicy)
        self.xcol_QLabel.setMinimumSize(QtCore.QSize(92, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.xcol_QLabel.setFont(font)
        self.xcol_QLabel.setObjectName(_fromUtf8("xcol_QLabel"))
        self.gridLayout.addWidget(self.xcol_QLabel, 2, 1, 1, 1)
        self.inXAxis = QtGui.QComboBox(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inXAxis.sizePolicy().hasHeightForWidth())
        self.inXAxis.setSizePolicy(sizePolicy)
        self.inXAxis.setMinimumSize(QtCore.QSize(87, 0))
        self.inXAxis.setMaximumSize(QtCore.QSize(20000, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.inXAxis.setFont(font)
        self.inXAxis.setObjectName(_fromUtf8("inXAxis"))
        self.gridLayout.addWidget(self.inXAxis, 2, 3, 1, 2)
        self.label_8 = QtGui.QLabel(PlotterWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 1, 1, 1)
        self.inYAxis = QtGui.QComboBox(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inYAxis.sizePolicy().hasHeightForWidth())
        self.inYAxis.setSizePolicy(sizePolicy)
        self.inYAxis.setMinimumSize(QtCore.QSize(87, 0))
        self.inYAxis.setMaximumSize(QtCore.QSize(2000, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.inYAxis.setFont(font)
        self.inYAxis.setObjectName(_fromUtf8("inYAxis"))
        self.gridLayout.addWidget(self.inYAxis, 3, 3, 1, 2)
        self.inPlotType = QtGui.QComboBox(PlotterWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.inPlotType.setFont(font)
        self.inPlotType.setObjectName(_fromUtf8("inPlotType"))
        self.inPlotType.addItem(_fromUtf8(""))
        self.inPlotType.addItem(_fromUtf8(""))
        self.inPlotType.addItem(_fromUtf8(""))
        self.inPlotType.addItem(_fromUtf8(""))
        self.inPlotType.addItem(_fromUtf8(""))
        self.inPlotType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.inPlotType, 4, 3, 1, 1)
        self.maxtstep_QLabel = QtGui.QLabel(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxtstep_QLabel.sizePolicy().hasHeightForWidth())
        self.maxtstep_QLabel.setSizePolicy(sizePolicy)
        self.maxtstep_QLabel.setMinimumSize(QtCore.QSize(130, 30))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.maxtstep_QLabel.setFont(font)
        self.maxtstep_QLabel.setWordWrap(True)
        self.maxtstep_QLabel.setObjectName(_fromUtf8("maxtstep_QLabel"))
        self.gridLayout.addWidget(self.maxtstep_QLabel, 5, 1, 1, 1)
        self.inStep = QtGui.QDoubleSpinBox(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inStep.sizePolicy().hasHeightForWidth())
        self.inStep.setSizePolicy(sizePolicy)
        self.inStep.setMaximum(1000.0)
        self.inStep.setSingleStep(1.0)
        self.inStep.setProperty("value", 0.0)
        self.inStep.setObjectName(_fromUtf8("inStep"))
        self.gridLayout.addWidget(self.inStep, 5, 3, 1, 1)
        self.inWindowSize = QtGui.QLineEdit(PlotterWidget)
        self.inWindowSize.setObjectName(_fromUtf8("inWindowSize"))
        self.gridLayout.addWidget(self.inWindowSize, 6, 3, 1, 1)
        self.label = QtGui.QLabel(PlotterWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 6, 1, 1, 1)
        self.inXLabel = QtGui.QLineEdit(PlotterWidget)
        self.inXLabel.setObjectName(_fromUtf8("inXLabel"))
        self.gridLayout.addWidget(self.inXLabel, 2, 2, 1, 1)
        self.inYLabel = QtGui.QLineEdit(PlotterWidget)
        self.inYLabel.setObjectName(_fromUtf8("inYLabel"))
        self.gridLayout.addWidget(self.inYLabel, 3, 2, 1, 1)
        self.inDataSourceLine = QtGui.QLineEdit(PlotterWidget)
        self.inDataSourceLine.setObjectName(_fromUtf8("inDataSourceLine"))
        self.gridLayout.addWidget(self.inDataSourceLine, 0, 2, 1, 3)
        self.inOptRefresh = QtGui.QCheckBox(PlotterWidget)
        self.inOptRefresh.setObjectName(_fromUtf8("inOptRefresh"))
        self.gridLayout.addWidget(self.inOptRefresh, 6, 4, 1, 1)
        self.inPlot = QtGui.QPushButton(PlotterWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inPlot.sizePolicy().hasHeightForWidth())
        self.inPlot.setSizePolicy(sizePolicy)
        self.inPlot.setMinimumSize(QtCore.QSize(97, 20))
        self.inPlot.setMaximumSize(QtCore.QSize(200, 20))
        self.inPlot.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.inPlot.setFont(font)
        self.inPlot.setObjectName(_fromUtf8("inPlot"))
        self.gridLayout.addWidget(self.inPlot, 7, 1, 1, 1)

        self.retranslateUi(PlotterWidget)
        QtCore.QMetaObject.connectSlotsByName(PlotterWidget)

    def retranslateUi(self, PlotterWidget):
        PlotterWidget.setWindowTitle(_translate("PlotterWidget", "PlotterWidget", None))
        self.inDataSource.setText(_translate("PlotterWidget", "Data Source", None))
        self.label_2.setText(_translate("PlotterWidget", "title:", None))
        self.ycol_QLabel.setText(_translate("PlotterWidget", "y-axis:", None))
        self.xcol_QLabel.setText(_translate("PlotterWidget", "x-axis:", None))
        self.label_8.setText(_translate("PlotterWidget", "Plot type", None))
        self.inPlotType.setItemText(0, _translate("PlotterWidget", "line", None))
        self.inPlotType.setItemText(1, _translate("PlotterWidget", "line and marker", None))
        self.inPlotType.setItemText(2, _translate("PlotterWidget", "line and cross", None))
        self.inPlotType.setItemText(3, _translate("PlotterWidget", "marker", None))
        self.inPlotType.setItemText(4, _translate("PlotterWidget", "step-pre", None))
        self.inPlotType.setItemText(5, _translate("PlotterWidget", "step-post", None))
        self.maxtstep_QLabel.setText(_translate("PlotterWidget", "Discontinuous plot if time step > days", None))
        self.label.setText(_translate("PlotterWidget", "Windowing size", None))
        self.inOptRefresh.setText(_translate("PlotterWidget", "Refresh", None))
        self.inPlot.setText(_translate("PlotterWidget", "Plot chart", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PlotterWidget = QtGui.QWidget()
    ui = Ui_PlotterWidget()
    ui.setupUi(PlotterWidget)
    PlotterWidget.show()
    sys.exit(app.exec_())

