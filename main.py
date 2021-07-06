from tkinter import *
from tkinter.filedialog import askopenfile
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import time
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageTk

ws = Tk()
ws.title('Watermarking App')

ws['bg'] = 'gray22'

style = ttk.Style()
style.configure('BW.TLabel', background='gray22', foreground='white', font=('Sans', '12', 'normal'))
boldstyle = ttk.Style()
boldstyle.configure('Bold.TLabel', background='gray22', foreground='white', font=('Sans', '20', 'bold'))
error = ttk.Style()
error.configure('TLabel', background='gray22', foreground='red', font=('Sans', '12', 'normal'))

name_image = ''
name_watermark_image = ''
watermark_text = ''


def scale_image(input_image, output_image, width=None, height=None):
    original_image = Image.open(input_image)
    w, h = original_image.size
    if width and height:
        max_size = (width, height)
    elif width:
        max_size = (width, h)
    elif height:
        max_size = (w, height)
    else:
        raise RuntimeError('Width or height required!')
    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image)


def open_file(file):
    global name_image, name_watermark_image
    filepath = askopenfile(mode='r', filetypes=[('Image Files', '*png')])
    if file == 'image':
        shutil.copy(filepath.name, os.path.abspath('upload image'))
        name_image = filepath.name.split('/')[-1]
    elif file == 'watermark_image':
        shutil.copy(filepath.name, os.path.abspath('upload watermark'))
        name_watermark_image = filepath.name.split('/')[-1]
        scale_image(os.path.abspath('upload watermark') + f'\\{name_watermark_image}',
                    os.path.abspath('upload watermark') + f'\\{name_watermark_image}', 40)


def watermarking_text(input_image, text):
    photo = Image.open(input_image).convert()
    txt = Image.new('RGBA', photo.size, (255, 255, 255, 0))
    drawing = ImageDraw.Draw(txt)
    font = ImageFont.truetype("arial.ttf", 25)
    drawing.text((50, 50), text, fill=(0, 0, 0, 50), font=font)
    combined = Image.alpha_composite(photo, txt)
    combined.save(os.path.abspath('results' + f'\\{name_image}'))


def watermarking_photo(input_image, watermark_image):
    base_image = Image.open(input_image)
    watermark = Image.open(watermark_image)
    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (50, 50), mask=watermark)
    transparent.save(os.path.abspath('results' + f'\\{name_image}'))


def ent_text():
    global watermark_text
    watermark_text = entry.get()


def errors(text):
    mb.showwarning('Warning', text)


def callback(selection):
    if selection == 'Image':
        entry.grid_forget()
        b_ok.grid_forget()
        label_s.grid(row=3, column=0)
        c_f.grid(row=3, column=1, pady=10)
    elif selection == 'Text':
        label_s.grid_forget()
        c_f.grid_forget()
        entry.grid(row=3, column=0)
        b_ok.grid(row=3, column=1, pady=10)


def upload_file():
    global error
    pb = ttk.Progressbar(ws, orient=HORIZONTAL, length=200, mode='determinate')
    pb.grid(row=5, pady=20, columnspan=3)
    for i in range(5):
        ws.update_idletasks()
        pb['value'] += 20
        time.sleep(1)
    pb.destroy()
    if name_image == '':
        errors('Please choose image!')
    elif name_watermark_image == '' and clicked.get() == 'Image':
        errors('Please сhoose a image for your watermark!')
    elif watermark_text == '' and clicked.get() == 'Text':
        errors('Please enter text for the watermark!')
    else:
        if clicked.get() == 'Text':
            watermarking_text(os.path.abspath('upload image') + f'\\{name_image}', watermark_text)
        else:
            watermarking_photo(os.path.abspath('upload image') + f'\\{name_image}',
                               os.path.abspath('upload watermark') + f'\\{name_watermark_image}')
            os.remove(os.path.abspath('upload watermark') + f'\\{name_watermark_image}')
        scale_image(os.path.abspath('results') + f'\\{name_image}',
                    os.path.abspath('rescale_results') + f'\\{name_image}', 400)
        img = ImageTk.PhotoImage(Image.open(os.path.abspath('rescale_results') + f'\\{name_image}'))
        label = Label(ws, image=img)
        label.image = img
        label.grid(row=6, column=0)
        os.remove(os.path.abspath('rescale_results') + f'\\{name_image}')
        os.remove(os.path.abspath('upload image') + f'\\{name_image}')


label_s = ttk.Label(ws, text='Photo of watermark: ', style='BW.TLabel')
c_f = Button(ws, text='Choose File', command=lambda: open_file('watermark_image'))
entry = Entry(ws, text='Enter Text')
b_ok = Button(ws, text='Done', command=lambda: ent_text())

name_title = ttk.Label(ws, text='Image Watermarking App', style='Bold.TLabel').grid(row=0, column=0)
image_label = ttk.Label(ws, text='Photo for watermark: ', style='BW.TLabel')
image_label.grid(row=1, column=0)
button = Button(ws, text='Choose File', command=lambda: open_file('image'))
button.grid(row=1, column=1, pady=10)
watermark_label = ttk.Label(ws, text='What kind of watermark: ', style='BW.TLabel')
watermark_label.grid(row=2, column=0)
options = ['', 'Image', 'Text']
clicked = StringVar()
clicked.set(options[0])
select = ttk.OptionMenu(ws, clicked, *options, command=callback)
select.grid(row=2, column=1)
upload = Button(ws, text='Upload', command=lambda: upload_file()).grid(row=4, column=0, pady=10)

ws.mainloop()
