import time, requests, json, urllib

def make_msg(resp):
    for msg in resp['result']:
        try:
            text = msg['message']['text']
            chat_id = msg['message']['chat']['id']
            args = text.split()
            if args[0] == 'breed':
                send_image(args[1],chat_id)
            elif args[0] == 'random':
                if args[1] in ['CAT','cat','Cat']:
                    random_cat(chat_id)
                elif args[1] in ['DOG','Dog','dog']:
                    random_dog(chat_id)
            else:
                send_message(args,chat_id)
        except Exception as e:
            print(e)
        