# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import pprint

import telegram
from os import getenv
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN=getenv('BOT_TOKEN')
BOT_CHAT_ID=getenv('BOT_CHAT_ID')
DVMN_TOKEN=getenv('DVMN_TOKEN')


def find_late_timestamp(response, status='results'):
    print(response.json())
    results = response.json()[status]
    results.sort(key=lambda x: -x['timestamp'])
    return results[0]['timestamp']


# 'new_attempts'

def return_timestamp_to_request(response):
    messages = response.json()
    if messages['status'] == "found":
        return messages['last_attempt_timestamp']
    elif messages['status'] == "timeout":
        return messages["timestamp_to_request"]
    else:
        return ''


def get_with_long_poling(headers):
    url = 'https://dvmn.org/api/long_polling/'
    url_with_timestamp = 'https://dvmn.org/api/long_polling/?timestamp={}'
    timestamp = None
    timeout = 60

    while True:
        try:
            print(1)
            print(timestamp)
            if timestamp:
                response = requests.get(url_with_timestamp.format(timestamp), headers=headers, timeout=timeout)
                response.raise_for_status()
                timestamp = None
            else:
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()


        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.HTTPError:
            pass
        # raise HTTPError(http_error_msg, response=self)
        # requests.exceptions.HTTPError: 400 # Client
        # Error: Bad # Request # for url: https: // dvmn.org / api / long_polling /
        else:
            timestamp = return_timestamp_to_request(response)
            new_messages=generate_message(response)
            for message in new_messages:
                communication_with_bot(BOT_TOKEN, BOT_CHAT_ID, message)
            communication_with_bot(BOT_TOKEN, BOT_CHAT_ID, response.json())
            pprint.pprint(response.json())


def generate_message(response):
    response_messages = response.json()

    if response_messages['status'] == "found":

        new_message = 'У вам проверили работу "{title}"\nURL:{URL}\n\n{result}'
        attemp_list = response_messages['new_attempts']
        new_message_list = []
        for attemp in attemp_list:
            lesson_url = attemp['lesson_url']

            if attemp['is_negative']:
                job_review_result = 'К сожалению, в работе нашлись ошибки.'
            else:
                job_review_result = 'Преподавателю все понравилось,' \
                                    'можно приступать к следующему уроку!'

            new_message_list.append(new_message.format(
                        title=attemp['lesson_title'],
                        URL=lesson_url,
                        result=job_review_result))
        return new_message_list

    elif response_messages['status'] == "timeout":
        pass


def communication_with_bot(token, chat_id, message):
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def main():

    url = 'https://dvmn.org/api/user_reviews/'
    dvmn_headers = {'Authorization': DVMN_TOKEN}

    get_with_long_poling(dvmn_headers)


    # response = requests.get(url, headers=dvmn_headers, timeout=5)
    # response_result = response.json()
#  # #
#  find_late_timestamp(response)
#
# response_result['results'].sort(key=lambda x: -x['timestamp'])
# timestamp = response_result['results'][0]['timestamp']
# for message in response.json()['results']:
#     print(message['timestamp'])
#
# print(timestamp)


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
