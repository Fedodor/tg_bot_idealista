"""
All SQLAlchemy ORM models.

Rules (from AGENTS.md §5):
  - All 7 required tables must exist: users, user_searches, listings,
    listing_analysis, matches, notifications, feedback.
  - All column names snake_case.
  - All PKs are integer auto-increment.
  - created_at always uses server_default=func.now().
  - Unique constraints enforced at DB level.
  - No business logic here — data models only.
"""
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Shared declarative base for all models."""
    pass


# ─── Enums ────────────────────────────────────────────────────────────────────

class Language(str, enum.Enum):
    EN = "en"
    RU = "ru"


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class UserPlan(str, enum.Enum):
    FREE = "free"
    BETA = "beta"
    PRO = "pro"


class RentalType(str, enum.Enum):
    APARTMENT = "apartment"
    ROOM = "room"
    BOTH = "both"
    UNKNOWN = "unknown"


class ListingStatus(str, enum.Enum):
    ACTIVE = "active"
    REMOVED = "removed"
    UNKNOWN = "unknown"


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ContractType(str, enum.Enum):
    LONG_TERM = "long_term"
    TEMPORADA = "temporada"
    UNKNOWN = "unknown"


class EmpadronamientoStatus(str, enum.Enum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


class FeedbackType(str, enum.Enum):
    USEFUL = "useful"
    NOT_RELEVANT = "not_relevant"
    SUSPICIOUS = "suspicious"
    CONTACTED = "contacted"
    HIDE_SIMILAR = "hide_similar"


class NotificationStatus(str, enum.Enum):
    SENT = "sent"
    FAILED = "failed"
    PENDING = "pending"


# ─── Models ───────────────────────────────────────────────────────────────────

class User(Base):
    """
    A Telegram user who has started the bot.

    telegram_id is the unique Telegram user ID (int64).
    consent_at must be set before creating any UserSearch (privacy rule).
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    language: Mapped[Language] = mapped_column(
        Enum(Language, name="language_enum"), nullable=False, default=Language.EN
    )
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus, name="user_status_enum"), nullable=False, default=UserStatus.ACTIVE
    )
    plan: Mapped[UserPlan] = mapped_column(
        Enum(UserPlan, name="user_plan_enum"), nullable=False, default=UserPlan.FREE
    )
    consent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    searches: Mapped[list["UserSearch"]] = relationship("UserSearch", back_populates="user", cascade="all, delete-orphan")
    matches: Mapped[list["Match"]] = relationship("Match", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    feedback: Mapped[list["Feedback"]] = relationship("Feedback", back_populates="user", cascade="all, delete-orphan")


class UserSearch(Base):
    """
    A user's saved search / filter profile.

    preferred_areas and must_have/nice_to_have are stored as JSONB arrays.
    """
    __tablename__ = "user_searches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="barcelona")
    rental_type: Mapped[RentalType] = mapped_column(
        Enum(RentalType, name="rental_type_enum"), nullable=False, default=RentalType.BOTH
    )
    min_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    max_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    min_rooms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    preferred_areas: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    excluded_areas: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    keywords: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    must_have: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    nice_to_have: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="searches")
    matches: Mapped[list["Match"]] = relationship("Match", back_populates="search", cascade="all, delete-orphan")


class Listing(Base):
    """
    A normalized rental listing from any source.

    dedup_hash is SHA-256 of (price + city + area_m2 + title).
    raw_data stores the original source payload.
    """
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)          # e.g. "manual_import"
    external_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="EUR")
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    district: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    neighborhood: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    address_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rental_type: Mapped[RentalType] = mapped_column(
        Enum(RentalType, name="listing_rental_type_enum"), nullable=False, default=RentalType.UNKNOWN
    )
    area_m2: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    rooms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bathrooms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    floor: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    has_elevator: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    is_furnished: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    agency_or_private: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    available_from: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    status: Mapped[ListingStatus] = mapped_column(
        Enum(ListingStatus, name="listing_status_enum"), nullable=False, default=ListingStatus.ACTIVE
    )
    dedup_hash: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True, index=True)

    # Relationships
    analysis: Mapped[Optional["ListingAnalysis"]] = relationship(
        "ListingAnalysis", back_populates="listing", uselist=False, cascade="all, delete-orphan"
    )
    matches: Mapped[list["Match"]] = relationship("Match", back_populates="listing", cascade="all, delete-orphan")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="listing", cascade="all, delete-orphan")
    feedback: Mapped[list["Feedback"]] = relationship("Feedback", back_populates="listing", cascade="all, delete-orphan")


class ListingAnalysis(Base):
    """
    AI-generated analysis for a listing.

    One analysis per listing — shared across all users.
    model_name and analysis_version are stored for audit purposes.
    """
    __tablename__ = "listing_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    listing_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, unique=True, index=True
    )
    summary_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    summary_ru: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    risk_level: Mapped[Optional[RiskLevel]] = mapped_column(
        Enum(RiskLevel, name="risk_level_enum"), nullable=True
    )
    red_flags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    positive_signals: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    questions_to_ask: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    contract_type: Mapped[Optional[ContractType]] = mapped_column(
        Enum(ContractType, name="contract_type_enum"), nullable=True
    )
    empadronamiento_possible: Mapped[Optional[EmpadronamientoStatus]] = mapped_column(
        Enum(EmpadronamientoStatus, name="empadronamiento_enum"), nullable=True
    )
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    analysis_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    listing: Mapped["Listing"] = relationship("Listing", back_populates="analysis")


class Match(Base):
    """
    A match between a user search and a listing.

    unique(user_id, listing_id) prevents duplicate matches.
    """
    __tablename__ = "matches"
    __table_args__ = (
        UniqueConstraint("user_id", "listing_id", name="uq_match_user_listing"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    search_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("user_searches.id", ondelete="SET NULL"), nullable=True)
    match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reason_en: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reason_ru: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    should_notify: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="matches")
    listing: Mapped["Listing"] = relationship("Listing", back_populates="matches")
    search: Mapped[Optional["UserSearch"]] = relationship("UserSearch", back_populates="matches")


class Notification(Base):
    """
    A record of a Telegram alert sent to a user about a listing.

    Checked before sending to prevent duplicate alerts.
    """
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    match_id: Mapped[int] = mapped_column(Integer, ForeignKey("matches.id", ondelete="CASCADE"), nullable=False, index=True)
    telegram_message_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[NotificationStatus] = mapped_column(
        Enum(NotificationStatus, name="notification_status_enum"),
        nullable=False,
        default=NotificationStatus.PENDING,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")
    listing: Mapped["Listing"] = relationship("Listing", back_populates="notifications")


class Feedback(Base):
    """
    User feedback on a listing (useful, not relevant, suspicious, etc.)
    """
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False, index=True)
    feedback_type: Mapped[FeedbackType] = mapped_column(
        Enum(FeedbackType, name="feedback_type_enum"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="feedback")
    listing: Mapped["Listing"] = relationship("Listing", back_populates="feedback")
