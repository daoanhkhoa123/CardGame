from tkinter import *
from os import path
from random import choice, randint
from PIL import Image, ImageTk
from Alpha.cards import Card, Deck
from Alpha.hand import Hand
from time import sleep

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
dealer_frame = Frame(window, bg="green", padx=0, pady=0)
dealer_frame.pack(side="top", pady=20)

dealer_hand = Hand("dealer", dealer_frame, 5)
dealer_score = IntVar(dealer_frame)
dealer_score_label = Label(dealer_frame, font=DEFAULT_FONT,
                           padx=10, pady=10, textvariable=dealer_score)


my_frame = Frame(window, bg="green", padx=0, pady=0)
my_frame.pack(side="bottom")

my_hand = Hand("player", my_frame, 5)
my_score = IntVar(my_frame)
my_score_label = Label(my_frame, font=DEFAULT_FONT,
                       padx=10, pady=10, textvariable=my_score)

deck = Deck(joker=True)


for i in range(2):
    dealer_hand.hit_deck(deck)
    my_hand.hit_deck(deck)

for i in range(3):
    choice = randint(0, 3)
    if choice:
        dealer_hand.hit_deck(deck)


def hit_me(hand: Hand):
    global my_score
    card = hand.hit_deck(deck)
    my_score.set(hand.score)


score_label = Label(my_frame, font=DEFAULT_FONT, padx=10, pady=10,
                    bg="green", textvariable=my_score, text=str())
score_label.pack()


def clear_card(hand: Hand):
    global my_hand, dealer_hand
    my_hand.clear_cards()
    dealer_hand.clear_cards()
    global deck
    deck = Deck(joker=True)

    for i in range(2):
        dealer_hand.hit_deck(deck)
        my_hand.hit_deck(deck)

    if my_hand > dealer_hand:
        print(f"You win!. {my_hand.score}| {dealer_hand.score}")
    sleep(5)


def unfold(hand: Hand):
    hand.unfold_cards()
    dealer_hand.unfold_cards()


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
