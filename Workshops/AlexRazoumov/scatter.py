from writeNodesEdges import writeObjects

import pandas as pd
variables = ['number', 'date', 'route', 'sailingtime', 'vessel', 'scheduled', 'actual',
             'arrival', 'status', 'time', 'traffic', 'wind', 'delay', 'temp']
data = pd.read_csv('ferryData.csv', skiprows=1, names=variables).dropna()
data = data.astype({'traffic': int, 'wind': int, 'delay': int, 'temp': int})

# data.shape   # 3060 rows, 14 columns

wind = [w/11. for w in data.wind.tolist()]
traffic = [t/4. for t in data.traffic.tolist()]
delay = [d/203. for d in data.delay.tolist()]

itraffic = data.traffic.tolist()
temp = data.temp.tolist()

xyz = [[i,j,k] for i,j,k in zip(wind,traffic,delay)]

writeObjects(xyz, fileout='sailing',
             scalar = itraffic, name = 'traffic',
             scalar2 = temp, name2 = 'temperature')

# # count unique points
# points = set()
# for i, j, k in zip(data.wind.tolist(), data.traffic.tolist(), data.delay.tolist()):
#     points.add((i,j,k));
# len(points)
