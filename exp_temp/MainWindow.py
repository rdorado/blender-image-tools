import sys
from PySide6.QtWidgets import (
  QApplication,
  QLabel,
  QStatusBar,
  QToolBar,
  QGridLayout,
  QHBoxLayout,
  QMainWindow,
  QMenu,
  QMenuBar,
  QPushButton,
  QSizePolicy,
  QTabWidget,
  QVBoxLayout,
  QWidget,
)
from PySide6.QtGui import (
  QPalette,
  QColor,
  QIcon,
  QPixmap,
  QAction,
)
from PySide6.QtCore import (
  Qt,
  QSize,
  QRect,
  QCoreApplication,
)


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setWindowTitle("My App")
        self.resize(706, 556)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        self.leftBarWidget = QWidget()
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.leftBarWidget.setLayout(self.verticalLayout_2)

        toolbar = QWidget()
        #self.leftBarWidget.setStyleSheet("border: 1px solid red; padding:0; ");
        toolbar.setFixedWidth(70)
        self.verticalLayout_2.addWidget(toolbar)
        layout.addWidget(self.leftBarWidget)
        

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.gridLayout = QGridLayout(toolbar)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")

        # Side tools penButton
        self.penButton = QPushButton(toolbar)
        self.penButton.setMinimumSize(QSize(30, 30))
        self.penButton.setMaximumSize(QSize(30, 30))
        self.penButton.setText("")
        icon8 = QIcon()
        icon8.addPixmap(QPixmap("icons/pencil.png"), QIcon.Normal, QIcon.Off)
        self.penButton.setIcon(icon8)
        self.penButton.setCheckable(True)
        self.penButton.setObjectName("penButton")
        self.gridLayout.addWidget(self.penButton, 0, 0, Qt.AlignTop)

        # Side tools selectrectButton
        self.selectrectButton = QPushButton(toolbar)
        self.selectrectButton.setMinimumSize(QSize(30, 30))
        self.selectrectButton.setMaximumSize(QSize(30, 30))
        self.selectrectButton.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap("icons/selection.png"), QIcon.Normal, QIcon.Off)
        self.selectrectButton.setIcon(icon2)
        self.selectrectButton.setCheckable(True)
        self.selectrectButton.setObjectName("selectrectButton")
        self.gridLayout.addWidget(self.selectrectButton, 0, 1, Qt.AlignTop)

        # Side tools lineButton
        self.lineButton = QPushButton(toolbar)
        self.lineButton.setMinimumSize(QSize(30, 30))
        self.lineButton.setMaximumSize(QSize(30, 30))
        self.lineButton.setText("")
        icon14 = QIcon()
        icon14.addPixmap(QPixmap("icons/layer-shape-line.png"), QIcon.Normal, QIcon.Off)
        self.lineButton.setIcon(icon14)
        self.lineButton.setCheckable(True)
        self.lineButton.setObjectName("lineButton")
        self.gridLayout.addWidget(self.lineButton, 1, 0, Qt.AlignTop)

        # Side tools Rect Select
        self.rectButton = QPushButton(toolbar)
        self.rectButton.setMinimumSize(QSize(30, 30))
        self.rectButton.setMaximumSize(QSize(30, 30))
        self.rectButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap("icons/layer-shape.png"), QIcon.Normal, QIcon.Off)
        self.rectButton.setIcon(icon)
        self.rectButton.setCheckable(True)
        self.rectButton.setObjectName("rectButton")
        self.gridLayout.addWidget(self.rectButton, 1, 1, Qt.AlignTop)


        '''
        # Side tools selectpolyButton
        self.selectpolyButton = QPushButton(toolbar)
        self.selectpolyButton.setMinimumSize(QSize(30, 30))
        self.selectpolyButton.setMaximumSize(QSize(30, 30))
        self.selectpolyButton.setText("")
        icon6 = QIcon()
        icon6.addPixmap(QPixmap("icons/selection-poly.png"), QIcon.Normal, QIcon.Off)
        self.selectpolyButton.setIcon(icon6)
        self.selectpolyButton.setCheckable(True)
        self.selectpolyButton.setObjectName("selectpolyButton")
        self.gridLayout.addWidget(self.selectpolyButton, 0, 1, Qt.AlignTop)




        # Side tools eraserButton
        self.eraserButton = QPushButton(toolbar)
        self.eraserButton.setMinimumSize(QSize(30, 30))
        self.eraserButton.setMaximumSize(QSize(30, 30))
        self.eraserButton.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap("icons/eraser.png"), QIcon.Normal, QIcon.Off)
        self.eraserButton.setIcon(icon3)
        self.eraserButton.setCheckable(True)
        self.eraserButton.setObjectName("eraserButton")
        self.gridLayout.addWidget(self.eraserButton, 1, 1, Qt.AlignTop)
        
        # Side tools fillButton
        self.fillButton = QPushButton(toolbar)
        self.fillButton.setMinimumSize(QSize(30, 30))
        self.fillButton.setMaximumSize(QSize(30, 30))
        self.fillButton.setText("")
        icon9 = QIcon()
        icon9.addPixmap(QPixmap("icons/paint-can.png"), QIcon.Normal, QIcon.Off)
        self.fillButton.setIcon(icon9)
        self.fillButton.setCheckable(True)
        self.fillButton.setObjectName("fillButton")
        self.gridLayout.addWidget(self.fillButton, 2, 0, Qt.AlignTop)

        # Side tools dropperButton
        self.dropperButton = QPushButton(toolbar)
        self.dropperButton.setMinimumSize(QSize(30, 30))
        self.dropperButton.setMaximumSize(QSize(30, 30))
        self.dropperButton.setText("")
        icon5 = QIcon()
        icon5.addPixmap(QPixmap("icons/pipette.png"), QIcon.Normal, QIcon.Off)
        self.dropperButton.setIcon(icon5)
        self.dropperButton.setCheckable(True)
        self.dropperButton.setObjectName("dropperButton")
        self.gridLayout.addWidget(self.dropperButton, 2, 1, Qt.AlignTop)

        # Side tools brushButton
        self.brushButton = QPushButton(toolbar)
        self.brushButton.setMinimumSize(QSize(30, 30))
        self.brushButton.setMaximumSize(QSize(30, 30))
        self.brushButton.setText("")
        icon7 = QIcon()
        icon7.addPixmap(QPixmap("icons/paint-brush.png"), QIcon.Normal, QIcon.Off)
        self.brushButton.setIcon(icon7)
        self.brushButton.setCheckable(True)
        self.brushButton.setObjectName("brushButton")
        self.gridLayout.addWidget(self.brushButton, 3, 0, Qt.AlignTop)

        # Side tools sprayButton
        self.sprayButton = QPushButton(toolbar)
        self.sprayButton.setMinimumSize(QSize(30, 30))
        self.sprayButton.setMaximumSize(QSize(30, 30))
        self.sprayButton.setText("")
        icon15 = QIcon()
        icon15.addPixmap(QPixmap("icons/spray.png"), QIcon.Normal, QIcon.Off)
        self.sprayButton.setIcon(icon15)
        self.sprayButton.setCheckable(True)
        self.sprayButton.setFlat(False)
        self.sprayButton.setObjectName("sprayButton")
        self.gridLayout.addWidget(self.sprayButton, 3, 1, Qt.AlignTop)

        # Side tools textButton
        self.textButton = QPushButton(toolbar)
        self.textButton.setMinimumSize(QSize(30, 30))
        self.textButton.setMaximumSize(QSize(30, 30))
        self.textButton.setText("")
        icon10 = QIcon()
        icon10.addPixmap(QPixmap("icons/edit.png"), QIcon.Normal, QIcon.Off)
        self.textButton.setIcon(icon10)
        self.textButton.setCheckable(True)
        self.textButton.setObjectName("textButton")
        self.gridLayout.addWidget(self.textButton, 4, 1, Qt.AlignTop)



        # Side tools Polyline Select
        self.polylineButton = QPushButton(toolbar)
        self.polylineButton.setMinimumSize(QSize(30, 30))
        self.polylineButton.setMaximumSize(QSize(30, 30))
        self.polylineButton.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap("icons/layer-shape-polyline.png"), QIcon.Normal, QIcon.Off)
        self.polylineButton.setIcon(icon1)
        self.polylineButton.setCheckable(True)
        self.polylineButton.setObjectName("polylineButton")
        self.gridLayout.addWidget(self.polylineButton, 4, 1, Qt.AlignTop)

        # Side tools polygonButton
        self.polygonButton = QPushButton(toolbar)
        self.polygonButton.setMinimumSize(QSize(30, 30))
        self.polygonButton.setMaximumSize(QSize(30, 30))
        self.polygonButton.setText("")
        icon11 = QIcon()
        icon11.addPixmap(QPixmap("icons/layer-shape-polygon.png"), QIcon.Normal, QIcon.Off)
        self.polygonButton.setIcon(icon11)
        self.polygonButton.setCheckable(True)
        self.polygonButton.setObjectName("polygonButton")
        self.gridLayout.addWidget(self.polygonButton, 5, 1, Qt.AlignTop)

        # Side tools ellipseButton
        self.ellipseButton = QPushButton(toolbar)
        self.ellipseButton.setMinimumSize(QSize(30, 30))
        self.ellipseButton.setMaximumSize(QSize(30, 30))
        self.ellipseButton.setText("")
        icon13 = QIcon()
        icon13.addPixmap(QPixmap("icons/layer-shape-ellipse.png"), QIcon.Normal, QIcon.Off)
        self.ellipseButton.setIcon(icon13)
        self.ellipseButton.setCheckable(True)
        self.ellipseButton.setObjectName("ellipseButton")
        self.gridLayout.addWidget(self.ellipseButton, 6, 0, Qt.AlignTop)

        # Side tools roundrectButton
        self.roundrectButton = QPushButton(toolbar)
        self.roundrectButton.setMinimumSize(QSize(30, 30))
        self.roundrectButton.setMaximumSize(QSize(30, 30))
        self.roundrectButton.setText("")
        icon12 = QIcon()
        icon12.addPixmap(QPixmap("icons/layer-shape-round.png"), QIcon.Normal, QIcon.Off)
        self.roundrectButton.setIcon(icon12)
        self.roundrectButton.setCheckable(True)
        self.roundrectButton.setObjectName("roundrectButton")
        self.gridLayout.addWidget(self.roundrectButton, 6, 1, Qt.AlignTop)
        '''

        # Documents
        self.documentTabs = QTabWidget()
        self.documentTabs.setTabsClosable(True);
        layout.addWidget(self.documentTabs)


        # Actions
        self.actionCopy = QAction(self)
        self.actionCopy.setObjectName("actionCopy")
        
        self.actionClearImage = QAction(self)
        self.actionClearImage.setObjectName("actionClearImage")
        
        self.actionOpenImage = QAction(self)
        icon16 = QIcon()
        icon16.addPixmap(QPixmap("icons/blue-folder-open-image.png"), QIcon.Normal, QIcon.Off)
        self.actionOpenImage.setIcon(icon16)
        self.actionOpenImage.setObjectName("actionOpenImage")
        
        self.actionSaveImage = QAction(self)
        icon17 = QIcon()
        icon17.addPixmap(QPixmap("icons/disk.png"), QIcon.Normal, QIcon.Off)
        self.actionSaveImage.setIcon(icon17)
        self.actionSaveImage.setObjectName("actionSaveImage")
        
        self.actionInvertColors = QAction(self)
        self.actionInvertColors.setObjectName("actionInvertColors")
        
        self.actionFlipHorizontal = QAction(self)
        self.actionFlipHorizontal.setObjectName("actionFlipHorizontal")
        
        self.actionFlipVertical = QAction(self)
        self.actionFlipVertical.setObjectName("actionFlipVertical")
        
        self.actionNewImage = QAction(self)
        icon18 = QIcon()
        icon18.addPixmap(QPixmap("icons/document-image.png"), QIcon.Normal, QIcon.Off)
        self.actionNewImage.setIcon(icon18)
        self.actionNewImage.setObjectName("actionNewImage")

        self.actionZoomIn = QAction(self)
        icon18 = QIcon()
        icon18.addPixmap(QPixmap("icons/magnifier-zoom-increase.png"), QIcon.Normal, QIcon.Off)
        self.actionZoomIn.setIcon(icon18)
        self.actionZoomIn.setObjectName("actionZoomIn")

        self.actionZoomOut = QAction(self)
        icon18 = QIcon()
        icon18.addPixmap(QPixmap("icons/magnifier-zoom-decrease.png"), QIcon.Normal, QIcon.Off)
        self.actionZoomOut.setIcon(icon18)
        self.actionZoomOut.setObjectName("actionZoomIn")

        self.actionBold = QAction(self)
        self.actionBold.setCheckable(True)
        icon19 = QIcon()
        icon19.addPixmap(QPixmap("icons/edit-bold.png"), QIcon.Normal, QIcon.Off)
        self.actionBold.setIcon(icon19)
        self.actionBold.setObjectName("actionBold")
        
        self.actionItalic = QAction(self)
        self.actionItalic.setCheckable(True)
        icon20 = QIcon()
        icon20.addPixmap(QPixmap("icons/edit-italic.png"), QIcon.Normal, QIcon.Off)
        self.actionItalic.setIcon(icon20)
        self.actionItalic.setObjectName("actionItalic")
        
        self.actionUnderline = QAction(self)
        self.actionUnderline.setCheckable(True)
        icon21 = QIcon()
        icon21.addPixmap(QPixmap("icons/edit-underline.png"), QIcon.Normal, QIcon.Off)
        self.actionUnderline.setIcon(icon21)
        self.actionUnderline.setObjectName("actionUnderline")
        
        self.actionFillShapes = QAction(self)
        self.actionFillShapes.setCheckable(True)
        icon22 = QIcon()
        icon22.addPixmap(QPixmap("icons/paint-can-color.png"), QIcon.Normal, QIcon.Off)
        self.actionFillShapes.setIcon(icon22)
        self.actionFillShapes.setObjectName("actionFillShapes")


        # Status Bar
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)


        # Color selector
        self.widget_3 = QWidget()
        self.widget_3.setMinimumSize(QSize(78, 0))
        self.widget_3.setMaximumSize(QSize(78, 16777215))
        self.widget_3.setObjectName("widget_3")
        
        self.secondaryButton = QPushButton(self.widget_3)
        self.secondaryButton.setGeometry(QRect(30, 10, 40, 40))
        self.secondaryButton.setMinimumSize(QSize(40, 40))
        self.secondaryButton.setMaximumSize(QSize(40, 40))
        self.secondaryButton.setText("")
        self.secondaryButton.setObjectName("secondaryButton")
        
        self.primaryButton = QPushButton(self.widget_3)
        self.primaryButton.setGeometry(QRect(10, 0, 40, 40))
        self.primaryButton.setMinimumSize(QSize(40, 40))
        self.primaryButton.setMaximumSize(QSize(40, 40))
        self.primaryButton.setText("")
        self.primaryButton.setObjectName("primaryButton")
        
        self.verticalLayout_2.addWidget(self.widget_3)
        
        
        # Menu Bar
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 706, 26))
        self.menuBar.setObjectName("menuBar")
        
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setTitle("File")
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuImage = QMenu(self.menuBar)
        self.menuImage.setObjectName("menuImage")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menuBar)
        
        self.menuFile.addAction(self.actionNewImage)
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addAction(self.actionSaveImage)

        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionClearImage)
        
        self.menuImage.addAction(self.actionInvertColors)
        self.menuImage.addSeparator()
        self.menuImage.addAction(self.actionFlipHorizontal)
        self.menuImage.addAction(self.actionFlipVertical)
        
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuImage.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())



        
        # Tool Bars
        self.fileToolbar = QToolBar(self)
        self.fileToolbar.setIconSize(QSize(16, 16))
        self.fileToolbar.setObjectName("fileToolbar")
        self.addToolBar(Qt.TopToolBarArea, self.fileToolbar)

        self.zoomToolbar = QToolBar(self)
        self.zoomToolbar.setIconSize(QSize(16, 16))
        self.zoomToolbar.setObjectName("zoomToolbar")
        self.addToolBar(Qt.TopToolBarArea, self.zoomToolbar)

        self.drawingToolbar = QToolBar(self)
        self.drawingToolbar.setIconSize(QSize(16, 16))
        self.drawingToolbar.setObjectName("drawingToolbar")
        self.addToolBar(Qt.TopToolBarArea, self.drawingToolbar)

        '''
        self.fontToolbar = QToolBar(self)
        self.fontToolbar.setIconSize(QSize(16, 16))
        self.fontToolbar.setObjectName("fontToolbar")
        self.addToolBar(Qt.TopToolBarArea, self.fontToolbar)
        '''

        self.fileToolbar.addAction(self.actionNewImage)
        self.fileToolbar.addAction(self.actionOpenImage)
        self.fileToolbar.addAction(self.actionSaveImage)

        self.zoomToolbar.addAction(self.actionZoomIn)
        self.zoomToolbar.addAction(self.actionZoomOut)

        self.retranslateUi(self)
        
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Extractor"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuImage.setTitle(_translate("MainWindow", "Image"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.fileToolbar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.drawingToolbar.setWindowTitle(_translate("MainWindow", "toolBar"))
        #self.fontToolbar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionClearImage.setText(_translate("MainWindow", "Clear Image"))
        self.actionOpenImage.setText(_translate("MainWindow", "Open Image..."))
        self.actionSaveImage.setText(_translate("MainWindow", "Save Image As..."))
        self.actionInvertColors.setText(_translate("MainWindow", "Invert Colors"))
        self.actionFlipHorizontal.setText(_translate("MainWindow", "Flip Horizontal"))
        self.actionFlipVertical.setText(_translate("MainWindow", "Flip Vertical"))
        self.actionNewImage.setText(_translate("MainWindow", "New Image"))
        self.actionBold.setText(_translate("MainWindow", "Bold"))
        self.actionBold.setShortcut(_translate("MainWindow", "Ctrl+B"))
        self.actionItalic.setText(_translate("MainWindow", "Italic"))
        self.actionItalic.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionUnderline.setText(_translate("MainWindow", "Underline"))
        self.actionFillShapes.setText(_translate("MainWindow", "Fill Shapes?"))
        

#app = QApplication(sys.argv)

#window = Ui_MainWindow()
#window.show()

#app.exec_()