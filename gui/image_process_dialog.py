import sys
import cv2
from PySide2.QtWidgets import (
    QLineEdit, QPushButton, QApplication,
    QLabel,
    QScrollArea,
    QVBoxLayout, QDialog
)
from PySide2.QtGui import (
    QPixmap,
    QImage,
)
from PySide2.QtCore import Qt

class Form(QDialog):
    
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")
        
        
        self.canvas = QLabel()
        self.canvas.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.canvas)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.scroll)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.greetings)

        # Load Pic
        img = cv2.imread("faces.jpg")
        #picture = QPixmap("faces.jpg")
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        picture = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.canvas.setPixmap(QPixmap(picture))

    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())

    '''
    def print_background(self):
        pixmap = QPixmap(self.canvas_h, self.canvas_h)
        self.canvas.setPixmap(pixmap)
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
    
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())