from lib.variables import ITEM_DIC, POTIONS, inv_ITEM_DIC


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


def get_major_item_dic(filename):
    # ID/Name key/value dictionary
    # with added (type) to item
    count = 0
    lst = []
    val = []
    with open(filename, 'rb') as f:
        for i in ITEM_DIC.values():
            if i[2:] == '01':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(misc) " + word)
                val.append(i)
            if i[2:] == '05':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(armor) " + word)
                val.append(i)
            if i[2:] == '06':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(shield) " + word)
                val.append(i)
            if i[2:] == '07':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(weapon) " + word)
                val.append(i)
            if i[2:] == '09':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(helmet) " + word)
                val.append(i)
            if i[2:] == '0A':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(cloak) " + word)
                val.append(i)
            if i[2:] == '0B':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(glove) " + word)
                val.append(i)
            if i[2:] == '0C':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(ring) " + word)
                val.append(i)
            if i[2:] == '0D':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(wand) " + word)
                val.append(i)
            if i[2:] == '0E':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(belt) " + word)
                val.append(i)
            if i[2:] == '0F':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(boots) " + word)
                val.append(i)
            if i[2:] == '10':
                lst.append(list(POTIONS.keys())[count])
                count += 1
                val.append(i)
            if i[2:] == '11':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(scroll) " + word)
                val.append(i)
            if i[2:] == '12':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(key) " + word)
                val.append(i)
            if i[2:] == '13':
                f.seek(inv_ITEM_DIC.get(i))
                word = f.read(18).decode("utf-8").rstrip('\x00')
                lst.append("(amulet) " + word)
                val.append(i)
    lst, val = (list(t) for t in zip(*sorted(zip(lst, val))))
    return {**{'0000': 'NONE'}, **dict(zip(val, lst))}


def get_major_loot_lists(filename, addresses, name_length):
    name = []
    code = []
    address = []
    with open(filename, 'rb') as f:
        for a in addresses:
            f.seek(a)
            name.append(f.read(name_length).decode("utf-8").rstrip('\x00'))
            code.append(addresses.get(a))
            address.append(a)
    name, code, address = (list(t) for t in zip(*sorted(zip(name, code, address))))
    return name, code, address


def get_major_name_lists(filename, addresses, name_length):
    name = []
    address = []
    with open(filename, 'rb') as f:
        for a in addresses:
            f.seek(a)
            name.append(f.read(name_length).decode("utf-8").rstrip('\x00'))
            address.append(a)
    name, address = (list(t) for t in zip(*sorted(zip(name, address))))
    return name, address
