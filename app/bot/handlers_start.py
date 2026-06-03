"""
Handlers for the /start command and onboarding flow.
Includes the FSM for search creation.
"""
from __future__ import annotations

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy import select, func

from app.db.models import User, Language, UserSearch, RentalType
from app.db.session import AsyncSessionFactory
from app.bot.keyboards import get_language_keyboard, get_rental_type_keyboard
from app.services.translation import t
from app.logging import get_logger

logger = get_logger(__name__)
router = Router(name="start")


class SearchCreation(StatesGroup):
    """FSM states for creating a housing search."""
    choosing_language = State()
    choosing_rental_type = State()
    entering_budget_min = State()
    entering_budget_max = State()
    entering_areas = State()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    """Initial /start command. Greets user and asks for language."""
    user_id = message.from_user.id
    logger.info("User started bot", user_id=user_id)

    async with AsyncSessionFactory() as session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            user = User(telegram_id=user_id, language=Language.EN)
            session.add(user)
            try:
                await session.flush()
                logger.info("New user registered", user_id=user_id)
            except Exception:
                await session.rollback()
                result = await session.execute(select(User).where(User.telegram_id == user_id))
                user = result.scalar_one()
        
        await session.commit()
        
        welcome_text = t("welcome_start", user.language)
        
        await state.set_state(SearchCreation.choosing_language)
        await message.answer(welcome_text, reply_markup=get_language_keyboard(), parse_mode="Markdown")


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Shows help message."""
    user_id = message.from_user.id
    async with AsyncSessionFactory() as session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        lang = user.language if user else Language.EN
        
    await message.answer(t("help_text", lang), parse_mode="Markdown")


@router.callback_query(F.data.startswith("set_lang_"), SearchCreation.choosing_language)
async def process_language_selection(callback: types.CallbackQuery, state: FSMContext):
    """Handles language selection and proceeds to rental type."""
    lang_code = callback.data.replace("set_lang_", "")
    user_id = callback.from_user.id
    
    async with AsyncSessionFactory() as session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            user.language = Language.RU if lang_code == "ru" else Language.EN
            await session.commit()
            
    lang_name = "Русский 🇷🇺" if lang_code == "ru" else "English 🇬🇧"
    
    await callback.answer(t("language_set", lang_code))
    await callback.message.edit_text(
        f"✅ {lang_name}\n\n" + t("what_looking_for", lang_code),
        reply_markup=get_rental_type_keyboard()
    )
    await state.set_state(SearchCreation.choosing_rental_type)


@router.callback_query(F.data.startswith("type_"), SearchCreation.choosing_rental_type)
async def process_rental_type(callback: types.CallbackQuery, state: FSMContext):
    """Handles rental type selection (Apartment/Room/Both). Proceed to budget."""
    rtype_str = callback.data.replace("type_", "").upper()
    await state.update_data(rental_type=rtype_str)
    
    user_id = callback.from_user.id
    async with AsyncSessionFactory() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one()
        lang = user.language

    prompt = t("budget_min_room" if rtype_str == "ROOM" else "budget_min", lang)

    await callback.message.edit_text(f"🏠 {rtype_str.title()}\n\n{prompt}", parse_mode="Markdown")
    await state.set_state(SearchCreation.entering_budget_min)


@router.message(SearchCreation.entering_budget_min)
async def process_budget_min(message: types.Message, state: FSMContext):
    """Handles minimum budget input."""
    user_id = message.from_user.id
    async with AsyncSessionFactory() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one()
        lang = user.language

    if not message.text or not message.text.isdigit():
        await message.answer(t("enter_number", lang))
        return
    
    await state.update_data(min_price=float(message.text))
    await message.answer(t("budget_max", lang), parse_mode="Markdown")
    await state.set_state(SearchCreation.entering_budget_max)


@router.message(SearchCreation.entering_budget_max)
async def process_budget_max(message: types.Message, state: FSMContext):
    """Handles maximum budget input."""
    user_id = message.from_user.id
    async with AsyncSessionFactory() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        user = result.scalar_one()
        lang = user.language

    if not message.text or not message.text.isdigit():
        await message.answer(t("enter_number", lang))
        return
    
    await state.update_data(max_price=float(message.text))
    await message.answer(t("areas_prompt", lang))
    await state.set_state(SearchCreation.entering_areas)


@router.message(SearchCreation.entering_areas)
async def process_areas(message: types.Message, state: FSMContext):
    """Saves areas and finalizes search creation."""
    areas = [a.strip() for a in (message.text or "").split(",") if a.strip()]
    user_data = await state.get_data()
    user_id = message.from_user.id
    
    async with AsyncSessionFactory() as session:
        # Find internal user ID
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
             await message.answer(t("session_lost", Language.EN))
             await state.clear()
             return

        # Create search
        new_search = UserSearch(
            user_id=user.id,
            rental_type=RentalType[user_data['rental_type']],
            min_price=user_data['min_price'],
            max_price=user_data['max_price'],
            preferred_areas=areas,
            city="Barcelona",
            is_active=True
        )
        session.add(new_search)
        await session.commit()
        lang = user.language
    
    summary = t("search_summary", lang).format(
        city="Barcelona",
        type=user_data['rental_type'].title(),
        min=user_data['min_price'],
        max=user_data['max_price'],
        areas=", ".join(areas)
    )
    
    await message.answer(t("search_created", lang), parse_mode="Markdown")
    await message.answer(summary, parse_mode="Markdown")
    await state.clear()


@router.message(Command("my_search"))
async def cmd_my_search(message: types.Message):
    """Shows the user's active search."""
    user_id = message.from_user.id
    async with AsyncSessionFactory() as session:
        # Join user to get language and to filter by telegram_id
        stmt = (
            select(UserSearch, User.language)
            .join(User)
            .where(User.telegram_id == user_id, UserSearch.is_active == True)
        )
        result = await session.execute(stmt)
        row = result.first()
        
        if not row:
            # Need to get user language separately if no search found
            user_result = await session.execute(select(User).where(User.telegram_id == user_id))
            user = user_result.scalar_one_or_none()
            lang = user.language if user else Language.EN
            await message.answer(t("no_active_search", lang))
            return
            
        search, lang = row
        summary = t("search_summary", lang).format(
            city=search.city.title(),
            type=search.rental_type.value.title(),
            min=search.min_price,
            max=search.max_price,
            areas=", ".join(search.preferred_areas or [])
        )
        await message.answer(summary, parse_mode="Markdown")


@router.message(Command("delete_me"))
async def cmd_delete_me(message: types.Message):
    """Deletes all user data (GDPR requirement)."""
    user_id = message.from_user.id
    async with AsyncSessionFactory() as session:
        stmt = select(User).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            lang = user.language
            await session.delete(user)
            await session.commit()
            await message.answer(t("delete_confirm", lang))
        else:
            await message.answer(t("not_registered", Language.EN))
