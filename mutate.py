from PIL import Image

img = Image.open("Kiriko.png")
img.putpixel((10, 10), (255, 0, 0))
img.save("Kiriko.png")