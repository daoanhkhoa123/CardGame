from PIL import Image, ImageTk
from numpy import array
from random import choice
from os import path
from dataclasses import dataclass, field


_ASSET_DIRECTORY = path.join(path.dirname(
    path.dirname(path.abspath(__file__))), "Asset_cards")

SUITS = ("spades", "clubs", "hearts", "diamonds")
RANK_TEXT = {
    11: "jack",
    12: "queen",
    13: "king",
    14: "ace",
    15: "joker"
}


@dataclass(order=True, eq=True)
class Card:
    rank: int  # 2 to 15, 15 is joker
    suit: str = field(compare=False)
    folded: bool = field(compare=False, default=True, repr=False)
    __image: ImageTk.PhotoImage = field(
        compare=False, default=str(), repr=False)

    def __str__(self) -> str:
        if self.rank == 15:  # joker only has two suit
            # anything red for easier customization
            if self.suit == SUITS[3] or self.suit == SUITS[2]:
                return "red_joker"
            else:
                return "black_joker"

        return f"{RANK_TEXT.get(self.rank, self.rank)}_of_{self.suit}"

    @property
    def directory(self) -> str:
        file = str(self)
        if self.folded:
            file = "0_0"

        return path.join(_ASSET_DIRECTORY, f"{file}.png")

    def image(self, inverse_ratio: int = 4, rotation: int = 0) -> ImageTk:
        img = Image.open(self.directory)
        img = img.resize((img.size[0] // inverse_ratio,
                          img.size[1]//inverse_ratio), Image.Resampling.LANCZOS)
        img = img.rotate(rotation, expand=1)

        img = ImageTk.PhotoImage(img)
        self.__image = img
        return self.__image


class Deck:
    # i have to turn this into a list of number
    # for optimization, otherwise it would case a
    # lot of weird behaviour, and consume huge memory
    # 52 cards, each contain images
    # I will have to convert index to cards later
    def __init__(self, joker: bool = False) -> None:
        if not joker:
            self.__deck = [i for i in range(52)]
        else:
            self.__deck = [i for i in range(54)]

    @property
    def deck(self) -> list[Card]:
        return self.__deck

    @property
    def number_of_cards_left(self) -> int:
        return len(self.__deck)

    def is_empty(self) -> bool:
        return len(self.deck) == 0

    def deal_card(self) -> Card:
        """Get one random card from cards deck

        Args:
            cards_deck (list): list of card
        """
        if self.is_empty():
            raise IndexError("Deck is aleady empty. Can not get any card.")

        card_index = choice(self.deck)
        self.deck.remove(card_index)
        return index_to_card(card_index)


""" ULTILITY FUNCTIONS """


def index_to_card(i: int) -> Card:
    # maximum at 53
    if i == 52:
        return Card(15, SUITS[3])    # red joker
    elif i == 53:
        return Card(15, SUITS[0])     # black joker
    else:  # 51 to 0, divide by 4 we have 0 to 12
        rank = i//4 + 2  # i = 0 -> 2
        suit = i % 4
        return Card(rank, SUITS[suit])


if __name__ == "__main__":
    print(_ASSET_DIRECTORY)
