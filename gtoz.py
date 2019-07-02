from github import Github
import time
import schedule
import requests
import json
import logging
import os

logging.basicConfig(filename='debug.log', format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

"""
GITHUB CREDENTIALS
"""
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)
github_user = g.get_user()


"""
ZENDESK CREDENTIALS
"""
ZENDESK_URL = os.environ.get('ZENDESK_URL')
ZENDESK_EMAIL = os.environ.get('ZENDESK_EMAIL') + '/token'
ZENDESK_TOKEN = os.environ.get('ZENDESK_TOKEN')

"""
CRON JOB
"""
SCHEDULE_INTERVAL_MINUTES = int(1)


def notification_count():
    notif_count = github_user.get_notifications().totalCount
    logging.info("You have {} notifications.".format(notif_count))

    return notif_count


def notification_parser():
    for notification in github_user.get_notifications():
        if notification.subject.latest_comment_url is None:
            mark_notification_read(notification.id)
        else:
            comment_content = get_comment_data(notification)
            create_zendesk_ticket(comment_content)
            mark_notification_read(notification.id)


def mark_notification_read(notification_id):
    headers = {'Authorization': 'token ' + GITHUB_TOKEN}
    requests.patch("https://api.github.com/notifications/threads/{}".format(notification_id), headers=headers)
    notification_count()


def get_comment_data(notif):
    issue_subject = notif.subject.title
    issue_url = requests.get(notif.subject.latest_comment_url).json()['html_url']
    issue_comment = requests.get(notif.subject.latest_comment_url).json()['body']

    return {"url": issue_url, "comment": issue_comment, "subject": issue_subject}


def create_zendesk_ticket(comment_content):

    # New ticket info
    subject = 'Comment on Github ' + comment_content['subject']
    body = "Kindly review the comment on {}".format(comment_content['url']) + \
           "\n" + "Comment" + "\n" + comment_content['comment']

    # Package the data in a dictionary matching the expected JSON
    data = {'ticket': {'subject': subject, 'comment': {'body': body}}}

    # Encode the data to create a JSON payload
    payload = json.dumps(data)

    # Set the request parameters
    headers = {'content-type': 'application/json'}

    # Do the HTTP post request
    response = requests.post(ZENDESK_URL, data=payload, auth=(ZENDESK_EMAIL, ZENDESK_TOKEN), headers=headers)

    # Check for HTTP codes other than 201 (Created)
    if response.status_code != 201:
        logging.error('Status:', response.status_code, 'Problem with the request. Exiting.')

    # Report success
    logging.info('Successfully created the ticket.')


def main():
    notif_count = notification_count()

    if notif_count == 0:
        pass
    else:
        notification_parser()


# Executes a function at every X minutes. Reference - https://stackoverflow.com/a/55756963
schedule.every(SCHEDULE_INTERVAL_MINUTES).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(1)
