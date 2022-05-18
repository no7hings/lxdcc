# coding:utf-8
import rez.resolved_context as r_c

import rez.utils.graph_utils as r_g

r = r_c.ResolvedContext(
    ['lxdcc']
)

g = r.graph()

print str(r_g.write_compacted(g))
print str(r_g.write_dot(g))

# r_g.view_graph()


