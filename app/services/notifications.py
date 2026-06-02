"""
Notification service for Telegram alerts.

Formats and sends listing matches to users.
Includes AI Analysis results if available.
"""
from __future__ import annotations

from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.db.models import Match, Listing, User, Notification, Language
from app.db.session import AsyncSessionFactory
from app.logging import get_logger

logger = get_logger(__name__)


async def send_listing_alert(bot: Bot, match: Match, listing: Listing, user: User) -> bool:
    """
    Formats and sends a 1-to-1 alert for a specific match.
    """
    # 1. Format text based on user language
    if user.language == Language.RU:
        text = _format_ru(match, listing)
        btn_useful = "👍 Полезно"
        btn_not_rel = "👎 Не актуально"
        btn_scam = "🚩 Подозрительно"
        btn_open = "🔗 Открыть"
    else:
        text = _format_en(match, listing)
        btn_useful = "👍 Useful"
        btn_not_rel = "👎 Not relevant"
        btn_scam = "🚩 Suspicious"
        btn_open = "🔗 Open Listing"

    # 2. Build keyboard
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=btn_open, url=listing.url))
    builder.row(
        types.InlineKeyboardButton(text=btn_useful, callback_data=f"fb_{listing.id}_useful"),
        types.InlineKeyboardButton(text=btn_not_rel, callback_data=f"fb_{listing.id}_not_relevant")
    )
    builder.row(types.InlineKeyboardButton(text=btn_scam, callback_data=f"fb_{listing.id}_suspicious"))

    # 3. Send message
    try:
        msg = await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            reply_markup=builder.as_markup(),
            parse_mode="Markdown"
        )
        
        # 4. Record notification in DB
        async with AsyncSessionFactory() as session:
            session.add(Notification(
                user_id=user.id,
                listing_id=listing.id,
                match_id=match.id,
                telegram_message_id=msg.message_id,
                sent_at=msg.date
            ))
            await session.commit()
            
        logger.info("Alert sent", user_id=user.telegram_id, listing_id=listing.id)
        return True
    except Exception as e:
        logger.error("Failed to send alert", user_id=user.telegram_id, error=str(e))
        return False


def _format_en(match: Match, listing: Listing) -> str:
    """English alert template with AI section."""
    reasons = match.reason_en.split(", ") if match.reason_en else ["Matched your core filters"]
    reasons_fmt = "\n".join([f"• {r}" for r in reasons])
    
    output = (
        f"**New Rental Match**\n\n"
        f"EUR {listing.price:,.0f} / month\n"
        f"{listing.rental_type.title()} in {listing.district or 'Barcelona'}\n\n"
        f"Match: {match.match_score}/100\n\n"
        f"**Why it matches:**\n"
        f"{reasons_fmt}\n\n"
    )

    # Add AI Section (Task 6.16)
    if listing.analysis:
        analysis = listing.analysis
        risk = (analysis.risk_level.value if analysis.risk_level else "unknown").upper()
        summary = analysis.summary_en or "Analysis complete."
        output += f"**AI Analysis ({risk} RISK)**\n"
        output += f"_{summary}_\n\n"
        if analysis.red_flags:
            flags = "\n".join([f"🚩 {f}" for f in analysis.red_flags])
            output += f"**Red Flags:**\n{flags}\n"
    else:
        output += f"_AI Analysis pending..._"

    return output


def _format_ru(match: Match, listing: Listing) -> str:
    """Russian alert template with AI section."""
    reasons_en = match.reason_en.split(", ") if match.reason_en else ["Подходит под ваши фильтры"]
    reason_map = {
        "Great price for your budget": "Отличная цена для вашего бюджета",
        "Fits your budget": "Подходит по бюджету",
        "In your preferred area": "В предпочитаемом районе",
        "Furnished": "С мебелью",
        "Very short description": "Очень короткое описание"
    }
    reasons_fmt = "\n".join([f"• {reason_map.get(r, r)}" for r in reasons_en])
    rtype = "Квартира" if listing.rental_type == "apartment" else "Комната"
    
    output = (
        f"**Новое предложение**\n\n"
        f"EUR {listing.price:,.0f} / мес\n"
        f"{rtype} в {listing.district or 'Барселоне'}\n\n"
        f"Совпадение: {match.match_score}/100\n\n"
        f"**Почему подходит:**\n"
        f"{reasons_fmt}\n\n"
    )

    # Add AI Section
    if listing.analysis:
        analysis = listing.analysis
        risk_map = {"low": "НИЗКИЙ", "medium": "СРЕДНИЙ", "high": "ВЫСОКИЙ"}
        risk = risk_map.get(analysis.risk_level.value if analysis.risk_level else "unknown", "НЕИЗВЕСТНО")
        summary = analysis.summary_ru or "Анализ завершен."
        output += f"**AI Анализ (РИСК: {risk})**\n"
        output += f"_{summary}_\n\n"
        if analysis.red_flags:
            flags = "\n".join([f"🚩 {f}" for f in analysis.red_flags])
            output += f"**Внимание:**\n{flags}\n"
    else:
        output += f"_AI Анализ в процессе..._"

    return output
