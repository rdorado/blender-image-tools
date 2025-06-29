import random
import sys
import os

from PySide6.QtWidgets import (
  QApplication,
  QButtonGroup,
  QComboBox,
  QColorDialog,
  QFileDialog,
  QFontComboBox,
  QLabel,
  QMainWindow,
  QMenu,
  QScrollArea,
  QSlider,
  QVBoxLayout,
  QWidget,
)
from PySide6.QtGui import (
  QBrush,
  QColor,
  QFont,
  QKeySequence,
  QPainter,
  QPen,
  QPixmap,
)
from PySide6.QtCore import (
  Qt,
  QObject,
  QPoint,
  QRect,
  QTimer,
  Signal,
)

from MainWindow import Ui_MainWindow

'''
try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PySide2.QtWinExtras import QtWin
    myappid = 'com.learnpyqt.minute-apps.paint'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass
'''


'''

COLORS = [
    '#000000', '#82817f', '#820300', '#868417', '#007e03', '#037e7b', '#040079',
    '#81067a', '#7f7e45', '#05403c', '#0a7cf6', '#093c7e', '#7e07f9', '#7c4002',
    '#ffffff', '#c1c1c1', '#f70406', '#fffd00', '#08fb01', '#0bf8ee', '#0000fa',
    '#b92fc2', '#fffc91', '#00fd83', '#87f9f9', '#8481c4', '#dc137d', '#fb803c',
]
'''

BRUSH_MULT = 3
SPRAY_PAINT_MULT = 5
SPRAY_PAINT_N = 100
FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

MODES = [
    'selectpoly', 'selectrect',
    'eraser', 'fill',
    'dropper', 'spray',
    'pen', 'brush',
    'line', 'polyline',
    'rect', 'polygon',
    'ellipse', 'roundrect'
]

CANVAS_DIMENSIONS = 600, 400
PREVIEW_PEN = QPen(QColor(0x0, 0x0, 0x0), 1, Qt.SolidLine)
SELECTION_PEN = QPen(QColor(0x0, 0x0, 0x0), 1, Qt.DashLine)
'''
STAMPS = [
    'stamps/pie-apple.png',
    'stamps/pie-cherry.png',
    'stamps/pie-cherry2.png',
    'stamps/pie-lemon.png',
    'stamps/pie-moon.png',
    'stamps/pie-pork.png',
    'stamps/pie-pumpkin.png',
    'stamps/pie-walnut.png',
]

def build_font(config):
    """
    Construct a complete font from the configuration options
    :param self:
    :param config:
    :return: QFont
    """
    font = config['font']
    font.setPointSize(config['fontsize'])
    font.setBold(config['bold'])
    font.setItalic(config['italic'])
    font.setUnderline(config['underline'])
    return font
'''

