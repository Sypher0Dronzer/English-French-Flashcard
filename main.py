import random
from tkinter import *
import pandas

current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict("records")


def english_translate(f_word):
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=f_word["English"], fill="white")
    canvas.itemconfig(background_img, image=back_card)
    window.after_cancel(flash)


def next_card():
    global flash, current_card
    # here the purpose of stopping teh timer is that suppose you keep clicking on teh buttons u will notice that the
    # card will flip #after the 3 secs of the first card that you saw so here we will stop teh timer, and it will work
    # only after we land on a card , wait for 3 sec and only then will it flip
    window.after_cancel(flash)
    current_card = random.choice(to_learn)
    canvas.itemconfig(background_img, image=front_card)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    flash = window.after(3000, english_translate, current_card)
    canvas.itemconfig(background_img, image=front_card)


def already_know():
    to_learn.remove(current_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    next_card()


BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flash = window.after(3000, next_card)
front_card = PhotoImage(file="./images/card_front.png")
back_card = PhotoImage(file="./images/card_back.png")
canvas = Canvas(height=526, width=800)
background_img = canvas.create_image(400, 263, image=front_card)
canvas.grid(row=0, column=0, columnspan=2)

card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Buttons
right = PhotoImage(file="./images/right.png")
right_button = Button(image=right, highlightthickness=0, command=already_know)
right_button.grid(row=1, column=1)

wrong = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()
