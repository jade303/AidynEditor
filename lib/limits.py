# limits the same size
from tkinter import END


def limit_name_size(name, name_length, *args):
    n = name.get()
    if len(n) > name_length:
        name.set(n[:name_length])


# sets appropriate limits
# 'i' is what is being limited
# 'x' is the MAX value
def limit(i, x, *args):
    if i.get() == '00':
        i.set('0')
    if not i.get().isnumeric():
        val = ''.join(filter(str.isnumeric, i.get()))
        i.set(val)
    elif i.get().isnumeric():
        if int(i.get()) > x:
            i.set(x)
        else:
            i.set(i.get())


# check for neg/pos 127
def limit_127(i, *args):
    if i.get() == '00':
        i.set('0')
    val = i.get()
    if len(val) > 0 and val[0] == '-':
        if val == '-':
            return
        else:
            val = val[1:]
        if not val.isnumeric():
            val = ''.join(filter(str.isnumeric, val))
            i.set(int(val) * -1)
        elif val.isnumeric():
            if int(val) > 127:
                i.set('-128')
            else:
                i.set(int(val) * -1)
    else:
        if not val.isnumeric():
            val = ''.join(filter(str.isnumeric, val))
            i.set(val)
        elif val.isnumeric():
            if int(val) > 127:
                i.set(127)
            else:
                i.set(val)
