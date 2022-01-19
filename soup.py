import os

from bs4 import BeautifulSoup
import requests
import time
import csv
import time
from apscheduler.schedulers.blocking import BlockingScheduler


def fetch_dm():
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'}
    url = 'https://www.dailymirror.lk/'
    DISCORD_HOOK_URI = os.getenv('TOKEN')

    '''def key_words_search_words(self, user_message):
        words = user_message.split()[1:]
        keywords = '+'.join(words)
        search_words = ' '.join(words)
        return keywords, search_words'''

    response = requests.get(url, headers = headers)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    with open('dailymirror.csv', "r", newline='') as csvfile:
        combined = []
        data = csv.reader(csvfile)
        for line in data:
            combined.extend(line)

    

        
    for link in soup.find_all('div', attrs= {'class':'header lineg'}):
        title = link.find('h3').text
        url = link.find('a')['href']
        #with open("dailymirror2.csv", "r") as f:
        #with open('dailymirror2.csv', "r", newline='') as csvfile:
            #data = csv.reader(csvfile)
            #for line in data:
            #print(str(line))
        if url in combined:
            print ("news item already posted - not sent")
        else:
            excerpt= link.find('p').text
            img = link.find(('img'))


                    
            data = {
                    "username" : "Pomoji - LK News",
                    }   
            data["embeds"] = [
                    {
                        "description" : excerpt,
                        "url": url,
                        "title" : title,
                        "color": 0x00FFFF,
                        "thumbnail": {
                        "url": img['src'],
                        "height": 0,
                        "width": 0
                    },
                        "footer": {
                        "text": "Source: DailyMirror",
                        "icon_url": "https://th.bing.com/th/id/OIP.a98SDbFNBVtncfawW--pEQAAAA?pid=ImgDet&rs=1"
                    },
                            }
                        ]
            result = requests.post(DISCORD_HOOK_URI , json = data)
            with open('dailymirror.csv', 'a') as csvfile:
                fieldnames = ['url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'url': url})

            if result.status_code == 204:
                print('post success; returned no content')
            elif result.status_code != 200:
                print('post failed with error', result.status_code, 'because', result.reason)
            else:
                print('post success')
            time.sleep(5)
 
scheduler = BlockingScheduler()
scheduler.add_job(fetch_dm, 'interval', minutes=10)
print('Task initiated. Waiting 10 minutes before execution')
#time_of_next_run = scheduler.timeRemaining()
#print(type(time_of_next_run))  # <class 'datetime.datetime'>
scheduler.start()
