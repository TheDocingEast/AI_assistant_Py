import hashlib
import uuid

def hash_password(password):
    # Генерируем случайную соль
    salt = uuid.uuid4().hex
    # Хешируем пароль с солью
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    # Возвращаем хеш и соль
    return f"{hashed_password}:{salt}"

def check_password(hashed_password, user_password):
    # Разделяем хеш и соль
    password, salt = hashed_password.split(":")
    # Хешируем введенный пароль с той же солью
    new_hash = hashlib.sha256((salt + user_password).encode()).hexdigest()
    # Сравниваем хеши
    return password == new_hash

# Вводим пароль
password = input("Введите пароль: ")
# Хешируем пароль
hashed_password = hash_password(password)
print(f"Хешированный пароль: {hashed_password}")

# Проверка пароля
user_password = input("Введите пароль для проверки: ")
if check_password(hashed_password, user_password):
    print("Пароль верный")
else:
    print("Пароль неверный")
