import json
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choices
import sys

from encryption import Cryptography

PASSWORD_LENGTH = 21

def generate_password_file():
    with open("secrets.txt", "r") as file:
        encrypted = file.read().strip()
        decrypted = Cryptography().decrypt(encrypted.encode()).decode()
        passwords = json.loads(decrypted)
        with open("passwords.json", "w") as file:
            json.dump(passwords, file)

def main(length, username, app):
    with open("password.json", "r") as file:
        passwords = json.load(file)
    
    array = choices(ascii_lowercase + ascii_uppercase + digits + punctuation, k=length)
    password = "".join(array)
    
    if app in passwords:
        print("Password already exists for this app")
    else:
        with open("password.json", "w") as file:
            passwords.update({app: {"password": password, "username": username}})
            json.dump(passwords, file)
    
    with open("secrets.txt", "w") as file:
        text = json.dumps(passwords)
        encrypted = Cryptography().encrypt(text.encode())
        file.write(encrypted.decode() + "\n")


if __name__ == "__main__":
    argv = sys.argv

    if len(argv) == 2 and argv[1] == "generate":
        generate_password_file()
    elif len(argv) != 4:
        print("Usage: python main.py [APP] [USERNAME] [PASSWORD_LENGTH]")
    else:
        main(int(argv[3]), argv[2], argv[1])