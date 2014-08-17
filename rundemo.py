#!/usr/bin/env python

"""
author: Lu LIU
created at: 2014-07-25
Description:
    a sample of how to use pymmrouting to find multimodal optimal paths in
    transportation networks
"""

from pymmrouting import routeplanner
#from pymmrouting import datamodel
from pymmrouting import inferenceengine
from termcolor import colored

# For multimodal routing, a bunch of options are necessary other than routing
# origin and destination. The acceptable format of multimodal routing options
# are stored in a JSON file.
print "Generating multimodal routing plans... ",
inferer = inferenceengine.RoutingPlanInferer()
inferer.load_routing_options('./multimodal_routing_options.json')
# Routing plans of multimodal paths calculation can be generated by the
# inference engine with the routing options as inputs
routing_plans = inferer.generate_routing_plan()
print colored("done!", "green")

route_planner = routeplanner.RoutePlanner()
# A multimodal network data model is necessary for multimodal path finding. It
# loads network dataset from external sources, e.g. PostgreSQL database, plain
# text file, etc.
print "Connecting to multimodal data source... ",
# In this sample, the multimodal graph data set is stored in PostgreSQL
# database
route_planner.open_datasource(
    "POSTGRESQL",
    "dbname = 'sample_db' user = 'user' password = 'password'")
print colored("done!", "green")
# A multimodal network is assembled on-the-fly according to a concrete routing
# plan
for p in routing_plans:
    # FIXME: should be coordinates
    if p.mode_list[0] == 1001:
        p.source = 100101036067
    else:
        p.source = 100201006726
    if p.mode_list[-1] == 1001:
        p.target = 100101036092
    else:
        p.target = 100201006499
    print "Calculating multimodal path for routing plan: '" \
        + p.description + "'... "
    print "Routing from " + colored(str(p.source), "red") \
        + " to " + colored(str(p.target), "red")
    result = route_planner.find_path(p)
    print colored("Finish doing routing plan!", "green")
    print "Routing result is: "
    print "Total distance: ",
    print colored(str(result.length), "red"),
    print " meters"
    print "Total time (estimated): ",
    print colored(str(result.time), "red"),
    print " minutes"
    print "Total walking distance: ",
    print colored(str(result.walking_length), "red"),
    print " meters"
    print "Total walking time (estimated): ",
    print colored(str(result.walking_time), "red"),
    print " minutes"
    # Routing results contain all information related to the found paths which
    # can be rendered on top of a base map like MapBox
    result.show_on_map('MAPBOX')
route_planner.close_datasource()
