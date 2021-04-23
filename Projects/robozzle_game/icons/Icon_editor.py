from PIL import Image, ImageOps, ImageDraw
import PIL
img = Image.open("0_162_232_arrow_w.png")
imga = img.convert("RGBA")
datas = imga.getdata()
newData = list()
img=img.resize((20, 20), PIL.Image.ANTIALIAS)
img.save("0_162_232_arrow_w.png", "PNG")
