from tkinter import *
from PIL import Image, ImageTk

root = Tk()

# Open an image file
image = Image.open("test1.png")
image = image.resize((1080, 720), Image.ANTIALIAS)
# Create a PhotoImage object
photo_image = ImageTk.PhotoImage(image)

# Create a label and set the image as its background
label = Label(root, image=photo_image)
label.pack()

root.mainloop()