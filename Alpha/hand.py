import Alpha.Config as config
from tkinter import Frame
from tkinter import *
from numpy import array
from Alpha.cards import Card, Deck


class __HandHolder:
    """ This is a class that is solely built for organizing card slot,
    storing cards, and rendering them to show on the screen.

    Imagine a  drawn frame of many slots where you put each card into those.
    It is drawn on the table without the care for player.
    """

    def __init__(self, name: str, master_frame: Frame, max_cards: int, rotation: int = 0) -> None:
        """HandHolder should stay inside a frame. 
        That frame represent the whole player

        Handholder has a frame that contains labels, with its width and height
        each label shows a card. Number of labels is max_cards.

        Each label will be packed on grid either on x (horizontal),
        or y (vertical), along with pad for spacing between cards.
        The rotation (veriticality) is depend on rotation argument.

        Args:
            name (str): Name of this Hand
            master_frame (Frame): the frame that this stays inside
            max_cards (int): the maximum amout of cards

        Atributes:
            name (str): Name
            frame (Frame): The frame to hold the slots.
            slot_list (list[Label]): list of card slots
            card_list (list[Card]): list of cards
            count_card (int): Tracking numbers of current card
            rotation (int, optional): 0, 90, 180. 270

        API:
            get_card(self): yield cards in hand
            update_image(func): update image decorator 
            hit_deck(self, deck): get a card from deck
            unfold_cards(self)
            clear_cards(self): clear all card in hand
        """

        # lists delcaration
        self._label_list: list[Label] = [None] * max_cards
        self._card_list: list[Card] = [None] * max_cards

        """ Frame """
        self.__frame: LabelFrame = LabelFrame(
            master_frame, labelanchor="n", text=name, font=config.DEFAULT_FONT)
        self.__frame.pack()

        """ Card Label """
        for i in range(max_cards):
            self._label_list[i] = Label(
                self.__frame, image=str())

            if (rotation//90) % 2 == 0:  # 0 or 180
                self._label_list[i].grid(row=0, column=i, padx=config.PAD)
            else:
                self._label_list[i].grid(row=i, column=0, pady=config.PAD)

        # ultility
        self.__count_card: int = 0  # for convience in tracking card
        self.__rotation: int = rotation
        self.name = name

    @property
    def max_card(self):
        return len(self._card_list)

    @property
    def rotation(self):
        return self.__rotation

    def is_full(self) -> bool:
        return self.__count_card >= self.max_card  # because count card is index

    def get_card(self):
        for i in range(self.__count_card):
            if self._card_list[i] is not None:
                yield self._card_list[i]

    def update_image(func) -> None:
        """Update image decorator

        This will update the image of the whole list.
        Use with any function that would change the images.

        Args:
            func (function)
        """
        def inner(*args, **kwargs):
            func(*args, **kwargs)

            """ render image """
            self: __HandHolder = args[0]
            for i in range(self.__count_card):
                self._label_list[i].config(
                    image=self._card_list[i].image(inverse_ratio=config.CARD_SCALE, rotation=self.rotation))

        return inner

    @update_image
    def __hit_card(self, card: Card) -> None:
        """Add one card into hand
        NOTE: Default is cards are foleded

        Args:
            card (Card): card

        Raises:
            IndexError: Maximum capacity reached
        """

        if self.is_full():
            raise IndexError(
                "Invalid card: index out of range; Hand maximum capacity has reached.")

        # storing card and its image
        self._card_list[self.__count_card] = card
        self.__count_card += 1

    def hit_deck(self, deck: Deck) -> Card:
        card = None
        if not self.is_full() and not deck.is_empty():
            card = deck.deal_card()
            self.__hit_card(card)

        return card

    @update_image
    def unfold_cards(self) -> None:
        for i in range(self.__count_card):
            self._card_list[i].folded = False

    def clear_cards(self) -> None:
        for i in range(self.max_card):
            self._card_list[0] = None
            self._label_list[i].config(image=str())

        self.__count_card = 0


class Hand(__HandHolder):
    def __init__(self, name: str, master_frame: Frame, max_cards: int, rotation: int = 0) -> None:
        super().__init__(name, master_frame, max_cards, rotation)

        self.__money = 0

    @property
    def score(self) -> int:
        """Calculate score from the every cars in hands

        Returns:
            int: score
        """
        self.__score = 0
        joker_count = 0
        ace_count = 0

        # calculating the base points for all cards
        for card in self.get_card():
            if card.rank == 15:  # joker
                joker_count += 1
            elif card.rank == 14:  # ace
                ace_count += 1

            elif card.rank > 10:  # nobel card
                self.__score += 10
            else:
                self.__score += card.rank

        # only ace and joker
        for i in range(ace_count):
            self.__score += 11

        for i in range(ace_count):
            if self.__score > 21:
                self.__score -= 10  # switch to 1

        remain_score = 21 - self.__score
        if remain_score < joker_count:  # over 21
            return -1

        if remain_score < 11 * joker_count:  # lower  than 21 but still
            return 21                       # can use joker to get 21

        self.__score += 11 * joker_count    # too low to get 21

        if self.__score > 21:  # over 21
            self.__score = 21 - self.__score
            return self.__score

        if self.__score < 16:  # lower than 16 is lower
            self.__score = -16
            return self.__score

        if self.is_full() and self.__score < 21:
            self.__score = 22
            return self.__score  # five cards and below 21 should be higher

        return self.__score

    @property
    def money(self) -> int:
        return self.__money

    @money.setter
    def money(self, value: int) -> None:
        if type(value) is not int:
            raise ValueError("Money must be a int type")

        if value < 0:
            value = 0
            raise ValueError("Money can not be negative")
        self.__money = value

    def __lt__(self, __value: object) -> bool:
        if type(__value) is not Hand:
            raise TypeError("Invalid comparasion between two different object")
        return self.score < __value.score

    def __eq__(self, __value: object) -> bool:
        if type(__value) is not Hand:
            raise TypeError("Invalid comparasion between two different object")
        return self.score == __value.score

    def __repr__(self) -> str:
        return f"@{self.name} @{self.money}"


def load_from_string(data: str) -> tuple[str, int]:
    """Load name and money for Hand from string

    Args:
        data (str): repr of Hand

    Returns:
        tuple[str, int]: name and money
    """
    data = data[1:].split("@")
    return data[0], int(data[1])


if __name__ == "__main__":
    # from cards import Deck, Card
    ...
