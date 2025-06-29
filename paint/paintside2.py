import os
import sys
import pickle

from PySide2.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QAction,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
)
from PySide2.QtGui import (
    QPalette, 
    QColor,
    QBrush,
    QPixmap,
    QPainter,
)
from PySide2.QtCore import Qt

def RGBToHex(rgbcolor):
    return '#'+"".join(map(lambda x: str(hex(x))[2:], rgbcolor))
    
def HexToRGB(hexcolor):
    return [int(hexcolor[1:3], 16), int(hexcolor[3:5], 16), int(hexcolor[5:7], 16)]
    


class MyWidget(QWidget):

    def __init__(self, color):
        super(MyWidget, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    data = []
    canvas_h = 600
    canvas_w = 600
    max_id_surf = 0
    tmp = 0
        
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("My App")

        layout1 = QHBoxLayout()
        layout1.setContentsMargins(0,0,0,0)
        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0,0,0,0)

        self.canvas = QLabel()
        self.update_canvas()
        layout1.addWidget(self.canvas)
        
        self.create_tree()
        layout2.addWidget(self.tree_widget)

        self.create_table()
        layout2.addWidget(self.table_widget)
        layout1.addLayout(layout2)
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

        add_collection_action = QAction("&Open", self)
        add_collection_action.triggered.connect(self.add_collection)
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(add_collection_action)

    def create_table(self):
        self.table_widget = QTableWidget(0, 2, self);
        self.table_widget.verticalHeader().setVisible(False);
        self.table_widget.setHorizontalHeaderLabels(["Property", "Value"]);


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
        self.update_canvas()

    def tree_widget_item_pressed(self, item, column):
        print("-->tree_widget_item_pressed()")
        #print(dir(item))
        #print(column)

    def print_background(self):
        pixmap = QPixmap(self.canvas_h, self.canvas_h)
        self.canvas.setPixmap(pixmap)
        
        painter = QPainter(self.canvas.pixmap())

        #print(pixmap.width, pixmap.height)
        
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

    def update_canvas(self):
        self.print_background()
        painter = QPainter(self.canvas.pixmap())
        #if self.tmp >=4: return
        #self.tmp+=1
        for collection in self.data:
            for surface in collection.surfaces:
                p = painter.pen()
                p.setWidth(1)
                hexcol = RGBToHex(surface.color)
                p.setColor(QColor(hexcol))
                painter.setPen(p)
                for vector in surface.vectors:
                    #print(vector)
                    if not vector.visible: continue
                    ppoint = vector.points[-1]
                    for point in vector.points:
                        (x1, y1) = ppoint
                        (x2, y2) = point
                        painter.drawLine(y1, x1, y2, x2)
                        ppoint = point
        painter.end()
        self.update()

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
        self.update_canvas()


app = QApplication(sys.argv)

window = MainWindow()
window.resize(800, 600)
window.show()

app.exec_()

