# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os
from tkinter.ttk import Spinbox

import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import pandas as pd
from os import path
from PIL import ImageTk, Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib
import matplotlib.pyplot as plt
import re

import tkinter as tk
# from tkinter import *
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from tkinter import colorchooser
from tkinter import messagebox


def printing(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f', {name}')  # Press ⌘F8 to toggle the breakpoint.


def dataCleaning(textToProcess):
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"

    text = " " + textToProcess + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    sentences = pd.DataFrame(sentences)
    sentences.columns = ['sentence']

    # convert sentence data to list
    data = sentences['sentence'].values.tolist()
    # type(data)
    # print(len(data))
    return data


# Text cleaning and tokenization using function
def textCleaning(texts, stoplist):
    # Remove numbers and alphanumerical words we don't need
    texts = [re.sub("[^a-zA-Z]+", " ", str(text)) for text in texts]
    # print('after Remove numbers and alphanumerical words we donot need')
    # print(texts)

    # Tokenize & lowercase each word
    texts = [[word for word in text.lower().split()] for text in texts]
    # print('after Tokenize & lowercase each word')
    # print(texts)

    # Stem each word
    lmtzr = WordNetLemmatizer()
    texts = [[lmtzr.lemmatize(word) for word in text] for text in texts]
    # print('after Stem each word')
    # print(texts)

    # Remove stopwords
    texts = [[word for word in text if word not in stoplist] for text in texts]
    # print('after Remove stopwords')
    # print(texts)

    # Remove short words less than 3 letters in length
    texts = [[word for word in tokens if len(word) >= 3] for tokens in texts]
    # print('after Remove short words less than 3 letters in length')
    # type(texts)

    return texts


# Analyze word frequency
def analyze_word_frequency(text_to_process, most_common):
    freq_dist = nltk.FreqDist()

    for word in word_tokenize(text_to_process):
        freq_dist[word.lower()] += 1

    common_words = freq_dist.most_common(most_common)
    for freq in common_words:
        print(freq)

    return common_words
    # plt.figure(figsize=(12, 6))
    # freq_dist.plot(50)
    # plt.show()


def perform_WordCloud(text_to_process, stop_words, max_wordsss, image_file_name, background_color, heightt, widthh):
    cleaned_Data = dataCleaning(text_to_process)
    # print(cleaned_Data)

    stoplist = stopwords.words('english')
    stoplist.append("india")
    cleaned_Txt = textCleaning(cleaned_Data, stoplist)
    # print(cleaned_Txt)

    # converting 2-D Array into single String
    cleaned_data_text = ' '.join(' '.join(map(str, i)) for i in cleaned_Txt)
    print(cleaned_data_text)

    # analyze_word_frequency(cleaned_data_text, freqWordCount)

    # print(max_wordsss)
    # print(heightt)
    # print(widthh)

    wordcloud = WordCloud(max_words=max_wordsss, stopwords=stop_words, random_state=1,
                          background_color=background_color,
                          height=heightt, width=widthh).generate(cleaned_data_text)
    wordcloud.generate(cleaned_data_text)
    wordcloud.to_file(image_file_name)
    return cleaned_data_text


class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill='y', side='right', expand='false')
        canvas = ttk.Canvas(self, bd=0, highlightthickness=0,
                            yscrollcommand=vscrollbar.set)
        canvas.pack(side='left', fill='both', expand='true')
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor='nw')

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


