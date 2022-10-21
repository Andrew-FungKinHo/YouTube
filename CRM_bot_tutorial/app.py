from ast import parse
from genericpath import isfile
import requests
from flask import Flask, jsonify,request
import json
import os 
import time
import datetime
# from dotenv import load_dotenv

# load_dotenv()


TOKEN = os.environ["TOKEN"]
NOTION_BEAR_TOKEN = os.environ["NOTION_BEAR_TOKEN"]
HEADERS = {
    "accept": os.environ["ACCEPT"],
    "Notion-Version": os.environ["NOTION_VERSION"],
    "content-type":  os.environ["CONTENT_TYPE"],
    "Authorization": os.environ["AUTHORIZATION"]
}
BANNED_USERNAMES = []
BANNED_USER_IDS = []

app = Flask(__name__)

sample_response =  {
    'update_id': 6068183, 
    'message': 
        {'message_id': 1, 
        'from': {'id': 1399917123, 'is_bot': False, 'first_name': 'Lol', 'last_name': 'Yeet', 'username': 'yeetorbeyeeted69', 'language_code': 'en'}, 
        'chat': {'id': 1399917123, 'first_name': 'Lol', 'last_name': 'Yeet', 'username': 'yeetorbeyeeted69', 'type': 'private'}, 
        'date': 1664881469, 
        'text': '/start', 
        'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
        }
}

# load all the username from the notion spreadsheet and return a dictionary in the format 
def loadUsernames():
    url = "https://api.notion.com/v1/databases/dc9c9681720a4941a317e75312ab9d69/query"

    payload = {"page_size": 100}

    response = requests.post(url, json=payload, headers=HEADERS)

    data = response.text
    # turn JSON string back into python dictionary
    parsed = json.loads(data)

    username_dict = {}

    for entry in parsed['results']:
        # check its username
        if entry['properties']['User']['title']:
            # check its product
            if entry['properties']['Product']['select']:
                # check its status
                if entry['properties']['Status']['select']:
                    # { username: (selected_product, status, page id) }
                    username_dict[entry['properties']['User']['title'][0]['text']['content']] = (entry['properties']['Product']['select']['name'],entry['properties']['Status']['select']['name'],entry['id'])
    return username_dict

def sendMessage(msg,item):
    chat_id = item['chat']['id']
    user_id = item["from"]["id"]
    username = item['from']["username"]

    new_msg = f'{msg} {username}'
    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={new_msg}&parse_mode=HTML'
    resp = requests.post(to_url)

def sendLocalSourceFiles(item, product):
    chat_id = item['chat']['id']
    directory = os.getcwd() + f'/sourceFiles/{product}'

    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        # check if it is a file
        if os.path.isfile(f):
            doc = open(os.path.join(directory,filename), 'rb')
            files = {'document': doc}
            to_url = 'https://api.telegram.org/bot{}/sendDocument?chat_id={}&parse_mode=HTML'.format(TOKEN,chat_id)
            resp = requests.post(to_url,files=files)
            print(f'File:   {filename} is sent')
            time.sleep(0.75)

def askingProductQuestion(item):
    chat_id = item["chat"]["id"]
    question = 'Which product is the customer interested in purchasing?'
    payload = {
        "chat_id": chat_id,
        "text": question,
        "reply_markup": {
            "one_time_keyboard": True,
            "resize_keyboard": True,
            "remove_keyboard": True,
            "keyboard": [
                [
                    {
                        "text": "Product A is targeted",
                        "callback_data": "productA"
                    }
                ],
                [
                    {
                        "text": "Product B is targeted",
                        "callback_data": "productB"
                    }
                ]
            ]
        }
    }

    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    r = requests.post(to_url, json=payload)
    print(f'Status code: {r.status_code}, Response: {r.json()}')

def removeKeyboard(item):
    chat_id = item["chat"]["id"]
    sendText = "removing keyboard"
    payload = {
        "chat_id": chat_id,
        "text": sendText,
        "reply_markup": {
            "remove_keyboard": True
        }
    }

    to_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    r = requests.post(to_url, json=payload)
    print(f'Status code: {r.status_code}, Response: {r.json()}')

