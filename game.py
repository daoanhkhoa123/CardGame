from tkinter import *
from tkinter import messagebox
from os import path
from random import choice, randint, random
from PIL import Image, ImageTk
from Alpha.cards import Card, Deck
from Alpha.hand import Hand
from Alpha.hand import load_from_string
from Alpha.Config import *
PLAY_FEE = 100
winner = None
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

my_hand = Hand(name, my_frame, 5)

with open(path.join("saves", "Phong.txt"), "r") as file:
    x = int(file.readline().strip())
    my_hand.money = x if x != 0 else 500
    my_hand.maxMoney = int(file.readline().strip())

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
    if score < 16:
        return "Under 16!"
    if score > 21:
        return "Over 21!"
    if score == 22:
        return "Royal!"
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
    global player_list, deck, button_deal, button_card, my_money_label, winner
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

    player_list[0].unfold_cards()

    if not checkmate():
        my_score.set(my_hand_score())
        player_list[0].unfold_cards()

        button_deal["state"] = "active"
        button_card["state"] = "active"
    else:
        printwinner()


def game_restart_pop_up():
    global my_hand
    if messagebox.askyesno("Continue?", f"Do you want to play a new game?\n Play fee is {PLAY_FEE}"):
        game_start()


def checkmate():
    global player_list, winner, status
    status = ""
    lst = [item.rank for item in player_list[0].get_card()]
    if 14 in lst:
        if 10 in lst or 11 in lst or 12 in lst or 13 in lst:
            winner = player_list[0]
            status = "blackjack"
        elif lst[0] == 14 and lst[1] == 14:
            winner = player_list[0]
            status = "double blackjack"
    lst = [item.rank for item in player_list[1].get_card()]
    if 14 in lst:
        if 10 in lst or 11 in lst or 12 in lst or 13 in lst:
            winner = player_list[1]
            status = "blackjack"
        elif lst[0] == 14 and lst[1] == 14:
            winner = player_list[1]
            status = "double blackjack"
    return status

def royalcheck():
    global player_list, winner
    if player_list[0].is_full() and player_list[0].score <=21:
        winner = player_list[0]
        return True
    elif player_list[1].is_full() and player_list[1].score <=21:
        winner = player_list[1]
        return True

    return False

def game_restart():
    global player_list, deck, window, button_card, button_deal,  my_money_label, winner
    bot_hit()

    button_deal["state"] = "disabled"
    button_card["state"] = "disabled"

    for hand in player_list:
        hand.unfold_cards()
    print(dealer_hand.score)
    print(player_list[0].score)

    royalcheck()
    # if royal, then declare the winner
    if royalcheck():
        print('calling royal')
        printwinner()
        return
    # not royal, we compare the score
    if player_list[1].score == player_list[0].score:
        winner = player_list[1]
    else:
        if player_list[0].score < 16 and player_list[1].score < 16:
            winner = max(player_list, key = lambda x: x.score)
        elif player_list[0].score > 21 and player_list[1].score >21:
            winner = min(player_list, key = lambda x: x.score)
        elif (player_list[0].score < 16 or player_list[0].score > 21) and 16 <= player_list[1].score  <=21:
            winner = player_list[1]
        elif  16 <= player_list[0].score <= 21 and (player_list[1].score >21 or player_list[1].score <16):
            winner = player_list[0]
        elif  16 <= player_list[0].score <=21 and 16 <=player_list[1].score <=21:
            winner = max(player_list, key = lambda x: x.score)
        elif 16 > player_list[0].score and player_list[1].score >21 or 16>player_list[1].score and player_list[0]>21:
            winner = min(player_list, key = lambda x: abs((16-x.score)*2 if x.score <16 else x.score - 21))
    printwinner()

def printwinner():
    global winner, player_list, window

    if winner is player_list[0]:  # if player win:
        player_list[0].money += int(PLAY_FEE * 2)
        my_money.set(player_list[0].money)
        player_list[0].maxMoney = player_list[0].money if player_list[0].money > player_list[0].maxMoney else player_list[0].maxMoney
        with open (path.join("saves", f"{player_list[0].name}.txt"), "w") as file:
            file.write(str(player_list[0].money)+"\n")
            file.write(str(player_list[0].maxMoney))

    # GET WINNER AND POP UP HERE
    texttowrite = f"{winner.name} won with ace" if checkmate() else f"{winner.name} won!"
    win_text = Label(window, background=BACKGROUD_COLOR, font=BIG_FONT,
                     text=texttowrite)
    win_text.pack()

    window.after(2000, win_text.destroy)
    window.after(2000, game_restart_pop_up)

def bot_hit():
    global dealer_hand, deck, window, player_list
    for i in range(5):
        if dealer_hand.score < 16 and dealer_hand.score != -1:
            dealer_hand.hit_deck(deck)
        elif dealer_hand.score >= 21:
            break

        elif dealer_hand.score != -1 and random() <= (21 - dealer_hand.score)/13 and not dealer_hand.is_full():
            print('score=', dealer_hand.score)
            print((21 - dealer_hand.score)/13 )
            dealer_hand.hit_deck(deck)


game_start()

window.mainloop()
