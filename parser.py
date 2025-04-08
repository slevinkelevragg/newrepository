import requests
from bs4 import BeautifulSoup
import subprocess
import validators


def git_commit(message):
    """Создает коммит в Git."""
    try:
        # Проверяем наличие изменений
        result = subprocess.run(["git", "diff", "--cached", "--quiet"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print("Нет изменений для коммита.")
            return

        # Добавляем все изменения в индекс
        subprocess.run(["git", "add", "."], check=True)

        # Создаем коммит
        subprocess.run(["git", "commit", "-m", message], check=True)

        print("Коммит успешно создан!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении Git-команды: {e.stderr.decode().strip()}")


def check_git_remote():
    """Проверяет настроенные удаленные репозитории Git."""
    try:
        # Проверяем, является ли текущая директория Git-репозиторием
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Получаем список удалённых репозиториев
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, check=True)
        print("Удаленные репозитории:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e.stderr.strip() or 'Не удалось найти Git-репозиторий.'}")


def parse_page(url):
    """Парсит заголовок страницы по заданному URL и сохраняет результат в файл."""
    title = "Заголовок не найден"  # Инициализация переменной
    try:
        # Проверка корректности URL
        if not validators.url(url):
            print("Некорректный URL. Пожалуйста, введите правильный URL.")
            return

        # Отправляем GET-запрос
        response = requests.get(url, timeout=10)  # Добавляем таймаут
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Парсинг заголовка страницы
        title_tag = soup.title
        title = title_tag.string.strip() if title_tag and title_tag.string else "Заголовок не найден"
        print(f"Заголовок страницы: {title}")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")

    # Сохраняем результат в файл
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(f"URL: {url}\nЗаголовок: {title}\n{'-' * 40}\n")
    print("Данные сохранены в output.txt")


if __name__ == "__main__":
    while True:
        print("\nВыберите действие:")
        print("1. Проверить удаленные репозитории")
        print("2. Создать коммит")
        print("3. Спарсить страницу")
        print("4. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            check_git_remote()
        elif choice == "2":
            commit_message = input("Введите сообщение для коммита: ")
            git_commit(commit_message)
        elif choice == "3":
            url = input("Введите URL для парсинга: ")
            parse_page(url)
        elif choice == "4":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")
  