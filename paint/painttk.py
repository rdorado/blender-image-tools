from tkinter import *
from tkinter.colorchooser import askcolor
from ttkwidgets import CheckboxTreeview
from tkinter import filedialog
from PIL import Image

import pickle
import os

class Paint(object):

    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    my_filetypes = [('dat files', '.dat')]
    data = {}
    
    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        self.brush_button.grid(row=0, column=1)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.tree = CheckboxTreeview(self.root, columns=[])
        self.tree.im_checked.paste(Image.open('non-visible.jpg'))
        self.tree.im_unchecked.paste(Image.open('visible.jpg'))
        self.tree.im_tristate.paste(Image.open('tristate.jpg'))
        self.tree.grid(row=1, column=5)
        
        self.tree.heading('#0', text='Objects', anchor='w')
        
        #self.tree.insert("", "end", "1", text="1")
        #self.tree.insert("1", "end", "11", text="11")
        #self.tree.insert("1", "end", "12",  text="12", values=['2 bytes'])
        #self.tree.insert("11", "end", "111", text="111", values=['100 bytes'])
        #self.tree.insert("", "end", "2", text="2", values=['20 bytes'])

        self.c = Canvas(self.root, bg='white', borderwidth=0, highlightthickness=0, width=600, height=600)
        self.c.grid(row=1, columnspan=5)
        
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Add Objects", command=self.add_dat)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        self.root.config(menu=self.menubar)

        self.setup()
        self.root.mainloop()


    def add_dat(self):
        answer = filedialog.askopenfilename(parent=self.root,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=self.my_filetypes)
        if answer != "":
            with (open(answer, "rb")) as openfile:
                data = pickle.load(openfile)
            colname = os.path.basename(answer)[:-4]
            self.tree.insert("", "end", colname, text=colname)
            #self.update_canvas(data)
            i=1
            for (surface, color) in data:
                self.tree.insert(colname, "end", colname+"_"+str(i), text=str(i))
                j=1
                for vector in surface:
                    idv = colname+"_"+str(i)+"_"+str(j)
                    obj = self.tree.insert(colname+"_"+str(i), "end", idv, text=str(j), tags=[idv])
                    self.tree.tag_bind(idv, '<ButtonPress-1>', self.itemClicked)
                    self.add_to_canvas(idv, vector, color)
                    j+=1
                i+=1

    def itemClicked(self, event):
       print(self)
       print(dir(event))
       print(event.widget.find_closest(event.x, event.y))


    def add_to_canvas(self, idv, vector, color):
        self.data[idv] = (vector, color, True)
        ppoint = vector[0]
        for point in vector[1:]:
            (x1, y1) = ppoint
            (x2, y2) = point
            hexcol = '#'+"".join(map(lambda x: str(hex(x))[2:],color))
            print(hexcol)
            self.c.create_line(x1, y1, x2, y2, fill=hexcol, width=1)
            #print(x1, y1, x2, y2)
            ppoint = point
    
    def donothing():
        filewin = Toplevel(root)
        button = Button(filewin, text="Do nothing button")
        button.pack()


    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]
        
        print(self.color[0],int(self.color[1:3],16),int(self.color[3:5],16),int(self.color[5:7],16))


    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    Paint()