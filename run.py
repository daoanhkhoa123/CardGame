from tkinter import *
from tkinter import messagebox
from os import path
from random import choice, randint
from PIL import Image, ImageTk
from Alpha.cards import Card, Deck
from Alpha.hand import Hand
from Alpha.hand import load_from_string
from Alpha.Config import *
PLAY_FEE = 100

""" WINDOW INITIALIZE"""
window = Tk()
window.title("My Card Game")
# root.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
window.geometry("1280x720")
window.configure(background="green")
player_list: list[Hand] = [None for i in range(2)]
deck = Deck()


""" PLAYER FRAME"""
my_frame = Frame(window, bg="green", padx=20, pady=20)
my_frame.pack(side="bottom")
name = "Phong"
money = 200
with open(path.join("saves", "Phong.txt"), "r") as file:
    name, money = load_from_string(file.read())

my_hand = Hand(name, my_frame, 5)
my_hand.money = money
my_score = StringVar(my_frame)
my_score_label = Label(my_frame, font=DEFAULT_FONT,
                       padx=10, pady=10, textvariable=my_score)
my_score_label.pack(side="top")
my_money = IntVar(window)
my_money_label = Label(window, font=BIG_FONT,
                       textvariable=my_money, background=BACKGROUD_COLOR)
my_money_label.pack(side="left", pady=60, padx=30)
my_money.set(my_hand.money)


def my_hand_score() -> str:
    global my_hand
    score = my_hand.score
    if score == -16:
        return "Under 16!"
    if score == -1:
        return "Over 21!"
    else:
        return str(score)


player_list[0] = my_hand


""" BOT """
dealer_frame = Frame(window, bg="green", padx=20, pady=20)
dealer_frame.pack(side="top", pady=20)

dealer_hand = Hand("dealer", dealer_frame, 5, 180)
dealer_score = IntVar(dealer_frame)
dealer_score.set(dealer_hand.score)
my_score_label = Label(my_frame, font=DEFAULT_FONT,
                       padx=10, pady=10, textvariable=my_score)
player_list[1] = dealer_hand

""" BUTTON """
button_frame = Frame(my_frame, bg="green")
button_frame.pack(side=BOTTOM, pady=20)

button_deal = Button(button_frame, text="Stand",
                     font=DEFAULT_FONT, command=lambda: game_restart())
button_deal.grid(row=0, column=1)


def my_hand_hit_card(deck):
    global player_list, my_score
    player_list[0].hit_deck(deck)
    player_list[0].unfold_cards()
    my_score.set(my_hand_score())


button_card = Button(button_frame, text="Hit Card",
                     font=DEFAULT_FONT, command=lambda: my_hand_hit_card(deck))
button_card.grid(row=0, column=0, padx=0)


""" GAME """


def game_start():
    global player_list, deck, button_deal, button_card, my_money_label
    if player_list[0].money < PLAY_FEE:
        messagebox.showinfo(
            "Insufficient money.", f"You have {player_list[0].money} while play fee is {PLAY_FEE}")
        return
    player_list[0].money -= PLAY_FEE
    my_money.set(player_list[0].money)
    deck = Deck()

    for hand in player_list:
        hand.clear_cards()

    for hand in player_list:
        hand.hit_deck(deck)  # start with 2 cards
        hand.hit_deck(deck)

    my_score.set(my_hand_score())
    player_list[0].unfold_cards()

    button_deal["state"] = "active"
    button_card["state"] = "active"


def game_restart_pop_up():
    global my_hand
    if messagebox.askyesno("Continue?", f"Do you want to play a new game?\n Play fee is {PLAY_FEE}\n Quiting will save your progress."):
        game_start()
    else:
        with open(path.join("saves", f"{my_hand.name}.txt"), "+w") as file:
            file.write(repr(my_hand))


def game_restart():
    global player_list, deck, window, button_card, button_deal,  my_money_label

    bot_hit()

    button_deal["state"] = "disabled"
    button_card["state"] = "disabled"

    for hand in player_list:
        hand.unfold_cards()

    winner = max((player_list))
    if winner is player_list[0]:  # if player win:
        player_list[0].money += int(PLAY_FEE * 2)
        my_money.set(player_list[0].money)

    # GET WINNER AND POP UP HERE
    win_text = Label(window, background=BACKGROUD_COLOR, font=BIG_FONT,
                     text=f"{winner.name} won!")
    win_text.pack()

    window.after(2000, win_text.destroy)
    window.after(2000, game_restart_pop_up)


def bot_hit():
    global dealer_hand, deck, window
    for i in range(5):
        if dealer_hand.score < 16:
            dealer_hand.hit_deck(deck)
        elif dealer_hand.score >= 21:
            break

        elif randint(0, 2) and not dealer_hand.is_full():
            dealer_hand.hit_deck(deck)


game_start()

window.mainloop()
