@echo off
REM Скрипт для запуска генератора паролей

echo Запуск генератора паролей...

REM Проверяем, установлены ли зависимости
python -c "import typer, rich" 2>nul
if errorlevel 1 (
    echo Устанавливаем зависимости...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Ошибка при установке зависимостей. Проверьте, установлен ли Python и pip.
        pause
        exit /b 1
    )
)

REM Запускаем приложение
echo Запускаем приложение...
python main.py %*

REM Пауза, чтобы пользователь мог увидеть результат
pause