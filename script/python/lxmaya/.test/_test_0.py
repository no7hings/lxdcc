# coding:utf-8

a = [(0.0, 0.0), (0.5, 0.0), (0.5, 0.5), (0.0, 0.5), (0.5, 0.0), (1.0, 0.0), (1.0, 0.5), (0.5, 0.5), (0.0, 0.5), (0.5, 0.5), (0.5, 1.0), (0.0, 1.0), (0.5, 0.5), (1.0, 0.5), (1.0, 1.0), (0.5, 1.0)]

b = sorted(set(a), key=a.index)
print b
c = []
for i in a:
    c.append(b.index(i))

print c

print 'ae_osl_color_correct'[len('ae_'):]


