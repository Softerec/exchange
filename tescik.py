# .t0
# 001
#    .t1
#    002
#       .t2
#    003
#       .t3

p = print

import pprint
prpr = pprint.PrettyPrinter(indent=2)

pp = prpr.pprint

ta='ta'
tb='tb'
tc='tc'
td='td'
p()
p()

#

i1 = 2
i2 = 1
i3 = 1

#

T3 = [td, td]
T2 = [tc, tc]
T1 = [tb, tb, T2 * i2, T3 * i3]
T0 = [ta, ta, T1] * i1

pp(T0)

p()
p()

#

P3 = ['i3']
P2 = ['i2']
P1 = [P2 * i2, P3 * i3]
P0 = [P1] * i1

pp(P0)
