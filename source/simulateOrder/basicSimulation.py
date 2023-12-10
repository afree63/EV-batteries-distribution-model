from source.processOrder.processOrders import orderProcessing
from source.services.service import *
from source.processData.latLongBoundary import *

class basicSimulation:
    def simulate(
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
    ):
        orders = orderProcessing(
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
            ordersPerDay
        )
        orders.populateData()                                                             # O(nlogn) + O(number of medians * car in hub) + # O(number of farm * car in farm) + 2 * O(number of solar farm data)
        orders.time_to_order = populateOrders(orders.time_to_order)                       # O(nlogn), n = number of orders

        day = 0
        second = 0

        previousOrder = 0
        previousReject = 0

        previousRejectDay = 0
        batteryAskedDay = 0

        while second < 86400:
            time = day*86400 + second
            second += 1

            if time % 3600 == 0:
                print("Time Now:", second_to_time(time), "Orders in last hour:", orders.order_count - previousOrder, "Rejected in last hour:", orders.total_rejected - previousReject)
                previousOrder = orders.order_count
                previousReject = orders.total_rejected

            if second == 86400 and day < days_of_simulation-1:
                day += 1
                second = 0
                print("========= Last day report =========")
                print("Orders rejected last day:", orders.total_rejected - previousRejectDay)
                print("Battery asked from farm in last day:", orders.battery_asked - batteryAskedDay)
                print("Battery in hubs:", orders.battery_in_hub)
                print("Charged battery in farms:", orders.charged_battery_in_farm)
                print("===================================")
                previousRejectDay = orders.total_rejected
                batteryAskedDay = orders.battery_asked
                # orders.time_to_order = generate_order_data(ordersPerDay, list_of_nodes, orders.time_to_order, day)          # O(nlogn), n = number of orders

            number_of_farm = len(solar_farm_nodes)

            for farm_index in range(number_of_farm):                                    # O(number of farm * 2 * maximum charge hour)
                orders.chargeBatteryInfarm(time, farm_index, 7.5)                       # O(2 * maximum charge hour)

            orders.prioritizeWaitingHubs(time)            # Important                   # O(nlogn), n = number of medians +  O(number of farms * number of farm car * nlogn), n = number of nodes, same as processOrder for memoization

            orders.supplyBatteryToHub(time)                                             # O(number of battery request * nlogn), n = number of nodes
            orders.batteryToFarm(time)                                                  # O(number of battery request) 

            orders.processOrder(time)                     # Important                   # O(number of orders * number of hub cars * nlogn), n = number of nodes  -> O(number of orders * number of hub cars) + O(nlogn), with memoization


        print("Battery asked from HUB:", orders.battery_asked, " times")
        print("Battery supplied HUB:", orders.battery_supplied, " times")
        print("Total rejected orders:", orders.total_rejected, " times")
        print("Rejected for batteries each hub:", orders.rejected_for_battery)

        log_summary = [("Battery asked from HUB:", orders.battery_asked), ("Battery supplied HUB:", orders.battery_supplied), ("Total rejected orders:", orders.total_rejected), ("Rejected for batteries each hub:", orders.rejected_for_battery)]
        logSummary_df = pd.DataFrame(log_summary)
        logSummary_df.to_csv(path + '/logSummary.csv')

        confirmData_df = pd.DataFrame(orders.confirmOrderData)
        confirmData_df.columns = ['Order Node', 'Hub No.', 'Time of Order', 'Waiting Time', 'Time of Delivery', 'Time To Reach', 'Previous Location', 'Car Index', 'Battery Left in Car']
        confirmData_df.to_csv(path + '/confirmedOrders.csv')

        rejectData_df = pd.DataFrame(orders.rejectOrderData)
        rejectData_df.columns = ['Order Node', 'Hub No.', 'Time of Order', 'Wait upto', 'Minimum Time for Delivery', 'Reason for Rejection']
        rejectData_df.to_csv(path + '/rejectedOrders.csv')

        carData_df = pd.DataFrame(orders.carData)
        carData_df.columns = ['Hub No.', 'Car Index', 'Time When Reach Hub', 'Time on Road']
        carData_df.to_csv(path + '/carReachHub.csv')

        hubData_df = pd.DataFrame(orders.hubData)
        hubData_df.columns = ['Hub No.', 'Time of Request', 'Number of Battery Requested', 'Remaining Battery in Hub', 'Battery on the Road', 'Farm Index', 'car Index', 'delivery Time']
        hubData_df.to_csv(path + '/hubRequests.csv')

        farmData_df = pd.DataFrame(orders.farmData)
        farmData_df.columns = ['Farm Index', 'Time', 'Battery Charged to Full', 'Number of Uncharged Batteries']
        farmData_df.to_csv(path + '/farmChargeFull.csv')

