from PIL import Image,ImageDraw,ImageFont
import random
import io
class code:
    def __init__(self):
        self.width=120
        self.height=50
        self.im=None
        self.lineNum=0
        self.pointNum=0
        self.codecon='abcdefjhmnkABCDEFGHKUYZS2345678'
        self.codelen=4
        self.fontsize=35
        self.arr=''
        self.bg=0
    def randombg(self):
        self.bg = (random.randint(0,120),random.randint(0,120),random.randint(0,120),255)
        return self.bg
        # return (random.randint(0,120),random.randint(0,120),random.randint(0,120),255)
    def randomfg(self):
        return (random.randint(120,255),random.randint(120,255),random.randint(120,255),255)
    def create(self):
        self.bg = self.randombg()
        self.im=Image.new("RGBA",(self.width,self.height),color=self.bg)
    def lines(self):
        lineNum=self.lineNum or random.randint(4,10)
        draw = ImageDraw.Draw(self.im)
        for item in range(lineNum):
            place = (random.randint(0,self.width),random.randint(0,self.height),random.randint(0,self.width),random.randint(0,self.height))
            draw.line(place,fill=self.randomfg(),width=random.randint(1,2))
    def points(self):
        pointNum = self.lineNum or random.randint(30, 60)
        draw = ImageDraw.Draw(self.im)
        for item in range(pointNum):
            place = (random.randint(0, self.width), random.randint(0, self.height))
            draw.point(place, fill=self.randomfg())
    def texts(self):
        arr = ''
        draw = ImageDraw.Draw(self.im)
        for item in range(self.codelen):
            letter=self.codecon[random.randint(0,len(self.codecon)-1)]
            x = item*(self.width/self.codelen)+random.randint(-10,10)
            y = random.randint(-10,10)
            draw.text((x,y),letter,fill=self.randomfg(),font=ImageFont.truetype("C:\WINDOWS\Fonts\SITKA.TTC",self.fontsize))
            arr = arr+letter
        self.rotate()
        self.arr=arr
    def rotate(self):
        self.im = self.im.rotate(random.randint(-10,10))
        im1 = Image.new("RGBA",(self.width,self.height),color=self.bg)
        self.im = Image.composite(self.im,im1,self.im)
    def output(self):
        self.create()
        self.texts()
        self.lines()
        self.points()
        bt = io.BytesIO()
        self.im.save(bt,'png')
        return bt.getvalue()
