
import PIL.ImageOps 
from PIL import Image, ImageFont, ImageDraw







fontsize = 72

# use a truetype font
font = ImageFont.truetype("Consolas.ttf", fontsize )
im = Image.new("RGBA", (fontsize, fontsize))
draw = ImageDraw.Draw(im)

for code in range(33,127):
  w, h = draw.textsize(chr(code), font=font)
  im = Image.new("RGBA", (70, 70))
  draw = ImageDraw.Draw(im)
  draw.text((15,0), chr(code), font=font, fill="#000000")
  im.save(str(code) + ".png")