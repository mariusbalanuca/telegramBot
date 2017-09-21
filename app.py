import json 
import requests
import time
import urllib2
import re

TOKEN = "413360913:AAFkA4qDK3ht2NGEeBdPshhfYbHLz3rxsAE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content
    
def weather(oras):
    site = "http://api.openweathermap.org/data/2.5/weather?q="+oras+"&appid=631cf33df60fe496c2a9d57992fa99ba"
    data = json.load(urllib2.urlopen(site))
    return oras + ": %d C - %s" % (int(data["main"]["temp"] - 273.15), data["weather"][0]["main"])

def score(team):
    text = "Team not found or doesn`t have a match today"
    site = "http://www.tablesleague.com/livescores/"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    page = urllib2.urlopen(req)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page,"html.parser")
    soup.prettify()
    for link in soup.findAll("div", { "class" : "cell name" }):
        if re.search(team, link.text, re.IGNORECASE):
           text = re.split('(\d+)', link.text)
           text = ' '.join(text)
    return text
    
def timee(city):
    text = "City not found"
    words = city.split()
    if len(words)>=2:
        city = city.split()[0] + "+" + city.split()[1]
    site = "https://www.timeanddate.com/worldclock/?query="+city
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    page = urllib2.urlopen(req)
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(page,"html.parser")
    soup.prettify()
    for link in soup.findAll("td", { "class" : "rbi" }):
        text = link.text
        break
    return city + " - " + text

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    hello = {"Hello", "Hi", "Sup", "hi", "hello"}
    if text in hello:
        url = URL + "sendMessage?text={}&chat_id={}".format("Hello there!", chat_id)
    elif "#weather" in text:
        words = text.split()
        if len(words)>2:
            text = text.split()[1] + text.split()[2]
        else:
            text = text.split()[1]
        url = URL + "sendMessage?text={}&chat_id={}".format(weather(text).encode('utf-8'), chat_id)
    elif "#score" in text:
        text = text.split()[1]
        url = URL + "sendMessage?text={}&chat_id={}".format(score(text), chat_id)
    elif "#time" in text:
        words = text.split()
        if len(words)>2:
            text = text.split()[1] + " " + text.split()[2]
        else:
            text = text.split()[1]
        url = URL + "sendMessage?text={}&chat_id={}".format(timee(text).encode('utf-8'), chat_id)
    else:
        url = URL + "sendMessage?text={}&chat_id={}".format("I`m stupid now...i don`t know much", chat_id)
    get_url(url)
    
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)
    
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)
            
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
