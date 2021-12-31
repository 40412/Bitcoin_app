from datetime import datetime
import datetime
from pycoingecko import CoinGeckoAPI

def date_to_timestamp(dateobject):
    value = datetime.datetime.strptime(dateobject, "%d/%m/%Y").replace(tzinfo=datetime.timezone.utc).timestamp()
    return value

def timestamp_to_readable_date(stamp):
    return datetime.datetime.utcfromtimestamp(stamp).strftime('%d/%m/%Y %H:%M:%S')

def get_data(from_date, to_date):
    cg = CoinGeckoAPI()
    data = cg.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='eur',from_timestamp=from_date,to_timestamp=to_date)
    return data

def get_day_price(fromdate, todate, prices):
    day_now = 0
    data = get_data(fromdate, todate)
    filtered_data = data.get("prices")
    for data in filtered_data:
        if day_now == 0:    
            prices[data[0]] = data[1]
            day_now = data[0]
        elif data[0] >= day_now + 84600000:
            prices[data[0]] = data[1]
            day_now = data[0]

def calculate_bearish(prices):
    count = 0
    longest_bearish = 0
    last_price = 0
    for price in prices.values():
        if last_price != 0 and last_price > price:
            count += 1
            last_price = price
            if longest_bearish < count:
                longest_bearish = count
        elif last_price == 0:
            last_price = price
        else:
            if longest_bearish < count:
                longest_bearish = count
            count = 0
            last_price = price
    return longest_bearish

def highest_volume(data):
    vd = data.get("total_volumes")
    volume = 0
    date_of_highest = 0
    for data in vd:
        date = data[0]
        vol = data[1]
        if vol > volume:
            volume = vol
            date_of_highest = date

    return " " + str(timestamp_to_readable_date(date_of_highest / 1000)) + " Volume: " + str(volume) + " euros"

def lowest_and_highest_price(data):
    prices = data
    lowest = 0
    highest = 0
    lowest_day = 0
    highest_day = 0
    for x in prices.items():
        day = x[0]
        price = x[1]
        if lowest_day == 0 or highest_day == 0:
            lowest_day = day
            highest_day = day
            lowest = price
            highest = price
        if price < lowest:
            lowest = price
            lowest_day = day
        if price > highest:
            highest = price
            highest_day = day

    if int(calculate_bearish(prices)) == len(prices) - 1:
        l = []
        l.append("There is no good day to sell or buy in given range")
        return l
    else:
        stamp1 = int(lowest_day) / 1000
        stamp2 = int(highest_day) / 1000
        low = str(timestamp_to_readable_date(stamp1)) + " Price: " + str(lowest)
        high = str(timestamp_to_readable_date(stamp2)) + " Price: " + str(highest)
        l = []
        l.append(low)
        l.append(high)
        return l

def is_valid(datestring):
    
    try:
        datetime.datetime.strptime(datestring, "%d/%m/%Y")
        return True
    except ValueError:
        return False