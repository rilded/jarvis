# jarvis_launcher_7.py - ЛАУНЧЕР ДЛЯ ВЕРСИИ 7.0
import sys
import os
import json
import traceback

def setup_vosk_environment():
    """Настройка окружения для VOSK в EXE"""
    
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ JARVIS")
    print("=" * 60)
    
    # Определяем базовый путь
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        print(f"Режим: EXE")
        print(f"EXE путь: {sys.executable}")
        print(f"Базовая директория: {base_dir}")
        
        # Добавляем MEIPASS в пути
        if hasattr(sys, '_MEIPASS'):
            print(f"Временная папка (MEIPASS): {sys._MEIPASS}")
            # Добавляем в sys.path для импорта
            if sys._MEIPASS not in sys.path:
                sys.path.insert(0, sys._MEIPASS)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Режим: Разработка")
        print(f"Директория скрипта: {base_dir}")
    
    # Ищем модель VOSK
    model_name = "vosk-model-small-ru-0.22"
    model_paths = []
    
    # Все возможные пути
    model_paths.append(os.path.join(base_dir, model_name))  # Рядом с EXE
    model_paths.append(model_name)  # В текущей папке
    
    if hasattr(sys, '_MEIPASS'):
        model_paths.append(os.path.join(sys._MEIPASS, model_name))  # В MEIPASS
    
    # Ищем существующую модель
    for path in model_paths:
        if path and os.path.exists(path):
            # Проверяем структуру
            required = ['am', 'conf', 'graph']
            if all(os.path.exists(os.path.join(path, f)) for f in required):
                print(f"✓ Модель VOSK найдена: {path}")
                
                # Устанавливаем переменную окружения
                os.environ['VOSK_MODEL_PATH'] = path
                
                # Для vosk нужно явно указать путь
                from vosk import Model
                
                try:
                    model = Model(path)
                    print("✅ Модель VOSK успешно загружена!")
                    return model
                except Exception as e:
                    print(f"❌ Ошибка загрузки модели: {e}")
                    return None
    
    # Если модель не найдена
    print("❌ МОДЕЛЬ VOSK НЕ НАЙДЕНА!")
    print("Искал в следующих местах:")
    for path in model_paths:
        exists = os.path.exists(path) if path else False
        print(f"  {'✓' if exists else '✗'} {path}")
    
    # Показываем сообщение об ошибке
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        error_msg = (
            "Не найдена модель распознавания речи!\n\n"
            "Скачайте модель VOSK с сайта:\n"
            "https://alphacephei.com/vosk/models\n\n"
            "И распакуйте папку 'vosk-model-small-ru-0.22'\n"
            f"в директорию: {base_dir}"
        )
        
        messagebox.showerror("Ошибка Jarvis", error_msg)
        root.destroy()
    except:
        pass
    
    return None

# Инициализируем VOSK ПЕРЕД всем остальным
vosk_model = setup_vosk_environment()

if vosk_model is None:
    print("\n" + "="*60)
    print("ВНИМАНИЕ: Программа запускается без голосового управления!")
    print("Будет использоваться только текстовый ввод.")
    print("="*60 + "\n")
    
    # Можно продолжить без голоса
    use_voice = False
else:
    use_voice = True
    from vosk import KaldiRecognizer
def show_welcome():
    """Показать приветствие"""
    print("=" * 60)
    print(" " * 20 + "J.A.R.V.I.S. 9.2")
    print("=" * 60)
    print()
    print("Версия с расширенными настройками и сохранением в JSON")
    print("Все настройки сохраняются в файле jarvis_settings.json")
    print()

