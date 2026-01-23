# jarvis_sound_manager.py - МЕНЕДЖЕР ЗВУКОВЫХ ФАЙЛОВ ДЛЯ ДЖАРВИСА
import os
import random
import pygame
import threading
import time
import json

class JarvisSoundManager:
    def __init__(self, sounds_dir="jarvis_sounds"):
        self.sounds_dir = sounds_dir
        self.config_file = "jarvis_sounds_config.json"
        self.sounds = {}
        self.config = {}
        self.pygame_initialized = False
        self.current_sound = None
        
        # Создаем папку для звуков если нет
        if not os.path.exists(self.sounds_dir):
            os.makedirs(self.sounds_dir)
            
        self.load_config()
        self.load_sounds()
    
    def load_config(self):
        """Загрузить конфигурацию звуков"""
        default_config = {
            "sounds": {
                "thanks": "thanks.wav",
                "stupid": "stupid.wav",
                "run": "run.wav",
                "ready": "ready.wav",
                "ok4": "ok4.wav",
                "ok3": "ok3.wav",
                "ok2": "ok2.wav",
                "ok1": "ok1.wav",
                "not_found": "not_found.wav",
                "greet3": "greet3.wav",
                "greet2": "greet2.wav"
            },
            "responses": {
                "startup": ["run", "ready"],
                "acknowledgment": ["ok1", "ok2", "ok3", "ok4"],
                "error": ["not_found"],
                "completion": ["thanks"],
                "listening": ["greet2", "greet3"],
                "sarcastic": ["stupid"]
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Сохранить конфигурацию"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def init_pygame(self):
        """Инициализировать pygame для воспроизведения звуков"""
        if not self.pygame_initialized:
            try:
                pygame.mixer.init()
                self.pygame_initialized = True
                print("Pygame звуковая система инициализирована")
            except Exception as e:
                print(f"Ошибка инициализации pygame: {e}")
                return False
        return True
    
    def load_sounds(self):
        """Загрузить все звуковые файлы"""
        if not self.init_pygame():
            return False
            
        for sound_name, filename in self.config["sounds"].items():
            sound_path = os.path.join(self.sounds_dir, filename)
            if os.path.exists(sound_path):
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    self.sounds[sound_name] = sound
                    print(f"Звук загружен: {sound_name} -> {filename}")
                except Exception as e:
                    print(f"Ошибка загрузки звука {sound_path}: {e}")
            else:
                print(f"Звуковой файл не найден: {sound_path}")
        
        return len(self.sounds) > 0
    
    def play_sound(self, sound_name, wait=False):
        """Воспроизвести звук по имени"""
        if not self.init_pygame():
            return False
            
        if sound_name in self.sounds:
            try:
                # Останавливаем предыдущий звук
                if self.current_sound:
                    self.current_sound.stop()
                
                self.current_sound = self.sounds[sound_name]
                self.current_sound.play()
                
                if wait:
                    # Ждем завершения воспроизведения
                    while pygame.mixer.get_busy():
                        time.sleep(0.1)
                
                return True
            except Exception as e:
                print(f"Ошибка воспроизведения звука {sound_name}: {e}")
                return False
        else:
            print(f"Звук не найден: {sound_name}")
            return False
    
    def play_random_sound(self, category):
        """Воспроизвести случайный звук из категории"""
        if category in self.config["responses"]:
            sounds = self.config["responses"][category]
            if sounds:
                sound_name = random.choice(sounds)
                return self.play_sound(sound_name)
        return False
    
    def play_startup_sound(self):
        """Воспроизвести звук при запуске"""
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
    
    def get_available_sounds(self):
        """Получить список доступных звуков"""
        return list(self.sounds.keys())
    
    def get_sound_categories(self):
        """Получить категории звуков"""
        return list(self.config["responses"].keys())
