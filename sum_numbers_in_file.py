import csv
import datetime

d0 = datetime.date(2023, 12, 31)
d1 = datetime.date(2024, 12, 31)
balinit = {"EUR": 8147.42, "GBP": 17791.13, "USD": 0}
balance = balinit.copy()
balmax = balance.copy()
balmin = balance.copy() 
balave = balance.copy() 
for ccy in balave:
    balave[ccy] = balance[ccy] * (d1 - d0).days
with open('transaction-history.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        direction = row['Direction']
        sign = 0
        if direction == 'IN':
            sign = 1
        if direction == 'OUT' or direction == 'NEUTRAL':
            sign = -1
        if sign != 0:
            d = datetime.date.fromisoformat( row['Finished on'][:10])
            ccy = row['Source currency']
            x = float(row['Source amount (after fees)'])
            if row['Source fee amount'] != '':
                x += float(row['Source fee amount'])
            x *= sign
            if ccy not in balance:
                balance[ccy] = 0
            balance[ccy] -= x
            if balance[ccy] > balmax[ccy]:
                balmax[ccy] = balance[ccy]
            if balance[ccy] < balmin[ccy]:
                balmin[ccy] = balance[ccy]
            balave[ccy] -= x * (d - d0).days
        if direction == 'NEUTRAL' and ccy != row['Target currency']:
            tccy = row['Target currency']
            if tccy not in balance:
                balance[tccy] = 0
            # print (tccy, round(balance[tccy], 2))
            x = -float(row['Target amount (after fees)'])
            balance[tccy] += x
            if balance[tccy] > balmax[tccy]:
                balmax[tccy] = balance[tccy]
            if balance[tccy] < balmin[tccy]:
                balmin[tccy] = balance[tccy]
            balave[tccy] += x * (d - d0).days
            # print((d - d0).days, d, ccy, round(x, 2), round(balance[ccy], 2), tccy, round(balance[tccy], 2))
x = 1 / (d1 - d0).days
for ccy in balave:
    balave[ccy] *=  x
print ("CCY", d0, d1, "MAX MIN AVERAGE")
for ccy in balance:
    print(ccy
          , round(balinit[ccy], 2)
          , round(balance[ccy], 2)
          , round(balmax[ccy], 2)
          , round(balmin[ccy], 2)
          , round(balave[ccy], 2)
          )
