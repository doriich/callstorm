#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Модуль конфигурации CallStorm
Управление настройками системы звонков
"""

import json


class Config:
    """Класс конфигурации"""
    
    def __init__(self, config_data):
        self.target_numbers = config_data.get("target_numbers", [])
        self.call_frequency = config_data.get("call_frequency", 10)  # секунды между звонками
        self.duration = config_data.get("duration", 60)  # максимальное количество звонков
        self.twilio_sid = config_data.get("twilio_sid", "")
        self.twilio_token = config_data.get("twilio_token", "")
        self.twilio_phone = config_data.get("twilio_phone", "")
    
    def add_target_number(self, number):
        """Добавление целевого номера"""
        if number not in self.target_numbers:
            self.target_numbers.append(number)
            return True
        return False
    
    def remove_target_number(self, number):
        """Удаление целевого номера"""
        if number in self.target_numbers:
            self.target_numbers.remove(number)
            return True
        return False
    
    def set_call_frequency(self, frequency):
        """Установка частоты звонков"""
        if frequency > 0:
            self.call_frequency = frequency
            return True
        return False
    
    def set_duration(self, duration):
        """Установка продолжительности атаки"""
        if duration > 0:
            self.duration = duration
            return True
        return False
    
    def set_twilio_credentials(self, sid, token, phone):
        """Установка учетных данных Twilio"""
        self.twilio_sid = sid
        self.twilio_token = token
        self.twilio_phone = phone
        return True
    
    def save_to_file(self, filepath="config/settings.json"):
        """Сохранение конфигурации в файл"""
        config_data = {
            "target_numbers": self.target_numbers,
            "call_frequency": self.call_frequency,
            "duration": self.duration,
            "twilio_sid": self.twilio_sid,
            "twilio_token": self.twilio_token,
            "twilio_phone": self.twilio_phone
        }
        
        try:
            with open(filepath, "w") as f:
                json.dump(config_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            return False