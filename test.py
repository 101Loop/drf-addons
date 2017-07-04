from collections import defaultdict


def min_s_d(t, a):
    d = abs(t-a)
    e = 60 - d
    return (d, 0) if d < e else ((e, -1) if t < a else (e, 1))


def min_h_d(t, a):
    d = abs(t-c-a)
    return min(d, 24 - d)


def min_t_d(t, aih, aim, ais):
    sec = abs(t[2] - ais)
    min = abs(t[1] - aim)
    hor = abs(t[0] - aih)
    if sec == 30:
        min -= 1
    else:
        min
    if min == 30:
        hor -= 1
    t[1] += m
    mi, m = min_s_d(t[1], aim)
    t[0] += m
    return min_h_d(t[0], aih)

tc = int(input())
ct = []
at = []
cst_map = defaultdict(dict)


for x in range(tc):
    c, a = map(int, input().split())
    for k in range(c):
        ct.append(list(map(int, input().split(':'))))
    for y in range(a):
        ail, aim, ais = map(int, input().split(':'))
        at.append([ail, aim, ais])
        for z in range(c):
            cst = min_t_d(ct[z], ail, aim, ais)
            cst_map[cst].setdefault(y, []).append(z)
print(cst_map)