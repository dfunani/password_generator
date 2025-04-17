import json
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choices
from sys import argv

from encryption import Cryptography

PASSWORD_LENGTH = 21


def read_passwords():
    with open("secrets.txt", "r") as file:
        encrypted = file.read().strip()
        decrypted = Cryptography().decrypt(encrypted.encode()).decode()
        passwords = json.loads(decrypted)
        return passwords


def remove_password(app: str):
    with open("secrets.txt", "r") as file:
        encrypted = file.read().strip()
        decrypted = Cryptography().decrypt(encrypted.encode()).decode()
        passwords = json.loads(decrypted)

        try:
            del passwords[app]
        except BaseException as e:
            print(f"Password Could not be Deleted - {str(e)}")

        write_passwords(passwords)


def write_passwords(passwords: dict):
    with open("secrets.txt", "w") as file:
        text = json.dumps(passwords)
        encrypted = Cryptography().encrypt(text.encode())
        file.write(encrypted.decode() + "\n")


def main(length: int, username: str, app: str):
    passwords = read_passwords()

    array = choices(ascii_lowercase + ascii_uppercase + digits + punctuation, k=length)
    password = "".join(array)

    if app in passwords:
        print("Password already exists for this app")
    else:
        passwords.update({app: {"password": password, "username": username}})
        print(password)

    write_passwords(passwords)


if __name__ == "__main__":
    if len(argv) == 2 and argv[1] == "all":
        print(json.dumps(read_passwords(), indent=4))
    elif len(argv) == 3 and argv[1] == "remove":
        remove_password(argv[2])
    elif len(argv) == 3 and argv[1] == "get":
        print(
            json.dumps(
                read_passwords().get(
                    argv[2], f"Password Could not Be Retrieved - '{argv[2]}'"
                ),
                indent=4,
            )
        )
    elif len(argv) != 4:
        print("Usage: python main.py [APP] [USERNAME] [PASSWORD_LENGTH]")
    else:
        main(int(argv[3]), argv[2], argv[1])
