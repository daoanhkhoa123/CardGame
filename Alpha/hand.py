from tkinter import *
if __name__ != "__main__":
    from Alpha.cards import Card
else:
    from cards import Card


class _HandHolder:
    """ This is a class that is solely built for organizing card slot,
    storing cards, and rendering them to show on the screen.

    Imagine a  drawn frame of many slots where you put each card into those.
    It is drawn on the table without the care for player.

    Args:
        master_frame (Frame): the frame that this stays inside
        max_cards (int): the maximum amout of cards
        rotation (int): 0, 90, 180, 270.

    Atributes:
        frame (Frame): The frame to hold the slots. MIGHT BE REMOVED
        slot_list (list[Label]): list of card slots
        card_list (list[Card]): list of cards
        image_list (list[Image]): list of card images
    """

    def __init__(self, master_frame, max_cards, pad=0, borderwidth=0, vertical=False, rotation=0) -> None:
        """HandHolder should stay inside a frame. 
        That frame represent the whole player

        Handholder has a frame that contains labels, 
        each label shows a card. Number of labels is max_cards.

        Each label will be packed on grid either on x (horizontal),
        or y (vertical), along with pad for spacing between cards.
        The rotation (veriticality) is depend on rotation argument.
        """

        # lists delcaration
        self._label_list: list[Label] = [None] * max_cards
        self._card_list: list[Card] = [None] * max_cards

        """ Frame """
        self.__frame: LabelFrame = LabelFrame(
            master_frame, bd=borderwidth)
        self.__frame.pack()

        """ Card Label """
        for i in range(max_cards):
            self._label_list[i] = Label(  # one label one card
                self.__frame, text=str())
            if not vertical:
                self._label_list[i].grid(
                    row=0, column=i, pady=pad, padx=pad)
            else:
                self._label_list[i].grid(column=0, row=i,
                                         pady=pad, padx=pad)

        # ultility
        self.__count_card = 0  # for convience in tracking card

    def get_card(self):
        for i in range(self.__count_card):
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
            self: _HandHolder = args[0]
            for i in range(self.__count_card):
                self._label_list[i].config(image=self._card_list[i].image)

        return inner

    @update_image
    def hit_card(self, card: Card) -> None:
        """Add one card into hand
        NOTE: Default is cards are foleded

        Args:
            card (Card): card

        Raises:
            IndexError: Maximum capacity reached
        """
        if self.__count_card + 1 > len(self._label_list):
            raise IndexError(
                "Invalid card: index out of range; Hand maximum capacity has reached.")

        current_slot = self.__count_card
        self.__count_card += 1

        # storing card and its image
        self._card_list[current_slot] = card

    @update_image
    def unfold_cards(self) -> None:
        for i in range(self.__count_card):
            self._card_list[i].folded = False

    # I can not use @update_image since it would be
    # impossible to change the count_card attribute
    # changing #update_image would be too complex

    # since python garbage collector is shit, i have to do it manual

    # this is bullshit, i can not clear the card, please help
    def clear_cards(self) -> None:

        self._card_list.clear()
        for i in range(self.__count_card):
            self._label_list[i].config(image=None)
            ...

        self.__count_card = 0


class Hand(_HandHolder):
    def __init__(self, master_frame, max_cards, pad=0, borderwidth=0, vertical=False) -> None:
        super().__init__(master_frame, max_cards, pad, borderwidth, vertical)

        self.__score = 0
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

        if self.__score > 21:
            return -1
        return self.__score

    def __lt__(self, __value: object) -> bool:
        return self.score > __value.score

    def __eq__(self, __value: object) -> bool:
        return self.score == __value.score