def turnStatusToClosed(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {
        "properties": {
            "Status": {"select": {"name": "Closed"}},
            "Date": {"date": {"start": datetime.datetime.today().strftime("%Y-%m-%d")}}
        }
    }


    response = requests.patch(url, headers=HEADERS, json=payload)

    print(response.text)

def addUserResponse(item,userStatus=""):
    url = "https://api.notion.com/v1/pages/"
    payload = {
        "parent": {
            "database_id": '30b44a61cc184d3b888d3f586b294d0d'
        },
        "properties": {
            "Message ID": {
                "number": item["message_id"]
            },
            "Username": {
                "title": [
                    {
                        "text": {
                            "content": f"@{item['from']['username']}"
                        }
                    }
                ]
            },
            "Message": {
                "rich_text": [
                    {
                        "text": {
                            "content": item['text']
                        }
                    }
                ]
            },
            "Remarks": {
                "rich_text": [
                    {
                        "text": {
                            "content": userStatus
                        }
                    }
                ]
            },
            "Message_datetime_in_UNIX": {
                "number": item['date'] * 1000
            },
            "User ID": {
                "number": item['from']['id']
            }
        }
    }
        
    response = requests.post(url, json=payload, headers=HEADERS)
    print(response.text)

def addUserToDatabase(username,status,product):
    url = "https://api.notion.com/v1/pages/"
    payload = {
        "parent": {
            "database_id": 'dc9c9681720a4941a317e75312ab9d69'
        },
        "properties": {
            "User": {
                "title": [
                    {
                        "text": {
                            "content": username
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": status
                }
            },
            "Product": {
                "select": {
                    "name": product
                }
            }
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    print(response.text)

def welcome_message(item):
    print(item)

    chat_id = item['chat']['id']
    user_id = item["from"]["id"]
    username = item['from']["username"]
    customers = loadUsernames()

    if 'text' in item:
        # check if the user has been banned
        if user_id in BANNED_USER_IDS or username in BANNED_USERNAMES:
            addUserResponse(item,userStatus="Banned user")
            sendMessage("You have been banned by this bot", item)
            return

        addUserResponse(item)
        if item['text'].lower() == '/start':
            if username in customers.keys():
                print(customers[username])
                if customers[username][1] == 'Pending':
                    sendMessage(f'sending {customers[username][0]} information',item)
                    sendLocalSourceFiles(item,customers[username][0])
                    # close their requests (turn their status from pending to closed)
                    turnStatusToClosed(customers[username][2])
                    return 
                elif customers[username][1] == 'Closed':
                    sendMessage(f'Your previous request has been closed. Please contact the admins for further information.',item)
                    return 

                elif customers[username][1] == 'Admin':
                    sendMessage('Hello admin. What customer do you want to add?',item)
                    askingProductQuestion(item)
                    return
                else:
                    addUserResponse(item,userStatus="Unknown user")
                    sendMessage(f'Unknown user. Please contact the admins for further information.',item)
                    return

        elif item['text'] == "Product A is targeted":
            removeKeyboard(item)
            addUserToDatabase(" ","Lead","Product A")

        elif item['text'] == "Product B is targeted":
            removeKeyboard(item)
            addUserToDatabase(" ","Lead","Product B")

        elif item['text'].startswith("admin add:"):
            if customers[username][1] == 'Admin':
                inputItems = item['text'][10:].split(",")
                if len(inputItems) == 2:
                    username, product = inputItems
                    addUserToDatabase(username,"Pending",product)
                    sendMessage(f'User {username} with the status Pending has been added successfully.',item)
                    return
                else:
                    sendMessage("Not enough values to unpack",item)
                    return
            else:
                sendMessage(f'You are not authorized to add users to the database.',item)
                return
        else:
            sendMessage('Command not found. Please start the bot with the command /start', item)
            return
                    
@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        data = request.get_json()
        print(f'DATA: {data}')
        if 'message' in data:
            data = data['message']
            welcome_message(data)
            return {'statusCode': 200, 'body': 'Success', 'data': data}
        else:
            return {'statusCode': 404, 'body': 'User has left the chat room and deleted the chat', 'data': data}
    else:
        return {'statusCode': 200, 'body': 'Success'}


if __name__ == '__main__':
    app.run(debug=True)

