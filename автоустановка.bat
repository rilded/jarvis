@echo off
echo Установка зависимостей для программы...
echo.

:: Обновление pip до последней версии
python -m pip install --upgrade pip

:: Основные библиотеки
pip install pyautogui
pip install winsound
pip install pyperclip
pip install keyboard
pip install psutil
pip install loky
pip install pygame
pip install pyttsx3
pip install SpeechRecognition
pip install pyaudio

:: Если есть requirements.txt, можно использовать его
if exist requirements.txt (
    echo Обнаружен requirements.txt, устанавливаю из него...
    pip install -r requirements.txt
)

echo.
echo Установка завершена!
pause