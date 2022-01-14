import requests,csv,os
from bs4 import BeautifulSoup
from slack import WebClient

response = requests.get('https://www.donaldjtrump.com/news')
soup = BeautifulSoup(response.text)
statement = soup.find('h2','title title-med-2',text='Statement by Donald J. Trump, 45th President of the United States of America')
therest = statement.parent
href=therest.get('href')

tweetpage = requests.get('https://www.donaldjtrump.com'+href)
tsoup = BeautifulSoup(tweetpage.text)
date=tsoup.find('p','date')
tweet=tsoup.find('div','body')
tweet_id=str.replace(href,'/news/','')
filepath=r'C:\Users\ken_k\Python\Notebooks\ids.csv'
csv_file = csv.reader(open(filepath, 'r'))
data = list(csv_file)[0][0]
tweet_text=tweet.p.text

if(tweet_id!=data):
    os.environ["SLACK_API_TOKEN"] = "xoxb-2976018224672-2976095641104-EcL36VAkIuxDuMECd4lVvGX9"

    slack_token = os.environ["SLACK_API_TOKEN"]
    client = WebClient(token=slack_token)

    response = client.chat_postMessage(
        channel="tweets",
        text=tweet_text
    )
    
    with open(filepath,'w',newline='') as f:
        wtr = csv.writer(f)
        wtr.writerow([tweet_id])
    f.close()