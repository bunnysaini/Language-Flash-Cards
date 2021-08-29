import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
random_word = {}
words_dictionary = {}

try:
    word_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanish_words.csv")
    words_dictionary = original_data.to_dict(orient="records")
else:
    words_dictionary = word_data.to_dict(orient="records")


def pick_a_word():
    global random_word, flip_duration
    window.after_cancel(flip_duration)
    random_word = random.choice(words_dictionary)
    canvas.itemconfig(card_language, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=random_word["Spanish"], fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    flip_duration = window.after(5000, func=flip_card)


def knows_card():
    words_dictionary.remove(random_word)
    print(len(words_dictionary))
    data = pandas.DataFrame(words_dictionary)
    data.to_csv("data_stock/words_to_learn.csv", index=False)

    pick_a_word()


def flip_card():
    canvas.itemconfig(card_language, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_word["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back)


window = Tk()
window.title("Flash Cards - An Efficient Way To Learn")
window.config(padx=50, pady=15, bg=BACKGROUND_COLOR)

flip_duration = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front)
card_language = language = canvas.create_text(400, 150, text="Spanish", font=("Arial", 25, "italic"))
card_word = word = canvas.create_text(400, 263, text="word", font=("COUTURE", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

check_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")

right_button = Button(image=check_image, highlightthickness=0, borderwidth=0, relief="groove",  command=knows_card)
right_button.grid(row=1, column=1)

wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, relief="groove", command=pick_a_word)
wrong_button.grid(row=1, column=0)

pick_a_word()

window.mainloop()