def check_settings():
    """Проверить и создать файл настроек если нужно"""
    settings_file = "jarvis_settings.json"
    
    default_settings = {
        "voice_pack": {
            "current_voice": "original"
        },
        "recognition": {
            "engine": "vosk",
            "vosk_model": "vosk-model-small-ru-0.22",
            "activation_phrase": "джарвис",
            "listen_timeout": 5.0,
            "phrase_time_limit": 4.0
        },
        "voice": {
            "tts_enabled": True,
            "tts_rate": 180,
            "tts_volume": 0.9,
            "prefer_cached_sounds": True
        },
        "interface": {
            "color_scheme": "default",
            "always_on_top": True,
            "auto_start_voice": True,
            "show_timestamp": True,
            "log_max_lines": 500
        },
        "reaction": {
            "reactor_speed": 1.0,
            "auto_reactor": True,
            "reactor_duration": 2.5
        },
        "llm": {
            "enabled": False,
            "model": "deepseek-r1:8b",
            "ollama_path": r"C:\Users\123\AppData\Local\Programs\Ollama\ollama.exe",
            "system_prompt": "Ты — Джарвис, голосовой помощник на русском языке. Отвечай только по-русски. Если ты не знаете ответа, скажите мне честно. Твои ответы должны быть короткими — максимум 2–3 предложения."
        },
        "hotkeys": {
            "global_hotkey": "ctrl+alt+j",
            "activate_hotkey": "ctrl+shift+j",
            "show_desktop_hotkey": "ctrl+alt+d"
        },
        "paths": {
            "sounds_dir": "jarvis_sounds",
            "vosk_models_dir": "voice_models",
            "screenshots_dir": "screenshots"
        }
    }
    
    if not os.path.exists(settings_file):
        print("Файл настроек не найден, создаю стандартные настройки...")
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=4, ensure_ascii=False)
            print(f"Создан файл настроек: {settings_file}")
        except Exception as e:
            print(f"Ошибка создания файла настроек: {e}")
    else:
        print(f"Файл настроек найден: {settings_file}")
        # Проверяем и обновляем структуру настроек
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                existing_settings = json.load(f)
            
            # Проверяем наличие voice_pack
            if "voice_pack" not in existing_settings:
                existing_settings["voice_pack"] = {"current_voice": "original"}
                print("Добавлен раздел voice_pack в настройки")
            
            # Проверяем наличие всех необходимых полей
            updated = False
            for section, values in default_settings.items():
                if section not in existing_settings:
                    existing_settings[section] = values
                    updated = True
                    print(f"Добавлен раздел {section} в настройки")
                elif isinstance(values, dict):
                    for key, value in values.items():
                        if key not in existing_settings[section]:
                            existing_settings[section][key] = value
                            updated = True
                            print(f"Добавлен параметр {section}.{key} в настройки")
            
            # Сохраняем обновленные настройки
            if updated:
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_settings, f, indent=4, ensure_ascii=False)
                print("Настройки обновлены")
                
        except Exception as e:
            print(f"Ошибка проверки настроек: {e}")

def check_requirements():
    """Проверить требования"""
    print("Проверка требований...")
    
    # Проверяем Python
    python_ver = sys.version_info
    if python_ver.major < 3 or (python_ver.major == 3 and python_ver.minor < 8):
        print(f" Python 3.8+ требуется (у вас {sys.version})")
        return False
    
    print(f"Python {sys.version}")
    
    # Проверяем Tkinter
    try:
        import tkinter
        print(" Tkinter доступен")
    except ImportError:
        print("  Tkinter не доступен")
        print("  Для Windows: Переустановите Python с python.org")
        print("  Для Linux: sudo apt-get install python3-tk")
        return False
    
    # Проверяем основные файлы версии 5.0
    required_files = [
        'cursor_simple.py',
        'desktop_manager.py', 
        'voice_input.py'
    ]
    
    print("\nПроверка файлов версии 5.0...")
    for file in required_files:
        if os.path.exists(file):
            print(f"{file}")
        else:
            print(f" {file} - не найден")
            return False
    
    return True

def install_dependencies():
    """Установить зависимости"""
    print("\nОпциональные зависимости для лучшего опыта:")
    print("  pip install pyautogui")
    print("  pip install psutil")
    print("  pip install vosk (для офлайн распознавания)")
    print("  pip install SpeechRecognition pyaudio (для онлайн распознавания)")
    print()

def main():
    """Главная функция"""
    show_welcome()
    
    # Проверяем и создаем настройки
    check_settings()
    install_dependencies()
    
    try:
        from jarvis_visual import main as visual_main
        visual_main()
    except Exception as e:
        print(f"Ошибка запуска визуального интерфейса: {e}")
        import traceback
        traceback.print_exc()
        input("\nНажмите Enter для выхода...")

def check_sound_files():
    """Проверить наличие звуковых файлов"""
    sounds_dir = "jarvis_sounds"
    required_files = [
        "thanks.wav", "stupid.wav", "run.wav", "ready.wav",
        "ok4.wav", "ok3.wav", "ok2.wav", "ok1.wav", 
        "not_found.wav", "greet3.wav", "greet2.wav"
    ]
    
    missing_files = []
    
    for filename in required_files:
        filepath = os.path.join(sounds_dir, filename)
        if not os.path.exists(filepath):
            missing_files.append(filename)
    
    if missing_files:
        print("\n" + "="*60)
        print("ВНИМАНИЕ: Отсутствуют звуковые файлы!")
        print("="*60)
        print("Отсутствующие файлы:")
        for filename in missing_files:
            print(f"  • {filename}")
        print("\nЗапустите create_default_sounds.py для создания заглушек")
        print("или добавьте реальные записи в папку jarvis_sounds/")
        print("="*60)
        
        # Предлагаем создать файлы
        response = input("\nСоздать базовые звуковые файлы? (да/нет): ")
        if response.lower() in ['да', 'yes', 'y']:
            import create_default_sounds
            create_default_sounds.main()

if __name__ == "__main__":
    main()