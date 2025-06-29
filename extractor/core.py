

class AssetTemplate:
    def __init__(self):
        self.layout = None
        self.content = []


class Asset:
    def __init__(self):
        self.layout = None
        self.content = []

class Layout:
    def __init__(self, x, y, w, h, content):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.content = content

    def json(self):
        content_str = None
        if type(self.content) == list:
            content = []
            for c in self.content:
                content.append(c.json())
            content_str = "["+(",".join(content))+"]"
        else:
            content_str = str(self.content.rowid)
        return '{"x":'+str(self.x)+', "y":'+str(self.x)+', "w":'+str(self.w)+', "h":'+str(self.h)+', "content": '+content_str+'}'
    
    def svg(self):
        content = '<svg width="'+str(self.w)+'" height="'+str(self.h)+'" xmlns="http://www.w3.org/2000/svg">\n'
        paths = self.as_svg_paths()
        for path in paths:
            content += path+"\n"
        return content+"<\svg>"

    def as_svg_paths(self):
        resp = []
        if type(self.content) != list:
            paths = self.content.as_svg_paths()
            resp.extend(paths)
        else:
            for obj in self.content:
                paths = obj.as_svg_paths()
                resp.extend(paths)
        return resp

    @staticmethod
    def parse(json):
        return Layout(json["x"], json["y"], json["w"], json["h"], json["content"])
 
class Collection:
     def __init__(self, name):
         self.name = name

class GraphicObject:
    def __init__(self, name, rowid, surfaces):
        self.name = name
        self.surfaces = surfaces

        self.minx = None
        self.miny = None
        self.maxx = None
        self.maxy = None

        #extra features for UI
        self.visible = True
        self.rowid = rowid
 
    @staticmethod
    def parse(json):
        return GraphicObject(json['name'], json['rowid'], Surface.parse(json['content']))

    def calculateBoundaries(self):
        self.minx, self.miny, self.maxx, self.maxy = float('inf'),float('inf'), float('-inf'), float('-inf')
        def calculateBundariesPointSequence(pointSequence):
            for point in pointSequence.points:
                if point.x < self.minx: self.minx = point.x
                if point.y < self.miny: self.miny = point.y
                if point.x > self.maxx: self.maxx = point.x
                if point.y > self.maxy: self.maxy = point.y

        for surface in self.surfaces:
            calculateBundariesPointSequence(surface.outer)
            for hole in surface.holes:
                calculateBundariesPointSequence(hole)

    def getMinX(self):
        if self.minx == None: self.calculateBoundaries()
        return self.minx

    def getMinY(self):
        if self.miny == None: self.calculateBoundaries()
        return self.miny

    def getMaxX(self):
        if self.maxx == None: self.calculateBoundaries()
        return self.maxx

    def getMaxY(self):
        if self.maxy == None: self.calculateBoundaries()
        return self.maxy

    def getWidth(self):
        if self.minx == None or self.maxx == None: self.calculateBoundaries()
        return self.maxx - self.minx

    def getHeight(self):
        if self.miny == None or self.maxy == None: self.calculateBoundaries()
        return self.maxy - self.miny

    def as_svg_paths(self):
        resp = []
        for surface in self.surfaces:
            resp.append(surface.as_svg_path())
        return resp

class Surface:
    def __init__(self, name, outer, holes=[], color=None):
        self.name = name
        self.color = color
        self.outer = outer
        self.holes = holes

        #extra features for UI
        self.visible = True

    @staticmethod
    def parse(json):
        result = []
        for s in json:
            result.append(Surface(s['name'], PointSequence.parse(s['outer']), [PointSequence.parse(hole) for hole in s['holes']]))
        return result
    
    def as_svg_path(self):
        return '<path d="'+self.outer.as_svg_path()+'"/>'

class PointSequence:
    def __init__(self, points=[]):
        self.points = points
        self.isClosed = True
        #extra features for UI
        self.visible = True

    @staticmethod
    def parse(json):
        return PointSequence([Point(p[0], p[1]) for p in json])

    def as_svg_path(self, rev=False):
        temp = self.points
        if rev: temp.reverse()
        p = temp[0]
        resp = "M "+str(p.x)+" "+str(p.y)
        for p in temp[1:]:
            resp = resp+" L "+str(p.x)+" "+str(p.y)
        return resp + " Z"

    
class Point:
     def __init__(self, x, y):
         self.x = x
         self.y = y

         #extra features for UI
         self.visible = True
         self.selected = False
     def xy(self):
         return (self.y, self.x)