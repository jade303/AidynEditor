from variables import ITEM_DIC, inv_ITEM_DIC

lst = []
for i in ITEM_DIC.values():
    print(i[2:])
    if i[-2] == '13':
        f.seek(inv_ITEM_DIC.get(i))
        word = i
        lst.append("(amulet) " + word)
        print(word)
