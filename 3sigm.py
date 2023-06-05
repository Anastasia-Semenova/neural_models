import pandas as pd


def clean_3sigm(region, number):
    df = pd.read_csv(f'{region}/{number}_filtered.csv')
    print(df.head())

    mean = df.mean()
    std = df.std()

    lower_limit = mean - 3 * std
    upper_limit = mean + 3 * std

    filtered_df = df[
        (df['friend_count'] > lower_limit['friend_count'])
        & (df['friend_count'] < upper_limit['friend_count'])
        & (df['followers_count'] > lower_limit['followers_count'])
        & (df['followers_count'] < upper_limit['followers_count'])
        & (df['pages'] > lower_limit['pages'])
        & (df['pages'] < upper_limit['pages'])
        & (df['groups'] > lower_limit['groups'])
        & (df['groups'] < upper_limit['groups'])
        & (df['posts_last_year'] > lower_limit['posts_last_year'])
        & (df['posts_last_year'] < upper_limit['posts_last_year'])
        & (df['posts_likes'] > lower_limit['posts_likes'])
        & (df['posts_likes'] < upper_limit['posts_likes'])
        & (df['photos_last_year'] > lower_limit['photos_last_year'])
        & (df['photos_last_year'] < upper_limit['photos_last_year'])
        & (df['photo_likes'] > lower_limit['photo_likes'])
        & (df['photo_likes'] < upper_limit['photo_likes'])
        ]

    filtered_df.to_csv(f'{region}/{number}_filtered_no_outliers.csv', index=False)


if __name__ == "__main__":
    clean_3sigm('bashkortostan', 8)
