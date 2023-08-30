import os
import requests
import datetime

community_notes_download_url = "https://twitter.com/i/communitynotes/download-data"

base_url = "https://ton.twimg.com/birdwatch-public-data"
today = datetime.datetime.utcnow().date()

flag = False
urls = []
valid_day = today
for _ in range(10):
    date = str(today.year) + "/" + str(today.month).zfill(2) +"/" + str(today.day).zfill(2)
    num = 0
    url = base_url + "/" + date + "/" + f"notes/notes-{str(num).zfill(5)}.tsv"
    r = requests.get(url, stream=True)
    if r.status_code == requests.codes.ok:
        break
    else:
        valid_day = today - datetime.timedelta(days=1)

date_url = base_url + "/"\
        + str(valid_day.year) + "/"\
        + str(valid_day.month).zfill(2) +"/"\
        + str(valid_day.day).zfill(2)
note_kinds = ["notes/notes",
              "noteRatings/ratings", 
              "noteStatusHistory/noteStatusHistory",
             "userEnrollment/userEnrollment"]        

for note_kind in note_kinds:
    num = 0
    for x in range(10):
        url = date_url + "/" + f"{note_kind}-{str(num).zfill(5)}.tsv"
        r = requests.get(url, stream=True)
        if r.status_code == requests.codes.ok:
            filename = os.path.basename(url)
            filename = "data/" + filename
            with open(filename, 'wb') as f:
              for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                  f.write(chunk)
                  f.flush()
            num += 1
        else:
            break 