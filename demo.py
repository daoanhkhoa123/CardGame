from tkinter import *
from os import path
from random import choice
from PIL import Image, ImageTk
from Alpha.cards import Card, Deck
from Alpha.hand import Hand

DEFAULT_FONT = ("Helvetica", 14)
DEFAULT_BACKGROUND = "green"

""" WINDOW """
window = Tk()
window.title("My Card Game")
# root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
window.geometry("1280x720")
window.configure(background="green")

""" BUTTOM FRAME """
button_frame = Frame(window, bg="green")
button_frame.pack(side="bottom", pady=20)


""" DEALER AND PLAYER FRAME"""

my_frame = Frame(window, bg="green", padx=0, pady=0)
my_frame.pack(side="bottom")
my_name = Label(my_frame, font=DEFAULT_FONT,
                height=2, bg="green", text="Player")
my_name.pack()
my_hand = Hand(my_frame, 5, pad=2,
               borderwidth=0)
my_score = IntVar(my_frame)
my_score_label = Label(my_frame, font=DEFAULT_FONT,
                       padx=10, pady=10, textvariable=my_score)

deck = Deck(joker=True)


def hit_me(hand: Hand):
    global my_score
    card = deck.deal_card()
    hand.hit_card(card)
    my_score.set(hand.score)


score_label = Label(my_frame, font=DEFAULT_FONT, padx=10, pady=10,
                    bg="green", textvariable=my_score, text=str())
score_label.pack()


def clear_card(hand: Hand):
    hand.clear_cards()


def unfold(hand: Hand):
    hand.unfold_cards()


""" BUTTON """

button_deal = Button(button_frame, text="Unfold cards",
                     font=DEFAULT_FONT, command=lambda: unfold(my_hand))
button_deal.grid(row=0, column=0)

card_button = Button(button_frame, text="Hit Card",
                     font=DEFAULT_FONT, command=lambda: hit_me(my_hand))
card_button.grid(row=0, column=1, padx=0)

stand_button = Button(button_frame, text="Clear cards",
                      font=DEFAULT_FONT, command=lambda: clear_card(my_hand))
stand_button.grid(row=0, column=2)


window.mainloop()
