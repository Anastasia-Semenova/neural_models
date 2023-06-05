import vk_api
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

data_file = 'bashkortostan/1_data.csv'
filtered_file = 'bashkortostan/1_filtered.csv'
TOKEN = os.getenv('TOKEN')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')


def get_info(vk, id):
    sender_info = vk.users.get(user_ids={id},
                               fields='city, country, home_town, bdate, counters, followers_count, timezone, status, sex, followers',
                               version=5.89)[0]
    if not sender_info['is_closed']:
        int_id = sender_info['id']
        # print(sender_info)
        count = 100
        now = datetime.now()
        year_ago = now - timedelta(days=365)
        # параметры запроса
        params = {
            'owner_id': int_id,
            'count': count
        }
        paramsphoto = {
            'owner_id': int_id,
            'count': count,
            'extended': 1,
            'fields': 'photo'
        }
        responsephotos = vk.photos.getAll(**paramsphoto)
        response = vk.wall.get(**params)
        posts_count = 0
        posts_likes = 0
        for item in response['items']:
            date = datetime.fromtimestamp(item['date'])
            if date >= year_ago:
                posts_count += 1
                posts_likes += item['likes']['count']
        photo_likes = 0
        photos_count = 0
        for item in responsephotos['items']:
            date = datetime.fromtimestamp(item['date'])
            if date >= year_ago:
                photos_count += 1
                photo_likes += item['likes']['count']

        id = sender_info['id']
        try:
            city = sender_info['city']['id']
        except KeyError:
            city = -1
        try:
            country = sender_info['country']['id']
        except KeyError:
            country = -1
        # home_town = sender_info['home_town']
        friend_count = sender_info['counters']['friends']
        followers_count = sender_info['counters']['followers']
        try:
            bdate = sender_info['bdate']
        except KeyError:
            bdate = -1
        try:
            groups_count = sender_info['counters']['groups']
        except KeyError:
            groups_count = -1
        sex = sender_info['sex']
        pages = sender_info['counters']['pages']
        if bdate != -1:
            try:
                birthdate_date = datetime.strptime(bdate, "%d.%m.%Y").date()
                today_date = datetime.today().date()
                age = today_date.year - birthdate_date.year - (
                        (today_date.month, today_date.day) < (birthdate_date.month, birthdate_date.day))
            except ValueError:
                age = -1
        else:
            age = -1
        data = [
            id, sex, age, city, country, friend_count, followers_count, pages, groups_count, posts_count, posts_likes,
            photos_count,
            photo_likes
        ]
        write_csv(data)


def write_csv(data):
    # wr = pd.DataFrame(columns=['id', 'sex', 'age', 'city', 'country', 'friend_count', 'followers_count', 'pages', 'groups', 'posts_last_year', 'posts_likes', 'photos_last_year', 'photo_likes'])
    # wr.to_csv('1_data.csv', index=False)

    df = pd.read_csv(data_file)
    df.loc[len(df)] = data
    df.set_index('id', inplace=True)
    df = df[~df.index.duplicated(keep='last')]
    df.to_csv(data_file, index=True)


def connect_vk():
    vk_session = vk_api.VkApi(
        token=TOKEN,
        login=LOGIN,
        password=PASSWORD)
    vk = vk_session.get_api()
    # get_info(vk, id)
    return vk


def collect_data(vk):
    collecting = vk.users.search(count=1000, city=264, sex=2, age_from=55, age_to=100, sort=0)
    return collecting


def clean_data(id_country_1, id_country_2, id_country_3):
    df = pd.read_csv(data_file)
    df = df[df['groups'] != -1]
    df = df[(df['city'] == id_country_1) | (df['city'] == id_country_2) | (df['city'] == id_country_3)]
    df.to_csv(filtered_file, index=False)


if __name__ == "__main__":
    vk = connect_vk()
    coll = collect_data(vk)
    # print(coll)
    for item in coll['items']:
        get_info(vk, item['id'])
    # clean_data(151, 135, 264)
