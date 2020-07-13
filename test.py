PC = (4.0+5.0)/2
PCT = 6.5


def alfa():
    if PC < 2.5:
        return 0
    if PC < 4.9:
        return (PC/7) - 0.35
    else:
        return 0.35


NF = PC * (1-alfa()) + PCT * alfa()

print(alfa())
print(NF)
