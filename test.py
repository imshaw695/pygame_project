import re
import json
import os
import mechanize

def get_activity_id(activity):
        return activity['activity']['activityId']

def get_activity_type(activity):
        return activity['activity']['activityType']['key']

def get_query_info(schema):
        total = int(schema['results']['search']['totalPages'])
        activities_per = int(schema['results']['search']['query']['activitiesPerPage'])

        return (total, activities_per)

def fetch_gpx_file(br, activity_id):
        print("Fetching activity id", activity_id)
        url = "http://connect.garmin.com/proxy/activity-service-1.1/gpx/activity/" + activity_id + "?full=true"
        r = br.open(url)

        filename = "gpx/" + activity_id + ".gpx"
        f = open(filename, "w")
        f.write(r.read())
        f.close()

# First, use mechanize to login in to my Garmin account
def fetch_schema():
        br = mechanize.Browser()
        br.open("http://connect.garmin.com/signin")

        br.select_form(name="login")
        br["login:loginUsernameField"] = 'xxxxxxx'
        br["login:password"] = 'xxxxxxxxx'

        br.submit()
        r = br.response()

        # Now load however many pages of activity data we have
        search_url = "http://connect.garmin.com/proxy/activity-search-service-1.0/json/activities?_dc=1220170621856&start="

        r = br.open(search_url + "0")
        schema = json.loads(r.read())

        qi = get_query_info(schema)
        print("Total # of pages:", qi[0])
        print("Activities per page:", qi[1])

        activities = schema['results']['activities']
        for activity in activities:
            act_type = get_activity_type(activity)
            if act_type == "running":
                    act_id = get_activity_id(activity)
                    fetch_gpx_file(br, act_id)

        # Fetch the subsequent pages
        page = 1
        for j in range(qi[0]):
                r = br.open(search_url + str(qi[1] * page))
                schema = json.loads(r.read())

                activities = schema['results']['activities']
                for activity in activities:
                        act_type = get_activity_type(activity)
                        if act_type == "running":
                                act_id = get_activity_id(activity)
                                fetch_gpx_file(br, act_id)
                page += 1

if not os.path.exists("gpx"):
        os.mkdir("gpx")

fetch_schema()