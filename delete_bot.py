import pandas as pd

id = 8
filtered_file = f'bashkortostan/{id}_filtered_no_outliers.csv'
result_file = f'bashkortostan/{id}_main.csv'

if __name__ == "__main__":
    # загружаем csv файл в dataframe
    df = pd.read_csv(filtered_file)

    # оставляем только те строки, в которых сумма значений в столбцах friend_count, followers_count, pages, groups, posts_last_year, posts_likes, photos_last_year, photo_likes не равна нулю
    df = df[(df['friend_count'] + df['followers_count'] + df['pages'] + df['groups'] + df['posts_last_year'] + df[
        'posts_likes'] + df['photos_last_year'] + df['photo_likes']) != 0]

    # сохраняем новый dataframe в csv файл
    df.to_csv(result_file, index=False)