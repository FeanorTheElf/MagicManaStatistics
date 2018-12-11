import math

def evalTurn(deck, hand, lands, turnDepth):
    if turnDepth == 0:
        return 0

    totalCardsInDeck = sum(deck)
    totalEval = 0
    for cardType in range(len(deck)):
        if deck[cardType] == 0:
            continue

        hand[cardType] += 1
        oldHand = hand[:]
        deck[cardType] -= 1
        currentEval = 0

        if hand[0] > 0:
            hand[0] -= 1
            lands += 1
        availableMana = lands
        for playCardType in reversed(range(1, len(hand))):
            while hand[playCardType] > 0 and availableMana >= playCardType:
                currentEval += playCardType
                hand[playCardType] -= 1
                availableMana -= playCardType

        currentEval += evalTurn(deck, hand, lands, turnDepth - 1)

        if oldHand[0] > 0:
            lands -= 1
        hand = oldHand
        deck[cardType] += 1
        hand[cardType] -= 1

        totalEval += currentEval * (deck[cardType] / totalCardsInDeck)
    return totalEval

assert evalTurn([5, 5], [0, 0], 0, 1) == 0
assert evalTurn([5, 5], [1, 0], 0, 1) == 0.5
assert evalTurn([5, 5], [0, 0], 0, 2) == 0.5555555555555556

def binomial(k, n):
    return math.factorial(n)/math.factorial(k)/math.factorial(n-k)

def drawCardsThenPlay(deck, hand, cardNumber, turnDepth, result):
    def forCardCombination(cards):
        for cardType in range(len(deck)):
            if cards[cardType] > deck[cardType]:
                return

        probability = 1
        for cardType in range(len(deck)):
            probability *= binomial(cards[cardType], deck[cardType])
        probability /= binomial(cardNumber, sum(deck))

        for cardType in range(len(deck)):
            deck[cardType] -= cards[cardType]

        result[0] += evalTurn(deck, cards[:], 0, turnDepth) * probability

        for cardType in range(len(deck)):
            deck[cardType] += cards[cardType]
    bucketDistributions(len(deck), cardNumber, [0 for i in deck], forCardCombination)

def bucketDistributions(buckets, elements, current, f):
    if buckets == 1:
        current[0] = elements
        f(current)
        return
    for currentBucketEls in range(elements + 1):
        current[buckets - 1] = currentBucketEls
        bucketDistributions(buckets - 1, elements - currentBucketEls, current, f)

testExpected = (1/2 * (4/9 * (3/8 * 5/7 + 5/8 * (3/7 + 4/7 * 2)) + 
                       5/9 * (4/8 * (3/7 + 4/7 * 2) + 4/8 * 2)) + 
                1/2 * (5/9 * (4/8 * (3/7 + 4/7 * 2) + 4/8 * 2) + 
                       4/9 * (5/8 * 2 + 3/8 * 5/7)))
testActual = [0]
drawCardsThenPlay([5, 5], [0, 0], 2, 2, testActual)
assert math.fabs(testActual[0] - testExpected) < 0.00001

deck = [31, 9, 8, 7, 6, 4, 2]
result = [0]
drawCardsThenPlay(deck, [0, 0, 0, 0, 0, 0, 0], 7, 5, result)
print(result)