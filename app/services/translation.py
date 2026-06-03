"""
EN/RU string translation helpers.

Placeholder — implemented in Epic 2.
"""
from __future__ import annotations

_STRINGS: dict[str, dict[str, str]] = {
    # Onboarding
    "welcome_start": {
        "en": "🇬🇧 **Relocation Rental Radar**\n\nI help people relocating to Spain find apartments and rooms faster with AI-powered analysis.\n\n"
              "Please choose your language:",
        "ru": "🇷🇺 **Relocation Rental Radar**\n\nЯ помогаю тем, кто переезжает в Испанию, быстрее находить квартиры и комнаты с помощью анализа объявлений нейросетью.\n\n"
              "Пожалуйста, выберите язык:",
    },
    "choose_language": {
        "en": "Please choose your language:",
        "ru": "Пожалуйста, выберите язык:",
    },
    "language_set": {
        "en": "Language set to English 🇬🇧",
        "ru": "Язык установлен: Русский 🇷🇺",
    },
    "what_looking_for": {
        "en": "🏠 What are you looking for?",
        "ru": "🏠 Что вы ищете?",
    },
    "budget_min": {
        "en": "💰 What is your **MINIMUM** monthly budget in EUR? (e.g. 600)",
        "ru": "💰 Какой ваш **МИНИМАЛЬНЫЙ** месячный бюджет в евро? (например, 600)",
    },
    "budget_min_room": {
        "en": "💰 What is your **MINIMUM** monthly budget for a ROOM in EUR?",
        "ru": "💰 Какой ваш **МИНИМАЛЬНЫЙ** бюджет на КОМНАТУ в евро?",
    },
    "budget_max": {
        "en": "💰 And your **MAXIMUM** monthly budget? (e.g. 1500)",
        "ru": "💰 И ваш **МАКСИМАЛЬНЫЙ** месячный бюджет? (например, 1500)",
    },
    "enter_number": {
        "en": "Please enter a number (e.g. 1000):",
        "ru": "Пожалуйста, введите число (например, 1000):",
    },
    "areas_prompt": {
        "en": "📍 Which areas in Barcelona do you prefer?\n\nEnter area names or zip codes (e.g. Eixample, Gràcia, 08005).\nSeparate with commas.",
        "ru": "📍 Какие районы Барселоны вы предпочитаете?\n\nВведите названия районов или почтовые индексы (например, Eixample, Gràcia, 08005).\nРазделяйте запятыми.",
    },
    "search_created": {
        "en": "✅ **Search created!**\n\nI will now start monitoring listings for you. You will receive alerts here as soon as we find something that matches your criteria.",
        "ru": "✅ **Поиск создан!**\n\nЯ начинаю следить за объявлениями. Вы будете получать уведомления здесь, как только мы найдем что-то подходящее под ваши критерии.",
    },
    "search_summary": {
        "en": "**Search Summary**\n📍 City: {city}\n🏠 Type: {type}\n💰 Budget: {min} - {max} EUR\n🗺️ Areas: {areas}",
        "ru": "**Параметры поиска**\n📍 Город: {city}\n🏠 Тип: {type}\n💰 Бюджет: {min} - {max} EUR\n🗺️ Районы: {areas}",
    },
    
    # Commands
    "help_text": {
        "en": "🤖 **Relocation Rental Radar Help**\n\n"
              "I monitor rental listings and use AI to analyze them for risks and relevance.\n\n"
              "**Available Commands:**\n"
              "/start - Restart onboarding or update settings\n"
              "/my_search - View your active search filters\n"
              "/help - Show this help message\n"
              "/delete_me - Permanently delete your data (GDPR)\n\n"
              "**How it works:**\n"
              "1. You set your filters.\n"
              "2. I scan sources like Idealista.\n"
              "3. AI analyzes promising listings.\n"
              "4. You get an alert with a risk assessment and summary.",
        "ru": "🤖 **Помощь Relocation Rental Radar**\n\n"
              "Я слежу за объявлениями об аренде и использую ИИ для их анализа на риски и релевантность.\n\n"
              "**Доступные команды:**\n"
              "/start - Начать заново или изменить настройки\n"
              "/my_search - Просмотреть текущие фильтры поиска\n"
              "/help - Показать это сообщение\n"
              "/delete_me - Безвозвратно удалить ваши данные (GDPR)\n\n"
              "**Как это работает:**\n"
              "1. Вы задаете фильтры.\n"
              "2. Я сканирую источники (например, Idealista).\n"
              "3. ИИ анализирует многообещающие варианты.\n"
              "4. Вы получаете уведомление с оценкой рисков и резюме.",
    },
    "no_active_search": {
        "en": "You don't have an active search yet. Run /start to create one.",
        "ru": "У вас еще нет активного поиска. Запустите /start, чтобы создать его.",
    },
    "delete_confirm": {
        "en": "Your account and all searches have been deleted. Goodbye!",
        "ru": "Ваш аккаунт и все поиски удалены. До свидания!",
    },
    "not_registered": {
        "en": "You are not registered in our system.",
        "ru": "Вы не зарегистрированы в нашей системе.",
    },
    "session_lost": {
        "en": "Error: User session lost. Please run /start again.",
        "ru": "Ошибка: Сессия потеряна. Пожалуйста, запустите /start снова.",
    },
}


def t(key: str, language: str = "en") -> str:
    """Return the translated string for the given key and language."""
    # Handle language input carefully (could be an Enum or short string)
    if not isinstance(language, str):
        try:
            language = language.value.lower()
        except AttributeError:
            language = "en"
    
    language = language.lower()
    entry = _STRINGS.get(key, {})
    return entry.get(language, entry.get("en", key))
