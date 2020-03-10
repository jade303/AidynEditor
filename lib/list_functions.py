from lib.variables import ITEM_DIC, POTIONS


def build_lst(filename, addresses, name_length):
    # builds a list from addresses in a dictionary
    lst = []
    with open(filename, 'rb') as f:
        for a in addresses:
            f.seek(a)
            lst.append(f.read(name_length).decode("utf-8").rstrip('\x00'))
    return lst


def get_minor_dic(filename, dic, name_length):
    # ID/Name key/value dictionary
    # dictionary keys must be addresses
    lst = []
    with open(filename, 'rb') as f:
        for a in dic.keys():
            f.seek(a)
            lst.append(f.read(name_length).decode("utf-8").rstrip('\x00'))
    return {**{'0000': 'NONE'}, **dict(zip(dic.values(), lst))}


def get_major_dic(filename):
    # ID/Name key/value dictionary
    # with added (type) to item
    lst = []
    with open(filename, 'rb') as f:
        for i in ITEM_DIC:
            if list(ITEM_DIC).index(i) < 49:
                f.seek(i)
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(acc) " + word)
            if 48 < list(ITEM_DIC).index(i) < 97:
                f.seek(i)
                word = f.read(22).decode("utf-8").rstrip('\x00')
                lst.append("(armor) " + word)
            if 96 < list(ITEM_DIC).index(i) < 159:
                f.seek(i)
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(other) " + word)
            if list(ITEM_DIC).index(i) == 159:
                for p in POTIONS.keys():
                    lst.append(p)
            if 173 < list(ITEM_DIC).index(i) < 237:
                f.seek(i)
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(scroll) " + word)
            if 236 < list(ITEM_DIC).index(i) < 257:
                f.seek(i)
                word = f.read(22).decode("utf-8").rstrip('\x00')
                lst.append("(shield) " + word)
            if 256 < list(ITEM_DIC).index(i) < 280:
                f.seek(i)
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(wand) " + word)
            if 279 < list(ITEM_DIC).index(i):
                f.seek(i)
                word = f.read(21).decode("utf-8").rstrip('\x00')
                lst.append("(weapon) " + word)
    return {**{'0000': 'NONE'}, **dict(zip(ITEM_DIC.values(), lst))}
