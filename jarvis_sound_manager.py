# jarvis_sound_manager.py - МЕНЕДЖЕР ЗВУКОВЫХ ФАЙЛОВ ДЛЯ ДЖАРВИСА
import os
import random
import pygame
import threading
import time
import json
from datetime import datetime

class JarvisSoundManager:
    def __init__(self, voice_pack="original"):
        self.voice_pack = voice_pack
        # Правильные пути к папкам голосов
        self.voice_folders = {
            "original": "jarvis_sounds_original",
            "haudi": "jarvis_sounds_haudi", 
            "remaster": "jarvis_sounds_remaster"
        }
        self.sounds_dir = self.voice_folders.get(voice_pack, "jarvis_sounds_original")
        self.sounds = {}
        self.config = {}
        self.pygame_initialized = False
        self.current_sound = None
        self.voice_pack = voice_pack
        print(f"JarvisSoundManager инициализирован с голосом: {voice_pack}")
        
        print(f"Инициализация звукового менеджера: {self.voice_pack}")
        print(f"Папка звуков: {self.sounds_dir}")
        
        # Создаем папку для звуков если нет
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
            print(f"Создана папка: {self.sounds_dir}")
            
        self.load_config()
        self.load_sounds()

    def set_voice_pack(self, voice_pack):
        """Переключить голосовой пакет"""
        valid_packs = ["original", "haudi", "remaster"]
        if voice_pack not in valid_packs:
            print(f"Неверный голосовой пакет: {voice_pack}")
            return False
            
        print(f"set_voice_pack вызван: {voice_pack}")
            
        if voice_pack != self.voice_pack:
            old_pack = self.voice_pack
            self.voice_pack = voice_pack
            self.sounds_dir = self.voice_folders.get(voice_pack, "jarvis_sounds_original")
            
            print(f"Переключение голоса: {old_pack} -> {voice_pack}")
            print(f"Папка звуков: {self.sounds_dir}")
            
            # Останавливаем текущий звук
            self.stop_current_sound()
            
            # Перезагружаем конфиг и звуки
            self.load_config()
            success = self.load_sounds()
            
            if success:
                print(f"Голос успешно переключен на: {voice_pack}")
                return True
            else:
                # В случае ошибки возвращаем старый голос
                self.voice_pack = old_pack
                self.sounds_dir = self.voice_folders.get(old_pack, "jarvis_sounds_original")
                self.load_config()
                self.load_sounds()
                print(f"Ошибка переключения голоса, возвращен: {old_pack}")
                return False
        else:
            print(f"Голос уже установлен: {voice_pack}")
        return True
    
    def load_config(self):
        """Загрузить конфигурацию звуков для каждого голоса"""
        configs = {
            "original": {
                "sounds": {
                    "thanks": "thanks.wav",
                    "stupid": "stupid.wav", 
                    "run": "run.wav",
                    "run2": "run2.wav",
                    "reply3": "reply3.wav",
                    "reply2": "reply2.wav",
                    "reply1": "reply1.wav",
                    "ok4": "ok4.wav",
                    "ok3": "ok3.wav", 
                    "ok2": "ok2.wav",
                    "ok1": "ok1.wav",
                    "off": "off.wav",
                    "not_found": "not_found.wav",
                    "ready": "ready.wav"
                },
                "responses": {
                    "startup": ["run", "run2"],
                    "acknowledgment": ["ok1", "ok2", "ok3", "ok4", "reply1", "reply2", "reply3"],
                    "error": ["not_found"],
                    "completion": ["thanks"],
                    "listening": ["reply1", "reply2", "reply3"],
                    "sarcastic": ["stupid"],
                    "greeting": ["run", "run2"]
                }
            },
            "haudi": {
                "sounds": {
                    "greet1": "greet1.wav",
                    "greet2": "greet2.wav",
                    "greet3": "greet3.wav",
                    "not_found": "not_found.wav",
                    "ok1": "ok1.wav",
                    "ok2": "ok2.wav",
                    "ok3": "ok3.wav",
                    "ok4": "ok4.wav",
                    "ready": "ready.wav",
                    "run": "run.wav",
                    "stupid": "stupid.wav",
                    "thanks": "thanks.wav"
                },
                "responses": {
                    "startup": ["ready", "run"],
                    "acknowledgment": ["ok1", "ok2", "ok3", "ok4"],
                    "error": ["not_found"],
                    "completion": ["thanks"],
                    "listening": ["greet1", "greet2", "greet3"],
                    "sarcastic": ["stupid"],
                    "greeting": ["run", "ready"]
                }
            },
            "remaster": {
                "sounds": {
                    "greet_day": "greet_day.mp3",
                    "greet_evening": "greet_evening.mp3", 
                    "greet_morning": "greet_morning.mp3",
                    "greet_night": "greet_night.mp3",
                    "greet1": "greet1.mp3",
                    "ok1": "ok1.mp3",
                    "ok2": "ok2.mp3",
                    "ok3": "ok3.mp3",
                    "ok4": "ok4.mp3",
                    "reply1": "reply1.mp3",
                    "reply2": "reply2.mp3",
                    "reply3": "reply3.mp3",
                    "reply5": "reply5.mp3",
                    "reply6": "reply6.mp3",
                    "stupid": "stupid.mp3",
                    "thanks": "thanks.mp3"
                },
                "responses": {
                    "startup": ["greet_day", "greet_evening", "greet_morning", "greet_night"],
                    "acknowledgment": ["ok1", "ok2", "ok3", "ok4", "reply1", "reply2", "reply3"],
                    "error": ["greet1"],  # Используем greet1 как замену not_found
                    "completion": ["thanks", "reply5"],
                    "listening": ["greet1", "reply6"],
                    "sarcastic": ["stupid"],
                    "greeting": ["greet_day", "greet_evening", "greet_morning", "greet_night"]
                }
            }
        }
        
        self.config = configs.get(self.voice_pack, configs["original"])
        print(f"Загружена конфигурация для {self.voice_pack}")
    
    def init_pygame(self):
        """Инициализировать pygame для воспроизведения звуков"""
        if not self.pygame_initialized:
            try:
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.init()
                self.pygame_initialized = True
                print("Pygame инициализирован успешно")
                return True
            except Exception as e:
                print(f"Ошибка инициализации pygame: {e}")
                return False
        return True
    
    def load_sounds(self):
        """Загрузить все звуковые файлы"""
        if not self.init_pygame():
            print("Ошибка: pygame не инициализирован")
            return False
            
        loaded_count = 0
        for sound_name, filename in self.config["sounds"].items():
            sound_path = os.path.join(self.sounds_dir, filename)
            if os.path.exists(sound_path):
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    self.sounds[sound_name] = sound
                    loaded_count += 1
                    print(f"Загружен звук: {sound_name} -> {filename}")
                except Exception as e:
                    print(f"Ошибка загрузки {sound_path}: {e}")
            else:
                print(f"Файл не найден: {sound_path}")
        
        print(f"Загружено звуков: {loaded_count}/{len(self.config['sounds'])}")
        return loaded_count > 0
    
    def play_sound(self, sound_name, wait=False):
        """Воспроизвести звук по имени"""
        
        if not self.init_pygame():
            print("Ошибка: pygame не доступен")
            return False
            
        if sound_name in self.sounds:
            try:
                # Останавливаем предыдущий звук
                if self.current_sound:
                    self.current_sound.stop()
                
                self.current_sound = self.sounds[sound_name]
                channel = self.current_sound.play()
                
                if wait:
                    # Ждем завершения воспроизведения
                    while channel.get_busy():
                        time.sleep(0.1)
                
                return True
            except Exception as e:
                print(f"Ошибка воспроизведения {sound_name}: {e}")
                return False
        else:
            print(f"Звук не найден: {sound_name}")
            print(f"Доступные звуки: {list(self.sounds.keys())}")
            return False
    
    def play_random_sound(self, category):
        """Воспроизвести случайный звук из категории"""
        
        if category in self.config["responses"]:
            sounds = self.config["responses"][category]
            if sounds:
                # Для ремастера используем времязависимое приветствие ТОЛЬКО для greeting и startup
                if (category in ["greeting", "startup"]) and self.voice_pack == "remaster":
                    return self.play_time_based_greeting()
                
                sound_name = random.choice(sounds)
                return self.play_sound(sound_name)
        
        print(f"Категория не найдена: {category}")
        return False
    
    def play_time_based_greeting(self):
        """Воспроизвести приветствие в зависимости от времени суток (ТОЛЬКО для ремастера)"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            sound_name = "greet_morning"
        elif 12 <= hour < 17:
            sound_name = "greet_day" 
        elif 17 <= hour < 22:
            sound_name = "greet_evening"
        else:
            sound_name = "greet_night"
        
        return self.play_sound(sound_name)
    
    def play_startup_sound(self):
        """Воспроизвести звук при запуске"""
        # Только для ремастера используем времязависимое приветствие
        if self.voice_pack == "remaster":
            return self.play_time_based_greeting()
        return self.play_random_sound("startup")
    
    def play_acknowledgment(self):
        """Воспроизвести звук подтверждения"""
        return self.play_random_sound("acknowledgment")
    
    def play_error_sound(self):
        """Воспроизвести звук ошибки"""
        return self.play_random_sound("error")
    
    def play_completion_sound(self):
        """Воспроизвести звук завершения"""
        return self.play_random_sound("completion")
    
    def play_listening_sound(self):
        """Воспроизвести звук готовности слушать"""
        return self.play_random_sound("listening")
    
    def play_sarcastic_sound(self):
        """Воспроизвести саркастический звук"""
        return self.play_random_sound("sarcastic")
    
    def stop_current_sound(self):
        """Остановить текущий звук"""
        if self.current_sound:
            self.current_sound.stop()
            self.current_sound = None
            print("Звук остановлен")
    
    def set_voice_pack(self, voice_pack):
        """Переключить голосовой пакет"""
        valid_packs = ["original", "haudi", "remaster"]
        if voice_pack not in valid_packs:
            print(f"Неверный голосовой пакет: {voice_pack}")
            return False
            
        if voice_pack != self.voice_pack:
            old_pack = self.voice_pack
            self.voice_pack = voice_pack
            self.sounds_dir = self.voice_folders.get(voice_pack, "jarvis_sounds_original")
            
            # Останавливаем текущий звук
            self.stop_current_sound()
            
            # Перезагружаем конфиг и звуки
            self.load_config()
            success = self.load_sounds()
            
            if success:
                print(f"Переключен голос с {old_pack} на: {voice_pack}")
                return True
            else:
                # В случае ошибки возвращаем старый голос
                self.voice_pack = old_pack
                self.sounds_dir = self.voice_folders.get(old_pack, "jarvis_sounds_original")
                self.load_config()
                self.load_sounds()
                print(f"Ошибка переключения голоса, возвращен: {old_pack}")
                return False
        return True
