from tkinter import *
from tkinter import ttk, font, filedialog as fd
from tkmacosx import Button
from tkinterdnd2 import DND_FILES, TkinterDnD
import PIL
from PIL import Image
import filetype
from file_n_api import cutter, kw_arr
from gif_player import GifPlay
import io

f = None

mw = TkinterDnD.Tk()
mw.geometry('400x500')
mw.resizable(False, False)
mw.configure(background='black')
mw.title('Everypixel keywording API')

fnt_big = ('Inter', 36)
fnt_sml = ('Inter', 32)

def mainPage():
    for i in mw.winfo_children():
        i.destroy()
    mw.geometry('400x500')
    f = None
    Label(mw, text='Everypixel API', font=fnt_big, fg='#3EC96D', bg='black').place(x=85, y=39)
    Button(mw, text='TRY', command=convertPage, font=fnt_big, fg='#3EC96D', bg='black').place(width=300, height=85, x=50, y=140)
    Button(mw, text='OPTIONS', command=optionsPage, font=fnt_big, fg='#3EC96D', bg='black').place(width=300, height=85, x=50, y=271)
    Button(mw, text='QUIT', command=mw.destroy, font=fnt_sml, fg='#3EC96D', bg='black').place(width=250, height=60, x=75, y=402)

def optionsPage():
    for i in mw.winfo_children():
        i.destroy()
    Label(mw, text='Options', font=fnt_big, fg='#3EC96D', bg='black').place(x=135, y=39)
    Button(mw, text='BACK', command=mainPage, font=fnt_sml, fg='#3EC96D', bg='black').place(width=250, height=60, x=75, y=402)

def convertPage():
    for i in mw.winfo_children():
        i.destroy()    
    global file_lbl
    file_lbl = GifPlay(mw)
    file_lbl.load('media/ukral.gif')
    file_lbl.drop_target_register(DND_FILES)
    file_lbl.dnd_bind('<<Drop>>', lambda e: prep(e.data))
    file_lbl.place(x=65, y=25, width=270, height=270)
    Button(mw, text='CHOOSE FILE', command=file_job, font=('Inter', 28), fg='#3EC96D', bg='black').place(width=250, height=60, x=75, y=314)
    Button(mw, text='BACK', command=mainPage, font=fnt_sml, fg='#3EC96D', bg='black').place(width=250, height=60, x=75, y=402)

def changes():
    mw.geometry('400x700')
    kwlist = Listbox(mw, bg='black', fg='#3EC96D', font=('Inter'))
    scrollbar = Scrollbar(mw, orient='vertical', bg='black', command=kwlist.yview)
    scrollbar.place(x=384, y=500, height=199)
    kwlist.config(yscrollcommand=scrollbar.set)
    kwlist.place(x=0, y=500, width=400, height=199)

    kwords_only = []
    count = 1
    cutter(fl)
    
    for id in range(len(kw_arr)):
        for j in kw_arr[id]['keywords']:
            kwords_only.append(j['keyword'])

    for i in set(kwords_only):
        kwlist.insert(END, str(count) + '. ' + i)
        count += 1

def prep(file):
    global f,fl
    f = file
    if isinstance(f, io.TextIOWrapper):
        fl = f.name
    else:
        fl = f

    if filetype.is_image(fl):
        img = Image.open(fl)
        img.resize((270, 270), PIL.Image.ANTIALIAS)
        file_lbl.load(img)
        changes()
    else:
        print('Kartinku nado')

def file_job():
    global f
    if f == None:
        f = fd.askopenfile(
            title='Choose an image you want to keyword',
            filetypes=[('image files', ('.png', '.jpg', '.jpeg'))]
        )
        if f:
            prep(f)
        else:
            print('Nado fail')
    else:
        prep(f)

mainPage()
mw.mainloop()
 