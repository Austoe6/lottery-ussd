"""In-memory entry store (replace with a database when M-Pesa goes live)."""

import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Entry:
    entry_id: str
    phone_number: str
    raffle_id: str
    raffle_name: str
    prize: str
    tickets: int
    total_kes: int
    draw_date: str
    status: str = "pending_payment"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


_entries: list[Entry] = []


def create_entry(
    phone_number: str,
    raffle_id: str,
    raffle_name: str,
    prize: str,
    tickets: int,
    total_kes: int,
    draw_date: str,
) -> Entry:
    entry = Entry(
        entry_id=f"LD-{secrets.token_hex(3).upper()}",
        phone_number=phone_number,
        raffle_id=raffle_id,
        raffle_name=raffle_name,
        prize=prize,
        tickets=tickets,
        total_kes=total_kes,
        draw_date=draw_date,
        status="confirmed",
    )
    _entries.append(entry)
    return entry


def entries_for_phone(phone_number: str) -> list[Entry]:
    return [e for e in _entries if e.phone_number == phone_number]
