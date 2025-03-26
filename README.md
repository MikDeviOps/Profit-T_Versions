# 🤖 Бот мониторинга изменений конфигурации «Профи-Т»

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Aiogram-3.x-green?style=for-the-badge" alt="Aiogram">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

## 📌 О проекте

Автоматизированная система для отслеживания изменений в конфигурационных файлах кассовой программы «Профи-Т». Бот анализирует историю изменений и предоставляет удобный интерфейс для просмотра через Telegram и веб-версию.

## 🌟 Возможности

### 📊 Основной функционал
- Автоматическое обнаружение последних изменений
- Интеллектуальный парсинг истории изменений
- Гибкая система фильтрации и сортировки

### 📱 Интерфейсы
- Удобный Telegram-бот с интерактивным меню
- Полноценная веб-версия для детального анализа
- Два типа клавиатур: обычные и inline-кнопки

### 🔍 Аналитика
- Группировка по авторам изменений
- Хронологическое представление данных
- Детализированные отчеты по файлам

## 🛠 Технологии

<div align="center">
  
| Компонент       | Технология         |
|-----------------|--------------------|
| Язык           | Python 3.12+       |
| Фреймворк      | Aiogram 3.x        |
| Парсинг        | Regular Expressions|
| Работа с файлами | Pathlib           |
| Асинхронность  | Asyncio            |

</div>

## 🏗 Архитектура

```text
bot/
│   ├── __init__.py
│   ├── config.py
│   ├── keyboards.py
│   ├── routers.py
│   ├── check_updates.py
|   ├── DockerFile
|   ├── docker-compose.yml
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── reporter.py
│   │   └── utils.py
├── main.py
├── .env
```
## 🚀 Быстрый старт
<details><summary>Клонируйте репозиторий:</summary>
<br>

bash
Copy
git clone https://github.com/your-username/profi-t-monitor-bot.git
cd profi-t-monitor-bot
</details>

<details><summary>Установите зависимости:</summary><br>


bash
Copy
pip install -r requirements.txt
</details>

<details><summary>Настройте конфигурацию:</summary><br>
nano bot/config.py
</details>

<details><summary>Запустите бота:</summary><br>
python bot/main.py
</details>

## 📌 Команды бота
<details><summary>Основные команды:</summary><br>
/start	Главное меню <br><br>
/info	Информация о боте <br><br>
/check	Проверить изменения <br><br>
</details>

<details><summary>Inline-кнопки:</summary><br>

🔄 Обновить - получить свежие данные <br><br>

👤 По авторам - фильтр по разработчикам <br><br>

🌐 Веб-версия - полная история изменений <br><br>
</details>
