import urllib.request
import os
import cv2
from PIL import Image

def correct_image(img_path):
    img = Image.open(img_path)
    img.load()

    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])

    background.save('foo.jpg', 'JPEG', quality=100)

url = "https://images.rappi.com/products/494072-1559235067.png?d=500x500&e=webp"
path = "hola.png"
print(urllib.request.urlretrieve(url, path))
correct_image(path)
os.path.exists("hola.jpg")
