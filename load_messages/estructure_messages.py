import os
import time
import json

def eval_file(messages_file_name):
    messages_file = open(messages_file_name)
    lines = messages_file.readlines()
    entry = []
    for n, l in enumerate(lines):
        try:
            dict_s = dict()
            if ";vip=1" in l:
                l = l.replace(";vip=1", "")
                dict_s["vip"] = 1
            segments = l.split(";")
            for s in segments:
                attribute, value = tuple(s.split("=", 1))
                if attribute == "user-type":
                    if "USERNOTICE" in value:
                        user, msg = tuple(value.split("USERNOTICE", 1))
                        dict_s["type"] = "USERNOTICE"
                        dict_s["user"] = user.strip()[1:]
                        dict_s["channel"] = msg.strip()
                    elif "PRIVMSG" in value:
                        user, msg = tuple(value.split("PRIVMSG", 1))
                        dict_s["type"] = "PRIVMSG"
                        dict_s["user"] = user.strip()[1:]
                        channel, msg = tuple(msg.split(":", 1))
                        dict_s["channel"] = channel.strip()
                        dict_s["msg"] = " ".join(msg.split())
                    elif "CLEARCHAT" in value:
                        user, msg = tuple(value.split("CLEARCHAT", 1))
                        dict_s["type"] = "CLEARCHAT"
                        dict_s["user"] = user.strip()[1:]
                        channel, msg = tuple(msg.split(":", 1))
                        dict_s["channel"] = channel.strip()
                        dict_s["msg"] = " ".join(msg.split())
                else:
                    dict_s[attribute] = value.strip()
            entry.append(dict_s)

        except Exception as e:
            with open(f'messages_errors.txt', 'a') as messages_file:
                messages_file.write(l)

    if not os.path.exists("messages_all.json"):
        print("create")
        with open('messages_all.json', "w") as file:
            json.dump([], file)

    with open('messages_all.json', "r") as file:
        data = json.load(file)
    data.extend(entry)

    with open('messages_all.json', "w") as file:
        json.dump(data[-1000:], file)

    messages_file.close()
    os.remove(messages_file_name)

def estructure_all_messages():
    while True:
        messages_path = f"{os.getcwd()}/messages"
        finished_messages = [n for n in os.listdir(messages_path) if ("messages" in n) and ("finished" in n)]
        for f in finished_messages:
            print(f"Process {f}")
            eval_file(messages_path+"/"+f)
        time.sleep(10)

estructure_all_messages()