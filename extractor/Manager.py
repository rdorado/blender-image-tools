import os
import sys
import pickle
import logging

from PySide2.QtWidgets import (
    QAbstractItemView,
    QApplication, 
    QAction,
    QGraphicsScene,
    QGraphicsView,
    QGridLayout,
    QGraphicsLineItem,
    QGraphicsRectItem,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget, 
    QVBoxLayout, 
    QTreeWidget,
    QTreeWidgetItem,

    QTableWidget,
    
    QTableWidgetItem,
    QFileDialog,
)
from PySide2.QtGui import (
    QPalette, 
    QColor,
    QBrush,
    QIcon,
    QPixmap,
    QPainter,
    QPen,

)
from PySide2.QtCore import (
    Qt,
    QByteArray,
    QSize,
    QUrl,
)

from PySide2.QtSvg import QSvgWidget
from PySide2.QtWebEngineWidgets import QWebEngineView

from core import Layout, GraphicObject, Surface, PointSequence, Point
from utils import RGBToHex, HexToRGB
from ManagerDialogs import AddObjectDialog, SaveAssetDialog, OpenAssetDialog
from Database import select_object_by_id, insert_asset, select_asset_by_id
from ImageProcessor import ImageProcessorMainWindow

RED_PEN_DASH = QPen(Qt.red, 1, Qt.DashDotLine)
RED_PEN_SOLID = QPen(Qt.red, 1, Qt.SolidLine)
BLACK_PEN = QPen(Qt.black, 1, Qt.SolidLine)

