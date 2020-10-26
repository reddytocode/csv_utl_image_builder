import pandas as pd
import cv2

def remove_special_characters(s: str) -> str:
    s = ''.join(c.lower() for c in s if c.isalnum() or c == ' ')
    return s.replace(' ', '-').replace("ñ", "n")


if __name__ == '__main__':
    csv_file_path = "productos_unimercas_url.csv"
    res = pd.DataFrame()
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    data = pd.read_csv(csv_file_path)
    for index, row in data.iterrows():
        import urllib.request

        try:
            image_name = "{}_{}_{}.jpg".format(remove_special_characters(row['Nombre']), row['ID_PRODUCTO'], row['ID'])
            image_path = "images/{}".format(image_name)
            urllib.request.urlretrieve(row["URL FOTO"], image_path)

            cv_image = cv2.imread(image_path)
            cv2.imwrite(image_path, cv_image)

            row['Foto 1'] = image_name
        except Exception as e:
            row['Foto 1'] = "No image"
        res = res.append(row, ignore_index=True)
        # print(row['ID_PRODUCTO'], row['ID'], row['Nombre'],row['Descripcion'],row['% Impuesto'],row['Atributos'],row['Sabor'],
        #       row['Foto 1'], row['Foto 2'], row['Foto 3'])
    res.to_csv("processed_{}".format(csv_file_path))
