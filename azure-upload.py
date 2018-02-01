import sys
import os
import azure
import optparse
import magic

from optparse import OptionParser
mime = magic.Magic(mime=True)
from sys import argv

parser = OptionParser()
parser.add_option("-d", "--directory", action="store", dest="dirupload",
                  help="Dir tree to upload", metavar="DIRECTORY")

parser.add_option("-c", "--container", action="store", dest="container",
                  help="remote container name", metavar="DIRECTORY")

parser.add_option("-a", "--accountname", action="store", dest="acctname",
                  help="Account name", metavar="ACOUNTNAME")

parser.add_option("-k", "--acctkey", action="store", dest="acctkey",
                  help="Account Key", metavar="ACCOUNTKEY")
(options,args) = parser.parse_args()

acctname  = options.acctname
acctkey   = options.acctkey
container = options.container
dirupload = options.dirupload
null = ""
from azure.storage.blob import BlobService

blob_service = BlobService(account_name=acctname, account_key=acctkey)

for subdir, dirs, files in os.walk(dirupload):
 for file in files:
#Subdir2 is to prevent double-naming the directory and the blob (e.g /files/files/)
  subdir2 = subdir.replace(container + "/", "")
  tomime = os.path.join(subdir, file)
#  BlobService._BLOB_MAX_DATA_SIZE = 32 * 1024 * 1024 * 1024
  toupload = os.path.join(subdir2, file)
  filemimetype = mime.from_file(tomime)
  print "PUT-BLOB: " + toupload + " " + filemimetype
  mimetypeupload = filemimetype
  blob_service.put_block_blob_from_path(
     container,
     toupload,
     toupload 
)
  blob_service.set_blob_properties(
   container, 
   toupload,
   null, 
   mimetypeupload
)
  with open(subdir2 + ".log", "a") as logfile:
   logfile.write(toupload + " " + filemimetype + "\n")
  os.remove(toupload)
