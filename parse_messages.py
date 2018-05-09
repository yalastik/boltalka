import vk
import time
import pickle
from telethon.tl.types import User
from telethon import TelegramClient
import re

# stuff for vk
session = vk.Session(access_token='VK_TOKEN')
vkapi = vk.API(session)

SELF_ID = 83784811
SLEEP_TIME = 0.3

friends = vkapi('friends.get',version='5.74')

# stuff for telegram

# Use my own values here
api_id = 100000
api_hash = 'api_hash'

client = TelegramClient('messages_hist', api_id, api_hash)

assert client.connect()

if not client.is_user_authorized():
    phone_number = '+555555555'
    client.send_code_request(phone_number)
    myself = client.sign_in(phone_number, input('Enter code: '))

def get_tg_dialogs():
    my_dialogs = client.get_dialogs()
    messages = []
    for dialog in my_dialogs:
        if type(dialog.entity) == User:
            messages.append(client.get_message_history(dialog.entity, limit=None))
            print('added messages with {}'.format(dialog.entity.username))
    return messages


def save_data(data, file_name='tg_messages.dat'):
    with open(file_name,'wb') as f:
        pickle.dump(data, f)


def get_dialogs(user_id):
    dialogs = vkapi('messages.getDialogs', user_id=user_id, version='5.74')
    return dialogs


def get_history(friends, sleep_time=SLEEP_TIME):
    all_history = []
    i = 0
    for friend in friends:
        friend_dialog = get_dialogs(friend)
        time.sleep(sleep_time)
        dialog_len = friend_dialog[0]
        friend_history = []
        if dialog_len > 200:
            rest = dialog_len
            offset = 0
            while rest > 0:
                friend_history += vkapi('messages.getHistory',
                                        user_id=friend,
                                        count=200,
                                        offset=offset,
                                        version='5.74')
                time.sleep(sleep_time)
                rest -= 200
                offset += 200
                if rest > 0:
                    print('--processing', friend, ':', rest,
                          'of', dialog_len, 'messages left')
            all_history += friend_history
        i += 1
        print('processed', i, 'friends of', len(friends))
    return all_history


def get_messages_for_user(data):
    messages = []
    for dialog in data:
        if type(dialog) == dict:
            m_text = re.sub("<br>", " ", dialog['body'])
            messages.append(m_text)
    print('Extracted', len(messages), 'messages in total')
    return messages


def save_vk_messages(data, file_name='vk_messages.txt', my_id=SELF_ID):
    length = len(data)
    with open(file_name, 'w') as f:
        my_message, other_message, current_speaker = "", "", 0
        for index, message in enumerate(data):
            if message['from_id'] == my_id:
                if not my_message:
                    start_index = index - 1
                my_message += message['body'] + ' '
            elif my_message:
                for cnt in range(start_index, 0, -1):
                    tmp_mess = data[cnt]
                    if not tmp_mess['body']:
                        my_message, other_message, current_speaker = "", "", 0
                        break
                    if not current_speaker:
                        current_speaker = tmp_mess['from_id']
                    elif current_speaker != tmp_mess['from_id']:
                        other_message = clean_message(other_message)
                        my_message = clean_message(my_message)
                        f.write(other_message + '\n')
                        f.write(my_message + '\n')
                        break
                    other_message = ' ' + tmp_mess['body'] + ' ' + other_message
                my_message, other_message, current_speaker = "", "", 0
            if index % 100 == 0:
                print('saved {} messages, {} left'.format(index, length - index))


def save_tg_messages(data, file_name='tg_messages.txt', my_id=359134637):
    length = len(data)
    with open(file_name, 'w') as f:
        my_message, other_message, current_speaker = "","",0
        for index, message in enumerate(data):
            if message.from_id == my_id:
                if not my_message:
                    start_index = index - 1
                if message.message:
                    my_message += message.message + ' '
            elif my_message:
                for cnt in range(start_index, 0, -1):
                    tmp_mess = data[cnt]
                    if not tmp_mess.message:
                        my_message, other_message, current_speaker = "","",0
                        break
                    if not current_speaker:
                        current_speaker = tmp_mess.from_id
                    elif current_speaker != tmp_mess.from_id:
                        other_message = clean_message(other_message)
                        my_message = clean_message(my_message)
                        f.write(other_message + '\n')
                        f.write(my_message + '\n')
                        break
                    other_message = ' ' + tmp_mess.message + ' ' + other_message
                my_message, other_message, current_speaker = "","",0
            if index % 100 == 0:
                print('saved {} messages, {} left'.format(index, length - index))


def clean_message(message):
    # Remove new lines within message
    cleanedMessage = message.replace('\n',' ').lower()
    # Remove punctuation
    cleanedMessage = re.sub('([.,!?])','', cleanedMessage)
    # Remove multiple spaces in message
    cleanedMessage = re.sub(' +',' ', cleanedMessage)
    return cleanedMessage


def load_data(file_name):
    with open('vk_messages.dat', 'rb') as f:
        vk_messages = pickle.load(f)
        vk_messages = vk_messages[::-1]
        return vk_messages


if __name__ == '__main__':
    # all_history = get_history(friends)

    # saving vk messages (question; my answere)
    vk_messages = load_data('vk_messages.dat')
    vk_messages = [messages for messages in vk_messages[::-1] if type(messages) == dict]
    save_vk_messages(vk_messages)

    # saving tg messages (question; my answere)
    tg_messages = load_data('tg_messages.dat')
    data = sum(tg_messages, [])
    data = [mes for mes in data[::-1]]
    save_tg_messages(data)

