def score(self) -> int:
    score = 0
    joker_count = 0
    ace_count = 0

    for card in self:
        if card == 15:  # joker
            joker_count += 1
        elif card == 14:  # ace
            ace_count += 1

        elif card > 10:  # nobel card
            score += 10
        else:
            score += card

    # only ace and joker
    for i in range(ace_count):
        score += 11

    for i in range(ace_count):
        if score > 21:
            score -= 10  # switch to 1

    remain_score = 21 - score
    print(remain_score, ace_count, joker_count)
    if remain_score < joker_count:  # over 21
        return -1

    if remain_score < 11 * joker_count:
        return 21

    score += 11 * joker_count

    if score > 21:
        return -1
    return score


l = [15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 10, 15]
print(score(l))