class Analyzer_App:
    global img
    folder_path = ''
    text_content = ''
    # tuple
    colorchooser_result = ((0, 0, 0), '#000000')

    def __init__(self, master):
        self.textData = ''
        self.selected_file_label = None
        self.path_frame = None
        self.settings_frame = None
        self.content_frame = None
        self.frame2 = None
        self.textbox = None
        self.canvas = None
        self.canvas1 = None
        self.frame_inner = None
        self.scrolly = None
        self.scrollx = None
        self.colorchooser_output = None
        self.max_words = tk.IntVar()
        # self.varWidth = tk.IntVar()
        # self.varHeight = tk.IntVar()
        self.var_Width_Height = tk.IntVar()
        self.varFrequency = tk.IntVar()
        # self.varWidth.set(700)
        # self.varHeight.set(700)
        self.var_Width_Height.set(700)
        self.varFrequency.set(30)
        self.initialize_UI()

    def initialize_UI(self):
        # Variables

        root.bind('<Command-g>', lambda event: self.generate())
        root.bind('<Command-o>', lambda event: self.open_file_dialog())
        root.bind('<Command-p>', lambda event: self.clear_paste())
        root.bind('<Command-r>', lambda event: self.choose_color())

        # style applying to global
        styles = ttk.Style()
        styles.configure('.', font=('Helvetica', 18))

        # head_lbl = ttk.Label(text="Text Analyser", width=25, padding=15)
        # head_lbl.config(font=('Courier', 35, 'bold'), foreground='yellow')
        # head_lbl.pack()

        settings_row = ttk.Frame(root)
        settings_row.pack(fill=BOTH, expand=YES)
        # header and labelframe
        settings_frame_text = 'WordCloud Settings'
        self.settings_frame = ttk.Labelframe(settings_row, text=settings_frame_text, padding=15)
        self.settings_frame.pack(fill=BOTH, expand=YES, anchor=N)

        shortcut_lbl = ttk.Label(self.settings_frame, text="use keyboard to change the below values.")
        shortcut_lbl.config(foreground='blue', background='yellow')
        shortcut_lbl.config(font=('Courier', 15, 'bold'))
        shortcut_lbl.pack(padx=5, pady=5, side=TOP)
        # shortcut_lbl.config(wraplength=300)

        max_words_lbl = ttk.Label(self.settings_frame, text="Words To Show in image")
        max_words_lbl.config(font=('Courier', 18, 'bold'))
        max_words_lbl.pack(side=LEFT, padx=10, pady=10)
        max_words_lbl.config(wraplength=100)

        self.max_words.set(40)
        spinbox_max_words = Spinbox(self.settings_frame, from_=30, to=100, increment=10, textvariable=self.max_words)
        spinbox_max_words.config(font=('Courier', 24, 'bold'), width=3, foreground='yellow')
        spinbox_max_words.pack(side=LEFT, padx=10, pady=10)

        img_height_lbl = ttk.Label(self.settings_frame, text="Width  Height")
        img_height_lbl.config(font=('Courier', 22, 'bold'))
        img_height_lbl.pack(side=LEFT, padx=10, pady=10)
        img_height_lbl.config(wraplength=100)

        self.var_Width_Height.set(650)
        height_spinbox = Spinbox(self.settings_frame, from_=600, to=800, increment=50,
                                 textvariable=self.var_Width_Height)
        height_spinbox.config(font=('Courier', 24, 'bold'), width=4, foreground='yellow')
        height_spinbox.pack(side=LEFT, padx=10, pady=10)

        frequency_lbl = ttk.Label(self.settings_frame, text="Frequent Words Count")
        frequency_lbl.config(font=('Courier', 18, 'bold'))
        frequency_lbl.pack(side=LEFT, padx=10, pady=10)
        frequency_lbl.config(wraplength=100)

        self.varFrequency.set(20)
        frequency_spinbox = Spinbox(self.settings_frame, from_=20, to=40, increment=5,
                                    textvariable=self.varFrequency)
        frequency_spinbox.config(font=('Courier', 24, 'bold'), width=3, foreground='yellow')
        frequency_spinbox.pack(side=LEFT, padx=10, pady=10)

        styles.configure('ChooseColor.TButton', foreground='orange', font=('Helvetica', 23))
        colorchooser_button = ttk.Button(self.settings_frame, style='ChooseColor.TButton', text="Choose Color",
                                         command=self.choose_color)
        colorchooser_button.config()
        colorchooser_button.pack(side=LEFT, padx=10, pady=10)

        self.colorchooser_output = ttk.Canvas(self.settings_frame, width=50, height=50)
        self.colorchooser_output.config(background='black')
        self.colorchooser_output.pack(side=LEFT, padx=5, pady=5)

        shortcut_lbl = ttk.Label(self.settings_frame, text="cmd+R", width=5)
        shortcut_lbl.config(foreground='blue', background='yellow')
        shortcut_lbl.config(font=('Courier', 18, 'bold'))
        shortcut_lbl.pack(padx=5, pady=5, side=LEFT)
        shortcut_lbl.config(wraplength=300)

        path_row = ttk.Frame(root)
        path_row.pack(fill=BOTH, expand=YES)

        # header and labelframe option container
        path_frame_text = 'Images are saved in below Folder'
        # self.option_lf = ttk.Labelframe(root, text=option_text, padding=15, labelanchor="n")
        self.path_frame = ttk.Labelframe(path_row, text=path_frame_text, padding=15)
        self.path_frame.pack(fill=BOTH, expand=YES, anchor=N)

        self.selected_file_label = ttk.Label(self.path_frame, text="")
        self.folder_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.selected_file_label.config(text=f"{self.folder_path}")
        self.selected_file_label.config(foreground='yellow')
        self.selected_file_label.config(font=('Courier', 25, 'bold'))
        self.selected_file_label.pack(side=LEFT, padx=10, pady=5)
        self.selected_file_label.config(wraplength=600)

        shortcut_row = ttk.Frame(self.path_frame)
        shortcut_row.pack(side=RIGHT)

        shortcut_lbl = ttk.Label(shortcut_row, text="cmd+O\ncmd+G", width=5)
        shortcut_lbl.config(foreground='blue', background='yellow')
        shortcut_lbl.config(font=('Courier', 18, 'bold'))
        shortcut_lbl.pack(padx=5, pady=5, side=TOP)
        shortcut_lbl.config(wraplength=300)

        # self.selected_file_label.grid(row=0, column=1)
        styles.configure('analyse.TButton', foreground='orange', font=('Helvetica', 30))
        generate_button = ttk.Button(self.path_frame, style='analyse.TButton', text="Analyze", command=self.generate)
        generate_button.pack(side=RIGHT, padx=10, pady=5)

        open_button = ttk.Button(self.path_frame, text="Select a Folder", command=self.open_file_dialog)
        open_button.pack(side=RIGHT, padx=10, pady=5)

        # —————————————————————————————ui———————————————-

        panedwindow = ttk.Panedwindow(root, orient=HORIZONTAL)
        panedwindow.pack(fill=BOTH, expand=True)
        framel = ttk.Frame(panedwindow, width=10, height=300, relief=SUNKEN)
        self.frame2 = ttk.Frame(panedwindow, width=10, height=300, relief=SUNKEN)
        frame3 = ttk.Frame(panedwindow, width=350, height=300, relief=SUNKEN)
        panedwindow.add(framel, weight=1)
        panedwindow.add(self.frame2, weight=1)
        panedwindow.add(frame3, weight=3)

        # frame3 = ttk.Frame(panedwindow, width=50, height=400, relief=SUNKEN)
        # panedwindow.insert(1, frame3)

        style = ttk.Style()

        content_frame_text = 'Paste paragraph below'
        self.content_frame = ttk.Labelframe(framel, text=content_frame_text, padding=15)
        self.content_frame.pack(fill=X, expand=YES, anchor=N)

        shortcut_lbl = ttk.Label(self.content_frame, text="cmd+P", width=5)
        shortcut_lbl.config(foreground='blue', background='yellow')
        shortcut_lbl.config(font=('Courier', 18, 'bold'))
        shortcut_lbl.pack(padx=5, pady=5, side=TOP)
        shortcut_lbl.config(wraplength=300)

        self.textbox = ScrolledText(
            width=10, height=400,
            master=self.content_frame,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1)
        self.textbox.pack(fill=BOTH)
        self.textbox.config(font=('Courier', 25, 'normal'))

        default_txt = '''
        Previously, we discussed the importance of filtration for fish tanks because it cleans up debris particles, grows beneficial bacteria, and helps create water movement and surface agitation for improved oxygenation. However, is it possible your aquarium filter is overly powerful and produces current that is too strong for your fish? Some fish have long and flowy fins, are small in size, or originated from slow-moving waterways and aren’t built to handle torrents of water. Perpetually fighting against fast flow can cause your fish to get whipped around the tank, start hiding in shelters, and potentially develop illnesses from the constant stress. So, if you own a betta fish, goldfish, cherry shrimp, or other slow-swimming animal, consider implementing one of these techniques to reduce the current in your aquarium.

Use a Filter with Slow Flow
The simplest way to reduce the current is to not use too much filtration in your aquarium. In their quest to have the cleanest tank possible, people sometimes install multiple filters or get oversized filters that are meant for much bigger fish tanks. Other times, newcomers to the hobby pick up an all-in-one aquarium kit and don’t realize that the default filter is too strong for bettas and other slower fish. If you see your fish struggling, don’t be afraid to downsize your filter to better accommodate their needs.

Our favorite type of filtration for gentle flow is a sponge filter with a smaller or adjustable air pump. Its coarse foam is perfect for straining debris from the water without sucking up any baby fish, and the bubbles create good surface agitation to ensure your fish get enough oxygen. Some air pumps come with adjustable flow controls to lessen the air pressure if needed, but if the pump isn’t adjustable, you can also add an air valve outside of the fish tank to reduce the amount of bubbling. If you prefer to use another type of filtration like a hang-on-back or canister filter, check to see if it has an adjustable switch or knob that allows you to modify the flow rate of the water entering the aquarium.'''

        self.textbox.insert(END, default_txt)

        tabBar = ttk.Notebook(frame3)
        tabBar.pack()

        frame11 = ttk.Frame(tabBar)
        frame22 = ttk.Frame(tabBar)
        tabBar.add(frame11, text='Image')
        tabBar.add(frame22, text='Chart')

        tabBar.select()

        self.canvas = ttk.Canvas(frame11, width=self.var_Width_Height.get() + 170,
                                 height=self.var_Width_Height.get() + 170)
        self.canvas.pack(fill=BOTH, expand=YES)

        # create a scrollbar widget and set its command to the text widget
        # scrollbar = ttk.Scrollbar(root, orient='vertical', command = self.canvas.yview)
        # scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # scrollbar = ttk.Scrollbar(frame11, orient=VERTICAL)
        # scrollbar.pack(fill=BOTH, expand=YES)

    def choose_color(self):
        self.colorchooser_result = colorchooser.askcolor(initialcolor='#000000')
        self.colorchooser_output.config(background=self.colorchooser_result[-1])
        print(self.colorchooser_result)

    def generate(self):
        self.textData = self.textbox.get("1.0", tk.END)
        # print(self.textData)

        if self.validateFields():
            stopwords_wc = set(stopwords.words('english'))
            # self.max_words = self.max_words.get()
            # print(self.max_words)
            # print(type(self.colorchooser_result))
            # print(self.colorchooser_result[-1])

            imgfilename = self.folder_path + '/WordCloud.png'
            # print(imgfilename)

            cleaned_data_text = perform_WordCloud(self.textData, stopwords_wc, self.max_words.get(), imgfilename,
                                                  self.colorchooser_result[-1], self.var_Width_Height.get(),
                                                  self.var_Width_Height.get()
                                                  )

            img_file_name = self.folder_path + '/WordCloud.png'
            print(img_file_name)
            self.img = ImageTk.PhotoImage(Image.open(img_file_name))
            self.canvas.create_image(10, 10, anchor=NW, image=self.img)
            self.canvas.image = self.img

            common_words_tuple = analyze_word_frequency(cleaned_data_text, self.varFrequency.get())

            # style = ttk.Style()
            # # style.theme_use('classic')
            # style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")

            # deleting all child widgets
            for item in self.frame2.winfo_children():
                item.destroy()

            # self.canvas1 = ttk.Canvas(self.frame2, background="#ffffff", borderwidth=0)
            # self.frame_inner = ttk.Frame(self.canvas1)
            # self.scrolly = ttk.Scrollbar(self.frame2, orient="vertical", command=self.canvas1.yview)
            # self.scrollx = ttk.Scrollbar(self.frame2, orient="horizontal", command=self.canvas1.xview)
            # self.canvas1.configure(yscrollcommand=self.scrolly.set)
            # self.canvas1.create_window((4, 4), window=self.frame_inner, anchor="nw", tags="self.frame_inner")
            #
            # self.scrolly.pack(side="left", fill="y")
            # self.canvas1.pack(side="top", fill="both", expand=True)
            # self.scrollx.pack(side="bottom", fill="x")
            # self.canvas1.configure(scrollregion=self.canvas.bbox("all"))

            # self.frame_inner.bind("", self.onFrameConfigure)
            #
            # self.scrolly.set(0.0, 0.5)
            # CheckVar11 = tk.IntVar()
            # scrollbar1 = ttk.Scrollbar(self.frame2)
            # scrollbar1.pack(side=RIGHT, fill=Y)
            # pavanlist1 = ttk.Treeview(self.frame2, yscrollcommand=scrollbar1.set)
            # for pavanline1 in range(100):
            #     pavanlist1.insert(END, "Line Numbers are " + str(pavanline1) + " now in online ")
            #     if pavanline1 % 10 == 0:
            #         C11 = ttk.Checkbutton(self.frame2, text="Line Number : " + str(pavanline1), variable=CheckVar11)
            #         C11.pack()
            # pavanlist1.pack(side=LEFT, fill=BOTH)
            # scrollbar1.config(command=pavanlist1.yview)

            # scrollbar = ttk.Scrollbar(self.frame2)
            # listbox = ttk.Treeview(self.frame2, yscrollcommand=scrollbar.set, show="tree")
            # scrollbar.configure(command=listbox.yview)
            #
            # scrollbar.pack(side="right", fill="y")
            # listbox.pack(side="left", fill="both", expand=True)

            # for i in range(100):
            #     text = f"Item #{i + 1}"
            #     listbox.insert("", "end", text=text)

            # scrollbar = ttk.Scrollbar(root)
            # scrollbar.pack(side=RIGHT, fill=Y)
            # scrollbar.config(command=self.frame2.yview)

            # mainframe to make a scrollable window
            self.mainframe = VerticalScrolledFrame(self.frame2)
            self.mainframe.grid(row=0, column=0)
            self.mainframe.pack(fill=BOTH, expand=1)

            # create a notebook
            self.TNotebook_Overview = ttk.Notebook(self.mainframe.interior)
            self.TNotebook_Overview.grid(row=0, column=0)
            self.TNotebook_Overview.configure(takefocus="")

            self.Frame_Overview = ttk.Frame(self.TNotebook_Overview)

            self.TNotebook_Overview.add(self.Frame_Overview)
            self.TNotebook_Overview.tab(0, text="Common Words", compound="left", underline="-1", )

            # buttons = []
            # for i in range(300):
            #     buttons.append(ttk.Button(self.Frame_Overview, text="Button " + str(i)))
            #     buttons[-1].grid(column=0, row=i)

            rows = []
            for rrow in range(self.varFrequency.get()):
                cols = []
                for ccolumn in range(2):
                    if ccolumn == 0:
                        vall = common_words_tuple[rrow]
                        word_entry = ttk.Entry(self.Frame_Overview, width=9, font='Arial 30')
                        word_entry.grid(row=rrow, column=ccolumn)
                        word_entry.insert(END, (vall[0]))
                        cols.append(word_entry)
                        rows.append(cols)
                    else:
                        vall = common_words_tuple[rrow]
                        count_lbl = ttk.Label(self.Frame_Overview, text=vall[-1], width=10, font='Arial 25')
                        # count_lbl.config(padx=5)
                        count_lbl.grid(row=rrow, column=ccolumn)
                        cols.append(count_lbl)
                        rows.append(cols)

    def onFrameConfigure(self, event):
        self.canvas1.configure(scrollregion=self.canvas1.bbox("all"))

    def validateFields(self):
        # if len(self.textData.strip) <= 0:
        #     messagebox.showinfo(title='Empty content', message='Please paste a paragraph')
        #     return False
        # if len(self.imgfilename.strip) <= 0:
        #     return False
        # if len(self.textData.strip) <= 0:
        #     return False
        # if len(self.textData.strip) <= 0:
        #     return False
        return True

    def clear_paste(self):
        print('clearing')
        self.textbox.delete('1.0', 'end')
        self.textbox.focus()
        # Get the data from the clipboard
        cliptext = root.clipboard_get()
        self.textbox.insert(END, cliptext)

        # self.textbox.insert('')
        # entry.bind('<<Paste>>', lambda e: print('Paste'))

    def open_file_dialog(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.selected_file_label.config(text=f"{self.folder_path}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    printing('**************************')
    appWidth = 1200
    appHeight = 1000
    # root = ttk.Window(themename="darkly", size=(800, 800), resizable=(True, True), title='Text Analyzer',
    #                   maxsize = (1300, 1300),minsize=(appWidth, appHeight), position = (400, 400))
    root = ttk.Window(themename="darkly", resizable=(True, True), title='Text Analyzer', minsize=(appWidth, appHeight))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = int((screen_width / 2) - (appWidth / 2))
    y_position = int((screen_height / 2) - (appHeight / 2))

    pos = f'{appWidth}x{appHeight}' + f'+{x_position}+' + f'{y_position}'
    # print(pos)
    # root.geometry('200x150+400+300')
    root.geometry(f'{pos}')

    app = Analyzer_App(root)
    root.mainloop()
