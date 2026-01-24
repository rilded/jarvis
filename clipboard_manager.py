# clipboard_manager.py - УНИВЕРСАЛЬНЫЙ МЕНЕДЖЕР БУФЕРА ОБМЕНА
import tkinter as tk
import subprocess
import platform
import os

class UniversalClipboard:
    """Универсальный менеджер буфера обмена для разных платформ"""
    
    @staticmethod
    def copy(text):
        """Скопировать текст в буфер обмена"""
        try:
            system = platform.system()
            text = str(text).strip()  # Убедимся, что text - строка
            
            if not text:
                return False
                
            # Сначала попробуем Tkinter - самый надежный метод
            try:
                root = tk.Tk()
                root.withdraw()
                root.clipboard_clear()
                root.clipboard_append(text)
                root.update()
                root.destroy()
                return True
            except Exception as e:
                print(f"Tkinter copy failed: {e}")
                # Пробуем системные команды как запасной вариант
                if system == "Windows":
                    # Для Windows - используем PowerShell с правильной кодировкой
                    try:
                        # Конвертируем текст в UTF-16 LE с BOM
                        text_encoded = text.encode('utf-16-le')
                        # Добавляем BOM (Byte Order Marker)
                        bom = b'\xff\xfe'
                        full_data = bom + text_encoded
                        subprocess.run(['clip'], input=full_data, check=True, shell=True)
                        return True
                    except Exception as e:
                        print(f"Windows clip failed: {e}")
                        return False
                elif system == "Darwin":
                    # Для MacOS
                    try:
                        subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
                        return True
                    except Exception as e:
                        print(f"Mac pbcopy failed: {e}")
                        return False
                else:
                    # Для Linux и других систем
                    try:
                        subprocess.run(['xclip', '-selection', 'clipboard'], 
                                    input=text.encode('utf-8'), check=True)
                        return True
                    except Exception as e:
                        try:
                            subprocess.run(['xsel', '--clipboard', '--input'], 
                                        input=text.encode('utf-8'), check=True)
                            return True
                        except Exception as e2:
                            print(f"Linux clipboard failed: {e2}")
                            return False
        except Exception as e:
            print(f"Общая ошибка копирования: {e}")
            return False
    
    @staticmethod
    def paste():
        """Вставить текст из буфера обмена"""
        try:
            system = platform.system()
            
            # Сначала попробуем Tkinter - самый надежный метод
            try:
                root = tk.Tk()
                root.withdraw()
                text = root.clipboard_get()
                root.destroy()
                
                # Проверяем, что текст не None перед strip()
                if text is not None:
                    return text.strip()
                else:
                    return ""
            except Exception as e:
                print(f"Tkinter paste failed: {e}")
                
                # Пробуем системные команды как запасной вариант
                if system == "Windows":
                    # Для Windows - исправленная версия без ошибки UTF-16
                    try:
                        # Пробуем несколько методов для Windows
                        methods = [
                            # Метод 1: PowerShell с UTF-8
                            lambda: subprocess.run([
                                'powershell', '-Command', 
                                '[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String([System.Windows.Forms.Clipboard]::GetText()))'
                            ], capture_output=True, text=True, encoding='utf-8', shell=True),
                            
                            # Метод 2: Стандартный Get-Clipboard с UTF-8
                            lambda: subprocess.run([
                                'powershell', '-Command', 'Get-Clipboard -Format Text'
                            ], capture_output=True, text=True, encoding='utf-8', shell=True),
                            
                            # Метод 3: Альтернативный способ
                            lambda: subprocess.run([
                                'powershell', '-Command', 
                                'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::GetText()'
                            ], capture_output=True, text=True, encoding='utf-8', shell=True)
                        ]
                        
                        for method in methods:
                            try:
                                result = method()
                                if result.returncode == 0 and result.stdout.strip():
                                    text = result.stdout.strip()
                                    # Убираем возможные лишние символы
                                    if text and text != 'None':
                                        return text
                            except:
                                continue
                        
                        return ""
                    except Exception as e:
                        print(f"Windows paste failed: {e}")
                        return ""
                elif system == "Darwin":
                    # Для MacOS
                    try:
                        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                        if result.returncode == 0:
                            text = result.stdout
                            if text is not None:
                                return text.strip()
                        return ""
                    except Exception as e:
                        print(f"Mac pbpaste failed: {e}")
                        return ""
                else:
                    # Для Linux и других систем
                    try:
                        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                              capture_output=True, text=True)
                        if result.returncode == 0:
                            text = result.stdout
                            if text is not None:
                                return text.strip()
                        return ""
                    except Exception as e:
                        try:
                            result = subprocess.run(['xsel', '--clipboard', '--output'], 
                                                  capture_output=True, text=True)
                            if result.returncode == 0:
                                text = result.stdout
                                if text is not None:
                                    return text.strip()
                            return ""
                        except Exception as e2:
                            print(f"Linux paste failed: {e2}")
                            return ""
        except Exception as e:
            print(f"Общая ошибка вставки: {e}")
            return ""
    
    @staticmethod
    def test_clipboard():
        """Тестирование буфера обмена"""
        print("Тестирование буфера обмена...")
        
        # Тест копирования
        test_text = "Тестовый текст для проверки буфера обмена 123"
        success = UniversalClipboard.copy(test_text)
        print(f"Копирование: {'Успешно' if success else 'Не удалось'}")
        
        # Небольшая пауза для гарантии
        import time
        time.sleep(0.1)
        
        # Тест вставки
        pasted_text = UniversalClipboard.paste()
        print(f"Вставка: '{pasted_text}'")
        
        # Проверяем совпадение (игнорируем пробелы)
        if pasted_text and test_text.strip() == pasted_text.strip():
            print("Совпадение: Да")
        else:
            print(f"Совпадение: Нет (ожидалось: '{test_text}')")
        
        return success and (test_text.strip() == pasted_text.strip())

# Тестирование при прямом запуске
if __name__ == "__main__":
    UniversalClipboard.test_clipboard()
