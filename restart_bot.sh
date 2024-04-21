#!/bin/bash

# Остановка всех процессов с ботом, на всякий случай 5 раз
pkill -f 'python main.py'
pkill -f 'python main.py'
pkill -f 'python main.py'
pkill -f 'python main.py'
pkill -f 'python main.py'

# Очистка лога
rm nohup.out

# Запуск бота python main.py
sleep 3
nohup python main.py