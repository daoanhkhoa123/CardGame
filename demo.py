from tkinter import *
import os
from random import choice
from PIL import Image, ImageTk
from Alpha.cards import Card, Deck
# Resize Cards


def resize_card(card, smaller_ratio=3):
    print(card)
    img = Image.open(card)
    img = img.resize((img.size[0] // smaller_ratio,
                     img.size[1]//smaller_ratio), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    return img


root = Tk()
root.title("My Card Game")
# root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
root.geometry("1280x720")
root.configure(background="green")


my_frame = Frame(root, bg="green")
my_frame.pack(pady=20)

player_frame = LabelFrame(my_frame, text="Player", bd=0)
player_frame.grid(row=0, column=1, ipadx=20)

dealer_frame = LabelFrame(my_frame, text="Dealer", bd=0)
dealer_frame.grid(row=0, column=0, padx=20, ipadx=20)

player_label = Label(player_frame, text="")
player_label.pack(pady=20)

dealer_label = Label(dealer_frame, text=" ")
dealer_label.pack(pady=20)


# player and dealer global variable
dealer = list()
player = list()
dealer_image = list()
player_image = list()

# get cards deck
deck = Deck()


dealer, dealer_image, dealer_frame, dealer_label


def pick_cards(dealer: list, player: list, deck: list):
    # dealer
    global dealer_image
    global player_image
    card = deck.deal_card()
    dealer.append(card)
    dealer_image = resize_card(os.path.join(
        os.getcwd(), "MyCardGame", "Asset_cards", f"{card}.png"))
    dealer_label.config(image=dealer_image)
    # player
    card = deck.deal_card()
    player.append(card)
    player_image = resize_card(os.path.join(
        os.getcwd(), "MyCardGame", "Asset_cards", f"{card}.png"))
    player_label.config(image=player_image)

    print(len(deck))


button_frame = Frame(root, bg="green")
button_frame.pack(pady=20)

shuffle_button = Button(button_frame, text="Shuffle Deck",
                        font=("Helvetica", 14), command=lambda: pick_cards(dealer, player, deck))
shuffle_button.grid(row=0, column=0)


card_button = Button(button_frame, text="Get Cards", font=("Helvetica", 14))
card_button.grid(row=0, column=1, padx=0)

stand_button = Button(button_frame, text="Stand", font=("Helvetica", 14))
stand_button.grid(row=0, column=2)

root.mainloop()
