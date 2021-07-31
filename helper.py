import time, requests, json, urllib
from app import url
from config import cat_url,dog_url

def send_image(breed,chat_id,da):
    for d in filter(lambda d: d['breed'] == breed, da):
        rsp = requests.get(url+"/sendImage?photo={}&chat_id={}".format(d['image'], chat_id))
        rem = json.loads(rsp.content.decode("utf8"))

def random_cat(chat_id):
    resp = requests.get(cat_url)
    msg = json.loads(resp.text)
    rsp = requests.get(url+"/sendImage?photo={}&chat_id={}".format(msg['url'], chat_id))
    rem = json.loads(rsp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])

def random_dog(chat_id):
    resp = requests.get(dog_url)
    msg = json.loads(resp.text)
    rsp = requests.get(url+"/sendImage?photo={}&chat_id={}".format(msg['url'], chat_id))
    rem = json.loads(rsp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])

def send_message(args,chat_id):
    if args[0] == 'hi':
        reply = "Hello!"
    reply = urllib.parse.quote_plus(reply)
    resp = requests.get(url+"/sendMessage?text={}&chat_id={}".format(reply, chat_id))
    rem = json.loads(resp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])

def make_msg(resp,da):
    for msg in resp['result']:
        try:
            text = msg['message']['text']
            chat_id = msg['message']['chat']['id']
            args = text.split()
            if args[0] == 'breed':
                send_image(args[1],chat_id,da)
            elif args[0] == 'random':
                if args[1] in ['CAT','cat','Cat']:
                    random_cat(chat_id)
                elif args[1] in ['DOG','Dog','dog']:
                    random_dog(chat_id)
            else:
                send_message(args,chat_id)
        except Exception as e:
            print(e)
        
