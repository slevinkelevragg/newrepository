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
    """
    Проверяет настроенные удаленные репозитории Git.
    :return: Список удалённых репозиториев или None, если их нет.
    """
    try:
        # Проверяем, является ли текущая директория Git-репозиторием
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Получаем список удалённых репозиториев
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, check=True)
        print("Удаленные репозитории:")
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e.stderr.strip() or 'Не удалось найти Git-репозиторий.'}")
        return None


def update_git_remote(remote_name, new_url):
    """
    Обновляет URL удалённого репозитория.
    :param remote_name: Имя удалённого репозитория (например, 'origin')
    :param new_url: Новый URL удалённого репозитория
    """
    try:
        # Обновляем URL удалённого репозитория
        subprocess.run(["git", "remote", "set-url", remote_name, new_url], check=True)
        print(f"URL удалённого репозитория успешно изменён на: {new_url}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при обновлении удалённого репозитория: {e.stderr.decode().strip()}")


def add_git_remote(remote_name, remote_url):
    """
    Добавляет новый удалённый репозиторий.
    :param remote_name: Имя удалённого репозитория (например, 'origin')
    :param remote_url: URL удалённого репозитория
    """
    try:
        # Добавляем удалённый репозиторий
        subprocess.run(["git", "remote", "add", remote_name, remote_url], check=True)
        print(f"Удалённый репозиторий '{remote_name}' успешно добавлен: {remote_url}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при добавлении удалённого репозитория: {e.stderr.decode().strip()}")


def push_to_remote(branch_name="main"):
    """
    Отправляет изменения в удалённый репозиторий.
    :param branch_name: Имя ветки (по умолчанию 'main')
    """
    try:
        # Отправляем изменения
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
        print(f"Изменения успешно отправлены в ветку '{branch_name}'")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при отправке изменений: {e.stderr.decode().strip()}")


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
    REMOTE_URL = "https://github.com/slevinkelevragg/newrepository.git"
    REMOTE_NAME = "origin"
    BRANCH_NAME = "main"

    while True:
        print("\nВыберите действие:")
        print("1. Проверить удаленные репозитории")
        print("2. Настроить удаленный репозиторий")
        print("3. Создать коммит")
        print("4. Отправить изменения в удаленный репозиторий")
        print("5. Спарсить страницу")
        print("6. Выйти")
        choice = input("Введите номер действия: ")

        if choice == "1":
            check_git_remote()
        elif choice == "2":
            remotes = check_git_remote()
            if remotes and REMOTE_URL in remotes:
                print("Удалённый репозиторий уже настроен.")
            elif remotes and REMOTE_NAME in remotes:
                print("Обновляем URL удалённого репозитория...")
                update_git_remote(REMOTE_NAME, REMOTE_URL)
            else:
                print("Добавляем новый удалённый репозиторий...")
                add_git_remote(REMOTE_NAME, REMOTE_URL)
        elif choice == "3":
            commit_message = input("Введите сообщение для коммита: ")
            git_commit(commit_message)
        elif choice == "4":
            push_to_remote(BRANCH_NAME)
        elif choice == "5":
            url = input("Введите URL для парсинга: ")
            parse_page(url)
        elif choice == "6":
            print("Выход из программы.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")