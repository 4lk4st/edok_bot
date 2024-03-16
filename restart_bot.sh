#!/bin/bash

# Получение id процесса "python main.py"
pid=$(pgrep -f "python main.py")

# Остановка процесса с данным id
kill $pid

# Переход в директорию /usr/local/bin/edok_bot/
cd /usr/local/bin/edok_bot/

# Запуск виртуального окружения
source venv/bin/activate

# Запуск бота python main.py
nohup python main.py