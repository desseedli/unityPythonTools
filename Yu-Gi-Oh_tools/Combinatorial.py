from scipy.special import comb,perm

deckTotalNum = input("Deck Total Count?\n")
putIntoKeyCardNum = input("put into key card count?\n")
isFirstHand = input("isFirstHand? Y or N\n")

drawCardNum = isFirstHand.upper() == 'Y' and 5 or 6
denominator = comb(int(deckTotalNum),drawCardNum)
molecule = comb(int(deckTotalNum) - int(putIntoKeyCardNum),drawCardNum)
relust = 1 - (molecule / denominator)

print("relust:",relust)

