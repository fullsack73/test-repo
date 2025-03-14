a = int(input())
b = int(input())
c = int(input())

def max_num(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= a and b >= c:
        return b
    else:
        return c

print(max_num(a, b, c))