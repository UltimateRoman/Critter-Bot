import time, requests, json, urllib

token = input("Enter telegram bot token:")
url = "https://api.telegram.org/bot"+token


def get_message(offset):
    if offset:
        resp = requests.get(url+"/getUpdates?timeout=100&offset={}".format(offset))
    else:
        resp = requests.get(url+"/getUpdates?timeout=100")
    respd = json.loads(resp.content.decode("utf8"))
    return respd


def main():
    prev_id = None
    t1 = time.time()
    while True:
        try:
            t2 = time.time()
            if t2-t1>20:
                t1 = time.time()
            respn = get_message(prev_id)
            
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == '__main__':
    main()