class MyWidget(QWidget):

    def __init__(self, color):
        super(MyWidget, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

'''
   GCanvas
'''
class GCanvas(QGraphicsView):

    def __init__(self, data, *args, **kwargs):
        self.scene = QGraphicsScene()
        super().__init__(self.scene, *args, **kwargs)
        self.data = data
        self.layout_gi = LayoutGraphicsItem(data, self.scene)

    def printLayout(self, layout):
        rect = Handler(layout, "xy")
        self.scene.addItem(rect)
        rect = Handler(layout, "h")
        self.scene.addItem(rect)
        rect = Handler(layout, "w")
        self.scene.addItem(rect)
        rect = Handler(layout, "wh")
        self.scene.addItem(rect)
        rect = QGraphicsRectItem(layout.x, layout.y, layout.w, layout.h)
        self.scene.addItem(rect)

    def addAsset(self, layout):
        self.layout_gi.addLayout(layout)

    def getCurrentAsJson(self):
        return self.data.json()
    
    def setAsset(self, data):
        self.scene.clear()
        self.data = data
        self.layout_gi = LayoutGraphicsItem(data, self.scene)
'''
   GraphicObjectItem
'''
class GraphicObjectItem:

    def __init__(self, content, scene, container):
        self.scene = scene
        self.content = content
        self.container = container
        minx = content.getMinX()
        miny = content.getMinY()
        width = content.getWidth()
        self.lines = []
        self.bx = container.w/content.getWidth()
        self.by = container.h/content.getHeight()
        self.ax = container.x - minx*self.bx
        self.ay = container.y - miny*self.by
        for surface in self.content.surfaces:
            surface.outer = self.printPointSequence(surface.outer)
            holes = []
            for hole in surface.holes:
                holes.append(self.printPointSequence(hole))
            surface.holes = holes


    def printPointSequence(self, pointSequence):
        lines = []
        ppoint = pointSequence.points[-1]
        for point in pointSequence.points:
            line = QGraphicsLineItem(self.ax + self.bx*ppoint.x, self.ay + self.by*ppoint.y, self.ax + self.bx*point.x, self.ay + self.by*point.y)
            self.scene.addItem(line)
            lines.append((ppoint.x, ppoint.y, point.x, point.y, line))
            ppoint = point
        return lines

    def updateContent(self):
        self.bx = self.container.w/self.content.getWidth()
        self.by = self.container.h/self.content.getHeight()
        self.ax = self.container.x - self.content.getMinX()*self.bx
        self.ay = self.container.y - self.content.getMinY()*self.by
        def updateLine(l):
            (x1, y1, x2, y2, mline) = l
            mline.setLine(self.ax + self.bx*x1, self.ay + self.by*y1, self.ax + self.bx*x2, self.ay + self.by*y2)
        for surface in self.content.surfaces:
            for line in surface.outer:
                updateLine(line)
            for hole in surface.holes:
                for line in hole:
                    updateLine(line)
'''
   LayoutGraphicsItem
'''
class LayoutGraphicsItem(QGraphicsRectItem):
    def __init__(self, layout, scene, container=None):
        super().__init__(layout.x, layout.y, layout.w, layout.h)
        self.scene = scene
        self.layout = layout
        self.children = []

        self.setPen(RED_PEN_DASH)
        self.scene.addItem(self)

        self.rect1 = Handler(layout, "xy", self)
        self.rect1.setPen(RED_PEN_SOLID)
        self.scene.addItem(self.rect1)

        self.rect2 = Handler(layout, "yw", self)
        self.rect2.setPen(RED_PEN_SOLID)
        self.scene.addItem(self.rect2)

        self.rect3 = Handler(layout, "xh", self)
        self.rect3.setPen(RED_PEN_SOLID)
        self.scene.addItem(self.rect3)

        self.rect4 = Handler(layout, "wh", self)
        self.rect4.setPen(RED_PEN_SOLID)
        self.scene.addItem(self.rect4)
        
        
        if type(layout.content) == list:
            for obj in layout.content: 
                self.children.append(LayoutGraphicsItem(obj, self.scene, layout))
        else:
            self.children.append(GraphicObjectItem(layout.content, self.scene, layout))

    def addLayout(self, layout):
       self.layout.content.append(layout)
       self.children.append(LayoutGraphicsItem(layout, self.scene, self.layout))
       self.updateContent()

    def updateDelta(self, dx, dy, dw, dh):
        nx = self.layout.x + dx
        ny = self.layout.y + dy
        nw = self.layout.w + dw - dx
        nh = self.layout.h + dh - dy
        self.layout.x = nx
        self.layout.y = ny
        self.layout.w = nw
        self.layout.h = nh
        self.updateContent()
        
    def updateContent(self):
        self.setRect(self.layout.x, self.layout.y, self.layout.w, self.layout.h)
        self.rect1.setRect(self.layout.x-2, self.layout.y-2, 4, 4)
        self.rect2.setRect(self.layout.x+self.layout.w-2, self.layout.y-2, 4, 4)
        self.rect3.setRect(self.layout.x-2, self.layout.y+self.layout.h-2, 4, 4)
        self.rect4.setRect(self.layout.x+self.layout.w-2, self.layout.y+self.layout.h-2, 4, 4)
        for child in self.children:
            child.updateContent()

    '''
      Mouse events
    '''

    def mousePressEvent(self, e):
         self.initialpos = e.screenPos()
         self.ix = e.scenePos().x()
         self.iy = e.scenePos().y()

    def mouseMoveEvent(self, e):
        if self.initialpos != None and self.initialpos != e.scenePos():
            dx = (e.scenePos().x() - self.ix)
            dy = (e.scenePos().y() - self.iy)
            self.layout.x = self.layout.x + dx
            self.layout.y = self.layout.y + dy
            self.ix = e.scenePos().x()
            self.iy = e.scenePos().y()
            self.updateContent()

'''
   LayoutGraphicsItem
'''
class Handler(QGraphicsRectItem):
    def __init__(self, layout, attrstr, parent, *args, **kwargs):
        if attrstr == "xy":
            super().__init__(layout.x-2, layout.y-2, 4, 4)
        elif attrstr == "yw":
            super().__init__(layout.x+layout.w-2, layout.y-2, 4, 4)
        elif attrstr == "xh":
            super().__init__(layout.x-2, layout.y+layout.h-2, 4, 4)
        elif attrstr == "wh":
            super().__init__(layout.x+layout.w-2, layout.y+layout.h-2, 4, 4)

        self.parent = parent
        self.layout = layout
        self.attrstr = attrstr
        self.initialpos = None

    def updateDelta(self, dx, dy, dw, dh):
        self.parent.updateDelta(dx, dy, dw, dh)

    def mousePressEvent(self, e):
         self.initialpos = e.screenPos()
         self.ix = e.scenePos().x()
         self.iy = e.scenePos().y()

    def mouseMoveEvent(self, e):
        if self.initialpos != None and self.initialpos != e.scenePos():
            dx, dy, dw, dh = 0,0,0,0
            if self.attrstr == "xy":
                dx = (e.scenePos().x() - self.ix)
                dy = (e.scenePos().y() - self.iy)
            elif self.attrstr == "yw":
                dw = (e.scenePos().x() - self.ix)
                dy = (e.scenePos().y() - self.iy)
            elif self.attrstr == "xh":
                dx = (e.scenePos().x() - self.ix)
                dh = (e.scenePos().y() - self.iy)
            elif self.attrstr == "wh":
                dw = (e.scenePos().x() - self.ix)
                dh = (e.scenePos().y() - self.iy)
            self.ix = e.scenePos().x()
            self.iy = e.scenePos().y()
            self.updateDelta(dx, dy, dw, dh)
                 
    def mouseReleaseEvent(self, e):
         self.initialpos = None
         
'''
***********************************
   MainWindow
***********************************
'''
class MainWindow(QMainWindow):

    data = None
    max_id_surf = 0
    tmp = 0
        
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Asset Manger Tool")

        layout1 = QHBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0,0,0,0)

        toolbar = QWidget()
        toolbar.setFixedWidth(70)
        layout1.addWidget(toolbar)
        
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
        icon8.addPixmap(QPixmap("icons/pointer.png"), QIcon.Normal, QIcon.Off)
        self.penButton.setIcon(icon8)
        self.penButton.setCheckable(True)
        self.penButton.setObjectName("penButton")
        self.gridLayout.addWidget(self.penButton, 0, 0, Qt.AlignTop)
        
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
        self.gridLayout.addWidget(self.rectButton, 0, 1, Qt.AlignTop)

        self.data = Layout(0, 0, 150, 200, [])
        self.canvas = GCanvas(self.data)
        
        layout1.addWidget(self.canvas)
        
        # Tree 
        self.create_tree()
        layout2.addWidget(self.tree_widget)

        # Table 
        self.create_table()
        layout2.addWidget(self.table_widget)
        layout1.addLayout(layout2)
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

        # Menu 
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        open_asset_action = QAction("&Open asset...", self)
        open_asset_action.triggered.connect(self.open_asset)
        file_menu.addAction(open_asset_action)
        
        save_asset_action = QAction("&Save asset...", self)
        save_asset_action.triggered.connect(self.save_asset)
        file_menu.addAction(save_asset_action)
        
        save_asset_as_action = QAction("&Save asset as...", self)
        save_asset_as_action.triggered.connect(self.save_asset_as)
        file_menu.addAction(save_asset_as_action)
        
        add_pobject_action = QAction("&Add pobject...", self)
        add_pobject_action.triggered.connect(self.add_object)
        file_menu.addAction(add_pobject_action)

        render_menu = menu.addMenu("&Render")
        render_as_svg_action = QAction("&As svg...", self)
        render_as_svg_action.triggered.connect(self.render_as_svg)
        render_menu.addAction(render_as_svg_action)
        
        object_menu = menu.addMenu("&Object")
        launch_extractor_action = QAction("&Extract", self)
        launch_extractor_action.triggered.connect(self.launch_extractor)
        object_menu.addAction(launch_extractor_action)
    ''' 
      Table methods
    '''
    def create_table(self):
        self.table_widget = QTableWidget(0, 2, self);
        self.table_widget.verticalHeader().setVisible(False);
        self.table_widget.setHorizontalHeaderLabels(["Property", "Value"]);

    '''
      Tree methods
    '''
    def create_tree(self):
        self.tree_widget = QTreeWidget()
        self.tree_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_widget.setHeaderLabels(["Collections"])
        self.tree_widget.currentItemChanged.connect(self.tree_widget_current_item_changed)
        self.tree_widget.itemClicked.connect(self.tree_widget_item_clicked)
        self.tree_widget.itemPressed.connect(self.tree_widget_item_pressed)
        self.tree_widget.itemActivated.connect(self.tree_widget_item_activated)
        
    def tree_widget_current_item_changed(self, current, previous):
        print("-->tree_widget_current_item_changed()")
        obj = current.data(0, Qt.UserRole)
        if type(obj) == Vector:
            self.table_widget.setRowCount(0)
            self.table_widget_add_row("Name", obj.name)
        if type(obj) == Surface:
            self.table_widget.setRowCount(0)
            self.table_widget_add_row("Name", obj.name)
            self.table_widget_add_row("Color", RGBToHex(obj.color))
        if type(obj) == Collection:
            self.table_widget.setRowCount(0)
            self.table_widget_add_row("Name", obj.name)

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
            vect = item.data(0, Qt.UserRole)
            print(vect)
            if type(vect) == Vector: vect.visible = True
            print(vect)
        elif item.checkState(column) == Qt.Unchecked:
            vect = item.data(0, Qt.UserRole)
            print(vect)
            if type(vect) == Vector: vect.visible = False
            print(vect)
        self.canvas.update_canvas()

    def tree_widget_item_pressed(self, item, column):
        print("-->tree_widget_item_pressed()")

    def update_tree(self):
        self.tree_widget.clear()
        for collection in self.data:
            col_tree_item = QTreeWidgetItem([collection.name])
            col_tree_item.setFlags(col_tree_item.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            col_tree_item.setCheckState(0, Qt.Checked)
            self.tree_widget.addTopLevelItem(col_tree_item)
            for surface in collection.surfaces:
                surf_tree_item = QTreeWidgetItem([surface.name])
                surf_tree_item.setCheckState(0, Qt.Checked)
                surf_tree_item.setData(0, Qt.UserRole, surface)
                col_tree_item.addChild(surf_tree_item)
                for vector in surface.vectors:
                    vect_tree_item = QTreeWidgetItem(vector.name)
                    vect_tree_item.setCheckState(0, Qt.Checked)
                    vect_tree_item.setData(0, Qt.UserRole, vector)
                    #vect_tree_item.clicked.connect(self.vect_tree_item_clicked)
                    surf_tree_item.addChild(vect_tree_item)
        self.tree_widget.expandAll()

    def vect_tree_item_clicked(self):
        print(self)

    '''
      Action methods
    '''

    def render_as_svg(self):
        self.svgview = QWebEngineView()
        print(self.svgview.settings())
        #self.svgview.load(QUrl.fromLocalFile("test.html"))
        self.svgview.load(QUrl("http://localhost/"))
        #self.svgview.load(QUrl("https://qt-project.org/"))
        self.svgview.resize(1024, 750)
        self.svgview.show()

    '''
    def add_collection(self):
        (fname, file_type) = QFileDialog.getOpenFileName(self, 'Open file', '.',"Data files (*.dat)")
        col_tree_item = None
        with (open(fname, "rb")) as openfile:
            collection = pickle.load(openfile)
            colname = os.path.basename(fname)[:-4]
  
        coldata = Collection(colname)
        surfarrdata = []
        i = 1
        for (surface, color) in collection:
            j = 1
            surfdata = Surface(str(i), color)
            vectdata = []
            for vector in surface:
                vectdata.append(Vector(str(j), vector))
                j += 1
            surfdata.vectors = vectdata
            surfarrdata.append(surfdata)
            i += 1
        coldata.surfaces = surfarrdata
        self.data.append(coldata)
        self.update_tree()
        self.canvas.update_canvas()
    '''
    def open_asset(self):
        dlg = OpenAssetDialog()
        if dlg.exec():
            selected = dlg.list.selectedItems()
            if len(selected) > 0:
                selected = selected[0]
                objid = selected.data(Qt.UserRole)
                self.addAssetFromDatabase(objid)
            print("Ok")
        else:
            print("Cancel!")
    def save_asset(self):
        dlg = SaveAssetDialog()
        if dlg.exec():
            name = dlg.lineEdit.text()
            json = self.canvas.getCurrentAsJson()
            print(dlg.lineEdit)
            insert_asset(name, json)
            print("Ok")
        else:
            print("Cancel!")

    def save_asset_as(self):
        dlg = SaveAssetDialog()
        if dlg.exec():
            name = dlg.lineEdit.text()
            json = self.canvas.getCurrentAsJson()
            print(dlg.lineEdit)
            insert_asset(name, json)
            print("Ok")
        else:
            print("Cancel!")

    def add_object(self):
        dlg = AddObjectDialog()
        if dlg.exec():
            selected = dlg.list.selectedItems()
            for item in selected:
                objid = item.data(Qt.UserRole)
                self.addObjectFromDatabase(objid)
            print("Ok")
        else:
            print("Cancel!")

    def addObjectFromDatabase(self, objid):
        json = select_object_by_id(objid)
        pobj = GraphicObject.parse(json)
        x = pobj.getMinX()
        y = pobj.getMinY()
        width = pobj.getWidth()
        height = pobj.getHeight()
        self.canvas.addAsset(Layout(x, y, width, height, pobj))

    def addAssetFromDatabase(self, assetid):
        
        def loadLayoutFromJson(json):
            pobj = Layout.parse(json)
            print(type(pobj.content))
            if type(pobj.content) == list:
                layouts = []
                for item in pobj.content:
                    layout = loadLayoutFromJson(item)
                    layouts.append(layout)
                pobj.content = layouts
            elif type(pobj.content) == int:
                json = select_object_by_id(pobj.content)
                pobj.content = GraphicObject.parse(json)
                
            return pobj

        asset = select_asset_by_id(assetid)
        self.data = loadLayoutFromJson(asset["content"])
        self.canvas.setAsset(self.data)
        
    def launch_extractor(self):
        self.extractor = ImageProcessorMainWindow()
        #self.editor.addObjectData(pobj)
        self.extractor.show()



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    app.exec_()



