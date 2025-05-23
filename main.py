BACKGROUND_COLOR = "#B1DDC6"

import pandas as pd
import random
from tkinter import *

# Load vocab
try:
    file = pd.read_csv("vocab_to_learn.csv")
except FileNotFoundError:
    file = pd.read_csv("Data/french_words.csv")
french = [items for items in file["French"]]
english = [items for items in file["English"]]

# Combine into vocab list
vocab = list(zip(french, english))
vocab_to_learn = []
word = "hi"
flip_timer = None

def random_word(voc):
    if len(voc) == 0:
        return "The", "End"
    else:
        random_index = random.randint(0, len(voc) - 1)
        return vocab[random_index][0], vocab[random_index][1]

def flip_card(wor):
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(word_text, text=wor[1], fill="WHITE")
    canvas.itemconfig(title_text, text="English", fill="WHITE")

def check(cor):
    if len(vocab) == 0:
        if len(vocab_to_learn) != 0:
            fre = [words[0] for words in vocab_to_learn]
            eng = [words[1] for words in vocab_to_learn]
            dic = {"French": fre, "English": eng}
            df = pd.DataFrame(dic)
            df.to_csv("vocab_to_learn.csv", index=False)
        window.quit()
    else:
        if cor == 1:
            try:
                if word in vocab:
                    vocab.remove(word)
            except:
                pass
        elif cor == 0:
            try:
                if word in vocab:
                    vocab_to_learn.append(word)
                    vocab.remove(word)
            except:
                pass

def change_word(cor):
    global word, flip_timer
    check(cor)

    canvas.itemconfig(title_text, text="French", fill="BLACK")
    canvas.itemconfig(canvas_image, image=card_front_img)

    word = random_word(vocab)
    canvas.itemconfig(word_text, text=word[0], fill="BLACK")

    if flip_timer is not None:
        window.after_cancel(flip_timer)
    flip_timer = window.after(3000, lambda: flip_card(word))

# UI Setup
window = Tk()
window.title("Duolingo")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(height=526, width=800)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="Language", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_btn = Button(image=cross_image, highlightthickness=0, command=lambda: change_word(cor=0))
unknown_btn.grid(row=1, column=0)

tik_image = PhotoImage(file="images/right.png")
known_btn = Button(image=tik_image, highlightthickness=0, command=lambda: change_word(cor=1))
known_btn.grid(row=1, column=1)

window.mainloop()
