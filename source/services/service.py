import random
import math
from datetime import datetime


def generate_medians(list_of_nodes, number_of_medians):
  return random.sample(list_of_nodes, number_of_medians)



def generate_time():
  partOfDay = random.randint(0,9)

  if partOfDay < 2:
    return random.randint(0, 7*60*60)
  elif partOfDay > 7:
    return random.randint(20*60*60 + 1, 24*60*60 - 1)
  else:
    return random.randint(7*60*60 + 1, 20*60*60 - 1)



def generate_order_data(number_of_order, list_of_nodes, order_data, day = 0):
  temp_data = random.sample(list_of_nodes, number_of_order)

  for item in temp_data:
    timeOfOrder = generate_time() + day*86400
    waiting_time = random.randint(10*60, 2*60*60)

    order_data.append((item, timeOfOrder, waiting_time))
    

  return order_data



def second_to_time(time, timeOnly = False):
  initialTime = datetime(2013, 1, 1, 0, 0, 0)
  secondFromUnix = initialTime.timestamp()

  secondFromUnix += time

  date_time = datetime.fromtimestamp(secondFromUnix)

  if time == 1e9:
    return "N/A"

  if timeOnly:
    return date_time.strftime("%H:%M:%S")

  return date_time.strftime("%d/%m/%Y, %H:%M:%S")



def findNearestNode(latlong_to_node, ycoord, xcoord):
  diff = 1e9
  node = 0

  for key in latlong_to_node.keys():
    euclideanDis = math.sqrt(math.pow((xcoord - key[0]), 2) + math.pow((ycoord - key[1]), 2))

    if euclideanDis < diff:
      diff = euclideanDis
      node = latlong_to_node[key]
                    
  return node