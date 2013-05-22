StravaToGarminSync
==================

Uploads Strava ride to Garmin Connect


Ensure all required dependencies are installed

Go to http://sourceforge.net/projects/gcpuploader/ and download the zip file. Follow instructions in README file. Once that is done, change directory in the Garmin section of this script (at the end/bottom) to where those files have been extracted to.

Login to Strava in web browser, go to your profile page and copy the ~6 digit number from the web address, which is your athlete ID - enter this within the quotes below. Also enter your Strava username and password - this will be used to download the GPX #file.

Enter your Garmin Connect login details - this will be used to upload the GPX file to Garmin.

Change the stream directory variable to a location on your system (worth creating a new folder)

In the directory, create a text file called last_processed.txt and save a numerical value of zero in the file

I'm not too sure how secure any of it is with regards to how username and passwords are transmitted/stored - use at your own risk


Set up a cron job to run this script every 5 or 10 minutes, so the sync is done automatically.
