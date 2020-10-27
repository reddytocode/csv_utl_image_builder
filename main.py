import pandas as pd
import os
from PIL import Image
import numpy as np
import cv2


def correct_image(img_path):
    img = Image.open(img_path)
    img.load()
    try:
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        background.save(img_path, 'JPEG', quality=100)
    except Exception as e:
        print("error", e)


def remove_special_characters(s: str) -> str:
    s = ''.join(c.lower() for c in s if c.isalnum() or c == ' ')
    return s.replace(' ', '').replace("ñ", "n")


if __name__ == '__main__':
    unsaved_images = []
    csv_file_path = "productos_unimercas_v2.csv"
    res = pd.DataFrame()
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    data = pd.read_csv(csv_file_path)
    for index, row in data.iterrows():
        import urllib.request
        if len(str(row["URL FOTO"])) > 0:
            try:
                image_name = "{}_{}.png".format(row['ID_PRODUCTO'], row['ID'])
                image_path = "filtered/{}".format(image_name)
                urllib.request.urlretrieve(row["URL FOTO"], image_path)

                correct_image(image_path)
                row['Foto 1'] = image_name
                print(image_name)

            except Exception as e:
                unsaved_images.append([index, image_path])
                row['Foto 1'] = "Error"

            filtered_image = cv2.imread(image_path)
            if filtered_image is None:
                unsaved_images.append([index, image_path])
                print(image_path, " has an error  with url")
                row['Foto 1'] = 'Error con imagen y url'
            else:
                image_path_filtered = "images/{}".format(image_name)
                cv2.imwrite(image_path_filtered, filtered_image)
                row['Foto 1'] = image_path_filtered

        res = res.append(row, ignore_index=True)
        # print(row['ID_PRODUCTO'], row['ID'], row['Nombre'],row['Descripcion'],row['% Impuesto'],row['Atributos'],row['Sabor'],
        #       row['Foto 1'], row['Foto 2'], row['Foto 3'])
    res.to_csv("processed_{}".format(csv_file_path))

    print(unsaved_images)
    a_file = open("test.txt", "w")
    for row in unsaved_images:
        a_file.write("{} | \"{}\"\n".format(row[0], row[1]))

    a_file.close()
