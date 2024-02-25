# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

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
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib
import matplotlib.pyplot as plt
import re

import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText


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


def perform_WordCloud(text_to_process, stop_words, max_words, image_file_name, background_color, height, width):
    cleaned_Data = dataCleaning(text_to_process)
    # print(cleaned_Data)

    stoplist = stopwords.words('english')
    stoplist.append("india")
    cleaned_Txt = textCleaning(cleaned_Data, stoplist)
    # print(cleaned_Txt)

    # converting 2-D Array into single String
    cleaned_data_text = ' '.join(' '.join(map(str, i)) for i in cleaned_Txt)
    print(cleaned_data_text)

    analyze_word_frequency(cleaned_data_text, 30)

    wordcloud = WordCloud(max_words=max_words, stopwords=stop_words, random_state=1,
                          background_color=background_color,
                          height=height, width=width).generate(cleaned_data_text)
    wordcloud.generate(cleaned_data_text)
    wordcloud.to_file(image_file_name)


class Analyzer_App:
    folder_path = ''
    text_content = ''
    def __init__(self, master):
        self.selected_file_label = None
        self.path_frame = None
        self.content_frame = None
        self.textbox = None

        self.initialize_UI()

    def initialize_UI(self):
        styles = ttk.Style()
        # style applying to global
        styles.configure('.', font=('Helvetica', 18))

        head_lbl = ttk.Label(root, text="Text Analyser", width=25, padding=15)
        head_lbl.config(font=('Courier', 35, 'bold'), foreground='yellow')
        head_lbl.pack()

        # header and labelframe option container
        path_frame_text = 'Images are saved in below Folder'
        # self.option_lf = ttk.Labelframe(root, text=option_text, padding=15, labelanchor="n")
        self.path_frame = ttk.Labelframe(root, text=path_frame_text, padding=15)
        self.path_frame.pack(fill=X, expand=YES, anchor=N)

        path_row = ttk.Frame(self.path_frame)
        path_row.pack(fill=X, expand=YES)

        path_lbl = ttk.Label(path_row, text="Selected Folder Path :", width=25)
        # path_lbl.config(foreground='blue', background='yellow')
        path_lbl.config(font=('Courier', 18, 'bold'))
        path_lbl.pack()

        self.selected_file_label = ttk.Label(path_row, text="", width=170)
        folder_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        self.selected_file_label.config(text=f"{folder_path}")
        self.selected_file_label.config(foreground='yellow')
        self.selected_file_label.config(font=('Courier', 25, 'bold'))
        self.selected_file_label.pack()

        open_button = ttk.Button(path_row, text="Open File", command=self.open_file_dialog)
        open_button.pack(padx=20, pady=20)

        generate_button = ttk.Button(path_row, text="Show Analysed Text", command=self.generate)
        generate_button.pack(padx=20, pady=20)

        # ————————————————————————————————————————————-
        content_frame_text = 'Please paste the text / paragraph to process below'
        self.content_frame = ttk.Labelframe(root, text=content_frame_text, padding=15)
        self.content_frame.pack(fill=X, expand=YES, anchor=N)

        content_row = ttk.Frame(self.content_frame)
        content_row.pack(fill=X, expand=YES)

        style = ttk.Style()
        self.textbox = ScrolledText(
            master=content_row,
            highlightcolor=style.colors.primary,
            highlightbackground=style.colors.border,
            highlightthickness=1)
        self.textbox.pack(fill=BOTH)
        self.textbox.config(font=('Courier', 25, 'normal'))

        default_txt = ""
        self.textbox.insert(END, default_txt)

    def generate(self):
        textData =  self.textbox.get("1.0", tk.END)
        print(textData)
        stopwords_wc = set(stopwords.words('english'))
        max_words = 80
        perform_WordCloud(textData, stopwords_wc, max_words, 'WordCloud.png', 'black', 700, 700)

    def open_file_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_file_label.config(text=f"{folder_path}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    printing('**************************')
    root = ttk.Window(themename="darkly", size=(1200, 1000), resizable=(True, True), title='Text Analyzer', )
    app = Analyzer_App(root)
    root.mainloop()

    # textData = """ India """
    # stopwords_wc = set(stopwords.words('english'))
    # max_words = 80
    # perform_WordCloud(textData, stopwords_wc, max_words, 'WordCloud.png', 'black', 700, 700)

# b1 = ttk.Button(root, text="Button 1", bootstyle=SUCCESS)
# b1.pack(side=LEFT, padx=5, pady=10)
#
# b2 = ttk.Button(root, text="Button 2", bootstyle=(INFO, OUTLINE))
# b2.pack(side=LEFT, padx=5, pady=10)
