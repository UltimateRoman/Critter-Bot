import time, requests, json, urllib
from config import cat_url,dog_url,turl

token = input("Enter telegram bot token:")
url = turl + token


def send_image(breed,chat_id,da):
    found = False
    resp = ""
    for d in da:
        if d.tags['breed'] == breed:
            found = True
            resp = requests.get(url+"/sendPhoto?photo={}&chat_id={}".format(d.tags['image'], chat_id))
    if not found:
        reply = "Sorry, I could not find a matching image 🥺. Please try again"
        resp = requests.get(url+"/sendMessage?text={}&chat_id={}".format(reply, chat_id))

    rem = json.loads(resp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])
        

def random_cat(chat_id):
    resp = requests.get(cat_url)
    msg = json.loads(resp.text)
    rsp = requests.get(url+"/sendPhoto?photo={}&chat_id={}".format(msg['url'], chat_id))
    rem = json.loads(rsp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])


def random_dog(chat_id):
    resp = requests.get(dog_url)
    msg = json.loads(resp.text)
    rsp = requests.get(url+"/sendPhoto?photo={}&chat_id={}".format(msg['url'], chat_id))
    rem = json.loads(rsp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])


def send_message(args,chat_id):
    if args[0] == 'Hi' or args[0] == '/start':
        reply = "Hello, I'm Critter Bot! \n You can use help to get started 😃"
    elif args[0] == "Thanks":
        reply = "Goodbye! See you soon 😁"
    elif args[0] == "help":
        reply = "Hello 😊! You can make use of the following commands: \n\n breed [breed name]- Search images of cute doggos of any specific breed 🐶 \n random cat - Random image of a kitty 🐈 \n random dog - Random image of a doggo 🐕"
    else:
        reply = "Sorry, I did not understand 😅. Please try again"

    reply = urllib.parse.quote_plus(reply)
    resp = requests.get(url+"/sendMessage?text={}&chat_id={}".format(reply, chat_id))
    rem = json.loads(resp.content.decode("utf8"))
    print("Replied to:", rem['result']['chat']['first_name'])


def handle_msg(resp,da):
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
        
