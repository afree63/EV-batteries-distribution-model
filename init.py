from source.processData.processHourlyData import *
from source.simulateOrder.populateData import *
from source.processData.latLongBoundary import *
from source.processData.processData import *
from source.services.service import *

import os

# Variables to change for comparisons

number_of_medians = 20                                  # compare
# number_of_cars_in_hub = 5                               # compare
# number_of_cars_in_farm = 5                              # compare
hub_car_capacity = 5
farm_car_capacity = 50
# initial_charged_battery_in_hub = 50                     # compare
# initial_charged_battery_in_farm = 50                    # compare
initial_zero_charged_battery_in_farm = 100000           # compare
days_of_simulation = 7
hourToCover = 2
ordersPerDay = 2617                                                 # 10468/4 = 2617 (total EV count in the covered area = 10468)

solar_farm_latLong = [(40.85, -72.86), (40.77, -73.26)]             # (40.85, -72.86) -> Long Island Solar (40.77, -73.26) -> Brentwood Solar


initial_charged_battery_in_hubs = [50, 100]
initial_charged_battery_in_farms = [0, 100]
number_of_cars_in_hubs = [1,5,10,15,20]
number_of_cars_in_farms = [1, 5, 10, 15]



processNodes()          # O(total number of nodes)
processLinks()          # O(number of links)

initalMedians = generate_medians(list_of_nodes, number_of_medians)              # O(nlogn) of the number of samples -> can be improved for the logn, and more randomized data

# not necessary to change unless 100 iterations are completed, 
# or RAM cannot handle, in that case use the previously calculated medians as new medians
number_of_maximum_iterations = 100

from source.clusterData.kMeans import kMeans

kCluster = kMeans(initalMedians)               

print("Start clustering")

kCluster.kClusterData(number_of_maximum_iterations)                 # O(number of iterations * number of medians * total number of nodes)
kCluster.save_data()

kCluster.distanceServiceRef.node_to_node_distance = {}

populateLatLong(number_of_medians)          # O(number of median * number of node in each cluster) = O(total number of nodes)
updateMedians()                             # O(number of medians)
processHourlyData()                          # O(traffic data available) -> O(n)

solar_farm_nodes = []

for item in solar_farm_latLong:             # O(number of farms * total number of nodes)
    solar_farm_nodes.append(findNearestNode(latlong_to_node, item[0], item[1]))             # O(total number of nodes)

from source.simulateOrder.basicSimulation import basicSimulation

folderPath = 'simulationResults/medians_' + str(number_of_medians)
os.makedirs(folderPath, exist_ok=True)

for initial_charged_battery_in_hub in initial_charged_battery_in_hubs:
    for initial_charged_battery_in_farm in initial_charged_battery_in_farms:
        for number_of_cars_in_hub in number_of_cars_in_hubs:
            for number_of_cars_in_farm in number_of_cars_in_farms:
                print('=========', 'initial battery in hub:', initial_charged_battery_in_hub, 'initial battery in farm:', initial_charged_battery_in_farm, 'cars in hub:', number_of_cars_in_hub, 'cars in farm:', number_of_cars_in_farm, '=========')
                path = folderPath + '/batteryInFarm-' + str(initial_charged_battery_in_farm) + '-batteryInHub-' + str(initial_charged_battery_in_hub) + '-farmCar-' + str(number_of_cars_in_farm) + '-hubCar-' + str(number_of_cars_in_hub)
                os.makedirs(path, exist_ok=True)

                basicSimulation.simulate(
                    days_of_simulation,
                    number_of_medians, 
                    number_of_cars_in_hub, 
                    number_of_cars_in_farm, 
                    hub_car_capacity, 
                    farm_car_capacity,
                    initial_charged_battery_in_hub, 
                    initial_charged_battery_in_farm, 
                    initial_zero_charged_battery_in_farm,
                    hourToCover,
                    solar_farm_nodes,
                    ordersPerDay,
                    path
                )