class Canvas(QLabel):

    last_pos = None
    command_from_canvas = Signal(dict)
    
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.background_color = QColor(self.config.secondary_color) if self.config.secondary_color else QColor(Qt.white)
        
        self.active_shape_fn = None

        self.last_pos = None
        self.history_pos = None
        self.dash_offset = 0
        self.last_history = []
        self.locked = False
        self.active_shape_args = ()
        self.backward_history = []
        self.forward_history = []
        self.current_pixmap = None
        self.scale = 1.0

    def initialize(self):
        self.background_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color.setAlpha(100)
        self.reset()

    def setPixmap(self, pixmap, *args, **kwargs):
        self.current_pixmap = QPixmap(pixmap)
        size = pixmap.size()
        pixmap = pixmap.scaled(self.scale * size)
        super().setPixmap(pixmap, *args, **kwargs)

    def repaintCurrentPixmap(self):
        size = self.current_pixmap.size()
        pixmap = self.current_pixmap.scaled(self.scale * size)
        super().setPixmap(pixmap)

    def zoom_in(self):
        self.scale = self.scale*2
        self.repaintCurrentPixmap()

    def zoom_out(self):
        self.scale = self.scale/2
        self.repaintCurrentPixmap()

    def update_history(self):
        self.backward_history.append(self.current_pixmap)
        self.current_pixmap = QPixmap(self.pixmap())
        self.forward_history = []

    def undo(self):
        if len(self.backward_history) > 0:
           self.forward_history.append(self.current_pixmap)
           self.current_pixmap = self.backward_history[-1]
           super().setPixmap(self.current_pixmap)
           del self.backward_history[-1]

    def redo(self):
        if len(self.forward_history) > 0:
           self.backward_history.append(self.current_pixmap)
           self.current_pixmap = self.forward_history[-1]
           #self.current_pixmap = self.pixmap()
           super().setPixmap(self.current_pixmap)
           del self.forward_history[-1]

    #primary_color = QColor(Qt.black)
    #secondary_color = None

    '''
    active_color = None
    preview_pen = None

    current_stamp = None

    def initialize(self):
        self.background_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color.setAlpha(100)
        self.reset()

    def reset(self):
        # Create the pixmap for display.
        self.setPixmap(QPixmap(*CANVAS_DIMENSIONS))

        # Clear the canvas.
        self.pixmap().fill(self.background_color)
    '''
    def on_timer(self):
        #print("On Timer")
        if self.timer_event:
            #print("On Timer:", self.timer_event)
            self.timer_event()

    def start_timer(self, fn_call):
        #print("Start Timer")
        self.timer = QTimer()
        self.timer_event = fn_call
        self.timer.timeout.connect(self.on_timer)
        self.timer.setInterval(100)
        self.timer.start()

    def timer_cleanup(self):
        #print("Start Stop")
        self.timer.stop()

    def reset_(self):
        # Clean up active timer animations.
        #self.timer_cleanup()
        # Reset mode-specific vars (all)
        self.active_shape_fn = None
        #self.active_shape_args = ()

        #self.origin_pos = None

        #self.current_pos = None
        self.last_pos = None
        self.history_pos = None
        self.last_history = []

        #self.current_text = ""
        #self.last_text = ""

        #self.last_config = {}

        self.dash_offset = 0
        #self.locked = False


    def mousePressEvent(self, e):
    
        if e.button() == Qt.LeftButton:
            fn = getattr(self, "%s_mousePressEvent" % self.config.mode, None)
            if fn:
                self.repaintCurrentPixmap()
                return fn(e)
        elif e.button() == Qt.RightButton:
            
            menu = QMenu()
            menu.addAction("Create")
            #menu.addAction("Action2")
            p = self.mapToGlobal(e.pos())
            action = menu.exec_(p)
            print(action)
            if action is not None:
                print(self.origin_pos, self.last_pos)
                pixmap = self.current_pixmap.copy(self.origin_pos.x(),self.origin_pos.y(), self.last_pos.x(), self.last_pos.y())
                self.command_from_canvas.emit({"command":"create_new_document_from_selection", "selection": pixmap})
                #print(action.text())

    def mouseMoveEvent(self, e):
        fn = getattr(self, "%s_mouseMoveEvent" % self.config.mode, None)
        #print(fn, "%s_mouseMoveEvent" % self.config.mode)
        if fn:
            return fn(e)

    def mouseReleaseEvent(self, e):
        fn = getattr(self, "%s_mouseReleaseEvent" % self.config.mode, None)
        #print(fn, "%s_mouseReleaseEvent" % self.config.mode)
        if fn:
            return fn(e)

    def mouseDoubleClickEvent(self, e):
        fn = getattr(self, "%s_mouseDoubleClickEvent" % self.config.mode, None)
        #print(fn, "%s_mouseDoubleClickEvent" % self.config.mode)
        if fn:
            return fn(e)

    # Generic events (shared by brush-like tools)

    def generic_mousePressEvent(self, e):
        self.last_pos = e.pos()

        if e.button() == Qt.LeftButton:
            self.active_color = self.config.primary_color
        else:
            self.active_color = self.config.secondary_color

    def generic_mouseMoveEvent(self, e):
        self.last_pos = e.pos()

    def generic_mouseReleaseEvent(self, e, add_to_history=True):
        if add_to_history: self.update_history()
        self.last_pos = None


    # Mode-specific events.

    # Pen events

    def pen_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def pen_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.active_color, self.config.size, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
            p.drawLine(self.last_pos, e.pos())
            self.update()
        self.last_pos = e.pos()

    def pen_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)


    # Select rectangle events

    def selectrect_mousePressEvent(self, e):
        #self.preview_pen = SELECTION_PEN
        self.origin_pos = e.pos()
        self.current_pos = e.pos()

    def selectrect_mouseMoveEvent(self, e):
        if self.last_pos:
            pixmap = QPixmap(self.current_pixmap)
            p = QPainter(pixmap)
            p.setPen(SELECTION_PEN)
            p.drawRect(self.origin_pos.x(), self.origin_pos.y(), self.last_pos.x() - self.origin_pos.x(), self.last_pos.y() - self.origin_pos.y())
            p.end()
            super().setPixmap(pixmap)
        self.last_pos = e.pos()

    def selectrect_mouseReleaseEvent(self, e):
        #self.current_pos = e.pos()
        #self.locked = True
        #self.timer_cleanup()
        self.active_shape_fn = None

    def selectrect_copy(self):
        """
        Copy a rectangle region of the current image, returning it.

        :return: QPixmap of the copied region.
        """
        self.timer_cleanup()
        return self.pixmap().copy(QRect(self.origin_pos, self.current_pos))


    # Line events

    def line_mousePressEvent(self, e):
        self.origin_pos = e.pos()
        self.current_pos = e.pos()

    def line_mouseMoveEvent(self, e):
        if self.last_pos:
            pixmap = QPixmap(self.current_pixmap)
            p = QPainter(pixmap)
            p.setPen(PREVIEW_PEN)
            p.drawLine(self.origin_pos, self.last_pos)
            p.end()
            super().setPixmap(pixmap)
        self.last_pos = e.pos()

    def line_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    # Rectangle events

    def rect_mousePressEvent(self, e):
        self.origin_pos = e.pos()
        self.current_pos = e.pos()

    def rect_mouseMoveEvent(self, e):
        if self.last_pos:
            pixmap = QPixmap(self.current_pixmap)
            p = QPainter(pixmap)
            p.setPen(PREVIEW_PEN)
            p.drawRect(self.origin_pos.x(), self.origin_pos.y(), self.last_pos.x() - self.origin_pos.x(), self.last_pos.y() - self.origin_pos.y())
            p.end()
            super().setPixmap(pixmap)
        self.last_pos = e.pos()

    def rect_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)


    '''
    # Select polygon events

    def selectpoly_mousePressEvent(self, e):
        if not self.locked or e.button == Qt.RightButton:
            self.active_shape_fn = 'drawPolygon'
            self.preview_pen = SELECTION_PEN
            self.generic_poly_mousePressEvent(e)

    def selectpoly_timerEvent(self, final=False):
        self.generic_poly_timerEvent(final)

    def selectpoly_mouseMoveEvent(self, e):
        if not self.locked:
            self.generic_poly_mouseMoveEvent(e)

    def selectpoly_mouseDoubleClickEvent(self, e):
        self.current_pos = e.pos()
        self.locked = True

    def selectpoly_copy(self):
        """
        Copy a polygon region from the current image, returning it.

        Create a mask for the selected area, and use it to blank
        out non-selected regions. Then get the bounding rect of the
        selection and crop to produce the smallest possible image.

        :return: QPixmap of the copied region.
        """
        self.timer_cleanup()

        pixmap = self.pixmap().copy()
        bitmap = QBitmap(*CANVAS_DIMENSIONS)
        bitmap.clear()  # Starts with random data visible.

        p = QPainter(bitmap)
        # Construct a mask where the user selected area will be kept, 
        # the rest removed from the image is transparent.
        userpoly = QPolygon(self.history_pos + [self.current_pos])
        p.setPen(QPen(Qt.color1))
        p.setBrush(QBrush(Qt.color1))  # Solid color, Qt.color1 == bit on.
        p.drawPolygon(userpoly)
        p.end()

        # Set our created mask on the image.
        pixmap.setMask(bitmap)

        # Calculate the bounding rect and return a copy of that region.
        return pixmap.copy(userpoly.boundingRect())
    '''


    '''
    # Eraser events

    def eraser_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def eraser_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.config.eraser_color, 30, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def eraser_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)
    '''

    '''
    # Stamp (pie) events

    def stamp_mousePressEvent(self, e):
        p = QPainter(self.pixmap())
        stamp = self.current_stamp
        p.drawPixmap(e.x() - stamp.width() // 2, e.y() - stamp.height() // 2, stamp)
        self.update()
    '''




    '''
    # Brush events

    def brush_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def brush_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.active_color, self.config.size * BRUSH_MULT, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.drawLine(self.last_pos, e.pos())

            self.last_pos = e.pos()
            self.update()

    def brush_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)

    '''

    # Spray events

    def spray_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)

    def spray_mouseMoveEvent(self, e):
        if self.last_pos:
            p = QPainter(self.pixmap())
            p.setPen(QPen(self.active_color, 1))

            for n in range(self.config.size * SPRAY_PAINT_N):
                xo = random.gauss(0, self.config.size * SPRAY_PAINT_MULT)
                yo = random.gauss(0, self.config.size * SPRAY_PAINT_MULT)
                p.drawPoint(e.x() + xo, e.y() + yo)

        self.update()

    def spray_mouseReleaseEvent(self, e):
        self.generic_mouseReleaseEvent(e)
    '''
    # Text events

    def keyPressEvent(self, e):
        if self.mode == 'text':
            if e.key() == Qt.Key_Backspace:
                self.current_text = self.current_text[:-1]
            else:
                self.current_text = self.current_text + e.text()

    def text_mousePressEvent(self, e):
        if e.button() == Qt.LeftButton and self.current_pos is None:
            self.current_pos = e.pos()
            self.current_text = ""
            self.config["timer_event"] = self.text_timerEvent

        elif e.button() == Qt.LeftButton:

            self.timer_cleanup()
            # Draw the text to the image
            p = QPainter(self.pixmap())
            p.setRenderHints(QPainter.Antialiasing)
            font = build_font(self.config)
            p.setFont(font)
            pen = QPen(self.primary_color, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            p.setPen(pen)
            p.drawText(self.current_pos, self.current_text)
            self.update()

            self.reset_mode()

        elif e.button() == Qt.RightButton and self.current_pos:
            self.reset_mode()

    def text_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.RasterOp_SourceXorDestination)
        pen = PREVIEW_PEN
        p.setPen(pen)
        if self.last_text:
            font = build_font(self.last_config)
            p.setFont(font)
            p.drawText(self.current_pos, self.last_text)

        if not final:
            font = build_font(self.config)
            p.setFont(font)
            p.drawText(self.current_pos, self.current_text)

        self.last_text = self.current_text
        self.last_config = self.config.copy()
        self.update()
    '''
    # Fill events

    def fill_mousePressEvent(self, e):
        self.generic_mousePressEvent(e)
        #if e.button() == Qt.LeftButton:
        #    self.active_color = self.primary_color
        #else:
        #    self.active_color = self.secondary_color

        image = self.pixmap().toImage()
        w, h = image.width(), image.height()
        x, y = e.x(), e.y()

        # Get our target color from origin.
        target_color = image.pixel(x,y)

        have_seen = set()
        queue = [(x, y)]

        def get_cardinal_points(have_seen, center_pos):
            points = []
            cx, cy = center_pos
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x, cy + y
                if (xx >= 0 and xx < w and
                    yy >= 0 and yy < h and
                    (xx, yy) not in have_seen):

                    points.append((xx, yy))
                    have_seen.add((xx, yy))

            return points

        # Now perform the search and fill.
        p = QPainter(self.pixmap())
        p.setPen(QPen(self.active_color))

        while queue:
            x, y = queue.pop()
            if image.pixel(x, y) == target_color:
                p.drawPoint(QPoint(x, y))
                queue.extend(get_cardinal_points(have_seen, (x, y)))

        self.update()

    # Dropper events

    def dropper_mousePressEvent(self, e):
        c = self.pixmap().toImage().pixel(e.pos())
        hex_color = QColor(c).name()

        if e.button() == Qt.LeftButton:
            
            self.config.primary_color_updated.emit(hex_color)
            #self.primary_color_updated.emit(hex)  # Update UI.

        elif e.button() == Qt.RightButton:
            #self.config.secondary_color = QColor(c)
            self.config.secondary_color_updated.emit(hex_color)
            #self.secondary_color_updated.emit(hex)  # Update UI.


    # Generic shape events: Rectangle, Ellipse, Rounded-rect

    def generic_shape_mousePressEvent(self, e):
        self.origin_pos = e.pos()
        self.current_pos = e.pos()
        self.start_timer(self.generic_shape_timerEvent)

    def generic_shape_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.RasterOp_SourceXorDestination)
        pen = self.preview_pen
        pen.setDashOffset(self.dash_offset)
        p.setPen(pen)
        print(self.active_shape_fn)
        if self.last_pos:
            getattr(p, self.active_shape_fn)(QRect(self.origin_pos, self.last_pos), *self.active_shape_args)

        if not final:
            self.dash_offset -= 1
            pen.setDashOffset(self.dash_offset)
            p.setPen(pen)
            getattr(p, self.active_shape_fn)(QRect(self.origin_pos, self.current_pos), *self.active_shape_args)

        self.update()
        self.last_pos = self.current_pos

    def generic_shape_mouseMoveEvent(self, e):
        self.current_pos = e.pos()

    def generic_shape_mouseReleaseEvent(self, e):
        if self.last_pos:
            # Clear up indicator.
            self.timer_cleanup()

            p = QPainter(self.pixmap())
            p.setPen(QPen(self.config.primary_color, self.config.size, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))

            if self.config.fill:
                p.setBrush(QBrush(self.config.secondary_color))
            getattr(p, self.active_shape_fn)(QRect(self.origin_pos, e.pos()), *self.active_shape_args)
            self.update()

        self.reset_()

    # Generic poly events
    def generic_poly_mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.history_pos:
                self.history_pos.append(e.pos())
            else:
                self.history_pos = [e.pos()]
                self.current_pos = e.pos()
                #self.timer_event = self.generic_poly_timerEvent
                self.start_timer(self.generic_poly_timerEvent)

        elif e.button() == Qt.RightButton and self.history_pos:
            # Clean up, we're not drawing
            self.timer_cleanup()
            #self.reset_mode()

    def generic_poly_timerEvent(self, final=False):
        p = QPainter(self.pixmap())
        p.setCompositionMode(QPainter.RasterOp_SourceXorDestination)
        pen = self.preview_pen
        p.setPen(pen)

        #p = QPainter(self.pixmap())
        #p.setCompositionMode(QPainter.RasterOp_SourceXorDestination)
        #pen = self.preview_pen
        #pen.setDashOffset(self.dash_offset)
        #p.setPen(pen)
        #p.setPen(QPen(self.config.primary_color, self.config.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.last_history = self.history_pos + [self.last_pos]
        '''
        if self.last_history:
            #print(getattr(p, self.active_shape_fn), self.history_pos)
            #p.drawLines(self.last_history)
            print(self.last_history)
            p.drawPolyline(self.last_history)
            #p.drawLines([QPoint(10,10), QPoint(10,20), QPoint(20,20)])
            #p.drawPolyline([QPoint(10,10), QPoint(10,20), QPoint(10,20), QPoint(20,20)])
            #getattr(p, self.active_shape_fn)(self.last_history)

        if not final:
            self.dash_offset -= 1
            pen.setDashOffset(self.dash_offset)
            p.setPen(pen)
            #print(self.history_pos, *self.history_pos, self.current_pos)
            getattr(p, self.active_shape_fn)(self.history_pos + [self.current_pos])
        '''
        if self.last_history:

            #p.drawPolyline(self.last_history)
            getattr(p, self.active_shape_fn)(self.last_history)

        if not final:
            self.dash_offset -= 1
            pen.setDashOffset(self.dash_offset)
            p.setPen(pen)
            getattr(p, self.active_shape_fn)(self.history_pos + [self.current_pos])



        self.update()
        self.last_pos = self.current_pos
        

    def generic_poly_mouseMoveEvent(self, e):
        self.current_pos = e.pos()

    def generic_poly_mouseDoubleClickEvent(self, e):
        self.timer_cleanup()
        p = QPainter(self.pixmap())
        p.setPen(QPen(self.config.primary_color, self.config.size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        # Note the brush is ignored for polylines.
        if self.config.secondary_color:
            p.setBrush(QBrush(self.config.secondary_color))

        getattr(p, self.active_shape_fn)(self.history_pos + [e.pos()])
        self.update()
        #self.reset_mode()

    # Polyline events

    def polyline_mousePressEvent(self, e):
        self.active_shape_fn = 'drawLines'
        self.preview_pen = PREVIEW_PEN
        self.generic_poly_mousePressEvent(e)
        #self.setMouseTracking(True)

    def polyline_timerEvent(self, final=False):
        self.generic_poly_timerEvent(final)

    def polyline_mouseMoveEvent(self, e):
        self.generic_poly_mouseMoveEvent(e)

    def polyline_mouseDoubleClickEvent(self, e):
        self.generic_poly_mouseDoubleClickEvent(e)
        self.setMouseTracking(False)


    '''
    # Polygon events

    def polygon_mousePressEvent(self, e):
        self.active_shape_fn = 'drawPolygon'
        self.preview_pen = PREVIEW_PEN
        self.generic_poly_mousePressEvent(e)

    def polygon_timerEvent(self, final=False):
        self.generic_poly_timerEvent(final)

    def polygon_mouseMoveEvent(self, e):
        self.generic_poly_mouseMoveEvent(e)

    def polygon_mouseDoubleClickEvent(self, e):
        self.generic_poly_mouseDoubleClickEvent(e)
    '''
    # Ellipse events

    def ellipse_mousePressEvent(self, e):
        self.active_shape_fn = 'drawEllipse'
        self.active_shape_args = ()
        self.preview_pen = PREVIEW_PEN
        self.generic_shape_mousePressEvent(e)

    def ellipse_timerEvent(self, final=False):
        self.generic_shape_timerEvent(final)

    def ellipse_mouseMoveEvent(self, e):
        self.generic_shape_mouseMoveEvent(e)

    def ellipse_mouseReleaseEvent(self, e):
        self.generic_shape_mouseReleaseEvent(e)

    # Roundedrect events

    def roundrect_mousePressEvent(self, e):
        self.active_shape_fn = 'drawRoundedRect'
        self.active_shape_args = (25, 25)
        self.preview_pen = PREVIEW_PEN
        self.generic_shape_mousePressEvent(e)

    def roundrect_timerEvent(self, final=False):
        self.generic_shape_timerEvent(final)

    def roundrect_mouseMoveEvent(self, e):
        self.generic_shape_mouseMoveEvent(e)

    def roundrect_mouseReleaseEvent(self, e):
        self.generic_shape_mouseReleaseEvent(e)


class Document:

    def __init__(self, name, config):
        self.name = name
        self.canvas = Canvas(config)
        self.widget =  None

    def undo(self):
        self.canvas.undo()

    def redo(self):
        self.canvas.redo()

    def zoom_in(self):
        self.canvas.zoom_in()
        self.update_widget()

    def zoom_out(self):
        self.canvas.zoom_out()
        self.update_widget()
        
    def update_widget(self):
        pixmap = self.canvas.pixmap()
        iw = pixmap.width()
        ih = pixmap.height()
        self.widget.resize(iw, ih)

    # Store configuration settings, including pen width, fonts etc.
class Config(QObject):
    primary_color_updated = Signal(str)
    secondary_color_updated = Signal(str)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #colors
        self.primary_color = QColor('#000000')
        self.secondary_color = QColor('#ffffff')

        #Set initial eraser colors and background color
        self.eraser_color = QColor(self.secondary_color) if self.secondary_color else QColor(Qt.white)
        self.eraser_color.setAlpha(100)

        #Initial Mode
        self.mode = 'rectangle'

        # Drawing options.
        self.size = 1
        self.fill =  True

        # Font options.
        self.font = QFont('Times')
        self.fontsize = 12
        self.bold = False
        self.italic = False
        self.underline = False


class MainWindow(Ui_MainWindow):


    new_doc_seq = 1

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #self.setupUi(self)
        self.show()
        self.documents = []
        self.config = Config()
        self.config.primary_color_updated.connect(self.set_primary_color)
        self.config.secondary_color_updated.connect(self.set_secondary_color)

        '''
        # Replace canvas placeholder from QtDesigner.
        self.horizontalLayout.removeWidget(self.canvas)
        self.canvas = Canvas()
        self.canvas.initialize()
        # We need to enable mouse tracking to follow the mouse without the button pressed.
        self.canvas.setMouseTracking(True)
        # Enable focus to capture key inputs.
        self.canvas.setFocusPolicy(Qt.StrongFocus)
        self.horizontalLayout.addWidget(self.canvas)
        '''
        # Setup the mode buttons
        mode_group = QButtonGroup(self)
        mode_group.setExclusive(True)

        for mode in MODES:
            try:
                btn = getattr(self, '%sButton' % mode)
                btn.pressed.connect(lambda mode=mode: self.set_mode(mode))
                mode_group.addButton(btn)
            except AttributeError:
                pass


        # Setup the color selection buttons.
        self.primaryButton.pressed.connect(lambda: self.choose_color(self.set_primary_color))
        self.secondaryButton.pressed.connect(lambda: self.choose_color(self.set_secondary_color))
        '''
        # Initialize button colours.
        for n, hex in enumerate(COLORS, 1):
            btn = getattr(self, 'colorButton_%d' % n)
            btn.setStyleSheet('QPushButton { background-color: %s; }' % hex)
            btn.hex = hex  # For use in the event below

            def patch_mousePressEvent(self_, e):
                if e.button() == Qt.LeftButton:
                    self.set_primary_color(self_.hex)

                elif e.button() == Qt.RightButton:
                    self.set_secondary_color(self_.hex)

            btn.mousePressEvent = types.MethodType(patch_mousePressEvent, btn)

        # Setup up action signals
        self.actionCopy.triggered.connect(self.copy_to_clipboard)
        '''
        
        '''
        # Initialize temporal timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.canvas.on_timer)
        self.timer.setInterval(100)
        self.timer.start()
        '''

        # Setup to agree with Canvas.
        self.set_primary_color('#000000')
        self.set_secondary_color('#ffffff')

        '''
        # Setup the stamp state.
        self.current_stamp_n = -1
        self.next_stamp()
        self.stampnextButton.pressed.connect(self.next_stamp)
        '''
        
        # Menu options
        self.actionNewImage.triggered.connect(self.new_document)
        self.actionOpenImage.triggered.connect(self.open_file)
        self.actionSaveImage.triggered.connect(self.save_file)
        self.actionZoomIn.triggered.connect(self.document_zoom_in)
        self.actionZoomOut.triggered.connect(self.document_zoom_out)
        #self.actionClearImage.triggered.connect(self.canvas.reset)
        #self.actionInvertColors.triggered.connect(self.invert)
        #self.actionFlipHorizontal.triggered.connect(self.flip_horizontal)
        #self.actionFlipVertical.triggered.connect(self.flip_vertical)
        self.documentTabs.tabCloseRequested.connect(self.close_tab)

        '''
        # Setup the drawing toolbar.
        self.fontselect = QFontComboBox()
        self.fontToolbar.addWidget(self.fontselect)
        self.fontselect.setCurrentFont(QFont('Times'))

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])
        self.fontsize.currentTextChanged.connect(lambda f: self.canvas.set_config('fontsize', int(f)))

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontToolbar.addWidget(self.fontsize)

        self.fontToolbar.addAction(self.actionBold)
        self.actionBold.triggered.connect(lambda s: self.canvas.set_config('bold', s))
        self.fontToolbar.addAction(self.actionItalic)
        self.actionItalic.triggered.connect(lambda s: self.canvas.set_config('italic', s))
        self.fontToolbar.addAction(self.actionUnderline)
        self.actionUnderline.triggered.connect(lambda s: self.canvas.set_config('underline', s))
        '''
        
        sizeicon = QLabel()
        sizeicon.setPixmap(QPixmap('icons/border-weight.png'))
        self.drawingToolbar.addWidget(sizeicon)
        self.sizeselect = QSlider()
        self.sizeselect.setRange(1,20)
        self.sizeselect.setOrientation(Qt.Horizontal)
        #self.sizeselect.valueChanged.connect(lambda s: self.config.size=s)
        self.drawingToolbar.addWidget(self.sizeselect)

        #self.actionFillShapes.triggered.connect(lambda s: self.config.fill=s)
        self.drawingToolbar.addAction(self.actionFillShapes)
        self.actionFillShapes.setChecked(True)
        

    def document_zoom_out(self):
        indx = self.documentTabs.currentIndex()
        if indx >=0: self.documents[indx].zoom_out()

    def document_zoom_in(self):
        indx = self.documentTabs.currentIndex()
        if indx >=0: self.documents[indx].zoom_in()

    def set_primary_color(self, hex_color):
        self.config.primary_color = QColor(hex_color)
        self.primaryButton.setStyleSheet('QPushButton { background-color: %s; }' % hex_color)

    def set_secondary_color(self, hex_color):
        self.config.secondary_color = QColor(hex_color)
        self.secondaryButton.setStyleSheet('QPushButton { background-color: %s; }' % hex_color)

    #def set_config(self, key, value):
    #    self.config[key] = value

    def set_mode(self, mode):

        # Clean up active timer animations.
        #self.timer_cleanup()
        # Reset mode-specific vars (all)
        '''
        self.active_shape_fn = None
        self.active_shape_args = ()

        self.origin_pos = None

        self.current_pos = None
        self.last_pos = None

        self.history_pos = None
        self.last_history = []

        self.current_text = ""
        self.last_text = ""

        self.last_config = {}

        self.dash_offset = 0
        self.locked = False
        '''
        # Apply the mode
        self.config.mode = mode
        #self.mode = mode

    def reset_mode(self):
        self.set_mode(self.mode)

    '''
    def timer_cleanup(self):
        if self.config["timer_event"]:
            # Stop the timer, then trigger cleanup.
            timer_event = self.config["timer_event"]
            self.config["timer_event"] = None
            timer_event(final=True)
    '''


    def close_tab(self, index):
        doc_name = self.documentTabs.tabText(index)
        self.documentTabs.removeTab(index)
        del self.documents[index]

    def open_file(self):
        """
        Open image file for editing, scaling the smaller dimension and cropping the remainder.
        :return:
        """
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "PNG image files (*.png); JPEG image files (*jpg); All files (*.*)")

        if path:
            pixmap = QPixmap()
            pixmap.load(path)


            '''
            # Get the size of the space we're filling.
            cw, ch = CANVAS_DIMENSIONS
            if iw/cw < ih/ch:  # The height is relatively bigger than the width.
                pixmap = pixmap.scaledToWidth(cw)
                hoff = (pixmap.height() - ch) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(0, hoff), QPoint(cw, pixmap.height()-hoff))
                )

            elif iw/cw > ih/ch:  # The height is relatively bigger than the width.
                pixmap = pixmap.scaledToHeight(ch)
                woff = (pixmap.width() - cw) // 2
                pixmap = pixmap.copy(
                    QRect(QPoint(woff, 0), QPoint(pixmap.width()-woff, ch))
                )
            '''
            filename = os.path.basename(path)
            self.add_document(pixmap, filename)
            




    def add_document(self, pixmap, name=None):
        if name == None:
            name = "Document "+str(self.new_doc_seq)
            self.new_doc_seq += 1

        # Set new document with pixmap and name
        new_document = Document(name, self.config)
        new_document.canvas.setPixmap(pixmap)
        self.documents.append(new_document)

        # Create gui elements for the new document and add it to the tabs
        scroll = QScrollArea()
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(new_document.canvas)
        widget.setLayout(vbox)
        iw = pixmap.width()
        ih = pixmap.height()
        widget.resize(iw, ih)
        new_document.widget = widget
        scroll.setWidget(widget)
        self.documentTabs.addTab(scroll, name)
        self.documentTabs.setCurrentWidget(scroll)
        new_document.canvas.command_from_canvas.connect(self.process_command_from_canvas)

        # Signals for canvas-initiated color changes (dropper).
        #new_document.canvas.primary_color_updated.connect(self.set_primary_color)
        #new_document.canvas.secondary_color_updated.connect(self.set_secondary_color)
        
        # Font changed
        #self.fontselect.currentFontChanged.connect(lambda f: new_document.canvas.set_config('font', f))

    def process_command_from_canvas(self, params):
        if params["command"] == "create_new_document_from_selection":
            self.add_document(params["selection"])


    def new_document(self):
        cw, ch = CANVAS_DIMENSIONS
        pixmap = QPixmap(cw, ch)
        pixmap.fill( Qt.white )
        self.add_document(pixmap)
        #new_document.canvas.setPixmap(pixmap)
        # Add document to tabs
        #self.documentTabs.addTab(new_document.canvas, new_document.name)


    def choose_color(self, callback):
        dlg = QColorDialog()
        if dlg.exec():
            callback( dlg.selectedColor().name() )
    '''
    def set_primary_color(self, hex_color):
        #for document in self.documents:
        #    document.canvas.set_primary_color(hex_color)
        self.config.primary_color
        self.primaryButton.setStyleSheet('QPushButton { background-color: %s; }' % hex)

    def set_secondary_color(self, hex_color):
        for document in self.documents:
            document.canvas.set_secondary_color(hex_color)
        self.secondaryButton.setStyleSheet('QPushButton { background-color: %s; }' % hex)

    def next_stamp(self):
        self.current_stamp_n += 1
        if self.current_stamp_n >= len(STAMPS):
            self.current_stamp_n = 0

        pixmap = QPixmap(STAMPS[self.current_stamp_n])
        self.stampnextButton.setIcon(QIcon(pixmap))

        self.canvas.current_stamp = pixmap

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()

        if self.canvas.mode == 'selectrect' and self.canvas.locked:
            clipboard.setPixmap(self.canvas.selectrect_copy())

        elif self.canvas.mode == 'selectpoly' and self.canvas.locked:
            clipboard.setPixmap(self.canvas.selectpoly_copy())

        else:
            clipboard.setPixmap(self.canvas.pixmap())
    '''



    def save_file(self, pixmap=None):
        """
        Save active canvas to image file.
        :return:
        """
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "PNG Image file (*.png)")

        if path:
            if pixmap:
                pixmap.save(path, "PNG" )
            else:
                indx = self.documentTabs.currentIndex()
                if indx >=0:
                   pixmap = self.documents[indx].canvas.pixmap()
                   pixmap.save(path, "PNG" )
    '''
    def invert(self):
        img = QImage(self.canvas.pixmap())
        img.invertPixels()
        pixmap = QPixmap()
        pixmap.convertFromImage(img)
        self.canvas.setPixmap(pixmap)

    def flip_horizontal(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(-1, 1)))

    def flip_vertical(self):
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap.transformed(QTransform().scale(1, -1)))
'''

    def keyPressEvent(self, e):
        if e.matches(QKeySequence.Undo):
            indx = self.documentTabs.currentIndex()
            if indx >=0: self.documents[indx].undo()
            #print("undo()")
        elif e.matches(QKeySequence.Redo):
            indx = self.documentTabs.currentIndex()
            if indx >=0: self.documents[indx].redo()
            #print("redo()")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    #app.setWindowIcon(QtGui.QIcon('icons/piecasso.ico'))
    window = MainWindow()
    app.exec()