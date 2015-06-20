__author__ = 'max'

# Returns minimal buy or sell proposition
# buy_or_sell == 'buy' || 'sale'
def get_min(banks, buy_or_sale):
    min_item = banks[0]
    for bank in banks:
        if bank[buy_or_sale] < min_item[buy_or_sale]:
            min_item = bank
    return min_item


# Returns maximal buy or sell proposition
# buy_or_sell == 'buy' || 'sale'
def get_max(banks, buy_or_sale):
    max_item = banks[0]
    for bank in banks:
        if max_item[buy_or_sale] < bank[buy_or_sale]:
            max_item = bank
    return max_item


# Returns average buy or sell cost
# buy_or_sell == 'buy' || 'sale'
def get_average(banks, buy_or_sale):
    average = 0
    for bank in banks:
        average += bank[buy_or_sale]
    return average / len(banks)
