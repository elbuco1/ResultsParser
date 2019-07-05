
def truncate(number,n_decimal):
    number_td = int(number * 10**n_decimal)/10**n_decimal
    return number_td