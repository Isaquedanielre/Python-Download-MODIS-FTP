## downloadModis.py
## Tim Klug

import os
import sys
import string
import time
from datetime import datetime

import ftplib
from ftplib import FTP

def getModis(date, hInd, vInd):
  """
   This function downloads a single MODIS tile from the ladsweb FTP
   service at [ladsftp.nascom.nasa.gov]. "Partial" filenames for
   target images are build from user supplied parameters. The
   directories of the FTP server are then parsed for matching
   images.

   :param date:       string. date (mm/dd/YYYY) of the target image
   :param hInd:       integer. horizontal grid index of the target image
   :param vInd:       integer. vertical grid index of the target image
  """

  
  ## convert MM/DD/YYYY to julian date
  julianD = str(time.strptime(date, "%m/%d/%Y").tm_yday).zfill(3)
  year = date[6:]
  
  ## build partial filename from input parameters
  partial = "MOD09A1.A" + str(year) + str(julianD) +\
            ".h" + str(hInd).zfill(2) + "v" + str(vInd).zfill(2)
  print partial

  ## connect to ftp server and navigate to MOD09A1 folder, year, and day
  ftp = FTP('ladsftp.nascom.nasa.gov', 'anonymous')

  ## attempt to establish connection and download file
  try:
      ## navigate to directory containing target year and day
      ftp.cwd("/allData/5/MOD09A1/" + str(year) + "/" + str(julianD))
      ## define list of all items in current directory
      data = []
      ftp.dir(data.append)

      ## search list of items for partial filename and slice to just the file
      for item in data:
          if partial in item:
              filename = item
      filename = filename[56:]
    
      ## Download image file
      gFile = open(filename, "wb")
      ftp.retrbinary('RETR ' + filename, gFile.write)
      gFile.close()

      print "Image successfully downloaded to " + os.getcwd()
      
      ## Disconnect from ftp
      ftp.quit()

  ## Catch error from nonexistant directory/image file
  except Exception as e:
      print "    * Error: No image for this date/gridcell. *\n"


##  example function call
getModis("01/01/2001", 10, 5)
