

class Collection:
     def __init__(self, name):
         self.name = name

class Surface:
     def __init__(self, name, color):
         self.name = name
         self.color = color

class Vector:
     def __init__(self, name, points):
         self.name = name
         self.points = points
         self.visible = True