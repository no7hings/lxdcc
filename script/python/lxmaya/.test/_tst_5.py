# coding:utf-8

m = [
    1.0, .0, .0, .0,
    .0, 1.0, .0, .0,
    .0, .0, 1.0, .0,
    .0, .0, .0, 1.0
]

lis = []
for i in range(4):
    rows = []
    for j in range(4):
        rows.append(m[i*4+j])
    lis.append(rows)

print lis
