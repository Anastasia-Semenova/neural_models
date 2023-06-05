import pandas as pd


def process():
    # загружаем датасет в формате csv
    data = pd.read_csv('filename.csv')

    # удаляем строки с ненужными классами
    data = data[~data['label'].isin(['speech', 'skip'])]

    # сохраняем изменения
    data.to_csv('filename_filtered.csv', index=False)


if __name__ == "__main__":
    process()