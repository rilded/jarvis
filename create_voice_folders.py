import os
import json

def create_voice_structure():
    """Создает папки и базовые конфиги для голосов"""
    
    # Конфиги для каждого голоса
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
                "greet1": "greet1.wav",
                "greet2": "greet2.wav",
                "greet3": "greet3.wav",
                "greet_day": "run.wav",
                "greet_evening": "run.wav",
                "greet_morning": "run.wav",
                "greet_night": "run.wav",
                "ready": "ready.wav"
            },
            "responses": {
                "startup": ["run", "run2"],
                "acknowledgment": ["ok1", "ok2", "ok3", "ok4", "reply1", "reply2", "reply3"],
                "error": ["not_found"],
                "completion": ["thanks"],
                "listening": ["greet1", "greet2", "greet3"],
                "sarcastic": ["stupid"],
                "greeting": ["run", "run2"]
            }
        },
        "haudi": {
            "sounds": {
                "thanks": "thanks.wav",
                "stupid": "stupid.wav",
                "run": "run.wav", 
                "greet1": "greet1.wav",
                "greet2": "greet2.wav",
                "greet3": "greet3.wav",
                "not_found": "not_found.wav",
                "ok1": "ok1.wav",
                "ok2": "ok2.wav",
                "ok3": "ok3.wav",
                "ok4": "ok4.wav",
                "ready": "ready.wav",
                "greet_day": "run.wav",
                "greet_evening": "run.wav",
                "greet_morning": "run.wav", 
                "greet_night": "run.wav",
                "reply1": "greet1.wav",
                "reply2": "greet2.wav",
                "reply3": "greet3.wav"
            },
            "responses": {
                "startup": ["ready", "run"],
                "acknowledgment": ["ok1", "ok2", "ok3", "ok4", "greet1", "greet2", "greet3"],
                "error": ["not_found"],
                "completion": ["thanks"],
                "listening": ["greet1", "greet2", "greet3"],
                "sarcastic": ["stupid"],
                "greeting": ["run", "ready"]
            }
        },
        "remaster": {
            "sounds": {
                "thanks": "thanks.mp3",
                "stupid": "stupid.mp3",
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
                "ready": "greet1.mp3",
                "run": "greet_day.mp3"
            },
            "responses": {
                "startup": ["greet_day", "greet_evening", "greet_morning", "greet_night"],
                "acknowledgment": ["ok1", "ok2", "ok3", "ok4", "reply1", "reply2", "reply3"],
                "error": ["not_found"],
                "completion": ["thanks", "reply5"],
                "listening": ["greet1", "reply6"],
                "sarcastic": ["stupid"],
                "greeting": ["greet_day", "greet_evening", "greet_morning", "greet_night"]
            }
        }
    }
    
    for voice_name, config in configs.items():
        folder = f"jarvis_sounds_{voice_name}"
        
        # Создаем папку
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Создана папка: {folder}")
        
        # Создаем конфиг файл
        config_path = os.path.join(folder, "sound_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"Создан конфиг: {config_path}")
        
        # Создаем файлы-заглушки
        for sound_file in config["sounds"].values():
            sound_path = os.path.join(folder, sound_file)
            if not os.path.exists(sound_path):
                # Создаем пустой файл как заглушку
                with open(sound_path, 'w') as f:
                    f.write("")
                print(f"Создана заглушка: {sound_path}")
    
    print("Структура голосов создана!")

if __name__ == "__main__":
    create_voice_structure()
