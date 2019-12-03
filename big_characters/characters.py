import cv2
import PIL.ImageOps 
from PIL import Image, ImageFont, ImageDraw

fontsize = 38
# use a truetype font
font = ImageFont.truetype("Consolas.ttf", fontsize )
im = Image.new("RGBA", (fontsize, fontsize))
draw = ImageDraw.Draw(im)

#Gets the biggest h and w
max_h = 0
max_w = 0
for code in range(32,127):
  w, h = draw.textsize(chr(code), font=font)
  if h > max_h:
  	max_h = h
  if w > max_w:
  	max_w = w

for code in range(32,127):
  w, h = draw.textsize(chr(code), font=font)
  im = Image.new("L", (max_w, max_h),"#ffffff")

  draw = ImageDraw.Draw(im)
  draw.text((max_w-w,max_h-h -1), chr(code), font=font, fill="#000000")
  
  im.save(str(code) + ".png")

	