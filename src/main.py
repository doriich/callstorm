#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CallStorm - Атака звонками
Основной модуль приложения
"""

import os
import sys
import time
import json
from call_system import CallSystem
from config import Config


def show_menu():
    """Отображение главного меню"""
    print("\n===== CallStorm - Атака звонками =====")
    print("1. Запустить атаку звонками")
    print("2. Настроить параметры атаки")
    print("3. Просмотреть статистику")
    print("4. Остановить атаку")
    print("5. Выход")
    print("=" * 40)


def load_config():
    """Загрузка конфигурации"""
    try:
        with open("config/settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Файл конфигурации не найден. Создаю новый...")
        default_config = {
            "target_numbers": [],
            "call_frequency": 10,
            "duration": 60,
            "twilio_sid": "",
            "twilio_token": "",
            "twilio_phone": ""
        }
        with open("config/settings.json", "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config


def main():
    """Главная функция приложения"""
    print("Добро пожаловать в CallStorm - атака звонками!")
    
    # Загрузка конфигурации
    config_data = load_config()
    config = Config(config_data)
    
    # Инициализация системы звонков
    call_system = CallSystem(config)
    
    while True:
        show_menu()
        choice = input("Выберите действие (1-5): ").strip()
        
        if choice == "1":
            print("Запуск атаки звонками...")
            call_system.start_attack()
        elif choice == "2":
            print("Настройка параметров атаки...")
            # Здесь будет код для настройки
            print("Функция настройки будет реализована позже")
        elif choice == "3":
            print("Просмотр статистики...")
            call_system.show_statistics()
        elif choice == "4":
            print("Остановка атаки...")
            call_system.stop_attack()
        elif choice == "5":
            print("Спасибо за использование CallStorm. До свидания!")
            sys.exit(0)
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()