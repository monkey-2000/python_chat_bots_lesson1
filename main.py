import requests
import telegram
from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
BOT_CHAT_ID = getenv('BOT_CHAT_ID')
DVMN_TOKEN = getenv('DVMN_TOKEN')


def send_message_to_bot(token, chat_id, message):
    """Send message to telegram bot"""
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=message)


def find_out_timestamp_for_new_request(response):
    """Find out the timestamp for a new request, given the status value of the response."""
    messages = response.json()
    if messages['status'] == "found":
        return messages['last_attempt_timestamp']
    elif messages['status'] == "timeout":
        return messages["timestamp_to_request"]
    else:
        return ''


def generate_message(response):
    """Generate message from response for telegram bot"""
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


def main():

    dvmn_headers = {'Authorization': DVMN_TOKEN}
    url = 'https://dvmn.org/api/long_polling/'
    url_with_timestamp = 'https://dvmn.org/api/long_polling/?timestamp={}'

    timeout = 60
    timestamp = None

    while True:
        try:
            if timestamp:
                response = requests.get(url_with_timestamp.format(timestamp), headers=dvmn_headers, timeout=timeout)
                response.raise_for_status()
                timestamp = None
            else:
                response = requests.get(url, headers=dvmn_headers, timeout=timeout)
                response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.HTTPError:
            pass
        else:
            timestamp = find_out_timestamp_for_new_request(response)
            new_messages = generate_message(response)
            for message in new_messages:
                send_message_to_bot(BOT_TOKEN, BOT_CHAT_ID, message)


if __name__ == '__main__':
    main()
