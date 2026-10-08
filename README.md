# 🍽️ Debasus Bot

Telegram-бот для ресторана «Дебассус» (Воронеж).

Помогает гостям:
- 🔥 Узнать акцию дня
- 📍 Найти ресторан
- 📞 Забронировать столик

---

## 🚀 Быстрый старт (для разработчиков)

### Шаг 1: Клонировать проект

    git clone https://github.com/klrk526/debasus-bot.git
    cd debasus-bot

### Шаг 2: Создать виртуальное окружение

    python3.12 -m venv .venv

### Шаг 3: Активировать окружение

**macOS / Linux:**

    source .venv/bin/activate

**Windows:**

    .venv\Scripts\activate

После активации слева появится `(.venv)` — значит, всё ок.

### Шаг 4: Установить зависимости

    pip install -r requirements.txt

### Шаг 5: Установить pre-commit (защита от секретов)

    pip install pre-commit
    pre-commit install

### Шаг 6: Настроить переменные окружения

Скопировать шаблон:

    cp .env.example .env

Открыть `.env` и вписать **свой токен**:

    BOT_TOKEN=1234567890:твой_токен_от_BotFather
    ADMIN_IDS=твой_telegram_id
    DATABASE_URL=sqlite+aiosqlite:///bot.db

**Где взять токен:** Telegram → [@BotFather](https://t.me/BotFather) → `/newbot`

**Где взять свой ID:** Telegram → [@userinfobot](https://t.me/userinfobot) → Start

### Шаг 7: Запустить бота

    python Debassus.py

Бот запущен. Открой Telegram → напиши боту `/start`.

**Остановить:** `Ctrl + C` в терминале.

---

## 📁 Структура проекта

    debasus-bot/
    ├── bot/              # Telegram-логика
    │   ├── handlers/     # Обработчики команд
    │   ├── keyboards/    # Кнопки
    │   ├── states/       # Состояния диалога (FSM)
    │   ├── filters/      # Фильтры (например, только админ)
    │   └── middlewares/  # Прослойки
    ├── core/             # Общее
    │   ├── config.py     # Чтение .env
    │   └── logger.py     # Логирование
    ├── database/         # База данных
    │   ├── models.py     # Таблицы
    │   ├── session.py    # Подключение
    │   └── crud.py       # Функции работы с БД
    ├── services/         # Бизнес-логика (акции, бронирование)
    ├── .env              # Секреты (НЕ в Git!)
    ├── .env.example      # Шаблон
    ├── .gitignore        # Что не коммитить
    ├── .pre-commit-config.yaml  # Проверки перед коммитом
    ├── bot.py            # Точка входа
    ├── Debassus.py       # Черновик (будет разнесён по структуре)
    ├── requirements.txt  # Зависимости
    └── README.md         # Этот файл

---

## 🔄 Как работать с Git

### Перед началом работы

Всегда делай:

    git checkout main
    git pull

Это подтянет свежие изменения с GitHub.

### Создать ветку под задачу

    git checkout -b имя/что-делаешь

**Примеры:**
- `kirill/config` — настройка
- `ilya/booking` — бронирование
- `kirill/fix-start` — фикс бага

**Правило:** имя ветки = `автор/задача`, всё **маленькими** буквами, слова через **дефис**.

### После работы

    git status              # проверить, что изменилось
    git add .               # добавить в staging
    git status              # убедиться, что .env НЕ в списке!
    git commit -m "feat: что сделал"
    git push -u origin имя/что-делаешь

**При коммите автоматически запустится Gitleaks** — проверит на секреты.
Если найдёт — коммит заблокируется. Убери токен и попробуй снова.

### Создать Pull Request

1. Открой https://github.com/klrk526/debasus-bot
2. Нажми **Compare & pull request**
3. Заполни Title → **Create pull request**
4. Дождись CI (зелёная галочка ✅)
5. **Merge pull request** → **Confirm merge** → **Delete branch**

### После мержа — вернуться в main

    git checkout main
    git pull
    git branch -d имя/что-делаешь

---

## ⚠️ Правила

### ❌ НЕЛЬЗЯ

- **Коммитить `.env`** — там токен. Он в `.gitignore`.
- **Писать в `main` напрямую** — только через PR.
- **Хардкодить токен в коде** — только через `.env`.
- **Пушить с токеном** — Gitleaks заблокирует.

### ✅ НУЖНО

- **Всегда `git pull`** перед началом.
- **Каждая задача** — своя ветка.
- **Проверять `git status`** перед коммитом.
- **Проверять, что `.env`** не в списке.

---

## 🛡️ Безопасность

Проект защищён **тремя уровнями**:

1. **Pre-commit** — ловит секреты **до коммита** (на твоём компьютере).
2. **GitHub Actions** — ловит секреты **при PR** (на сервере GitHub).
3. **Ruleset на `main`** — запрещает **прямой push** в `main`.

**Что это значит:**
- Случайно закоммитить токен — **не получится**.
- Запушить с секретом — **не получится**.
- Сломать `main` — **не получится**.

---

## 🆘 Если что-то не работает

### `pip: command not found`

Активируй `.venv`:

    source .venv/bin/activate

Или используй `python -m pip` вместо `pip`.

### `ModuleNotFoundError: No module named 'aiogram'`

Установи зависимости:

    pip install -r requirements.txt

### `Token is invalid`

Проверь `.env` — там **новый** токен от @BotFather?

### `Error in the HTTP2 framing layer`

Проблема с сетью. Попробуй:

    git config --global http.version HTTP/1.1

Или выключи VPN.

### Git не пускает в `main`

**Так и должно быть.** `main` защищён. Работай через ветку:

    git checkout -b имя/задача

---


---

**Удачи!** 🚀
