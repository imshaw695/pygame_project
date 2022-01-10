import os
from datetime import datetime
this_directory = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    path_to_data = os.path.join(this_directory, 'pasted_data.txt')
    with open(path_to_data, 'r') as file:
        lines = file.read()
    lines = lines.split('\n')

    months = ['jan', 'feb', 'mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    entries = []
    yyyy = 2021
    for index,line in enumerate(lines):
        items = line.split(' ')
        item = items[0].strip()
        if len(item) == 3:
            try:
                if item.lower() in months:
                    date = items[1].strip()
                    if date.isdigit():

                        # We are now pretty sure that a block of data has started
                        yyyy = lines[index+1].strip()
                        datetime_object = datetime.strptime(f'{items[0]} {date} {yyyy}  12:00PM', '%b %d %Y %I:%M%p')
                        title = lines[index+2].strip()
                        activity = lines[index+3].strip()
                        distance = lines[index+4].strip()
                        duration = lines[index+6].strip()
                        pace = lines[index+8].strip()
                        elevation_gained = lines[index+10].strip()
                        avg_hr = lines[index+12].strip()
                        entry = dict(date=datetime_object, title=title, activity=activity, distance=distance,duration=duration,pace=pace,elevation_gained=elevation_gained,avg_hr=avg_hr)
                        entries.append(entry)
                        break_here = True
            except:
                pass
    1/0

    # turn pace into seconds per km to make it easier to work with
    # turn duration into seconds
    # turn strings into numbers
    # create function that will take the raw data, put it into the function, and return an object with the processed data
    # use disk storage with all my workouts
    # get it to ignore ones already on there and then add new ones to the disk