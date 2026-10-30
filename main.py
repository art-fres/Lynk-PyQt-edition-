from PyQt6 import *
import os

#Работа с темами приложения
THEMES = {
    "dark": os.path.join("styles", "dark.qss"),
    "light": os.path.join("styles", "light.qss")
}

def load_theam(name):
    path = THEMES.get(name)

    if path and os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as theme:
            return theme.read()

    return ""


#Работа с базами данных 1. БД для подписок 2. БД для уведомлений


