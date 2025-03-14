a = int(input())
b = int(input())
c = int(input())
d = int(input())

def interval_intersection(a, b, c, d):

    start = max(a, c)
    end = min(b, d)
    
    if start <= end:
        return end - start
    else:
        return 0
    
print(interval_intersection(a, b, c, d))