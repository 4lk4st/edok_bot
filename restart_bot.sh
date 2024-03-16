#!/bin/bash

# Получение id процесса "python main.py"
pid=$(pgrep -f "python main.py")

# Остановка процесса с данным id
kill $pid

# Запуск бота python main.py
sleep 3
nohup python main.py