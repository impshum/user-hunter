import praw
import configparser
import datetime
from psaw import PushshiftAPI


class C:
    W, G, R, P, Y, C = '\033[0m', '\033[92m', '\033[91m', '\033[95m', '\033[93m', '\033[36m'


def get_psaw_stats(api, username, target_subreddit):
    username = username.replace('u/', '')
    result = api.redditor_subreddit_activity(
        username, subreddit=target_subreddit)
    submission_count = result['submission'][target_subreddit]
    comment_count = result['comment'][target_subreddit]
    return f'\n\nSubmissions|Comments\n:-:|:-:\n{submission_count}|{comment_count}'


def main():
    config = configparser.ConfigParser()
    config.read('conf.ini')
    reddit_user = config['REDDIT']['reddit_user']
    reddit_pass = config['REDDIT']['reddit_pass']
    client_id = config['REDDIT']['client_id']
    client_secret = config['REDDIT']['client_secret']
    target_subreddit = config['REDDIT']['target_subreddit']
    contact_user = config['SETTINGS']['contact_user']
    contact_message = int(config['SETTINGS']['contact_message'])
    reply = config['SETTINGS']['reply']
    get_stats = int(config['SETTINGS']['get_stats'])
    test_mode = int(config['SETTINGS']['test_mode'])

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent='User hunter (by u/impshum)',
                         username=reddit_user,
                         password=reddit_pass)

    api = PushshiftAPI()

    if test_mode:
        t = f'{C.R}TEST MODE{C.Y}'
    else:
        t = ''

    if contact_message:
        bot_msg = f"\n\n> *^Beep, ^boop, ^I'm ^a ^bot ^and ^this ^action ^was ^performed ^automagically. ^Please ^contact ^u/{contact_user} ^if ^you ^have ^any ^questions ^or ^concerns.*"
    else:
        bot_msg = ''

    if not get_stats:
        stats = ''

    print(f"""{C.Y}
╦ ╦╔═╗╔═╗╦═╗  ╦ ╦╦ ╦╔╗╔╔╦╗╔═╗╦═╗
║ ║╚═╗║╣ ╠╦╝  ╠═╣║ ║║║║ ║ ║╣ ╠╦╝ {t}
╚═╝╚═╝╚═╝╩╚═  ╩ ╩╚═╝╝╚╝ ╩ ╚═╝╩╚═ {C.C}v1.0{C.W}
    """)

    for submission in reddit.subreddit(target_subreddit).stream.submissions():
        title = submission.title
        for word in title.split(' '):
            if word.startswith(('u/', '/u/')):
                username = word.replace('/u/', 'u/')
                if get_stats:
                    stats = get_psaw_stats(api, username, target_subreddit)
                if not test_mode:
                    reply = reply.format(username) + stats + bot_msg
                    submission.reply(reply)
                print(f'{C.P}{datetime.datetime.now():%H:%M:%S %d/%m/%Y} {C.C}{username}{C.W}')


if __name__ == '__main__':
    main()
