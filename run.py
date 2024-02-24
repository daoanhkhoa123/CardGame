from tkinter import *
from os import path
from random import choice
from PIL import Image, ImageTk
from Alpha.cards import Card, Deck
from Alpha.hand import Hand


root = Tk()
root.title("My Card Game")
# root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
root.geometry("1280x720")
root.configure(background="green")

""" DEALER AND PLAYER FRAME"""

dealer_frame = Frame(root, bg="green")
dealer_frame.pack(pady=20)
dealer_hand = Hand(dealer_frame, 5, row=0, name="Dealer",
                   padx=20, pady=20, borderwidth=0, ipadx=0, ipady=20)

my_frame = Frame(root, bg="green")
my_frame.pack(pady=0)
my_score = IntVar(my_frame)
my_hand = Hand(my_frame, 5, row=0, pady=20, padx=20,
               ipadx=20, borderwidth=0, name="You", ipady=20)


deck = Deck(joker=True)


def hit_me(hand: Hand):
    global my_score
    card = deck.deal_card()
    hand.hit_card(card)
    my_score.set(hand.score)


score_label = Label(my_frame, font=("Helvetica", 14), padx=10, pady=10,
                    bg="green", textvariable=my_score, text=str())
score_label.pack()


def clear_card(hand: Hand):
    hand.clear_cards()


def unfold(hand: Hand):
    hand.unfold_cards()


""" BUTTON """
button_frame = Frame(root, bg="green")
button_frame.pack(side=BOTTOM, pady=20)

button_deal = Button(button_frame, text="Unfold cards",
                     font=("Helvetica", 14), command=lambda: unfold(my_hand))
button_deal.grid(row=0, column=0)

card_button = Button(button_frame, text="Hit Card",
                     font=("Helvetica", 14), command=lambda: hit_me(my_hand))
card_button.grid(row=0, column=1, padx=0)

stand_button = Button(button_frame, text="Clear cards",
                      font=("Helvetica", 14), command=lambda: clear_card(my_hand))
stand_button.grid(row=0, column=2)


root.mainloop()
