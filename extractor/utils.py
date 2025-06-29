from PySide2.QtGui import QImage, QPixmap
import numpy as np

from core import Layout, GraphicObject
from Database import select_object_by_id, select_asset_by_id

def RGBToHex(rgbcolor):
    return '#'+"".join(map(lambda x: str(hex(x))[2:], rgbcolor))
    
def HexToRGB(hexcolor):
    return [int(hexcolor[1:3], 16), int(hexcolor[3:5], 16), int(hexcolor[5:7], 16)]

# QPixmap to np array
def QPixmap_to_nparray(pixmap):
    channels_count = 4
    image = pixmap.toImage()
    width, height = image.width(), image.height()
    b = image.bits()
    return np.frombuffer(b, np.uint8).reshape((height, width, channels_count))[:,:,:3]
    
# np array to QPixmap
def nparray_to_QPixmap(cvImg):
    print(cvImg.shape)
    _height, _width, channel = cvImg.shape
    bytesPerLine = 3 * _width
    qImg = QImage(cvImg.data, _width, _height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

def loadLayoutFromId(assetid):
    def loadLayoutFromJson(json):
        pobj = Layout.parse(json)

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
    print(assetid)
    asset = select_asset_by_id(assetid)
    return loadLayoutFromJson(asset["content"])