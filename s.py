import os
import sharepy
from constants import SHAREPOINT_URL, SHAREPOINT_USERNAME

SHAREPOINT_PASSWORD = os.getenv('SHAREPOINT_PASSWORD')
 
s = sharepy.connect(SHAREPOINT_URL, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)
site = "https://kendrion.sharepoint.com/sites/TeamsProjectWise"
library = "Shared Documents"

# Get list of all files and folders in library
files = s.get("{}/_api/web/lists/GetByTitle('{}')/items?$select=FileLeafRef,FileRef"
              .format(site, library)).json()["d"]["results"]

for file in files:
    source = "https://" + s.site + file["FileRef"]
    dest = "." + file["FileRef"]
    # Check if item is file or folder
    folder = s.get("{}/_api/web/GetFolderByServerRelativeUrl('{}')"
                   .format(site, file["FileRef"])).status_code == 200
    print(source)

    if not os.path.exists(dest):
        if folder:
            os.makedirs(dest)  # Create folders
        else:
            s.getfile(source, filename=dest)  # Download files