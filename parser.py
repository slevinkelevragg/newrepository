import requests
from bs4 import BeautifulSoup
import subprocess
import validators


def git_commit(message):
    try:
        # Добавляем все изменения в индекс
        subprocess.run(["git", "add", "."], check=True)
        
        # Создаем коммит
        subprocess.run(["git", "commit", "-m", message], check=True)
        
        print("Коммит успешно создан!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении Git-команды: {e}")


def check_git_remote():
    try:
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, check=True)
        print("Удаленные репозитории:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении Git-команды: {e}")


def parse_page(url):
    title = "Заголовок не найден"  # Инициализация переменной
    try:
        # Проверка корректности URL
        if not validators.url(url):
            print("Некорректный URL. Пожалуйста, введите правильный URL.")
            return
        
        # Отправляем GET-запрос
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Парсинг заголовка страницы
        title = soup.title.string if soup.title else "Заголовок не найден"
        print(f"Заголовок страницы: {title}")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
     
    # Сохраняем результат в файл
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"Заголовок: {title}\n")   
    print("Данные сохранены в output.txt")


if __name__ == "__main__":
    # Проверка удаленных репозиториев
    check_git_remote()

    # Создание коммита
    commit_message = input("Введите сообщение для коммита: ")
    git_commit(commit_message)

    # Парсинг страницы
    url = input("Введите URL для парсинга: ")
    parse_page(url)
  