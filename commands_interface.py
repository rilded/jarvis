# commands_interface.py - ИНТЕРФЕЙС УПРАВЛЕНИЯ КАСТОМНЫМИ КОМАНДАМИ
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from custom_commands import CustomCommandsManager

class CommandsInterface:
    def __init__(self, parent, colors, commands_manager):
        self.parent = parent
        self.colors = colors
        self.commands_manager = commands_manager
        
    def open_commands_window(self):
        """Открыть окно управления командами"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Управление кастомными командами")
        self.window.configure(bg=self.colors['bg'])
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # Создаем Notebook с вкладками
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        self.create_commands_tab(notebook)
        self.create_sequences_tab(notebook)
        self.create_manage_tab(notebook)
        
        # Кнопки снизу
        button_frame = tk.Frame(self.window, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Закрыть", bg='#222222', fg='#ff5555',
                 command=self.window.destroy).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(button_frame, text="Обновить список", bg='#222222', fg=self.colors['accent'],
                 command=self.refresh_lists).pack(side=tk.RIGHT, padx=5)
    
    def create_commands_tab(self, notebook):
        """Вкладка создания одиночных команд"""
        frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(frame, text="Создать команду")
        
        # Название команды
        tk.Label(frame, text="Название команды:", bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.command_name = tk.Entry(frame, bg='#222222', fg=self.colors['text'], width=30)
        self.command_name.pack(anchor=tk.W, padx=10, pady=5)
        
        # Тип команды
        tk.Label(frame, text="Тип действия:", bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.command_type = tk.StringVar(value="open_url")
        types = [
            ("Открыть URL", "open_url"),
            ("Запустить программу", "run_program"),
            ("Нажать клавиши", "press_keys"),
            ("Напечатать текст", "type_text"),
            ("Переместить курсор", "mouse_move"),
            ("Кликнуть мышью", "mouse_click")
        ]
        
        for text, value in types:
            tk.Radiobutton(frame, text=text, variable=self.command_type, value=value,
                          bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W, padx=20)
        
        # Параметры команды
        self.params_frame = tk.Frame(frame, bg=self.colors['bg'])
        self.params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_url_params()
        
        # Обработчик изменения типа
        self.command_type.trace('w', self.on_type_change)
        
        # Кнопка создания
        tk.Button(frame, text="Создать команду", bg='#333333', fg=self.colors['accent'],
                 command=self.create_command).pack(pady=20)
    
    def create_url_params(self):
        """Параметры для открытия URL"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.params_frame, text="URL адрес:", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)
        self.url_entry = tk.Entry(self.params_frame, bg='#222222', fg=self.colors['text'], width=50)
        self.url_entry.pack(fill=tk.X, pady=5)
        self.url_entry.insert(0, "https://")
    
    def create_program_params(self):
        """Параметры для запуска программы"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.params_frame, text="Путь к программе:", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)
        self.program_entry = tk.Entry(self.params_frame, bg='#222222', fg=self.colors['text'], width=50)
        self.program_entry.pack(fill=tk.X, pady=5)
        
        tk.Button(self.params_frame, text="Выбрать файл", bg='#333333', fg=self.colors['text'],
                 command=self.select_program).pack(anchor=tk.W)
    
    def create_keys_params(self):
        """Параметры для нажатия клавиш"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.params_frame, text="Клавиши (через + для комбинаций):", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)
        self.keys_entry = tk.Entry(self.params_frame, bg='#222222', fg=self.colors['text'], width=50)
        self.keys_entry.pack(fill=tk.X, pady=5)
        self.keys_entry.insert(0, "ctrl+c")
        
        tk.Label(self.params_frame, text="Примеры: enter, ctrl+c, alt+f4, win+d", bg=self.colors['bg'], fg='#888888',
                font=('Arial', 8)).pack(anchor=tk.W)
    
    def create_text_params(self):
        """Параметры для печати текста"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.params_frame, text="Текст для печати:", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)
        self.text_entry = tk.Text(self.params_frame, bg='#222222', fg=self.colors['text'], height=4, width=50)
        self.text_entry.pack(fill=tk.X, pady=5)
    
    def create_move_params(self):
        """Параметры для перемещения курсора"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        coords_frame = tk.Frame(self.params_frame, bg=self.colors['bg'])
        coords_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(coords_frame, text="X координата:", bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.x_entry = tk.Entry(coords_frame, bg='#222222', fg=self.colors['text'], width=10)
        self.x_entry.pack(side=tk.LEFT, padx=5)
        self.x_entry.insert(0, "100")
        
        tk.Label(coords_frame, text="Y координата:", bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.y_entry = tk.Entry(coords_frame, bg='#222222', fg=self.colors['text'], width=10)
        self.y_entry.pack(side=tk.LEFT, padx=5)
        self.y_entry.insert(0, "100")
        
        tk.Button(self.params_frame, text="Текущая позиция", bg='#333333', fg=self.colors['text'],
                 command=self.use_current_position).pack(anchor=tk.W, pady=5)
    
    def create_click_params(self):
        """Параметры для клика мышью"""
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        # Координаты
        coords_frame = tk.Frame(self.params_frame, bg=self.colors['bg'])
        coords_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(coords_frame, text="X координата:", bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.click_x_entry = tk.Entry(coords_frame, bg='#222222', fg=self.colors['text'], width=10)
        self.click_x_entry.pack(side=tk.LEFT, padx=5)
        self.click_x_entry.insert(0, "100")
        
        tk.Label(coords_frame, text="Y координата:", bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        self.click_y_entry = tk.Entry(coords_frame, bg='#222222', fg=self.colors['text'], width=10)
        self.click_y_entry.pack(side=tk.LEFT, padx=5)
        self.click_y_entry.insert(0, "100")
        
        # Тип клика
        tk.Label(self.params_frame, text="Тип клика:", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W, pady=(10,5))
        
        self.click_type = tk.StringVar(value="left")
        clicks = [("Левый клик", "left"), ("Правый клик", "right"), ("Двойной клик", "double")]
        
        for text, value in clicks:
            tk.Radiobutton(self.params_frame, text=text, variable=self.click_type, value=value,
                          bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W, padx=20)
        
        tk.Button(self.params_frame, text="Текущая позиция", bg='#333333', fg=self.colors['text'],
                 command=self.use_current_click_position).pack(anchor=tk.W, pady=5)
    
    def on_type_change(self, *args):
        """Обработчик изменения типа команды"""
        command_type = self.command_type.get()
        
        if command_type == "open_url":
            self.create_url_params()
        elif command_type == "run_program":
            self.create_program_params()
        elif command_type == "press_keys":
            self.create_keys_params()
        elif command_type == "type_text":
            self.create_text_params()
        elif command_type == "mouse_move":
            self.create_move_params()
        elif command_type == "mouse_click":
            self.create_click_params()
    
    def select_program(self):
        """Выбрать программу через диалог"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Выберите программу",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.program_entry.delete(0, tk.END)
            self.program_entry.insert(0, filename)
    
    def use_current_position(self):
        """Использовать текущую позицию курсора"""
        import pyautogui
        x, y = pyautogui.position()
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
        self.y_entry.delete(0, tk.END)
        self.y_entry.insert(0, str(y))
    
    def use_current_click_position(self):
        """Использовать текущую позицию для клика"""
        import pyautogui
        x, y = pyautogui.position()
        self.click_x_entry.delete(0, tk.END)
        self.click_x_entry.insert(0, str(x))
        self.click_y_entry.delete(0, tk.END)
        self.click_y_entry.insert(0, str(y))
    
    def create_command(self):
        """Создать новую команду"""
        name = self.command_name.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название команды")
            return
        
        command_type = self.command_type.get()
        params = {}
        
        try:
            if command_type == "open_url":
                params = {'url': self.url_entry.get().strip()}
                if not params['url']:
                    raise ValueError("Введите URL")
                    
            elif command_type == "run_program":
                params = {'path': self.program_entry.get().strip()}
                if not params['path']:
                    raise ValueError("Введите путь к программе")
                    
            elif command_type == "press_keys":
                keys = self.keys_entry.get().strip()
                if not keys:
                    raise ValueError("Введите клавиши")
                # Разбиваем комбинацию
                if '+' in keys:
                    params = {'keys': keys.split('+')}
                else:
                    params = {'keys': keys}
                    
            elif command_type == "type_text":
                text = self.text_entry.get(1.0, tk.END).strip()
                if not text:
                    raise ValueError("Введите текст")
                params = {'text': text}
                
            elif command_type == "mouse_move":
                params = {
                    'x': int(self.x_entry.get()),
                    'y': int(self.y_entry.get())
                }
                
            elif command_type == "mouse_click":
                params = {
                    'x': int(self.click_x_entry.get()),
                    'y': int(self.click_y_entry.get()),
                    'button': self.click_type.get()
                }
                if self.click_type.get() == "double":
                    params['type'] = "double_click"
            
            # Создаем команду
            success = self.commands_manager.create_command(name, command_type, params)
            if success:
                messagebox.showinfo("Успех", f"Команда '{name}' создана!")
                self.command_name.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Не удалось создать команду")
                
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка создания: {str(e)}")
    
    def create_sequences_tab(self, notebook):
        """Вкладка создания последовательностей"""
        frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(frame, text="Создать последовательность")
        
        # Название последовательности
        tk.Label(frame, text="Название последовательности:", bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.sequence_name = tk.Entry(frame, bg='#222222', fg=self.colors['text'], width=30)
        self.sequence_name.pack(anchor=tk.W, padx=10, pady=5)
        
        # Список доступных команд
        tk.Label(frame, text="Доступные команды:", bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        commands_frame = tk.Frame(frame, bg=self.colors['bg'])
        commands_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Левая часть - список команд
        left_frame = tk.Frame(commands_frame, bg=self.colors['bg'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text="Команды:", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)
        
        self.commands_listbox = tk.Listbox(left_frame, bg='#222222', fg=self.colors['text'], height=10)
        self.commands_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Правая часть - последовательность
        right_frame = tk.Frame(commands_frame, bg=self.colors['bg'])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_frame, text="Последовательность:", bg=self.colors['bg'], fg=self.colors['text']).pack(anchor=tk.W)
        
        self.sequence_listbox = tk.Listbox(right_frame, bg='#222222', fg=self.colors['text'], height=10)
        self.sequence_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки управления последовательностью
        buttons_frame = tk.Frame(frame, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(buttons_frame, text="Добавить →", bg='#333333', fg=self.colors['accent'],
                 command=self.add_to_sequence).pack(side=tk.LEFT, padx=2)
        
        tk.Button(buttons_frame, text="← Удалить", bg='#333333', fg='#ff5555',
                 command=self.remove_from_sequence).pack(side=tk.LEFT, padx=2)
        
        tk.Button(buttons_frame, text="↑ Вверх", bg='#333333', fg=self.colors['text'],
                 command=self.move_up).pack(side=tk.LEFT, padx=2)
        
        tk.Button(buttons_frame, text="↓ Вниз", bg='#333333', fg=self.colors['text'],
                 command=self.move_down).pack(side=tk.LEFT, padx=2)
        
        # Задержка между командами
        delay_frame = tk.Frame(frame, bg=self.colors['bg'])
        delay_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(delay_frame, text="Задержка между командами (секунды):", 
                bg=self.colors['bg'], fg=self.colors['text']).pack(side=tk.LEFT)
        
        self.delay_var = tk.StringVar(value="1.0")
        delay_entry = tk.Entry(delay_frame, textvariable=self.delay_var, bg='#222222', 
                             fg=self.colors['text'], width=5)
        delay_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопка создания последовательности
        tk.Button(frame, text="Создать последовательность", bg='#333333', fg=self.colors['accent'],
                 command=self.create_sequence).pack(pady=20)
        
        # Загружаем команды в список
        self.load_commands_to_list()
    
    def load_commands_to_list(self):
        """Загрузить команды в список"""
        self.commands_listbox.delete(0, tk.END)
        for name in self.commands_manager.commands.keys():
            self.commands_listbox.insert(tk.END, name)
    
    def add_to_sequence(self):
        """Добавить команду в последовательность"""
        selection = self.commands_listbox.curselection()
        if selection:
            command_name = self.commands_listbox.get(selection[0])
            self.sequence_listbox.insert(tk.END, command_name)
    
    def remove_from_sequence(self):
        """Удалить команду из последовательности"""
        selection = self.sequence_listbox.curselection()
        if selection:
            self.sequence_listbox.delete(selection[0])
    
    def move_up(self):
        """Переместить команду вверх"""
        selection = self.sequence_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            item = self.sequence_listbox.get(index)
            self.sequence_listbox.delete(index)
            self.sequence_listbox.insert(index-1, item)
            self.sequence_listbox.select_set(index-1)
    
    def move_down(self):
        """Переместить команду вниз"""
        selection = self.sequence_listbox.curselection()
        if selection and selection[0] < self.sequence_listbox.size()-1:
            index = selection[0]
            item = self.sequence_listbox.get(index)
            self.sequence_listbox.delete(index)
            self.sequence_listbox.insert(index+1, item)
            self.sequence_listbox.select_set(index+1)
    
    def create_sequence(self):
        """Создать последовательность"""
        name = self.sequence_name.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название последовательности")
            return
        
        if self.sequence_listbox.size() == 0:
            messagebox.showerror("Ошибка", "Добавьте команды в последовательность")
            return
        
        # Собираем действия
        actions = []
        for i in range(self.sequence_listbox.size()):
            command_name = self.sequence_listbox.get(i)
            actions.append({
                'type': 'command',
                'params': {'name': command_name},
                'delay': float(self.delay_var.get())
            })
        
        # Создаем последовательность
        success = self.commands_manager.create_sequence(name, actions)
        if success:
            messagebox.showinfo("Успех", f"Последовательность '{name}' создана!")
            self.sequence_name.delete(0, tk.END)
            self.sequence_listbox.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Не удалось создать последовательность")
    
    def create_manage_tab(self, notebook):
        """Вкладка управления командами - ИСПРАВЛЕННЫЙ ТОЛЬКО TREEVIEW"""
        frame = tk.Frame(notebook, bg=self.colors['bg'])
        notebook.add(frame, text="Управление")
        
        # ЖЕСТКАЯ НАСТРОЙКА СТИЛЯ TREEVIEW
        style = ttk.Style()
        
        # Пробуем разные темы для лучшей кастомизации
        available_themes = ['clam', 'alt', 'default', 'classic']
        for theme in available_themes:
            try:
                style.theme_use(theme)
                break
            except:
                continue
        
        # Цвета для темно-серого фона Treeview
        tree_bg = '#2b2b2b'  # ТЕМНО-СЕРЫЙ фон
        tree_fg = '#ffffff'  # БЕЛЫЙ текст
        tree_header_bg = '#333333'  # Темно-серый для заголовков
        tree_header_fg = '#00ffff'  # Акцентный цвет для заголовков
        tree_select_bg = '#444444'  # Цвет выделенной строки
        tree_select_fg = '#ffffff'  # Белый текст выделения
        
        # ПОЛНАЯ НАСТРОЙКА СТИЛЯ TREEVIEW
        style.configure("Dark.Treeview",
            background=tree_bg,
            foreground=tree_fg,
            fieldbackground=tree_bg,  # Фон пустого пространства
            borderwidth=0,
            font=('Arial', 9)
        )
        
        style.configure("Dark.Treeview.Heading",
            background=tree_header_bg,
            foreground=tree_header_fg,
            relief='flat',
            borderwidth=1,
            font=('Arial', 10, 'bold')
        )
        
        style.map("Dark.Treeview",
            background=[('selected', tree_select_bg)],
            foreground=[('selected', tree_select_fg)]
        )
        
        # Список команд
        tk.Label(frame, text="Сохраненные команды:", bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Создаем Treeview с новым стилем
        self.commands_tree = ttk.Treeview(frame, 
                                        columns=('name', 'type', 'created'), 
                                        show='headings', 
                                        style="Dark.Treeview")
        
        # Настраиваем столбцы
        self.commands_tree.heading('name', text='Название')
        self.commands_tree.heading('type', text='Тип')
        self.commands_tree.heading('created', text='Создана')
        
        self.commands_tree.column('name', width=150, anchor='w')
        self.commands_tree.column('type', width=100, anchor='center')
        self.commands_tree.column('created', width=150, anchor='center')
        
        self.commands_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Список последовательностей
        tk.Label(frame, text="Сохраненные последовательности:", bg=self.colors['bg'], fg=self.colors['text'],
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        self.sequences_tree = ttk.Treeview(frame, 
                                         columns=('name', 'actions', 'created'), 
                                         show='headings', 
                                         style="Dark.Treeview")
        
        self.sequences_tree.heading('name', text='Название')
        self.sequences_tree.heading('actions', text='Действий')
        self.sequences_tree.heading('created', text='Создана')
        
        self.sequences_tree.column('name', width=150, anchor='w')
        self.sequences_tree.column('actions', width=100, anchor='center')
        self.sequences_tree.column('created', width=150, anchor='center')
        
        self.sequences_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Кнопки управления
        buttons_frame = tk.Frame(frame, bg=self.colors['bg'])
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(buttons_frame, text="Удалить команду", bg='#333333', fg='#ff5555',
                command=self.delete_command).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="Удалить последовательность", bg='#333333', fg='#ff5555',
                command=self.delete_sequence).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="Выполнить команду", bg='#333333', fg=self.colors['accent'],
                command=self.execute_command).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="Выполнить последовательность", bg='#333333', fg=self.colors['accent'],
                command=self.execute_sequence).pack(side=tk.LEFT, padx=5)
        
        # Загружаем данные
        self.refresh_lists()

    def refresh_lists(self):
        """Обновить списки команд и последовательностей - ИСПРАВЛЕННОЕ ОТОБРАЖЕНИЕ"""
        # Очищаем деревья
        for item in self.commands_tree.get_children():
            self.commands_tree.delete(item)
        
        for item in self.sequences_tree.get_children():
            self.sequences_tree.delete(item)
        
        # ЗАГРУЗКА КОМАНД - ПРАВИЛЬНОЕ ОТОБРАЖЕНИЕ
        for name, data in self.commands_manager.commands.items():
            self.commands_tree.insert('', tk.END, values=(name, data['type'], data['created']))
        
        # ЗАГРУЗКА ПОСЛЕДОВАТЕЛЬНОСТЕЙ - ПРАВИЛЬНОЕ ОТОБРАЖЕНИЕ
        for name, data in self.commands_manager.sequences.items():
            action_count = len(data['actions'])
            self.sequences_tree.insert('', tk.END, values=(name, action_count, data['created']))
        
        # Обновляем список команд для вкладки последовательностей
        self.load_commands_to_list()

    
    def delete_command(self):
        """Удалить выбранную команду - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        selection = self.commands_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите команду для удаления")
            return
        
        item = selection[0]
        values = self.commands_tree.item(item)['values']
        name = values[0] if values else ""  # Берем имя из первого столбца
        
        if not name:
            messagebox.showerror("Ошибка", "Не удалось определить имя команды")
            return
            
        if messagebox.askyesno("Подтверждение", f"Удалить команду '{name}'?"):
            if self.commands_manager.delete_command(name):
                messagebox.showinfo("Успех", "Команда удалена")
                self.refresh_lists()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить команду")

    def delete_sequence(self):
        """Удалить выбранную последовательность - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        selection = self.sequences_tree.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", "Выберите последовательность для удаления")
            return
        
        item = selection[0]
        values = self.sequences_tree.item(item)['values']
        name = values[0] if values else ""  # Берем имя из первого столбца
        
        if not name:
            messagebox.showerror("Ошибка", "Не удалось определить имя последовательности")
            return
            
        if messagebox.askyesno("Подтверждение", f"Удалить последовательность '{name}'?"):
            if self.commands_manager.delete_sequence(name):
                messagebox.showinfo("Успех", "Последовательность удалена")
                self.refresh_lists()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить последовательность")

    def execute_command(self):
        """Выполнить выбранную команду - БЕЗ ВСПЛЫВАЮЩЕГО ОКНА"""
        selection = self.commands_tree.selection()
        if not selection:
            # Оставляем предупреждение, но не результат
            messagebox.showwarning("Предупреждение", "Выберите команду для выполнения")
            return
        
        item = selection[0]
        values = self.commands_tree.item(item)['values']
        name = values[0] if values else ""
        
        if not name:
            messagebox.showerror("Ошибка", "Не удалось определить имя команды")
            return
            
        # Выполняем команду и выводим результат в терминал
        success, message = self.commands_manager.execute_command(name)
        
        # Закрываем окно команд после выполнения
        self.window.destroy()
        
        # Выводим результат в основной терминал через основной интерфейс
        if hasattr(self, 'main_app') and self.main_app:
            if success:
                self.main_app.add_status_message(f"✅ Команда '{name}' выполнена успешно", source="SYSTEM")
                self.main_app.add_status_message(f"Результат: {message}", source="SYSTEM")
            else:
                self.main_app.add_status_message(f"❌ Ошибка выполнения команды '{name}'", source="ERROR")
                self.main_app.add_status_message(f"Ошибка: {message}", source="ERROR")
        else:
            # Fallback: если нет доступа к основному приложению
            print(f"Команда '{name}': {message}")

    def execute_sequence(self):
        """Выполнить выбранную последовательность - БЕЗ ВСПЛЫВАЮЩЕГО ОКНА"""
        selection = self.sequences_tree.selection()
        if not selection:
            # Оставляем предупреждение, но не результат
            messagebox.showwarning("Предупреждение", "Выберите последовательность для выполнения")
            return
        
        item = selection[0]
        values = self.sequences_tree.item(item)['values']
        name = values[0] if values else ""
        
        if not name:
            messagebox.showerror("Ошибка", "Не удалось определить имя последовательности")
            return
            
        # Выполняем последовательность и выводим результат в терминал
        success, message = self.commands_manager.execute_sequence(name)
        
        # Закрываем окно команд после выполнения
        self.window.destroy()
        
        # Выводим результат в основной терминал через основной интерфейс
        if hasattr(self, 'main_app') and self.main_app:
            if success:
                self.main_app.add_status_message(f"✅ Последовательность '{name}' выполнена успешно", source="SYSTEM")
                # Разбиваем сообщение на отдельные строки для лучшего чтения
                results = message.split(" | ")
                for result in results:
                    self.main_app.add_status_message(f"   {result}", source="SYSTEM")
            else:
                self.main_app.add_status_message(f"❌ Ошибка выполнения последовательности '{name}'", source="ERROR")
                self.main_app.add_status_message(f"Ошибка: {message}", source="ERROR")
        else:
            # Fallback: если нет доступа к основному приложению
            print(f"Последовательность '{name}': {message}")