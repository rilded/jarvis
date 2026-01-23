# create_default_sounds.py - СОЗДАНИЕ БАЗОВЫХ ЗВУКОВЫХ ФАЙЛОВ
import os
import pygame
import time

def create_silent_wav(filename, duration=2.0):
    """Создать тихий WAV файл (заглушка)"""
    import wave
    import struct
    
    # Параметры WAV файла
    sample_rate = 44100
    num_channels = 1
    sample_width = 2  # 16-bit
    
    num_samples = int(sample_rate * duration)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        
        # Записываем тишину (нулевые samples)
        for i in range(num_samples):
            value = 0
            packed_value = struct.pack('<h', value)
            wav_file.writeframes(packed_value)
    
    print(f"Создан файл: {filename}")

def main():
    """Создать все необходимые звуковые файлы"""
    sounds_dir = "jarvis_sounds"
    
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
    
    # Список необходимых файлов
    sound_files = [
        "thanks.wav",      # всегда к вашим услугам сэр
        "stupid.wav",      # очень тонкое замечание сэр  
        "run.wav",         # добрый день сэр
        "ready.wav",       # мы подключены и готовы
        "ok4.wav",         # как пожелаете
        "ok3.wav",         # запрос выполнен сэр
        "ok2.wav",         # загружаю сэр
        "ok1.wav",         # есть
        "not_found.wav",   # чего вы пытаетесь добиться сэр?
        "greet3.wav",      # слушаю сэр
        "greet2.wav"       # в вашим услугам сэр
    ]
    
    print("Создание базовых звуковых файлов...")
    print("Эти файлы будут заглушками. Замените их реальными записями!")
    
    for filename in sound_files:
        filepath = os.path.join(sounds_dir, filename)
        if not os.path.exists(filepath):
            create_silent_wav(filepath)
            print(f"✓ Создан: {filename}")
        else:
            print(f"✓ Уже существует: {filename}")
    
    print("\nЗвуковые файлы созданы!")
    print("ЗАМЕНИТЕ эти файлы реальными записями с фразами:")
    print("1. thanks.wav - 'всегда к вашим услугам сэр'")
    print("2. stupid.wav - 'очень тонкое замечание сэр'")
    print("3. run.wav - 'добрый день сэр'")
    print("4. ready.wav - 'мы подключены и готовы'")
    print("5. ok4.wav - 'как пожелаете'")
    print("6. ok3.wav - 'запрос выполнен сэр'")
    print("7. ok2.wav - 'загружаю сэр'")
    print("8. ok1.wav - 'есть'")
    print("9. not_found.wav - 'чего вы пытаетесь добиться сэр?'")
    print("10. greet3.wav - 'слушаю сэр'")
    print("11. greet2.wav - 'в вашим услугам сэр'")

if __name__ == "__main__":
    main()
