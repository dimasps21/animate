import os
import hashlib
import base64
from cryptography.fernet import Fernet

# --- Настройка (НЕ МЕНЯЙТЕ ЭТО ПОСЛЕ СОЗДАНИЯ) ---
DATABASE_FILE = "passwords.db"  # Файл для хранения зашифрованных данных
KEY_FILE = "secret.key"         # Файл для хранения ключа шифрования
# ---------------------------------------------

def generate_key():
    """Генерирует новый ключ шифрования и сохраняет его в файл."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Загружает ключ шифрования из файла."""
    if not os.path.exists(KEY_FILE):
        return generate_key() # Создаем, если не существует
    return open(KEY_FILE, "rb").read()

def encrypt(data, key):
    """Шифрует данные с использованием Fernet."""
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt(data, key):
    """Расшифровывает данные с использованием Fernet."""
    f = Fernet(key)
    return f.decrypt(data.encode()).decode()


def create_database_if_not_exists():
    """Создает пустой файл базы данных, если он не существует."""
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as f:
            f.write("")  # Создаем пустой файл

def get_master_password():
    """Получает мастер-пароль от пользователя (скрытно). Хранит хеш."""
    import getpass  # Используем getpass для скрытого ввода пароля
    while True:
        password = getpass.getpass("Введите мастер-пароль: ")
        if len(password) < 8:
            print("Мастер-пароль должен быть не менее 8 символов.")
        else:
            password_confirm = getpass.getpass("Подтвердите мастер-пароль: ")
            if password == password_confirm:
                # Хешируем мастер-пароль перед сохранением
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                return hashed_password
            else:
                print("Пароли не совпадают.")


def store_password(site, username, password, key):
    """Сохраняет зашифрованный пароль в файл."""
    encrypted_username = encrypt(username, key)
    encrypted_password = encrypt(password, key)
    with open(DATABASE_FILE, "a") as f:
        f.write(f"{site}:{encrypted_username}:{encrypted_password}\n")
    print(f"Пароль для сайта '{site}' успешно сохранен.")


def retrieve_password(site, key):
    """Извлекает и расшифровывает пароль из файла."""
    with open(DATABASE_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if parts[0] == site:
                encrypted_username = parts[1]
                encrypted_password = parts[2]
                username = decrypt(encrypted_username, key)
                password = decrypt(encrypted_password, key)
                return username, password
        return None, None  # Сайт не найден


def main():
    create_database_if_not_exists()
    key = load_key()

    # Проверяем, установлен ли мастер-пароль
    master_password_set = False
    try:
        with open(DATABASE_FILE, "r") as f:
            first_line = f.readline().strip()
            if first_line.startswith("MASTER_PASSWORD:"):
                master_password_set = True
    except FileNotFoundError:
        pass # Файл только что создан, мастер-пароля нет

    if not master_password_set:
        print("Мастер-пароль не установлен.")
        master_password = get_master_password()
        # Записываем хеш мастер-пароля в начало файла
        with open(DATABASE_FILE, "w") as f:
            f.write(f"MASTER_PASSWORD:{master_password}\n")

    # Верификация мастер-пароля (заглушка - нужно реализовать)
    # В реальной реализации нужно сравнивать введенный пароль с хешем в файле
    # и только после этого разрешать доступ к данным
    print("\n!!! ВНИМАНИЕ !!! Проверка мастер-пароля НЕ РЕАЛИЗОВАНА.")
    print("Это ОЧЕНЬ ВАЖНО реализовать для безопасности.\n")



    while True:
        print("\nМенеджер паролей:")
        print("1. Сохранить пароль")
        print("2. Получить пароль")
        print("3. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            site = input("Введите название сайта: ")
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            store_password(site, username, password, key)
        elif choice == "2":
            site = input("Введите название сайта: ")
            username, password = retrieve_password(site, key)
            if username and password:
                print(f"Имя пользователя: {username}")
                print(f"Пароль: {password}") # В РЕАЛЬНОМ ПРИЛОЖЕНИИ ЭТО ОПАСНО - ЛУЧШЕ НЕ ВЫВОДИТЬ ПАРОЛЬ
            else:
                print(f"Пароль для сайта '{site}' не найден.")
        elif choice == "3":
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()
