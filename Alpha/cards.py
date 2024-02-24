from dataclasses import dataclass, field
from PIL import Image, ImageTk
from random import choice
from os import path


_ASSET_DIRECTORY = path.join(path.dirname(
    path.dirname(path.abspath(__file__))), "Asset_cards")


SUITS = ("spades", "clubs", "hearts", "diamonds")
RANK = {
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

    def __repr__(self) -> str:
        if self.folded:
            return "0_0"

        if self.rank == 15:
            if self.suit == SUITS[3] or self.suit == SUITS[2]:
                return "red_joker"
            else:
                return "black_joker"
        return f"{RANK.get(self.rank, self.rank)}_of_{self.suit}"

    @property
    def image(self, inverse_ratio: int = 3, rotation: int = 0) -> ImageTk:
        img = Image.open(self.directory)
        img = img.resize((img.size[0] // inverse_ratio,
                          img.size[1]//inverse_ratio), Image.Resampling.LANCZOS)
        img = img.rotate(rotation)

        img = ImageTk.PhotoImage(img)
        return img

    @property
    def directory(self) -> str:
        return path.join(_ASSET_DIRECTORY, f"{self}.png")


class Deck:
    def __init__(self, joker: bool = False) -> None:
        if not joker:
            self.__deck = _init_deck()
        else:
            self.__deck = _init_deck_joker()

    @property
    def deck(self) -> list[Card]:
        return self.__deck

    def number_of_cards_left(self) -> int:
        return len(self.__deck)

    def deal_card(self) -> Card:
        """Get one random card from cards deck

        Args:
            cards_deck (list): list of card
        """
        card = choice(self.deck)
        self.deck.remove(card)
        return card
        

""" ULTILITY FUNCTIONS """
# initializing deck 54
def _init_deck_joker() -> list[Card]:
    cards = [Card(None, None)] * 54
    count = 0
    for rank in range(2, 16):
        for suit in SUITS:
            if rank == 15:
                if suit == SUITS[0] or suit == SUITS[3]:  # Spades or Hearts
                    cards[count] = Card(rank, suit)
                else:
                    continue

            cards[count] = Card(rank, suit)
            count += 1

    return cards


# 52
def _init_deck() -> list[Card]:
    cards = [Card(None, None)] * 52
    count = 0
    for rank in range(2, 16):
        for suit in SUITS:
            if rank == 15:
                continue

            cards[count] = Card(rank, suit)
            count += 1

    return cards


if __name__ == "__main__":
    print(_ASSET_DIRECTORY)
