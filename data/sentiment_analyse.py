from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import pandas as pd

# загружаем токенизатор и модель GPT2
tokenizer = GPT2Tokenizer.from_pretrained('sberbank-ai/rugpt3large_based_on_gpt2')
model = GPT2LMHeadModel.from_pretrained('sberbank-ai/rugpt3large_based_on_gpt2')

# запускаем модель на GPU, если он доступен, иначе на CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)


def sentiment_analysis(text):
    # токенизируем текст
    inputs = tokenizer(text, return_tensors='pt')

    # генерируем ответ модели, получаем последовательность токенов
    outputs = model(**inputs)
    logits = outputs.logits
    tokens = torch.argmax(logits, dim=-1).squeeze()

    # декодируем полученную последовательность токенов и передаем ее модели для классификации
    labels_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
    prompt = tokenizer.decode(tokens)
    prompt = prompt[prompt.find(text):]
    prompt = prompt[len(text):prompt.find('<')]
    prompt = prompt.strip()
    prompt = 'sentiment: ' + prompt
    prompt_encoded = tokenizer(prompt, return_tensors='pt').input_ids.to(device)
    prompt_length = len(tokenizer.encode(prompt))
    outputs = model.generate(prompt_encoded, do_sample=False, max_length=prompt_length+1)

    # декодируем полученную последовательность токенов и возвращаем классификацию
    output_str = tokenizer.decode(outputs[0]).split(':')[-1].strip()
    return labels_map[int(output_str) if output_str.isdigit() else 1]


if __name__ == "__main__":
    # загружаем датасет в формате txt
    data = pd.read_csv('filename_filtered.csv')

    # создаем DataFrame для записи результатов предсказаний
    df = pd.DataFrame(columns=['text', 'expected', 'predicted'])

    # проходим по всему датасету, делаем предсказания и записываем результаты в DataFrame
    for i in range(len(data)):
        row = data.iloc[i]
        text = row['text'].strip()
        expected = row['label'].strip()
        print(expected)
        predicted = sentiment_analysis(text)
        print(predicted + "    ------")
        df.loc[i] = [text, expected, predicted]

    # выводим точность модели
    accuracy = (df['expected'] == df['predicted']).sum() / len(df)
    print(f'Accuracy: {accuracy}')