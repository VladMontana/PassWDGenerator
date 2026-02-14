#!/bin/bash
# Скрипт для запуска генератора паролей

# Проверяем, установлены ли зависимости
if python -c "import typer, rich" &> /dev/null; then
    echo "Зависимости уже установлены"
else
    echo "Устанавливаем зависимости..."
    pip install -r requirements.txt
fi

# Запускаем приложение
python main.py "$@"