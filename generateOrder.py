import pandas as pd
from source.processData.latLongBoundary import *
from source.services.service import *

processNodes()          # O(total number of nodes)

days_of_simulation = 7              # change this if needed according to the same parameter in init.py
ordersPerDay = 2617                 # change this if needed according to the same parameter in init.py, 10468/4 = 2617 (total EV count in the covered area = 10468)

orders = []

for day in range(days_of_simulation):
    orders = generate_order_data(ordersPerDay, list_of_nodes, orders, day)

orders_df = pd.DataFrame(orders)
orders_df.columns = ['node', 'timeOfOrder', 'waitingTime']
orders_df.to_csv('assets/orders.csv')




