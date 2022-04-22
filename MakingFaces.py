#!/usr/bin/env python
from pms5003 import PMS5003

# Configure the PMS5003 for Enviro+
pms5003 = PMS5003(
    device='/dev/ttyAMA0',
    baudrate=9600,
    pin_enable=22,
    pin_reset=27
)

"""Animation"""
import os
import math
import time

import board
import adafruit_dotstar as dotstar

from PIL import (
    Image,
    ImageFont,
    ImageDraw,
    ImageSequence
)


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
FONT_PATH = os.path.join(FILE_PATH, 'font.ttf')

demo=1

class DotaView:
    def __init__(self, dots=64):
        self.dots = dotstar.DotStar(
            board.SCK,
            board.MOSI,
            dots,
            brightness=0.1 
#             brightness=0.4 
        )
        self.n_dots = dots

        self.real_width = int(math.sqrt(dots))
        self.width = self.real_width
        self.height = self.real_width
        self.size = (self.width, self.height)
        self.frames = []
        self.duration = []

        with Image.new('RGB', self.size, color=(0, 0, 0)) as img:
            self.loadPixels(img.load(), self.size)

    def setSize(self, width, height):
        self.width = width
        self.height = min(self.height, height)
        self.size = (self.width, self.height)

    def loadPixels(self, image, size):
        """ Load Gamma Corrected Pixels """
        self.setSize(size[0], size[1])
        self.pixels = []
        for x in range(self.width):
            w_pix = []
            for y in range(self.height):
                w_pix.append(image[x, y])
            self.pixels.append(w_pix)

    def loadImage(self, path):
        """ Load Image from Path """
        with Image.open(path).convert("RGB") as img:
            image = img.load()
            self.loadPixels(image, img.size)

    def loadText(self, text, red, green, blue):
        """ Convert Text to 8x8 Image and Load """
        long = len(text) * 9 + (2 * self.real_width)
        with Image.new('RGB', (long, 8), color=(0, 0, 0)) as img:
            font = ImageFont.truetype(FONT_PATH, 8)
            d = ImageDraw.Draw(img)
            d.text((self.real_width, 0), text, fill=(red, green, blue), font=font)
            self.loadPixels(img.load(), img.size)

    def show_image(self, image):
        image = image[:self.real_width]
        index = 0
        for x in range(self.real_width):
            for y in range(self.real_width):
                self.dots[index] = image[x][y]
                index += 1
        self.dots.show()
        # time.sleep(0.005)

    def loadGif(self, path):
        with Image.open(path) as img:
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        self.frames = []
        self.duration = []
        for frame in frames:
            frame = frame.convert("RGB")
            self.loadPixels(frame.load(), frame.size)
            self.frames.append(self.pixels)
            self.duration.append(frame.info['duration']/1000)

    def playAnimation(self):
        """ Play Loaded Gif Animation """
        for index, img in enumerate(self.frames):
            self.show_image(img)
            time.sleep(self.duration[index])

    def show(self):
        """ Draw Loaded Image """
        self.show_image(self.pixels)

    def play(self, delay=0.005):
        """ Scroll Image or Text """
        for i in range(self.width):
            end = i + self.real_width
            if end > self.width - 1:
                end = self.width - 1
            chunk = self.pixels[i:i+self.real_width]
            if len(chunk) < self.real_width:
                chunk += [[(0, 0, 0, 0.0)] * self.height] * \
                    (self.real_width - len(chunk))
            self.show_image(chunk)
            time.sleep(delay)
        self.clear()

    def clear(self):
        """ Clear DotaStar """
        self.dots.fill(0)


try:
    while True:
        data = pms5003.read()
        Data1 = data.pm_ug_per_m3(1.0)
        print("Data1:", data.pm_ug_per_m3(1.0))
        Data2 = data.pm_ug_per_m3(2.5)
        print("Data2.5:", data.pm_ug_per_m3(2.5))
        Data3 = data.pm_ug_per_m3(10)
        print("Data10:", data.pm_ug_per_m3(10))
        print()
        
        if __name__ == "__main__":
            dot = DotaView()
            Animation1 = "CrossAnim.gif"
            Text1 = "MEH"
            Text2 = "BAD"
            Text3 = "BAAAD"
            Text4 = "BAAAAAAD"
            
# Number of demos at start
            while(demo<=2):
                dot.loadGif(Animation1)
                dot.loadText('DEMO DEMO DEMO   ', 0, 255, 50)           
                dot.play()
                dot.playAnimation()            

                dot.loadGif(Animation1)
                dot.loadText(Text1, 50, 50, 50)           
                dot.play()
                dot.playAnimation()
                
                dot.loadGif(Animation1)
                dot.loadText(Text2, 255, 255, 255)
                dot.play()
                dot.playAnimation()
                
                dot.loadGif(Animation1)
                dot.loadText(Text3, 255, 0, 0)           
                dot.play()
                dot.playAnimation()
                
                dot.loadGif(Animation1)
                dot.loadText(Text4, 255, 0, 0)
                dot.play()
                dot.playAnimation()                
                
                demo=demo+1
            
            else: 

                time.sleep(0.1)
                
                if  0 < Data2 < 100:
                     pass
                elif 101 < Data2 < 250:
                    dot.loadGif(Animation1)
                    dot.loadText(Text1, 50, 50, 50)           
                    dot.play()
                    dot.playAnimation()
                elif 251 < Data2 < 350:
                    dot.loadGif(Animation1)
                    dot.loadText(Text2, 255, 255, 255)
                    dot.play()
                    dot.playAnimation()
                elif 351 < Data2 < 430:
                    dot.play()
                    dot.playAnimation()
                elif 431 < Data2 < 550:
                    dot.loadGif(Animation1)
                    dot.loadText(Text4, 255, 0, 0)
                    dot.play()
                    dot.playAnimation() 
                
                time.sleep(0.0)
                
                if 0 < Data3 < 60:
                    pass
                elif 61 < Data3 < 90:
                    dot.loadGif(Animation1)
                    dot.loadText(Text1, 50, 50, 50)           
                    dot.play()
                    dot.playAnimation()
                elif 91 < Data3 < 120:
                    dot.loadGif(Animation1)
                    dot.loadText(Text2, 255, 255, 255)
                    dot.play()
                    dot.playAnimation()
                elif 121 < Data3 < 250:
                    dot.loadGif(Animation1)
                    dot.loadText(Text3, 255, 0, 0)           
                    dot.play()
                    dot.playAnimation()
                elif 251 < Data3< 350:
                    dot.loadGif(Animation1)
                    dot.loadText(Text4, 255, 0, 0)
                    dot.play()
                    dot.playAnimation() 
                
                time.sleep(0.0)
        
except KeyboardInterrupt:
    pass