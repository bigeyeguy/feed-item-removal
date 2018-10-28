import xml.etree.ElementTree as ET
import gspread
import requests
import time
from oauth2client.service_account import ServiceAccountCredentials

URL = "https://www.example.co.uk/Google-Products-Xml.php"
response = requests.get(URL)
with open('/home/bigeyeguy/mysite/static/example-feed.xml', 'wb') as file:
    file.write(response.content)

time.sleep(3)

tree = ET.parse('/home/bigeyeguy/mysite/static/example-feed.xml')
root = tree.getroot()
parent_map = dict((c, p) for p in tree.getiterator() for c in p)
ns = {'BEG': 'http://base.google.com/ns/1.0'}

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

client = gspread.authorize(creds)
#sh = client.create('REMOVE_IDS')
#sh.share('you@email.co.uk', perm_type='user', role='writer')
sh = client.open('REMOVE_IDS')
worksheet = sh.get_worksheet(0)
remove_ids = worksheet.col_values(1)

items = tree.findall('.//item')
for item in items:
    id = item.findall('BEG:id', ns)
    # again above is the object of id, not its contents. id is a list object
    for i in id:
        for cell in remove_ids:
            if i.text == cell:
                parent_map[item].remove(item)

for item in items:
    avail = item.findall(BEG:availability', ns)
    for i in avail:
        if i.text == "Out of stock":
            parent_map[item].remove(item)

tree.write('/home/bigeyeguy/mysite/static/example-feed.xml')
