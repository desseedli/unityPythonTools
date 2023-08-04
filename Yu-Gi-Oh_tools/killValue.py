import random
from collections import Counter
deck = []
hardCards = []
keyCards = {
    "a": {
        "num": 8,
        "required": 1
    },
    "b": {
        "num": 5,
        "required": 1
    },
    "c": {
        "num": 7,
        "required": 1
    },
}

for key in keyCards:
    for _ in range(keyCards[key]["num"]):
        deck.append(key)

deck += [None for i in range(40 - len(deck))]

drawCount = 6
validDrawCount = 0
simulationCount = input("simulationCount:\n")
for count in range(int(simulationCount)):
    random.shuffle(deck)
    denominator = 0
    molecule = 0 
    handCards = random.sample(deck,drawCount)
    cardCounter = Counter(handCards)
    isValid = True
    for key in keyCards:
        if cardCounter[key] < keyCards[key]["required"]:  
            isValid = False
            break
    validDrawCount += 1 if isValid else 0
print(validDrawCount / int(simulationCount))

