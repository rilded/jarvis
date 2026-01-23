# custom_commands.py - СИСТЕМА КАСТОМНЫХ КОМАНД ДЛЯ ДЖАРВИСА
import json
import os
import time
import pyautogui
import webbrowser
import subprocess
from cursor_simple import SimpleCursor

class CustomCommandsManager:
    def __init__(self):
        self.commands_file = "custom_commands.json"
        self.sequences_file = "command_sequences.json"
        self.commands = self.load_commands()
        self.sequences = self.load_sequences()
        self.cursor = SimpleCursor()
    
    def load_commands(self):
        """Загрузить кастомные команды"""
        if os.path.exists(self.commands_file):
            try:
                with open(self.commands_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                print("Файл команд поврежден, создаю новый")
                return {}
        return {}
    
    def load_sequences(self):
        """Загрузить последовательности действий"""
        if os.path.exists(self.sequences_file):
            try:
                with open(self.sequences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                print("Файл последовательностей поврежден, создаю новый")
                return {}
        return {}
    
    def save_commands(self):
        """Сохранить команды"""
        with open(self.commands_file, 'w', encoding='utf-8') as f:
            json.dump(self.commands, f, indent=2, ensure_ascii=False)
    
    def save_sequences(self):
        """Сохранить последовательности"""
        with open(self.sequences_file, 'w', encoding='utf-8') as f:
            json.dump(self.sequences, f, indent=2, ensure_ascii=False)
    
    def create_command(self, name, action_type, params):
        """Создать новую команду"""
        self.commands[name.lower()] = {
            'type': action_type,
            'params': params,
            'created': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_commands()
        return True
    
    def create_sequence(self, name, actions):
        """Создать последовательность действий"""
        self.sequences[name.lower()] = {
            'actions': actions,
            'created': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_sequences()
        return True
    
    def execute_command(self, command_name):
        """Выполнить кастомную команду"""
        command_name = command_name.lower()
        
        if command_name not in self.commands:
            return False, f"Команда '{command_name}' не найдена"
        
        command = self.commands[command_name]
        
        try:
            if command['type'] == 'open_url':
                webbrowser.open(command['params']['url'])
                return True, f"Открываю {command['params']['url']}"
            
            elif command['type'] == 'run_program':
                subprocess.Popen(command['params']['path'])
                return True, f"Запускаю {command['params']['path']}"
            
            elif command['type'] == 'press_keys':
                keys = command['params']['keys']
                if isinstance(keys, list):
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(keys)
                return True, f"Нажимаю {keys}"
            
            elif command['type'] == 'type_text':
                text = command['params']['text']
                self.cursor.type_text(text)
                return True, f"Печатаю: {text}"
            
            elif command['type'] == 'mouse_move':
                x = command['params']['x']
                y = command['params']['y']
                self.cursor.move_to(x, y)
                return True, f"Перемещаю курсор на ({x}, {y})"
            
            elif command['type'] == 'mouse_click':
                x = command['params'].get('x')
                y = command['params'].get('y')
                button = command['params'].get('button', 'left')
                self.cursor.click(x, y, button)
                return True, f"Кликаю {button} кнопкой"
            
            else:
                return False, f"Неизвестный тип команды: {command['type']}"
                
        except Exception as e:
            return False, f"Ошибка выполнения: {str(e)}"
        
    def load_example_commands(self):
        """Загрузить примеры команд"""
        example_file = "example_commands.json"
        if os.path.exists(example_file):
            try:
                with open(example_file, 'r', encoding='utf-8') as f:
                    examples = json.load(f)
                    self.commands.update(examples)
                    self.save_commands()
                    return True
            except:
                return False
        return False
    
    def execute_sequence(self, sequence_name):
        """Выполнить последовательность действий"""
        sequence_name = sequence_name.lower()
        
        if sequence_name not in self.sequences:
            return False, f"Последовательность '{sequence_name}' не найдена"
        
        sequence = self.sequences[sequence_name]
        results = []
        
        for i, action in enumerate(sequence['actions']):
            try:
                action_type = action['type']
                params = action.get('params', {})
                delay = action.get('delay', 1.0)
                
                # Ждем перед выполнением действия
                if delay > 0:
                    time.sleep(delay)
                
                if action_type == 'command':
                    success, message = self.execute_command(params['name'])
                    results.append(f"{i+1}. {message}")
                
                elif action_type == 'open_url':
                    webbrowser.open(params['url'])
                    results.append(f"{i+1}. Открываю {params['url']}")
                
                elif action_type == 'run_program':
                    subprocess.Popen(params['path'])
                    results.append(f"{i+1}. Запускаю {params['path']}")
                
                elif action_type == 'press_keys':
                    keys = params['keys']
                    if isinstance(keys, list):
                        pyautogui.hotkey(*keys)
                    else:
                        pyautogui.press(keys)
                    results.append(f"{i+1}. Нажимаю {keys}")
                
                elif action_type == 'type_text':
                    self.cursor.type_text(params['text'])
                    results.append(f"{i+1}. Печатаю: {params['text']}")
                
                elif action_type == 'mouse_move':
                    self.cursor.move_to(params['x'], params['y'])
                    results.append(f"{i+1}. Перемещаю курсор")
                
                elif action_type == 'mouse_click':
                    self.cursor.click(params.get('x'), params.get('y'), params.get('button', 'left'))
                    results.append(f"{i+1}. Кликаю мышью")
                
                elif action_type == 'wait':
                    time.sleep(params['seconds'])
                    results.append(f"{i+1}. Жду {params['seconds']} сек")
                
                else:
                    results.append(f"{i+1}. Неизвестное действие: {action_type}")
                    
            except Exception as e:
                results.append(f"{i+1}. Ошибка: {str(e)}")
        
        return True, " | ".join(results)
    
    def list_commands(self):
        """Показать все команды"""
        if not self.commands:
            return "Нет сохраненных команд"
        
        result = "СОХРАНЕННЫЕ КОМАНДЫ:\n"
        result += "=" * 50 + "\n"
        
        for name, data in self.commands.items():
            result += f"• {name} ({data['type']}) - {data['created']}\n"
        
        return result
    
    def list_sequences(self):
        """Показать все последовательности"""
        if not self.sequences:
            return "Нет сохраненных последовательностей"
        
        result = "СОХРАНЕННЫЕ ПОСЛЕДОВАТЕЛЬНОСТИ:\n"
        result += "=" * 50 + "\n"
        
        for name, data in self.sequences.items():
            result += f"• {name} ({len(data['actions'])} действий) - {data['created']}\n"
        
        return result
    
    def delete_command(self, name):
        """Удалить команду"""
        name = name.lower()
        if name in self.commands:
            del self.commands[name]
            self.save_commands()
            return True
        return False
    
    def delete_sequence(self, name):
        """Удалить последовательность"""
        name = name.lower()
        if name in self.sequences:
            del self.sequences[name]
            self.save_sequences()
            return True
        return False
