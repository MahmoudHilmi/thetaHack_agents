"""Persistent decision memory built on SQLAlchemy."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import Float, Integer, String, Text, create_engine, select
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    """Base class for ORACLE memory database models."""


class DecisionMemoryEntry(Base):
    """Database record for a completed ORACLE decision."""

    __tablename__ = "decision_memory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    memory_scope: Mapped[str] = mapped_column(String(100), index=True)
    problem_description: Mapped[str] = mapped_column(Text)
    user_input: Mapped[str] = mapped_column(Text, default="")
    final_decision: Mapped[str] = mapped_column(Text)
    decision_reasoning: Mapped[str] = mapped_column(Text)
    final_confidence: Mapped[float] = mapped_column(Float)
    analyses_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column()


@dataclass(frozen=True)
class MemoryMatch:
    """A prior decision selected as useful context."""

    problem_description: str
    final_decision: str
    decision_reasoning: str
    final_confidence: float
    score: float


class DecisionMemory:
    """Store completed decisions and retrieve related decisions within a scope."""

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self.engine = self._create_engine(database_url)

    def initialize(self) -> None:
        """Create the memory tables when they do not already exist."""
        Base.metadata.create_all(self.engine)

    def is_ready(self) -> bool:
        """Return whether the configured database can be reached."""
        try:
            with self.engine.connect():
                return True
        except Exception:
            return False

    def store(
        self,
        *,
        memory_scope: str,
        problem_description: str,
        user_input: str,
        final_decision: str,
        decision_reasoning: str,
        final_confidence: float,
        analyses: dict[str, str],
    ) -> None:
        """Persist one successful decision for later retrieval."""
        entry = DecisionMemoryEntry(
            memory_scope=memory_scope,
            problem_description=problem_description,
            user_input=user_input,
            final_decision=final_decision,
            decision_reasoning=decision_reasoning,
            final_confidence=final_confidence,
            analyses_json=json.dumps(analyses, ensure_ascii=False),
            created_at=datetime.now(UTC),
        )
        with Session(self.engine) as session:
            session.add(entry)
            session.commit()

    def find_relevant(
        self, *, memory_scope: str, problem_description: str, user_input: str, limit: int = 3
    ) -> list[MemoryMatch]:
        """Return the most textually related decisions in the same memory scope."""
        query_tokens = self._tokens(f"{problem_description} {user_input}")
        if not query_tokens:
            return []

        statement = (
            select(DecisionMemoryEntry)
            .where(DecisionMemoryEntry.memory_scope == memory_scope)
            .order_by(DecisionMemoryEntry.id.desc())
            .limit(200)
        )
        with Session(self.engine) as session:
            entries = session.scalars(statement).all()

        matches = []
        for entry in entries:
            score = self._similarity(query_tokens, self._tokens(entry.problem_description))
            if score >= 0.12:
                matches.append(
                    MemoryMatch(
                        problem_description=entry.problem_description,
                        final_decision=entry.final_decision,
                        decision_reasoning=entry.decision_reasoning,
                        final_confidence=entry.final_confidence,
                        score=score,
                    )
                )
        return sorted(matches, key=lambda match: match.score, reverse=True)[:limit]

    @staticmethod
    def format_context(matches: list[MemoryMatch]) -> str:
        """Format previous decisions as non-authoritative context for agents."""
        if not matches:
            return ""
        entries = []
        for index, match in enumerate(matches, start=1):
            entries.append(
                f"Previous decision {index} (similarity {match.score:.0%}):\n"
                f"Problem: {match.problem_description}\n"
                f"Decision: {match.final_decision}\n"
                f"Reasoning: {match.decision_reasoning[:700]}"
            )
        return (
            "Relevant previous ORACLE decisions are below. Use them only as historical "
            "context; independently assess the current request and correct any weak past reasoning.\n\n"
            + "\n\n".join(entries)
        )

    @staticmethod
    def _create_engine(database_url: str) -> Engine:
        url = make_url(database_url)
        if url.drivername == "sqlite" and url.database and url.database != ":memory:":
            Path(url.database).parent.mkdir(parents=True, exist_ok=True)
        connect_args = {"check_same_thread": False} if url.drivername == "sqlite" else {}
        return create_engine(database_url, connect_args=connect_args)

    @staticmethod
    def _tokens(value: str) -> set[str]:
        normalized = unicodedata.normalize("NFKD", value.lower())
        normalized = "".join(char for char in normalized if not unicodedata.combining(char))
        return {token for token in re.findall(r"[^\W_]+", normalized, flags=re.UNICODE) if len(token) > 1}

    @staticmethod
    def _similarity(left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return len(left & right) / len(left | right)
