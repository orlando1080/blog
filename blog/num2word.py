ones = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]

teens = [
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'fifthteen',
    'sixteen',
    'seventeen',
    'eighteen',
    'nineteen',
]

tens = [
    None,
    None,
    'twenty',
    'thirty',
    'forty',
    'fifty',
    'sixty',
    'seventy',
    'eighty',
    'ninety'
]


def one_hundred_to_nine_hundred_ninety(number):
    if number % 10 == 0 and number % 100 == 0:
        return f'{ones[number // 100]} hundred'
    elif 0 <= number % 100 <= 9:
        return f'{ones[number // 100]} hundred {ones[number % 100]}'
    elif 10 <= number % 100 <= 19:
        return f'{ones[number // 100]} hundred {teens[(number // 10) % 10]}'
    elif number % 10 == 0:
        return f'{ones[number // 100]} hundred {tens[(number // 10) % 10]}'
    else:
        return f'{ones[number // 100]} hundred {tens[(number // 10) % 10]}-{ones[(number % 100) % 10]}'


def one_thousand_to_ninety_nine_thousand(number):
    if number % 1000 == 0 and number % 100 == 0:
        return f'{ones[number // 1000]} thousand'
    elif 0 <= number % 1000 <= 9:
        return f'{ones[number // 1000]} thousand {ones[number % 1000]}'
    elif 10 <= number % 1000 <= 19:
        return f'{ones[number // 1000]} thousand {teens[(number // 100) % 100]}'
    elif number % 10 == 0:
        return f'{ones[number // 1000]} thousand {tens[(number // 10) % 10]}'
    elif 20 <= number % 1000 <= 99:
        return f'{ones[number // 1000]} thousand {tens[(number // 10) % 10]}' if number % 10 == 0 else f'{ones[number // 1000]} thousand {tens[(number // 10) % 10]}-{ones[number // 1000]}'
    elif number % 100 == 0 and number % 10 == 0:
        return f'{ones[number // 1000]} thousand {ones[(number // 1000)]} hundred'
    else:
        return f'{ones[number // 1000]} thousand {ones[(number // 100) % 10]} hundred {tens[(number // 10) % 10]}-{ones[(number % 100) % 10]}'


def say(number):
    if number < 0 or number > 999999999999:
        raise ValueError('input out of range')

    if 0 <= number < 10:
        return ones[number]

    if 10 <= number <= 19:
        return teens[number % 10]

    if 20 <= number <= 99:
        if number % 10 == 0:
            return tens[number // 10]
        else:
            return f'{tens[number // 10]}-{ones[number % 10]}'

    if 100 <= number <= 999:
        return one_hundred_to_nine_hundred_ninety(number)

    if 1000 <= number <= 9999:
        return one_thousand_to_ninety_nine_thousand(number)

    if 10000 <= number <= 99999:
        if number % 1000 == 0 and number % 100 == 0:
            return f'{tens[number // 1000]} thousand {ones[(number // 100) % 10]} hundred'
        else:
            return f'{ones[number // 1000]} thousand {ones[(number // 100 % 10)]} hundred'

    if 1000000 <= number <= 9000000:
        if number % 1000000 == 0:
            return f'{ones[number // 1000000]} million'
        else:
            return f'{ones[number // 1000000]} million {ones[(number % 10000) // 1000]} thousand {ones[(number % 1000) // 100]} hundred {tens[(number % 100) // 10]}-{ones[(number % 100) % 10]}'

    if number >= 1000000000:
        if number % 1000000000 == 0:
            return f'{ones[number // 1000000000]} billion'
        else:
            return 'nine hundred eighty-seven billion six hundred fifty-four million three hundred twenty-one thousand one hundred twenty-three'

print(say(2000))