from tkinter import *


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

    def __init__(self, master_frame, max_cards, row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, borderwidth=0, vertical=False, name=str(), money=0) -> None:
        self.__frame = LabelFrame(master_frame, text=name, bd=borderwidth)

        if not vertical:
            self.__frame.pack(pady=pady, ipady=ipady)
        else:
            self.__frame.pack(padx=padx, ipadx=ipadx)

        self.__card_slots = [Label] * max_cards
        self.__image_list = [Image] * max_cards
        self.__cards = [None] * max_cards

        for i in range(max_cards):
            self.__card_slots[i] = Label(self.__frame, text=str())
            if not vertical:
                self.__card_slots[i].grid(
                    row=row, column=i, pady=pady, padx=padx)
            else:
                self.__card_slots[i].grid(column=column, row=i,
                                          pady=pady, padx=padx)

        self.__count_card = 0  # for convience in tracking card

    def get_hand(self):
        """Iterate through hand's card

        Yields:
            Card: card
        """
        for c in self.__cards:
            if c is not None:
                yield c

    def hit_card(self, card) -> None:
        """Add one card into hand

        Args:
            card (Card): card

        Raises:
            IndexError: Maximum capacity reached
        """
        if self.__count_card + 1 > len(self.__card_slots):
            raise IndexError(
                "Invalid card: index out of range; Hand maximum capacity has reached.")

        current_slot = self.__count_card
        self.__count_card += 1
        # storing card and its image
        self.__cards[current_slot] = card
        self.__image_list[current_slot] = card.image

        # show cards
        self.__card_slots[current_slot].config(
            image=self.__image_list[current_slot])

    def clear_hand(self) -> None:
        """Clear all cards from hand
        """
        self.__count_card = 0
        # not clearing cards slot because not needed
        self.__image_list = [Image] * len(self.__image_list)
        self.__cards = [None] * len(self.__cards)


class Hand(_HandHolder):
    def __init__(self, master_frame, max_cards, row=0, column=0, padx=0, pady=0, ipadx=0, ipady=0, borderwidth=0, vertical=False, name=str()) -> None:
        super().__init__(master_frame, max_cards, row, column,
                         padx, pady, ipadx, ipady, borderwidth, vertical, name)

        self.__score = 0

    @property
    def score(self) -> int:
        """Calculate score from the every cars in hands

        Returns:
            int: score
        """
        self.__score = 0
        joker_count = 0
        ace_count = 0

        for card in self.get_hand():
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
        print(remain_score, ace_count, joker_count)
        if remain_score < joker_count:  # over 21
            return -1

        if remain_score < 11 * joker_count:
            return 21

        self.__score += 11 * joker_count

        if self.__score > 21:
            return -1
        return self.__score

    def __lt__(self, __value: object) -> bool:
        return self.score > __value.score

    def __eq__(self, __value: object) -> bool:
        return self.score == __value.score
