import praw
import csv
from urllib.parse import urlparse, parse_qs
from database import add_to_table

# replace CLIENT-ID, CLIENT-SECRET, USERNAME, PASSWORD with your own
CLIENT_ID = 'CLIENT-ID'
CLIENT_SECRET = 'CLIENT-SECRET'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"


def filter_url(url):
    """
    Return Youtube viedo ID from URL


    Keyword arguments:
     url -- Full URL of Youtube
    :return: Video ID(String) of youtube link
    """

    if url.startswith(('youtu', 'www', 'm.youtube')):
        url = 'http://' + url

    query = urlparse(url)
    # print(query.hostname)

    video_id = ''

    # for full length youtube URL
    if 'youtube' in query.hostname:
        if query.path == '/watch':
            video_id = parse_qs(query.query)['v'][0]
        # for embed url
        elif query.path.startswith(('/embed/', '/v/')):
            video_id = query.path.split('/')[2]

    # for shorten URL
    elif 'youtu.be' in query.hostname:
        video_id = query.path[1:]

    # if it isn't even a youtube URL :3
    else:
        raise ValueError

    # remove any extra query eg. start at
    if '?' in video_id:
        video_id = video_id.split('?')[0]

    return video_id


def get_data():
    """
    Get Title and url from sub reddit using PRAW


    :return:
    postTitle -- List of post title
    postURL -- List of youtube URL
    """
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         password=PASSWORD,
                         user_agent=USER_AGENT,
                         username=USERNAME)

    # print(reddit.read_only)
    # enable read only mode for reading data
    reddit.read_only = True

    postTitles = []
    postURL = []

    for post in reddit.subreddit('cringe').top():
        # OLD formate
        # if 'www.youtube.com/' in post.url or 'youtu.be/' in post.url:
        #     postTitles.append(post.title)
        #
        #     if 'youtu.be' in post.url:
        #         videoID = post.url.split('/')[-1]
        #         postURL.append('https://www.youtube.com/watch?v='+videoID)
        #     else:
        #         postURL.append(post.url)


        # filter_url(post.url)

        if 'youtube.com' in post.url or 'youtu.be/' in post.url:
            postTitles.append(post.title)
            tube_url = 'https://www.youtube.com/watch?v=' + filter_url(post.url)
            postURL.append(tube_url)

    return postTitles, postURL


# Write into CSV file
def save_csv(postTitles, postURL):
    """
    Save data into CSV file


    Keyword arguments
     postTitles -- List of Title
     postURL -- List of URL
    """
    with open('tube.csv', 'w') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Title', 'URL'])

        for i in range(len(postTitles)):
            writer.writerow([postTitles[i], postURL[i]])

    print('Writing is done')


def save_database(postTitles, postURL):
    """
    Save data into Database


    Keyword arguments
     postTitles -- List of Title
     postURL -- List of URL
    """
    for i in range(len(postTitles)):
        add_to_table(postTitles[i], postURL[i])


if __name__ == '__main__':
    postTitles, postURL = get_data()
    # save_csv(postTitles, postURL)
    save_database(postTitles, postURL)
