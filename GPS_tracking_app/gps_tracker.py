import gpxpy
import gpxpy.gpx
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

# Code below will be to extract gpx file from garmin, by pressing an update button

# Open gpx file
with open('GPS_tracking_app/activity_7951831563.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

print(f'There are {gpx.get_track_points_no()} data points and the altitude range was {gpx.get_elevation_extremes()}. Total elevation gained was {gpx.get_uphill_downhill()}')
print()

# Create a pandas dataframe next out of the lat, long, and elevation points

route_info = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            route_info.append({
                'latitude': point.latitude,
                'longitude': point.longitude,
                'elevation': point.elevation
            })

route_df = pd.DataFrame(route_info)

# Turn the dataframe into a csv so that you can work with it

route_df.to_csv('GPS_tracking_app/route_df.csv', index=False)

# An example plot of what the route looks like, not for finished app

plt.figure(figsize=(14, 8))
plt.scatter(route_df['longitude'], route_df['latitude'], color='#101010')
plt.title('Route latitude and longitude points', size=20)
# plt.show()

import folium
from IPython.display import display

# Read in the CSV

route_df = pd.read_csv('GPS_tracking_app/route_df.csv')
print(route_df.head())

import webbrowser

# Create a class that will open the route on a map

class Map:
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
    
    def showMap(my_map):

        #Display the map
        my_map.save("map.html")
        webbrowser.open("map.html")

# Choose the starting location, you will have to figure out the best place to centre it

route_map = folium.Map(
    location=[50.377745, -4.172243],
    zoom_start=16,
    tiles='OpenStreetMap',
    width=1024,
    height=600
)

# Display the route on the map below, and connect them with polyline

coordinates = [tuple(x) for x in route_df[['latitude', 'longitude']].to_numpy()]
folium.PolyLine(coordinates, weight=6).add_to(route_map)

# Open it in the browser

Map.showMap(route_map)

from vincenty import vincenty

route_df['lastLat']=route_df['latitude'].shift(1)
route_df['lastLong']=route_df['longitude'].shift(1)
route_df['dist(meters)'] = route_df.apply(lambda x: vincenty((x['latitude'], x['longitude']), (x['lastLat'], x['lastLong'])), axis = 1) * 1000.

print('Total distance as summed between points in track:')
print('   ' + str(sum(route_df['dist(meters)'][1:])*0.001) + ' km')
# The df['dist'][1:] above is because the "shift" sets the first lastLon,lastLat as NaN.
