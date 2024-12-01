import openai
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Установка API-ключа
openai.api_key = os.getenv("OPENAI_API_KEY")

# Параметры токенов
token_max = 600


# Функция для чтения файлов
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Функция для записи файлов
def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


# Функция для подсчёта токенов
def count_tokens(text):
    return len(text.split())


# Функция для генерации резюме
def generate_summary(document_text):
    # Подсчёт входящих токенов
    input_tokens = count_tokens(document_text)

    # Промпт на русском языке
    prompt = f'''Вы — документалист. Ваша задача — анализировать документы, 
выделять основные темы и генерировать краткое резюме.
Используйте следующий формат JSON:
{{
    "topics": ["тема1", "тема2", "тема3"],
    "summary": "Краткое резюме документа"
}}
Документ: {document_text}
'''

    # Вызов OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=token_max  # Установлен лимит токенов
    )

    # Извлечение результата и подсчёт выходящих токенов
    output = response['choices'][0]['message']['content']
    output_tokens = count_tokens(output)

    # Вывод токенов для отладки
    print(f"Входящие токены: {input_tokens}, Выходящие токены: {output_tokens}")

    return output


# Путь к папке с файлами
folder_path = './files'
transcript_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

# Обработка файлов и генерация резюме
summaries = []
for i, file_name in enumerate(transcript_files, start=1):
    print(f"Обработка файла: {file_name}...")
    chunk_text = read_file(file_name)
    summary = generate_summary(chunk_text)
    summaries.append(summary)

    # Сохраняем резюме в файл
    write_file(f"summary_{i}.txt", summary)

# Объединяем все резюме
final_summary = "\n\n".join(summaries)
write_file("final_summary.txt", final_summary)

print("Резюме успешно сгенерированы и сохранены.")
