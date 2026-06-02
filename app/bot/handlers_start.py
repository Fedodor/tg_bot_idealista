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
        
        welcome_text = (
            "🇬🇧 Welcome! I help people relocating to Spain find apartments and rooms faster.\n\n"
            "🇷🇺 Добро пожаловать! Я помогаю людям, переезжающим в Испанию, быстрее находить квартиры и комнаты.\n\n"
            "Please choose your language / Пожалуйста, выберите язык:"
        )
        
        await state.set_state(SearchCreation.choosing_language)
        await message.answer(welcome_text, reply_markup=get_language_keyboard())


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
            
    lang_name = "Русский" if lang_code == "ru" else "English"
    
    # Text for the next step
    question = "What are you looking for? / Что вы ищете?"
    
    await callback.answer(f"Language set to {lang_name}")
    await callback.message.edit_text(
        f"Language: {lang_name}\n\n{question}",
        reply_markup=get_rental_type_keyboard()
    )
    await state.set_state(SearchCreation.choosing_rental_type)


@router.callback_query(F.data.startswith("type_"), SearchCreation.choosing_rental_type)
async def process_rental_type(callback: types.CallbackQuery, state: FSMContext):
    """Handles rental type selection (Apartment/Room/Both). Proceed to budget."""
    rtype_str = callback.data.replace("type_", "").upper()
    await state.update_data(rental_type=rtype_str)
    
    prompt = "What is your MINIMUM monthly budget in EUR? (e.g. 500)"
    if rtype_str == "ROOM":
         prompt = "What is your MINIMUM monthly budget for a ROOM in EUR?"

    await callback.message.edit_text(f"Type: {rtype_str}\n\n{prompt}")
    await state.set_state(SearchCreation.entering_budget_min)


@router.message(SearchCreation.entering_budget_min)
async def process_budget_min(message: types.Message, state: FSMContext):
    """Handles minimum budget input."""
    if not message.text or not message.text.isdigit():
        await message.answer("Please enter a number (e.g. 600):")
        return
    
    await state.update_data(min_price=float(message.text))
    await message.answer("And your MAXIMUM monthly budget? (e.g. 1500)")
    await state.set_state(SearchCreation.entering_budget_max)


@router.message(SearchCreation.entering_budget_max)
async def process_budget_max(message: types.Message, state: FSMContext):
    """Handles maximum budget input."""
    if not message.text or not message.text.isdigit():
        await message.answer("Please enter a number (e.g. 1500):")
        return
    
    await state.update_data(max_price=float(message.text))
    await message.answer(
        "Which areas in Barcelona do you prefer?\n"
        "Enter area names or zip codes (e.g. Eixample, Gràcia, 08005).\n"
        "Separate with commas."
    )
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
             await message.answer("Error: User session lost. Please run /start again.")
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
    
    summary = (
        "**Search created!**\n\n"
        f"City: Barcelona\n"
        f"Type: {user_data['rental_type']}\n"
        f"Budget: {user_data['min_price']} - {user_data['max_price']} EUR\n"
        f"Areas: {', '.join(areas)}\n\n"
        "I will now start monitoring listings for you. You will receive alerts here."
    )
    
    await message.answer(summary, parse_mode="Markdown")
    await state.clear()


@router.message(Command("my_search"))
async def cmd_my_search(message: types.Message):
    """Shows the user's active search."""
    user_id = message.from_user.id
    async with AsyncSessionFactory() as session:
        stmt = select(UserSearch).join(User).where(User.telegram_id == user_id, UserSearch.is_active == True)
        result = await session.execute(stmt)
        search = result.scalar_one_or_none()
        
        if not search:
            await message.answer("You don't have an active search yet. Run /start to create one.")
            return
            
        summary = (
            "**Your Active Search**\n\n"
            f"City: {search.city.title()}\n"
            f"Type: {search.rental_type.value}\n"
            f"Budget: {search.min_price} - {search.max_price} EUR\n"
            f"Areas: {', '.join(search.preferred_areas or [])}\n"
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
            await session.delete(user)
            await session.commit()
            await message.answer("Your account and all searches have been deleted. Goodbye!")
        else:
            await message.answer("You are not registered in our system.")
