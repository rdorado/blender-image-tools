from PySide2.QtWidgets import (
  QDialog,
  QDialogButtonBox,
  QLabel,
  QLineEdit,
  QListWidget,
  QListWidgetItem,
  QHBoxLayout,
  QVBoxLayout,
  QWidget,
)
from PySide2.QtCore import (
  Qt,
  QRect,
)

from Database import select_objects_names, select_assets_names

class AddObjectDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(400, 380)
        self.setWindowTitle("Search object")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        hlayout = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText("Search:")
        self.label.setGeometry(QRect(50, 32, 100, 10))
        hlayout.addWidget(self.label)

        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 30, 200, 20))
        hlayout.addWidget(self.lineEdit)

        self.list = QListWidget()
        self.list.setObjectName(u"list")
        self.list.setGeometry(QRect(80, 55, 100, 50))

        pobjects = select_objects_names()
        for pobject in pobjects:
            newItem = QListWidgetItem(pobject['name'])
            newItem.setData(Qt.UserRole, pobject['id'])
            self.list.addItem(newItem)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setGeometry(QRect(10, 10, 10, 32))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        
        hwidget = QWidget()
        hwidget.setLayout(hlayout)
        self.layout.addWidget(hwidget)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class SaveAssetDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(400, 250)
        self.setWindowTitle("Save asset")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        hlayout = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText("Asset name:")
        self.label.setGeometry(QRect(50, 32, 100, 10))
        hlayout.addWidget(self.label)

        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 30, 200, 20))
        hlayout.addWidget(self.lineEdit)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setGeometry(QRect(10, 10, 10, 32))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        
        hwidget = QWidget()
        hwidget.setLayout(hlayout)
        self.layout.addWidget(hwidget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
        
class OpenAssetDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(400, 380)
        self.setWindowTitle("Search asset")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        hlayout = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText("Search:")
        self.label.setGeometry(QRect(50, 32, 100, 10))
        hlayout.addWidget(self.label)

        self.lineEdit = QLineEdit()
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 30, 200, 20))
        hlayout.addWidget(self.lineEdit)

        self.list = QListWidget()
        self.list.setObjectName(u"list")
        self.list.setGeometry(QRect(80, 55, 100, 50))

        pobjects = select_assets_names()
        for pobject in pobjects:
            newItem = QListWidgetItem(pobject['name'])
            newItem.setData(Qt.UserRole, pobject['id'])
            self.list.addItem(newItem)

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setGeometry(QRect(10, 10, 10, 32))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        
        hwidget = QWidget()
        hwidget.setLayout(hlayout)
        self.layout.addWidget(hwidget)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)