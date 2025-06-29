from PySide2.QtWidgets import (
  QDialog,
  QDialogButtonBox,
  QLabel,
  QLineEdit,
  QVBoxLayout,
)
from PySide2.QtCore import (
  QRect,
)

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(400, 124)
        self.setWindowTitle("Apply Cluster")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.label = QLabel(self)
        self.label.setObjectName(u"label")
        self.label.setText("Number of clusters:")
        self.label.setGeometry(QRect(30, 30, 100, 13))
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 30, 221, 20))

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setGeometry(QRect(10, 90, 341, 32))
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        
        #self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
'''
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 124)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 70, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 30, 47, 13))
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 30, 221, 20))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
    # retranslateUi
'''