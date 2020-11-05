import os
import shutil
from fpdf import FPDF
import tkinter as tk
from PIL import Image, ImageTk



# Nazwa katalogu
directory = input("Nazwa operatu: ")
# Miejsce docelowe zapisu wszystkich skanów
allScans = "/Users/pawel/Desktop/wszystkieSkany/"
# Folder skany1 lub skany2
source = "/Users/pawel/Desktop/skany1"
# Path
path = os.path.join(allScans, directory)

# Stworzenie katalogu
os.mkdir(path)
print("Operat '% s' utworzony!" % directory)


# Przeniesienie plików
destination = path
files = os.listdir(source)

for file in files:
    new_path = shutil.move(f"{source}/{file}", destination)
print("Skopiowano wszystkie skany!")



# Zmiana nazwy plików
i = 0
for file in os.listdir(path):
    root = tk.Tk()
    root.geometry("+100+100")
    root.title("Okno")
    image = Image.open(path + "/" + file)
    image = image.resize((400, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)
    kod = input("Podaj kod: ")
    root.after(300, lambda: root.destroy())
    root.mainloop()
    os.rename(path + "/" + file,path + "/" + directory + "_{0:03}_".format(i) + kod + '.jpg')
    i+=1
print("Zmieniono nazwy skanów!")



# Tworzenie pliku PDF
pdf = FPDF()
imagelist = []
folder = path + "/"
name = directory + ".pdf"


# Dodanie zdjęć do listy
for dirpath, dirnames, filenames in os.walk(folder):
    for filename in [f for f in filenames if f.endswith(".jpg")]:
        full_path = os.path.join(dirpath, filename)
        imagelist.append(full_path)

# Sortowanie
imagelist.sort()
for i in range(0, len(imagelist)):
    lista = imagelist[i]

# Obrócenie zdjęcia
for i in range(0, len(imagelist)):
    im1 = Image.open(imagelist[i])
    width, height = im1.size
    if width > height:
        im2 = im1.transpose(Image.ROTATE_270)
        os.remove(imagelist[i])
        im2.save(imagelist[i])


# Konwersja do PDF
for image in imagelist:
    x = Image.open(os.path.join(path, image))
    width, height = x.size
    width, height = float(width * 0.264583), float(height * 0.264583)
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
    orientation = 'P' if width < height else 'L'
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
    pdf.add_page(orientation=orientation)
    pdf.image(image, 0, 0, width, height)

# Zapis pdf
pdf.output(folder + name, "F")

print("PDF wygnererowano!")


