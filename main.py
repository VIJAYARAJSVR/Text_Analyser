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

    for freq in freq_dist.most_common(most_common):
        print(freq)

    # plt.figure(figsize=(12, 6))
    # freq_dist.plot(50)
    # plt.show()


def perform_WordCloud(text_to_process, stop_words, max_wordsss, image_file_name, background_color, heightt, widthh,
                      freqWordCount):
    cleaned_Data = dataCleaning(text_to_process)
    # print(cleaned_Data)

    stoplist = stopwords.words('english')
    stoplist.append("india")
    cleaned_Txt = textCleaning(cleaned_Data, stoplist)
    # print(cleaned_Txt)

    # converting 2-D Array into single String
    cleaned_data_text = ' '.join(' '.join(map(str, i)) for i in cleaned_Txt)
    print(cleaned_data_text)

    analyze_word_frequency(cleaned_data_text, freqWordCount)

    # print(max_wordsss)
    # print(heightt)
    # print(widthh)

    wordcloud = WordCloud(max_words=max_wordsss, stopwords=stop_words, random_state=1,
                          background_color=background_color,
                          height=heightt, width=widthh).generate(cleaned_data_text)
    wordcloud.generate(cleaned_data_text)
    wordcloud.to_file(image_file_name)


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
        self.textbox = None
        self.canvas = None
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
        # spam = tk.StringVar()

        # style applying to global
        styles = ttk.Style()
        styles.configure('.', font=('Helvetica', 18))

        head_lbl = ttk.Label(text="Text Analyser", width=25, padding=15)
        head_lbl.config(font=('Courier', 35, 'bold'), foreground='yellow')
        head_lbl.pack()

        settings_row = ttk.Frame(root)
        settings_row.pack(fill=BOTH, expand=YES)
        # header and labelframe
        settings_frame_text = 'WordCloud Settings'
        self.settings_frame = ttk.Labelframe(settings_row, text=settings_frame_text, padding=15)
        self.settings_frame.pack(fill=BOTH, expand=YES, anchor=N)

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
        self.colorchooser_output.pack(side=LEFT, padx=10, pady=10)

        path_row = ttk.Frame(root)
        path_row.pack(fill=BOTH, expand=YES)

        # header and labelframe option container
        path_frame_text = 'Images are saved in below Folder'
        # self.option_lf = ttk.Labelframe(root, text=option_text, padding=15, labelanchor="n")
        self.path_frame = ttk.Labelframe(path_row, text=path_frame_text, padding=15)
        self.path_frame.pack(fill=BOTH, expand=YES, anchor=N)

        path_lbl = ttk.Label(self.path_frame, text="Selected Folder Path :", width=25)
        # path_lbl.config(foreground='blue', background='yellow')
        path_lbl.config(font=('Courier', 18, 'bold'))
        path_lbl.pack(side=LEFT, padx=10, pady=10)
        # path_lbl.grid(row=0, column=0)

        self.selected_file_label = ttk.Label(self.path_frame, text="")
        self.folder_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.selected_file_label.config(text=f"{self.folder_path}")
        self.selected_file_label.config(foreground='yellow')
        self.selected_file_label.config(font=('Courier', 25, 'bold'))
        self.selected_file_label.pack(side=LEFT, padx=10, pady=10)
        self.selected_file_label.config(wraplength=600)

        # self.selected_file_label.grid(row=0, column=1)
        styles.configure('analyse.TButton', foreground='orange', font=('Helvetica', 30))
        generate_button = ttk.Button(self.path_frame, style='analyse.TButton', text="Analyze", command=self.generate)
        generate_button.pack(side=RIGHT, padx=10, pady=10)

        open_button = ttk.Button(self.path_frame, text="Open File", command=self.open_file_dialog)
        open_button.pack(side=RIGHT, padx=10, pady=10)
        # open_button.grid(row=0,column=2)

        # generate_button.grid(row=1, column=1)

        # —————————————————————————————ui———————————————-

        panedwindow = ttk.Panedwindow(root, orient=HORIZONTAL)
        panedwindow.pack(fill=BOTH, expand=True)
        framel = ttk.Frame(panedwindow, width=10, height=300, relief=SUNKEN)
        frame2 = ttk.Frame(panedwindow, width=10, height=300, relief=SUNKEN)
        frame3 = ttk.Frame(panedwindow, width=350, height=300, relief=SUNKEN)
        panedwindow.add(framel, weight=1)
        panedwindow.add(frame2, weight=1)
        panedwindow.add(frame3, weight=3)

        # frame3 = ttk.Frame(panedwindow, width=50, height=400, relief=SUNKEN)
        # panedwindow.insert(1, frame3)

        style = ttk.Style()

        content_frame_text = 'Paste paragraph below'
        self.content_frame = ttk.Labelframe(framel, text=content_frame_text, padding=15)
        self.content_frame.pack(fill=X, expand=YES, anchor=N)

        self.textbox = ScrolledText(
            width=10, height=400,
            master=self.content_frame,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1)
        self.textbox.pack(fill=BOTH)
        self.textbox.config(font=('Courier', 25, 'normal'))

        default_txt = ""
        self.textbox.insert(END, default_txt)

        tabBar = ttk.Notebook(frame3)
        tabBar.pack()

        frame11 = ttk.Frame(tabBar)
        frame22 = ttk.Frame(tabBar)
        tabBar.add(frame11, text='Image')
        tabBar.add(frame22, text='Chart')

        # frame33 = ttk.Frame(tabBar)
        # tabBar.insert(1, frame33, text='Three')
        # tabBar.forget(1)
        # tabBar.add(frame33, text='Three')
        # tabBar.select(1)
        tabBar.select()

        # imgfilename = self.folder_path + '/WordCloud.png'
        # self.canvas = ttk.Canvas(frame11, width=300, height=300)
        # self.canvas.pack()
        # img = ImageTk.PhotoImage(Image.open(imgfilename))
        # canvas.create_image(20, 20, anchor=NW, image=img)

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

            perform_WordCloud(self.textData, stopwords_wc, self.max_words.get(), imgfilename,
                              self.colorchooser_result[-1], self.var_Width_Height.get(), self.var_Width_Height.get(),
                              self.varFrequency.get())

            img_file_name = self.folder_path + '/WordCloud.png'
            print(img_file_name)
            self.img = ImageTk.PhotoImage(Image.open(img_file_name))
            self.canvas.create_image(10, 10, anchor=NW, image=self.img)
            self.canvas.image = self.img

            # imgfilename = self.folder_path + '/WordCloud.png'
            # print(imgfilename)
            # img = ImageTk.PhotoImage(Image.open(imgfilename))
            # self.canvas.create_image(400, 400, anchor=NW, image=img)
            # self.canvas.image = img

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
