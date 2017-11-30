def handle_numbers(x, y, z):
    if z == 0:
        return "You can't divide by zero"
    if x > y:
        x, y = y, x

    return len([n for n in range(x, y + 1) if n % z == 0])


def handle_string(value):
    letters = 0
    digits = 0
    for i in value:
        if i.isalpha():
            letters += 1
        if i.isdigit():
            digits += 1

    return 'There are %s letters and %s digits' % (letters, digits)


def handle_list_of_tuples(l):
    return sorted(l, key=lambda person: (person[0], person[1], person[2], person[3]))
