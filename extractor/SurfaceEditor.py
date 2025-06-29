import os
import sys
import pickle
import logging

from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QTreeWidget,
    QTreeWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QToolBar,
    QVBoxLayout,
    QWidget, 
)
from PySide2.QtGui import (
    QPalette, 
    QColor,
    QBrush,
    QIcon,
    QPixmap,
    QPainter,
)
from PySide2.QtCore import (
    Qt,
    QSize,
)

def RGBToHex(rgbcolor):
    return '#'+"".join(map(lambda x: str(hex(x))[2:], rgbcolor))
    

def HexToRGB(hexcolor):
    return [int(hexcolor[1:3], 16), int(hexcolor[3:5], 16), int(hexcolor[5:7], 16)]

class Canvas(QLabel):
    def __init__(self, data, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.config = config

    def mousePressEvent(self, e):
         print(e)

    def mouseMoveEvent(self, e):
         print(e)

    def mouseReleaseEvent(self, e):
         print(e)

    def print_background(self):
 
        print(self.config.max_x, self.config.max_y, self.config.zoom, (self.config.max_x + 10)*self.config.zoom, (self.config.max_y + 10)*self.config.zoom)
        pixmap = QPixmap(600, 400)
        pixmap.fill((QColor('white')))
        self.setPixmap(pixmap)
        '''
        painter = QPainter(self.canvas.pixmap())
        for x in range(int(self.canvas_h/10)):
            for y in range(int(self.canvas_w/10)):
                color = '#EEEEEE'
                if (x+y)%2 == 0: color = '#CCCCCC'
                painter.setBrush(QBrush(QColor(color)))
                p = painter.pen()
                p.setWidth(0)
                p.setColor(QColor(color))
                painter.setPen(p)
                painter.drawRect(x*10,y*10,10,10)
        '''
        

    def update_canvas(self):

        self.print_background()
        painter = QPainter(self.pixmap())

        #if self.tmp >=4: return
        #self.tmp+=1
        #PaintableObject("Test Paintable Object", [Surface('Surface 1', PointSequence([Point(10, 10), Point(12, 10], , Point(15, 20]))])

        p = painter.pen()
        p.setWidth(1)
        p.setColor(QColor('black'))
        painter.setPen(p)

        def print_point_sequence(pointSequence):
            if not pointSequence.visible: return

            for point in pointSequence.points:
                painter.drawRect((point.y*self.config.zoom)-2, (point.x*self.config.zoom)-2, 4, 4)

            if len(pointSequence.points) > 1:
                if pointSequence.isClosed:
                    (x1, y1) = pointSequence.points[-1].xy()
                    (x2, y2) = pointSequence.points[0].xy()
                    painter.drawLine(x1*self.config.zoom, y1*self.config.zoom, x2*self.config.zoom, y2*self.config.zoom)
                ppoint = pointSequence.points[0]
                for point in pointSequence.points[1:]:
                    (x1, y1) = ppoint.xy()
                    (x2, y2) = point.xy()
                    painter.drawLine(x1*self.config.zoom, y1*self.config.zoom, x2*self.config.zoom, y2*self.config.zoom)
                    ppoint = point

        painter.drawLine(0, 0, 10, 10)
        for paintableObject in self.data:
            if not paintableObject.visible: continue
            logging.debug(len(paintableObject.surfaces))
            for surface in paintableObject.surfaces:
                if not surface.visible: continue
                print_point_sequence(surface.outer)
                for hole in surface.holes:
                    print_point_sequence(hole)

        painter.end()
        self.update()

class Config:
    def __init__(self):
        self.zoom=1
        self.max_x = 0
        self.max_y = 0

class MyWidget(QWidget):

    def __init__(self, color):
        super(MyWidget, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class SurfaceEditorMainWindow(QMainWindow):

    data = []
    canvas_h = 600
    canvas_w = 600
    max_id_surf = 0
    tmp = 0
        
    def __init__(self):
        super(SurfaceEditorMainWindow, self).__init__()
        self.config = Config()
        
        self.setWindowTitle("My App")

        layout1 = QHBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0,0,0,0)

        self.canvas = Canvas(self.data, self.config)

        scroll = QScrollArea()
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.canvas)
        widget.setLayout(vbox)
        widget.resize(600, 400)
        scroll.setWidget(widget)
        self.canvas.update_canvas()
        layout1.addWidget(scroll)
        
        self.create_tree()
        layout2.addWidget(self.tree_widget)

        self.create_table()
        layout2.addWidget(self.table_widget)
        layout1.addLayout(layout2)
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


        # Tool Bars
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

        self.zoomToolbar = QToolBar(self)
        self.zoomToolbar.setIconSize(QSize(16, 16))
        self.zoomToolbar.setObjectName("zoomToolbar")
        self.addToolBar(Qt.TopToolBarArea, self.zoomToolbar)

        self.zoomToolbar.addAction(self.actionZoomIn)
        self.zoomToolbar.addAction(self.actionZoomOut)

        #add_collection_action = QAction("&Open", self)
        #add_collection_action.triggered.connect(self.add_collection)
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        #file_menu.addAction(add_collection_action)

        self.actionZoomIn.triggered.connect(self.zoom_in)
        self.actionZoomOut.triggered.connect(self.zoom_out)


    def zoom_in(self):
        self.config.zoom = self.config.zoom*2
        self.canvas.update_canvas()

    def zoom_out(self):
        self.config.zoom = self.config.zoom/2
        self.canvas.update_canvas()

    def addObjectData(self, p_object):
        logging.debug(p_object)
        self.data.append(p_object)
        self.update_minmax(p_object)
        self.canvas.update_canvas()
        self.update_tree()

    def update_minmax(self, p_object):
        def update_minmax_sequence(pointSequence):
            for point in pointSequence.points:
                if self.config.max_x < point.x: self.config.max_x = point.x
                if self.config.max_y < point.x: self.config.max_y = point.y

        for surface in p_object.surfaces:
            update_minmax_sequence(surface.outer)
            for hole in surface.holes:
                update_minmax_sequence(hole)

    def create_table(self):
        self.table_widget = QTableWidget(0, 2, self);
        self.table_widget.verticalHeader().setVisible(False);
        self.table_widget.setHorizontalHeaderLabels(["Property", "Value"]);


    def create_tree(self):
        self.tree_widget = QTreeWidget()
        self.tree_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_widget.setHeaderLabels(["Surfaces"])
        self.tree_widget.currentItemChanged.connect(self.tree_widget_current_item_changed)
        self.tree_widget.itemClicked.connect(self.tree_widget_item_clicked)
        self.tree_widget.itemPressed.connect(self.tree_widget_item_pressed)
        self.tree_widget.itemActivated.connect(self.tree_widget_item_activated)
        
    def tree_widget_current_item_changed(self, current, previous):
        print("-->tree_widget_current_item_changed()")
        obj = current.data(0, Qt.UserRole)
        #if type(obj) == Vector:
        #    self.table_widget.setRowCount(0)
        #    self.table_widget_add_row("Name", obj.name)
        #if type(obj) == Surface:
        #    self.table_widget.setRowCount(0)
        #    self.table_widget_add_row("Name", obj.name)
        #    self.table_widget_add_row("Color", RGBToHex(obj.color))
        #if type(obj) == Collection:
        #    self.table_widget.setRowCount(0)
        #    self.table_widget_add_row("Name", obj.name)

    def table_widget_add_row(self, property_name, property_value):
        rowPosition = self.table_widget.rowCount()
        self.table_widget.insertRow(rowPosition)
        cell = QTableWidgetItem(property_name)
        cell.setFlags(cell.flags() & ~Qt.ItemIsEditable)
        self.table_widget.setItem(rowPosition , 0, cell)
        cell = QTableWidgetItem(property_value)
        self.table_widget.setItem(rowPosition, 1, cell)

    def tree_widget_item_activated(self, item, column):
        print("-->tree_widget_item_activated()")

    def tree_widget_item_clicked(self, item, column):
        print("-->tree_widget_item_clicked()")
        if item.checkState(column) == Qt.Checked:
            pobj = item.data(0, Qt.UserRole)
            pobj.visible = True
            #print(vect)
            #if type(vect) == Vector: vect.visible = True
            #print(vect)
        elif item.checkState(column) == Qt.Unchecked:
            pobj = item.data(0, Qt.UserRole)
            pobj.visible = False
            #print(vect)
            #if type(vect) == Vector: vect.visible = False
            #print(vect)
        self.canvas.update_canvas()

    def tree_widget_item_pressed(self, item, column):
        print("-->tree_widget_item_pressed()")
        #print(dir(item))
        #print(column)




    def update_tree(self):
        self.tree_widget.clear()

        def add_sequence_to_tree(tree_item, seq, name):
            vect_tree_item = QTreeWidgetItem(name)
            vect_tree_item.setCheckState(0, Qt.Checked)
            vect_tree_item.setData(0, Qt.UserRole, seq)
            tree_item.addChild(vect_tree_item)

        for paintableObject in self.data:
            col_tree_item = QTreeWidgetItem([paintableObject.name])
            col_tree_item.setFlags(col_tree_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            col_tree_item.setCheckState(0, Qt.Checked)
            self.tree_widget.addTopLevelItem(col_tree_item)
            for surface in paintableObject.surfaces:
                surf_tree_item = QTreeWidgetItem([surface.name])
                surf_tree_item.setCheckState(0, Qt.Checked)
                surf_tree_item.setData(0, Qt.UserRole, surface)
                col_tree_item.addChild(surf_tree_item)
                add_sequence_to_tree(surf_tree_item, surface.outer, ["outer"])
                
                for i in range(len(surface.holes)):
                    add_sequence_to_tree(surf_tree_item, surface.holes[i], ["hole "+str(i+1)])
            #        vect_tree_item = QTreeWidgetItem(vector.name)
            #        vect_tree_item.setCheckState(0, Qt.Checked)
            #        vect_tree_item.setData(0, Qt.UserRole, vector)
            #        #vect_tree_item.clicked.connect(self.vect_tree_item_clicked)
            #        surf_tree_item.addChild(vect_tree_item)
        self.tree_widget.expandAll()

    def vect_tree_item_clicked(self):
        print(self)

    def keyPressEvent(self, e):
        print(e)

'''
app = QApplication(sys.argv)

window = MainWindow()
window.resize(800, 600)
window.show()

app.exec_()
'''
