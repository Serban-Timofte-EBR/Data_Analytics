# Avem un array de prețuri ale unei acțiuni: [1, 6, 3, 6, 4, 9, 3, 4].
# Scrie un program care determină tranzacția (cumpărare-vânzare) cu cel mai mare profit posibil.

prices = [1, 6, 3, 6, 4, 9, 3, 4]

def calculateMaxProfit(prices):
    maxProfit = 0
    for i in range(len(prices)):
        for j in range(i+1, len(prices)):
            maxProfit = max(maxProfit, prices[j] - prices[i])
    return maxProfit

def calculateMaxProfitOn(prices):
    minPrice = float("inf")
    maxProfit = 0

    for price in prices:
        minPrice = min(minPrice, price)
        maxProfit = max(maxProfit, price - minPrice)

    return maxProfit

profit = calculateMaxProfit(prices)
print("Profitul maxim: " + str(profit))

profitOn = calculateMaxProfitOn(prices)
print("Profiton maxim: " + str(profitOn))