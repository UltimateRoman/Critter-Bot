import time, requests, json, urllib
from helper import make_msg
from jina import Document, DocumentArray
from jina.types.document.generators import from_csv

import csv

token = input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token
da = DocumentArray()

def get_message(offset):
    if offset:
        resp = requests.get(url+"/getUpdates?timeout=100&offset={}".format(offset))
    else:
        resp = requests.get(url+"/getUpdates?timeout=100")
    respd = json.loads(resp.content.decode("utf8"))
    return respd

def get_last_id(respd):
    ids=[]
    for msg in respd['result']:
        ids.append(int(msg['update_id']))
    return max(ids)

def load_da():
    with open('./dogs.csv','r') as data:
        for line in csv.DictReader(data):
            d = Document(line)
            da.append(d)


def main():
    load_da()
    prev_id = None
    t1 = time.time()
    while True:
        try:
            t2 = time.time()
            if t2-t1>20:
                t1 = time.time()
            respd = get_message(prev_id)
            if len(respd['result'])>0:
                prev_id = get_last_id(respd)+1
                make_msg(respd,da)
            time.sleep(1)
            
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    main()
