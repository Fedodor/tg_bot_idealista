"""
Handlers for user feedback on listings.
"""
from __future__ import annotations

from aiogram import Router, types, F
from sqlalchemy import insert

from app.db.models import Feedback, FeedbackType, User, Listing
from app.db.session import AsyncSessionFactory
from app.logging import get_logger

logger = get_logger(__name__)
router = Router(name="feedback")


@router.callback_query(F.data.startswith("fb_"))
async def process_feedback(callback: types.CallbackQuery):
    """
    Handles feedback button clicks.
    Format: fb_{listing_id}_{feedback_type}
    """
    parts = callback.data.split("_")
    if len(parts) < 3:
        await callback.answer("Invalid feedback data.")
        return

    listing_id = int(parts[1])
    fb_type_str = parts[2].upper()
    user_id = callback.from_user.id

    try:
        fb_type = FeedbackType[fb_type_str]
    except KeyError:
        await callback.answer("Unknown feedback type.")
        return

    async with AsyncSessionFactory() as session:
        # Find internal user ID
        from sqlalchemy import select
        stmt = select(User.id).where(User.telegram_id == user_id)
        result = await session.execute(stmt)
        internal_user_id = result.scalar_one_or_none()

        if not internal_user_id:
            await callback.answer("User not found. Please restart the bot.")
            return

        # Save feedback
        new_feedback = Feedback(
            user_id=internal_user_id,
            listing_id=listing_id,
            feedback_type=fb_type
        )
        session.add(new_feedback)
        await session.commit()

    # Friendly acknowledgement
    response_map = {
        FeedbackType.USEFUL: "Saved as useful",
        FeedbackType.NOT_RELEVANT: "Saved as not relevant",
        FeedbackType.SUSPICIOUS: "Reported as suspicious",
        FeedbackType.CONTACTED: "Great, good luck!",
        FeedbackType.HIDE_SIMILAR: "Similar listings will be hidden",
    }
    
    await callback.answer(response_map.get(fb_type, "Feedback received"))
    # We could also edit the message to remove buttons or update the UI
    logger.info("Feedback received", user_id=user_id, listing_id=listing_id, type=fb_type_str)
