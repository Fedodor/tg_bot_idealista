"""
AI Analysis service for listings using a local LLM via Ollama.

Extracts structured data, risks, and red flags from listing descriptions.
"""
from __future__ import annotations

import httpx
import json
import re
from typing import Any, Literal
from pydantic import BaseModel, Field

from app.config import settings
from app.logging import get_logger

logger = get_logger(__name__)

# Pydantic model for LLM output validation (Task 6.15)
class ListingAnalysisSchema(BaseModel):
    summary: str = Field(description="One sentence summary of the listing")
    rental_type: Literal["apartment", "room", "unknown"]
    contract_type: Literal["long-term", "temporary", "unknown"]
    empadronamiento: Literal["possible", "not possible", "unknown"]
    risk_level: Literal["low", "medium", "high"] = Field(description="Risk of scam or bad conditions")
    red_flags: list[str] = Field(default_factory=list, description="Specific suspicious points")
    positive_signals: list[str] = Field(default_factory=list, description="Points that build trust")
    questions_to_ask: list[str] = Field(default_factory=list, description="Key questions for the landlord")
    explanation: str = Field(description="Reasoning for the risk level")


class AIAnalysisService:
    """Service to interact with Ollama for listing analysis."""

    def __init__(self, base_url: str | None = None, model: str | None = None) -> None:
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.num_gpu = self._detect_gpu_setting()

    def _detect_gpu_setting(self) -> int:
        """Determines num_gpu based on settings and system presence."""
        if settings.ollama_num_gpu >= 0:
            return settings.ollama_num_gpu
        
        # Auto-detect (-1)
        import subprocess
        try:
            subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            logger.info("NVIDIA GPU detected, using GPU for Ollama")
            return -1 # -1 means auto in Ollama options
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.info("No NVIDIA GPU found, forcing CPU-only for Ollama")
            return 0

    async def analyze_listing(self, listing_text: str, language: str = "en") -> ListingAnalysisSchema | None:
        """
        Sends listing text to LLM and returns validated JSON analysis.
        """
        # 1. Privacy: Strip phone numbers and emails (Task 6.12)
        safe_text = self._strip_PII(listing_text)
        
        # 2. Build Prompt (Task 6.9/6.11)
        prompt = self._build_prompt(safe_text, language)
        
        # 3. Call Ollama (Task 6.6/6.7)
        # Apply timeout from settings (default 90s)
        timeout = float(settings.ai_analysis_timeout_seconds) if settings.ai_analysis_timeout_seconds > 0 else 120.0
        
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "format": "json",
                        "options": {
                            "num_gpu": self.num_gpu
                        }
                    }
                )
                response.raise_for_status()
                result_json = response.json().get("response", "{}")
                
                # 4. Parse and Validate (Task 6.14/6.15)
                data = json.loads(result_json)
                return ListingAnalysisSchema(**data)
                
        except Exception as e:
            logger.error("AI analysis failed", error=f"{type(e).__name__}: {str(e)}", model=self.model)
            return None

    def _strip_PII(self, text: str) -> str:
        """Removes emails and phone numbers from text."""
        # Simple regex for email
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL]', text)
        # Simple regex for phone numbers (Spanish format + variants)
        text = re.sub(r'\+?\d{1,3}[\s-]?\d{3}[\s-]?\d{3,6}', '[PHONE]', text)
        return text

    def _build_prompt(self, text: str, language: str) -> str:
        """Constructs the system prompt for the LLM."""
        target_lang = "Russian" if language == "ru" else "English"
        return f"""
Analyze the following rental listing description and provide a structured JSON analysis in {target_lang}.
Return ONLY the JSON object. Do not include any introductory text.

Rules:
- Be objective. If a fact is missing, mark as 'unknown'.
- Do not invent facts.
- Identify red flags (e.g., 'no visits allowed', 'payment in advance via Western Union', 'whatsapp only').
- Assess risk level based on signals.

JSON Schema:
{{
  "summary": "...",
  "rental_type": "apartment|room|unknown",
  "contract_type": "long-term|temporary|unknown",
  "empadronamiento": "possible|not possible|unknown",
  "risk_level": "low|medium|high",
  "red_flags": ["...", "..."],
  "positive_signals": ["...", "..."],
  "questions_to_ask": ["...", "..."],
  "explanation": "..."
}}

Listing text:
\"\"\"{text}\"\"\"
"""
