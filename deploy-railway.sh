#!/bin/bash

echo "Deploying FitPose to Railway..."

# Проверяем, что Railway CLI установлен
if ! command -v railway &> /dev/null; then
    echo "Railway CLI не установлен. Установите его:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Логинимся в Railway (если нужно)
echo "Проверяем авторизацию Railway..."
railway whoami || railway login

# Создаем новый проект или используем существующий
echo "Инициализируем проект Railway..."
railway init

# Устанавливаем переменные окружения для Railway
echo "Настраиваем переменные окружения..."
echo "ВАЖНО: Установите OPENAI_API_KEY в Railway dashboard после деплоя!"

# Проверяем что все файлы на месте
echo "Проверяем структуру проекта..."
if [[ ! -f "main.py" ]]; then
    echo "main.py не найден!"
    exit 1
fi

if [[ ! -f "requirements.txt" ]]; then
    echo "requirements.txt не найден!"
    exit 1
fi

# Деплоим backend
echo "Деплоим backend..."
railway up --detach

echo "Деплой запущен!"
echo ""
echo "Следующие шаги:"
echo "1. Откройте Railway dashboard: https://railway.app/dashboard"
echo "2. Найдите ваш проект FitPose"
echo "3. Перейдите в Variables и установите:"
echo "   OPENAI_API_KEY=your_actual_openai_key"
echo "4. Скопируйте URL вашего приложения"
echo "5. Обновите API_URL в src/frontend/src/App.jsx (dev: http://localhost:8000)"
echo "   Бэкенд эндпоинт анализа: POST /api/v1/analyze-exercise (multipart: file)"
echo "6. Протестируйте API: curl https://your-app.railway.app/health"
echo ""
echo "Готово! Ваш FitPose API деплоится на Railway!"
