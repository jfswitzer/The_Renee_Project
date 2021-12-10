from PIL import Image
im = Image.open(r"input.jpg")
width, height = im.size
newsize = (4 * width, 6 * height)
im2 = im.resize(newsize)
im2.save("resized.jpg")
