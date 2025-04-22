# Example from Raymond Hettinger

import jnettool.tools.elements.NetworkElement, \
       jnettool.tools.Routing, \
       jnettool.tools.RouteInsector

ne = jnettool.tools.elements.NetworkElement('171.0.2.45')
try:
  routing_table = ne.getRoutingTable()  # fetch table
  
except jnettool.tools.elements.MissingVar:
  # Record table fault
  logging.exception('''No routing table found''')
  # Undo partial changes
  ne.cleanup('''rollback''')

else:
  num_routes = routing_table.getSize()  # determine table size
  for RToffset in range(num_routes):
    route = routing_table.getRouteByIndex(RToffset)
    name = route.getName()  # route name
    ipaddr = route.getIPAddr()  # ip address
    print "%15s -> %s" % (name, ipaddr)  # format nicely
finally:
  ne.cleanup('''commit''')  # lockin changes
  ne.disconnect()
