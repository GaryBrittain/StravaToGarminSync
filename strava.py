#!/usr/bin/python

#Ensure all required dependencies are installed

#Go to http://sourceforge.net/projects/gcpuploader/ and download #the zip file. Follow instructions in README file. Once that is #done, change directory in the Garmin section of this script (at #the end/bottom) to where those files have been extracted to.

#Login to Strava in web browser, go to your profile page and copy #the ~6 digit number from the web address, which is your athlete #ID - enter this within the quotes below. Also enter your Strava #username and password - this will be used to download the GPX #file.

#Enter your Garmin Connect login details - this will be used to #upload the GPX file to Garmin.

#Change the stream directory variable to a location on your #system (worth creating a new folder)

#In the directory, create a text file called last_processed.txt #and save a numerical value of zero in the file

#I'm not too sure how secure any of it is with regards to how #username and passwords are transmitted/stored - use at your own #risk

import urllib2, mechanize, cookielib, json, os, sys

# Enter Strava athlete id and login details here.
AthleteID = ''
email = ''
password = ''

# Garmin Connect details
GarminUsername = ''
GarminPassword = ''

# Enter the directory to save GPX data to here.
stream_directory = '/home/pi/Snake/Cruzer/Strava/Streams/'

# Lookup the last processed ride ID
try:
  last_processed_dir = "%slast_processed.txt" % stream_directory
  fo = open(last_processed_dir,"rw+")
  last_processed = fo.readline()
  fo.close()
except:
  print 'Failed to lookup last processed ID'
  sys.exit()

# Find the last 50 rides for the athlete
try:
  f = urllib2.urlopen('http://app.strava.com/api/v1/rides?athleteId=' + AthleteID)
  json_string = f.read()
  parsed_json = json.loads(json_string)
  f.close()
except:
  print 'Failed to get rides from Strava'
  sys.exit()

# Slim the rides down to the last one.
ridelist = parsed_json["rides"]
MaxID = str(max(ridelist))
RideID = MaxID[8:16]

# See if the latest ride has been processed, if it has then stop.
if RideID == last_processed:
  print '%s - No new ride found, exiting...' % run_time
  sys.exit()

# For the ride id found above, download the details
try:
  f = urllib2.urlopen('http://www.strava.com/api/v2/rides/' + RideID)
  json_string = f.read()
  parsed_json = json.loads(json_string)
  f.close()
except:
  print 'Failed to download ride data from Strava'
  sys.exit()

# From the download above, get the name of the ride
name = parsed_json['ride']['name']

# Download the GPX data
try:
#  mechanize.cookiejar.clear()
  browser = mechanize.Browser()

  cj = cookielib.LWPCookieJar()
  browser.set_cookiejar(cj)

  browser.set_handle_equiv(True)
  browser.set_handle_redirect(True)
  browser.set_handle_referer(True)
  browser.set_handle_robots(False)
  browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                             max_time=1)

  browser.addheaders = [('User-agent',
                        ('Mozilla/5.0 (Windows; U; Windows NT 5.1; rv:1.7.3)'
                         ' Gecko/20041001 Firefox/0.10.1'))]

# Browse to the login page
  browser.open('https://www.strava.com/login')
  browser.select_form(nr=0)
  browser.form['email'] = email
  browser.form['password'] = password
  browser.submit()
# Open the GPX page and read the response
  gpx_url = "http://app.strava.com/activities/%s/export_gpx" % RideID
  browser.open(gpx_url)
  gpx_file = browser.response().read()
# Write the response to a file
  gpx_file_url = "%s%s.gpx" % (stream_directory, RideID)
  open(gpx_file_url, 'w').close()
  fo = open(gpx_file_url,"rw+")
  fo.write(gpx_file)
  fo.close()
except:
  print 'Failed to download GPX file'

# Update the log to the latest ride ID
last_processed_dir = "%slast_processed.txt" % stream_directory
try:
  fo = open(last_processed_dir,"rw+")
  fo.truncate()
  fo.write(RideID)
  fo.close()
except:
  print 'Failed to update processed log'
#  sys.exit()

# Upload to Garmin Connect
try:
  os.system("sudo python /home/pi/Python/pygupload/gupload.py -l %s %s -a %s %s%s.gpx" % (GarminUsername, GarminPassword, name, stream_directory, RideID,))
except:
  print 'Failed to upload to Garmin'

print 'Completed successfully'
sys.exit()
