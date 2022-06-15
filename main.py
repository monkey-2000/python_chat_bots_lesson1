from time import sleep
from os import getenv

import requests
import telegram
from dotenv import load_dotenv

from bot_logger import get_logger


FAIL_ATTEMPTS_COUNT = 10
SLEEP_TIME = 60 * 2



def find_out_timestamp_for_new_request(response):
    """Find out the timestamp for a new request, given the status value of the response."""
    messages = response.json()
    if messages['status'] == "found":
        return messages['last_attempt_timestamp']
    elif messages['status'] == "timeout":
        return messages["timestamp_to_request"]
    else:
        return ''


def generate_message(response_messages):
    """Generate message from response for telegram bot."""

    new_message = 'У Вас проверили работу "{title}"\nURL:{URL}\n\n{result}'
    attemps = response_messages['new_attempts']
    new_messages = []
    for attemp in attemps:
        lesson_url = attemp['lesson_url']

        if attemp['is_negative']:
            job_review_result = 'К сожалению, в работе нашлись ошибки.'
        else:
            job_review_result = 'Преподавателю все понравилось,' \
                                'можно приступать к следующему уроку!'

        new_messages.append(new_message.format(
            title=attemp['lesson_title'],
            URL=lesson_url,
            result=job_review_result))
    return new_messages


def main():

    load_dotenv()
    bot_token = getenv('BOT_TOKEN')
    bot_chat_id = getenv('BOT_USER_ID')
    dvmn_token = getenv('DVMN_TOKEN')

    bot = telegram.Bot(token=bot_token)
    logger = get_logger('dvmn_bot_logger', bot=bot, chat_id=bot_chat_id)
    dvmn_headers = {'Authorization': dvmn_token}
    url = 'https://dvmn.org/api/long_polling/'

    params = {}
    timeout = 60
    fail_count = 0

    logger.info("Бот запущен.")
    while True:

        try:
            response = requests.get(
                url=url,
                headers=dvmn_headers,
                params=params,
                timeout = timeout)
            response.raise_for_status()

        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            fail_count += 1
            if fail_count >= FAIL_ATTEMPTS_COUNT:
                sleep(SLEEP_TIME)

        except requests.exceptions.HTTPError:
            pass

        messages = response.json()

        if messages['status'] == "timeout":
            params["timestamp"] = messages["timestamp_to_request"]

        elif messages['status'] == "found":
            params["timestamp"] = messages['last_attempt_timestamp']

            new_messages = generate_message(messages)

            for message in new_messages:
                bot.send_message(chat_id=bot_chat_id, text=message)


if __name__ == '__main__':
    main()
