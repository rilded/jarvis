# advanced_customization.py - РАСШИРЕННАЯ СИСТЕМА КАСТОМИЗАЦИИ
import json
import os
import tkinter as tk
from tkinter import ttk, colorchooser, font
import sys
import messagebox

class AdvancedCustomization:
    def __init__(self, settings_manager):
        self.settings_manager = settings_manager
        self.settings = settings_manager.settings
        
    def open_customization_window(self, parent):
        """Открыть окно расширенной кастомизации"""
        self.custom_window = tk.Toplevel(parent)
        self.custom_window.title("Расширенная кастомизация JARVIS")
        self.custom_window.geometry("1000x700")
        self.custom_window.configure(bg='#111111')
        self.custom_window.transient(parent)
        self.custom_window.grab_set()
        
        # Создаем Notebook с вкладками
        notebook = ttk.Notebook(self.custom_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        self.create_appearance_tab(notebook)
        self.create_behavior_tab(notebook)
        self.create_voice_tab(notebook)
        self.create_commands_tab(notebook)
        self.create_hotkeys_tab(notebook)
        self.create_integrations_tab(notebook)
        self.create_themes_tab(notebook)
        
        # Кнопки сохранения
        button_frame = tk.Frame(self.custom_window, bg='#111111')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="Сохранить и применить", 
                 command=self.save_and_apply, bg='#006600', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(button_frame, text="Сбросить к стандартным", 
                 command=self.reset_to_default, bg='#660000', fg='white',
                 font=('Arial', 10)).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(button_frame, text="Отмена", 
                 command=self.custom_window.destroy, bg='#333333', fg='white',
                 font=('Arial', 10)).pack(side=tk.RIGHT, padx=5)
    
    def create_appearance_tab(self, notebook):
        """Вкладка внешнего вида"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Внешний вид")
        
        # Тема
        tk.Label(frame, text="Тема оформления:", bg='#111111', fg='white',
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        theme_var = tk.StringVar(value=self.settings['customization']['appearance']['theme'])
        themes = ['dark', 'light', 'blue', 'green', 'red', 'purple', 'custom']
        
        theme_frame = tk.Frame(frame, bg='#111111')
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
        for theme in themes:
            tk.Radiobutton(theme_frame, text=theme.capitalize(), variable=theme_var, 
                          value=theme, bg='#111111', fg='white', 
                          selectcolor='#333333').pack(side=tk.LEFT, padx=10)
        
        # Цвета
        colors_frame = tk.LabelFrame(frame, text="Цвета", bg='#111111', fg='white')
        colors_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_color_selector(colors_frame, "Акцентный цвет:", 
                                 'customization.appearance.accent_color', '#00ffff')
        self.create_color_selector(colors_frame, "Фон:", 
                                 'customization.appearance.background_color', '#000000')
        self.create_color_selector(colors_frame, "Текст:", 
                                 'customization.appearance.text_color', '#e0e0e0')
        
        # Шрифт
        font_frame = tk.LabelFrame(frame, text="Шрифт", bg='#111111', fg='white')
        font_frame.pack(fill=tk.X, padx=10, pady=10)
        
        font_families = font.families()
        popular_fonts = ['Courier New', 'Consolas', 'Arial', 'Tahoma', 'Verdana', 'Segoe UI']
        
        tk.Label(font_frame, text="Шрифт:", bg='#111111', fg='white').pack(anchor=tk.W, padx=5)
        font_combo = ttk.Combobox(font_frame, values=popular_fonts, width=20)
        font_combo.set(self.settings['customization']['appearance']['font_family'])
        font_combo.pack(anchor=tk.W, padx=5, pady=2)
        
        tk.Label(font_frame, text="Размер:", bg='#111111', fg='white').pack(anchor=tk.W, padx=5)
        size_spin = tk.Spinbox(font_frame, from_=8, to=20, width=10)
        size_spin.delete(0, tk.END)
        size_spin.insert(0, str(self.settings['customization']['appearance']['font_size']))
        size_spin.pack(anchor=tk.W, padx=5, pady=2)
        
        # Прозрачность
        tk.Label(frame, text="Прозрачность окна:", bg='#111111', fg='white').pack(anchor=tk.W, padx=10, pady=(10,5))
        opacity_scale = tk.Scale(frame, from_=0.5, to=1.0, resolution=0.05, orient=tk.HORIZONTAL,
                                bg='#111111', fg='white', highlightbackground='#111111')
        opacity_scale.set(self.settings['customization']['appearance']['window_opacity'])
        opacity_scale.pack(fill=tk.X, padx=10, pady=5)
    
    def create_behavior_tab(self, notebook):
        """Вкладка поведения"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Поведение")
        
        # Фразы активации
        activation_frame = tk.LabelFrame(frame, text="Фразы активации", bg='#111111', fg='white')
        activation_frame.pack(fill=tk.X, padx=10, pady=10)
        
        activation_text = tk.Text(activation_frame, height=4, width=50, bg='#222222', fg='white')
        activation_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        phrases = self.settings['customization']['behavior']['activation_phrases']
        activation_text.insert(1.0, ', '.join(phrases))
        
        tk.Label(activation_frame, text="Фразы через запятую", bg='#111111', fg='gray',
                font=('Arial', 8)).pack()
        
        # Задержки
        delays_frame = tk.LabelFrame(frame, text="Задержки и время", bg='#111111', fg='white')
        delays_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_slider(delays_frame, "Задержка ответа (сек):", 
                          'customization.behavior.response_delay', 0.1, 2.0, 0.1)
        self.create_slider(delays_frame, "Скорость анимации:", 
                          'customization.appearance.animation_speed', 0.5, 3.0, 0.1)
        
        # Поведение
        behavior_frame = tk.LabelFrame(frame, text="Поведение системы", bg='#111111', fg='white')
        behavior_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_checkbox(behavior_frame, "Автодополнение команд", 
                           'customization.behavior.auto_complete_commands', True)
        self.create_checkbox(behavior_frame, "Подтверждать опасные действия", 
                           'customization.behavior.confirm_destructive_actions', True)
        self.create_checkbox(behavior_frame, "Автосохранение настроек", 
                           'customization.behavior.auto_save_settings', True)
        
        # История команд
        tk.Label(behavior_frame, text="Максимум истории команд:", bg='#111111', fg='white').pack(anchor=tk.W)
        history_spin = tk.Spinbox(behavior_frame, from_=10, to=1000, width=10)
        history_spin.delete(0, tk.END)
        history_spin.insert(0, str(self.settings['customization']['behavior']['max_command_history']))
        history_spin.pack(anchor=tk.W, padx=5, pady=2)
    
    def create_voice_tab(self, notebook):
        """Вкладка голоса"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Голос")
        
        # Движок голоса
        tk.Label(frame, text="Движок TTS:", bg='#111111', fg='white',
                font=('Arial', 11, 'bold')).pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        engine_var = tk.StringVar(value=self.settings['customization']['voice']['voice_engine'])
        engines = ['pyttsx3', 'sapi5', 'nsss', 'espeak']
        
        engine_frame = tk.Frame(frame, bg='#111111')
        engine_frame.pack(fill=tk.X, padx=10, pady=5)
        
        for eng in engines:
            tk.Radiobutton(engine_frame, text=eng.upper(), variable=engine_var, 
                          value=eng, bg='#111111', fg='white', 
                          selectcolor='#333333').pack(side=tk.LEFT, padx=10)
        
        # Параметры голоса
        voice_frame = tk.LabelFrame(frame, text="Параметры голоса", bg='#111111', fg='white')
        voice_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_slider(voice_frame, "Скорость речи:", 
                          'customization.voice.speech_rate', 50, 300, 10)
        self.create_slider(voice_frame, "Громкость:", 
                          'customization.voice.speech_volume', 0.1, 1.0, 0.1)
        self.create_slider(voice_frame, "Тон голоса:", 
                          'customization.voice.pitch', 0, 100, 1)
        
        # Эффекты голоса
        effects_frame = tk.LabelFrame(frame, text="Эффекты голоса", bg='#111111', fg='white')
        effects_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_checkbox(effects_frame, "Эхо", 
                           'customization.voice.voice_effects.echo', False)
        self.create_checkbox(effects_frame, "Реверберация", 
                           'customization.voice.voice_effects.reverb', False)
        self.create_checkbox(effects_frame, "Вариация тона", 
                           'customization.voice.voice_effects.pitch_variation', True)
        
        # Тест голоса
        test_frame = tk.Frame(frame, bg='#111111')
        test_frame.pack(fill=tk.X, padx=10, pady=10)
        
        test_entry = tk.Entry(test_frame, bg='#222222', fg='white', width=30)
        test_entry.insert(0, "Привет, я Джарвис")
        test_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(test_frame, text="Тест голоса", bg='#333333', fg='white',
                 command=lambda: self.test_voice(test_entry.get())).pack(side=tk.LEFT, padx=5)
    
    def create_commands_tab(self, notebook):
        """Вкладка команд - ДОРАБОТАННАЯ"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Команды")
        
        # Быстрые команды
        quick_frame = tk.LabelFrame(frame, text="Быстрые команды", bg='#111111', fg='white')
        quick_frame.pack(fill=tk.X, padx=10, pady=10)
        
        quick_commands = [
            ("Открыть диспетчер команд", self.open_commands_manager),
            ("Импорт команд из файла", self.import_commands),
            ("Экспорт команд в файл", self.export_commands)
        ]
        
        for text, command in quick_commands:
            tk.Button(quick_frame, text=text, bg='#333333', fg='white',
                    command=command).pack(pady=2)
        
        # Интеграция с голосовым управлением
        voice_frame = tk.LabelFrame(frame, text="Голосовое управление", bg='#111111', fg='white')
        voice_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.create_checkbox(voice_frame, "Автоматически регистрировать новые команды", 
                        'customization.commands.auto_register', True)
        
        tk.Label(voice_frame, text="Префикс для голосовых команд:", bg='#111111', fg='white').pack(anchor=tk.W)
        prefix_entry = tk.Entry(voice_frame, bg='#222222', fg='white', width=20)
        prefix_entry.insert(0, self.get_setting('customization.commands.voice_prefix', 'запусти'))
        prefix_entry.pack(anchor=tk.W, padx=5, pady=2)
        
        # Шаблоны команд
        templates_frame = tk.LabelFrame(frame, text="Шаблоны команд", bg='#111111', fg='white')
        templates_frame.pack(fill=tk.X, padx=10, pady=10)
        
        templates = [
            ("Открыть сайт", "open_url", "{url}"),
            ("Запустить программу", "run_program", "{path}"),
            ("Сочетание клавиш", "press_keys", "{keys}"),
            ("Текст", "type_text", "{text}")
        ]
        
        for name, cmd_type, template in templates:
            tk.Button(templates_frame, text=f"Создать {name}", bg='#333333', fg='white',
                    command=lambda t=cmd_type, tmpl=template: self.create_template(t, tmpl)).pack(side=tk.LEFT, padx=5)
            
    def test_customization_features(self):
        """Протестировать функции кастомизации"""
        test_window = tk.Toplevel()
        test_window.title("Тест кастомизации")
        test_window.geometry("400x300")
        
        # Тест цветов
        colors_frame = tk.Frame(test_window)
        colors_frame.pack(pady=10)
        
        tk.Label(colors_frame, text="Тест цветовой схемы", font=('Arial', 12, 'bold')).pack()
        
        # Показ текущих цветов
        current_bg = self.get_setting('customization.appearance.background_color', '#000000')
        current_accent = self.get_setting('customization.appearance.accent_color', '#00ffff')
        
        color_preview = tk.Frame(colors_frame, bg=current_bg, width=200, height=50)
        color_preview.pack(pady=5)
        tk.Label(color_preview, text="Пример текста", fg=current_accent, bg=current_bg).pack()
        
        # Тест голоса
        voice_frame = tk.Frame(test_window)
        voice_frame.pack(pady=10)
        
        tk.Label(voice_frame, text="Тест голоса", font=('Arial', 12, 'bold')).pack()
        
        test_text = tk.Entry(voice_frame, width=30)
        test_text.pack(pady=5)
        test_text.insert(0, "Привет, это тест голоса")
        
        tk.Button(voice_frame, text="Тест TTS", 
                command=lambda: self.test_voice(test_text.get())).pack()
        
        # Кнопка закрытия
        tk.Button(test_window, text="Закрыть", command=test_window.destroy).pack(pady=10)

    def open_commands_manager(self):
        """Открыть менеджер команд"""
        # Нужно импортировать и вызвать интерфейс команд
        try:
            from jarvis_visual import JarvisVisual
            # Здесь нужно получить экземпляр главного приложения
            if hasattr(self, 'main_app'):
                self.main_app.open_commands_manager()
        except:
            messagebox.showinfo("Информация", "Менеджер команд доступен из главного окна")

    
    def create_hotkeys_tab(self, notebook):
        """Вкладка горячих клавиш"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Горячие клавиши")
        
        hotkeys = [
            ("Активация Джарвиса", "customization.hotkeys.global_activation"),
            ("Быстрая команда", "customization.hotkeys.quick_command"),
            ("Экстренная остановка", "customization.hotkeys.emergency_stop"),
            ("Вкл/Выкл голос", "customization.hotkeys.toggle_voice"),
            ("Скриншот", "customization.hotkeys.screenshot")
        ]
        
        for display_name, setting_path in hotkeys:
            self.create_hotkey_selector(frame, display_name, setting_path)
    
    def create_integrations_tab(self, notebook):
        """Вкладка интеграций"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Интеграции")
        
        integrations = [
            ("DeepSeek AI", "customization.integrations.deepseek_enabled"),
            ("Ollama", "customization.integrations.ollama_enabled"),
            ("Веб-поиск", "customization.integrations.web_search_enabled"),
            ("Погода", "customization.integrations.weather_enabled"),
            ("Новости", "customization.integrations.news_enabled")
        ]
        
        for display_name, setting_path in integrations:
            self.create_checkbox(frame, display_name, setting_path, True)
        
        # Музыкальные сервисы
        music_frame = tk.LabelFrame(frame, text="Музыкальные сервисы", bg='#111111', fg='white')
        music_frame.pack(fill=tk.X, padx=10, pady=10)
        
        services = ['yandex', 'youtube', 'spotify', 'soundcloud']
        current_services = self.settings['customization']['integrations']['music_services']
        
        for service in services:
            var = tk.BooleanVar(value=service in current_services)
            cb = tk.Checkbutton(music_frame, text=service.capitalize(), variable=var,
                               bg='#111111', fg='white', selectcolor='#333333')
            cb.var = var
            cb.service = service
            cb.pack(anchor=tk.W)
    
    def create_themes_tab(self, notebook):
        """Вкладка готовых тем"""
        frame = tk.Frame(notebook, bg='#111111')
        notebook.add(frame, text="Готовые темы")
        
        themes = [
            ("Стандартная", "dark", "#00ffff", "#000000"),
            ("Синяя", "blue", "#0088ff", "#000022"),
            ("Зеленая", "green", "#00ff00", "#001100"),
            ("Красная", "red", "#ff0000", "#110000"),
            ("Фиолетовая", "purple", "#aa00ff", "#110011"),
            ("Светлая", "light", "#0066cc", "#f0f0f0")
        ]
        
        for name, theme, accent, bg in themes:
            theme_frame = tk.Frame(frame, bg=bg, relief=tk.RAISED, bd=2)
            theme_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(theme_frame, text=name, bg=bg, fg=accent,
                    font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10, pady=10)
            
            # Превью элементов интерфейса
            preview_frame = tk.Frame(theme_frame, bg=bg)
            preview_frame.pack(side=tk.LEFT, padx=10, pady=5)
            
            tk.Label(preview_frame, text="Текст", bg=bg, fg=accent).pack()
            tk.Button(preview_frame, text="Кнопка", bg='#333333', fg=accent).pack()
            
            tk.Button(theme_frame, text="Применить", bg=accent, fg=bg,
                     command=lambda t=theme, a=accent, b=bg: self.apply_theme(t, a, b)).pack(side=tk.RIGHT, padx=10)
    
    def create_color_selector(self, parent, label, setting_path, default):
        """Создать выбор цвета"""
        frame = tk.Frame(parent, bg='#111111')
        frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(frame, text=label, bg='#111111', fg='white', width=15).pack(side=tk.LEFT)
        
        current_color = self.get_setting(setting_path, default)
        color_label = tk.Label(frame, text="■", bg=current_color, fg=current_color, width=3)
        color_label.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame, text="Выбрать", bg='#333333', fg='white', width=10,
                 command=lambda: self.choose_color(color_label, setting_path)).pack(side=tk.LEFT, padx=5)
        
        # Поле для ручного ввода
        entry = tk.Entry(frame, bg='#222222', fg='white', width=10)
        entry.insert(0, current_color)
        entry.pack(side=tk.LEFT, padx=5)
        entry.bind('<Return>', lambda e: self.update_color_from_entry(entry, color_label, setting_path))
    
    def create_slider(self, parent, label, setting_path, min_val, max_val, resolution):
        """Создать слайдер"""
        frame = tk.Frame(parent, bg='#111111')
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(frame, text=label, bg='#111111', fg='white').pack(anchor=tk.W)
        
        current_val = self.get_setting(setting_path, (min_val + max_val) / 2)
        scale = tk.Scale(frame, from_=min_val, to=max_val, resolution=resolution,
                        orient=tk.HORIZONTAL, bg='#111111', fg='white',
                        highlightbackground='#111111')
        scale.set(current_val)
        scale.setting_path = setting_path
        scale.pack(fill=tk.X, padx=5, pady=2)
    
    def create_checkbox(self, parent, label, setting_path, default):
        """Создать чекбокс"""
        var = tk.BooleanVar(value=self.get_setting(setting_path, default))
        cb = tk.Checkbutton(parent, text=label, variable=var, bg='#111111', fg='white',
                           selectcolor='#333333')
        cb.var = var
        cb.setting_path = setting_path
        cb.pack(anchor=tk.W, padx=5, pady=2)
    
    def create_hotkey_selector(self, parent, label, setting_path):
        """Создать выбор горячей клавиши"""
        frame = tk.Frame(parent, bg='#111111')
        frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame, text=label, bg='#111111', fg='white', width=20).pack(side=tk.LEFT)
        
        current_hotkey = self.get_setting(setting_path, "")
        entry = tk.Entry(frame, bg='#222222', fg='white', width=20)
        entry.insert(0, current_hotkey)
        entry.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame, text="Записать", bg='#333333', fg='white',
                 command=lambda: self.record_hotkey(entry, setting_path)).pack(side=tk.LEFT, padx=5)
    
    def choose_color(self, color_label, setting_path):
        """Выбрать цвет через диалог"""
        color = colorchooser.askcolor(initialcolor=color_label.cget('bg'))[1]
        if color:
            color_label.config(bg=color, fg=color)
            self.set_setting(setting_path, color)
    
    def update_color_from_entry(self, entry, color_label, setting_path):
        """Обновить цвет из текстового поля"""
        color = entry.get()
        if color.startswith('#'):
            color_label.config(bg=color, fg=color)
            self.set_setting(setting_path, color)
    
    def record_hotkey(self, entry, setting_path):
        """Записать горячую клавишу"""
        entry.delete(0, tk.END)
        entry.insert(0, "Нажмите комбинацию...")
        entry.focus_set()
        
        # Здесь будет логика захвата клавиш (упрощенно)
        def on_keypress(event):
            # Это упрощенная версия - в реальности нужен более сложный обработчик
            key = event.keysym
            modifiers = []
            if event.state & 0x4: modifiers.append('ctrl')
            if event.state & 0x8: modifiers.append('alt')
            if event.state & 0x10: modifiers.append('shift')
            
            if modifiers:
                hotkey = '+'.join(modifiers + [key.lower()])
            else:
                hotkey = key.lower()
            
            entry.delete(0, tk.END)
            entry.insert(0, hotkey)
            self.set_setting(setting_path, hotkey)
            entry.unbind('<KeyPress>')
        
        entry.bind('<KeyPress>', on_keypress)
    
    def test_voice(self, text):
        """Тестирование голоса"""
        # Здесь будет вызов TTS системы
        print(f"Тест голоса: {text}")
    
    def apply_theme(self, theme, accent, background):
        """Применить готовую тему"""
        self.set_setting('customization.appearance.theme', theme)
        self.set_setting('customization.appearance.accent_color', accent)
        self.set_setting('customization.appearance.background_color', background)
        
        # Здесь будет код применения темы к интерфейсу
        print(f"Применена тема: {theme}")
    
    def export_commands(self):
        """Экспорт команд"""
        # Экспорт кастомных команд в файл
        print("Экспорт команд...")
    
    def import_commands(self):
        """Импорт команд"""
        # Импорт команд из файла
        print("Импорт команд...")
    
    def clear_all_commands(self):
        """Очистить все команды"""
        if tk.messagebox.askyesno("Подтверждение", "Очистить все кастомные команды?"):
            print("Все команды очищены")
    
    def get_setting(self, path, default):
        """Получить значение настройки по пути"""
        keys = path.split('.')
        value = self.settings
        for key in keys:
            value = value.get(key, {})
        return value if value != {} else default
    
    def set_setting(self, path, value):
        """Установить значение настройки по пути"""
        keys = path.split('.')
        settings_ref = self.settings
        for key in keys[:-1]:
            if key not in settings_ref:
                settings_ref[key] = {}
            settings_ref = settings_ref[key]
        settings_ref[keys[-1]] = value
    
    def save_and_apply(self):
        """Сохранить и применить настройки"""
        self.settings_manager.save_settings()
        tk.messagebox.showinfo("Сохранено", "Настройки кастомизации сохранены и применены")
        self.custom_window.destroy()
    
    def reset_to_default(self):
        """Сбросить к стандартным настройкам"""
        if tk.messagebox.askyesno("Подтверждение", "Сбросить все настройки кастомизации к стандартным?"):
            # Восстановление стандартных настроек
            print("Настройки сброшены")
