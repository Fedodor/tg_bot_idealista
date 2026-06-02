"""
Dry Run Demo — See the logic in action without a working database.
Compatible with Windows console (no emojis).
"""
import asyncio
from dataclasses import dataclass
from typing import List

@dataclass
class MockListing:
    title: str
    price: float
    city: str
    rental_type: str
    district: str
    description: str
    url: str = "https://example.com/listing/123"

@dataclass
class MockSearch:
    city: str
    max_price: float
    rental_type: str
    preferred_areas: List[str]

async def run_demo():
    print("*** --- Relocation Rental Radar: DRY RUN DEMO --- ***\n")
    
    # 1. SAMPLE INPUT
    listing = MockListing(
        title="Modern Apartment in Gracia",
        price=950.0,
        city="Barcelona",
        rental_type="apartment",
        district="Gracia",
        description="Beautiful 2-bedroom flat. No visits allowed before payment. Long-term contract.",
    )
    print(f"-> [Ingested] {listing.title} ({listing.price} EUR)")

    # 2. MATCHING LOGIC
    search = MockSearch(
        city="Barcelona",
        max_price=1000.0,
        rental_type="apartment",
        preferred_areas=["Gracia", "Eixample"]
    )
    
    passed = listing.city == search.city and listing.price <= search.max_price
    print(f"-> [Matching] Listing passed hard filters: {passed}")

    # 3. SCORING LOGIC
    score = 40 
    reasons = []
    if listing.price <= search.max_price * 0.8: score += 30; reasons.append("Great budget fit")
    elif listing.price <= search.max_price: score += 15; reasons.append("Fits budget")
    if listing.district in search.preferred_areas: score += 15; reasons.append("Preferred area")
    
    print(f"-> [Scoring] Final Score: {score}/100. Reasons: {', '.join(reasons)}")

    # 4. AI ANALYSIS
    risk_level = "high"
    red_flags = ["No visits allowed before payment (Classic scam sign)"]
    print(f"-> [AI Analysis] Risk: {risk_level.upper()}. Flags: {red_flags[0]}")

    # 5. TELEGRAM FORMATTING
    print("\n--- TELEGRAM ALERT PREVIEW (ENGLISH) ---")
    print(f"**New Rental Match**\n")
    print(f"EUR {listing.price:,.0f} / month")
    print(f"{listing.rental_type.title()} in {listing.district}\n")
    print(f"Match: {score}/100 (Good)")
    print(f"Risk: {risk_level.upper()}\n")
    print(f"**Why it matches:**")
    for r in reasons: print(f" - {r}")
    print(f"Attention: {red_flags[0]}")
    
    print("\n--- TELEGRAM ALERT PREVIEW (RUSSIAN) ---")
    print(f"**Новое предложение**\n")
    print(f"EUR {listing.price:,.0f} / мес")
    print(f"Квартира в районе {listing.district}\n")
    print(f"Совпадение: {score}/100\n")
    print(f"**Почему подходит:**")
    print(" - Хорошая цена\n - Подходящий район")
    print(f"Внимание: Осмотр невозможен до оплаты (Признак мошенничества)")
    print("\n[Open] [Useful] [Not relevant] [Suspicious]")

if __name__ == "__main__":
    asyncio.run(run_demo())
