import pandas as pd
import datetime


id = 1
filtered_file = f'tatarstan/{id}_main.csv'
result_file = 'tatarstan/result.csv'
some_file = 'result.csv'


def get_social_activity_score(row): return (row['friend_count'] + row['followers_count'] + row['pages'] + row[
    'groups']) * 0.25 + (row['posts_last_year'] + row['photos_last_year']) * 0.5 + row['posts_likes'] + row[
                                               'photo_likes']


def get_social_isolation_score(row): return (row['friend_count'] + row['followers_count'] + row['pages'] + row[
    'groups']) * 0.25 - (row['posts_last_year'] + row['posts_likes'] + row['photos_last_year'] + row['photo_likes'])


def get_total_score(row): return row['friend_count'] + row['followers_count'] + row['pages'] + row['groups'] + row[
    'posts_last_year'] + row['posts_likes'] + row['photos_last_year'] + row['photo_likes']


def get_happiness_index(row):
    social_activity_score = get_social_activity_score(row)
    social_isolation_score = get_social_isolation_score(row)
    total_score = get_total_score(row)
    return (social_activity_score - social_isolation_score) / total_score


def new_happy(row):
    return (0.2*(row['friend_count']+row['followers_count'] + row['pages'] + row['groups']) + 0.4*(row[
    'posts_last_year'] + row['posts_likes']) + 0.4*(row['photos_last_year'] + row['photo_likes']))


def mean():
    df = pd.read_csv(some_file)

    # выбор столбца значения индексов
    index_col = 'Happiness Index'
    index_values = df[index_col]

    # вычисление минимального и максимального значения индексов
    index_min = index_values.min()
    index_max = index_values.max()
    print(index_min, index_max)

    # преобразование значений индексов по методу Min-Max
    index_new = ((index_values - index_min) / (index_max - index_min))

    # замена исходных значений в столбце индексов на преобразованные
    df[index_col] = index_new

    # сохранение изменений в файле result.csv
    df.to_csv(some_file, index=False)
    print(df['Happiness Index'].mean())
    mean = df['Happiness Index'].mean()
    write_norm_file(mean)


def write_norm_file(mean):
    new_df = pd.DataFrame({
        'id': id,
        'mean': mean,
        'data': [datetime.date.today().strftime('%d.%m.%Y')]
    })


    # new_df = pd.concat([new_df, new_df], ignore_index=True)

    # сохранение изменений в файле results.csv
    new_df.to_csv(result_file, mode='a', header=False, index=False)


if __name__ == "__main__":
    df = pd.read_csv(filtered_file)
    df['Happiness Index'] = df.apply(get_happiness_index, axis=1)
    mean_happiness_index = df['Happiness Index'].mean()
    # сохранение результатов в новый csv файл с двумя столбцами: id и Happiness Index
    df[['id', 'Happiness Index']].to_csv(some_file, index=False)
    mean()
