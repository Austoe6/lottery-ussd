"""USSD session handler for LuckyDraw lottery."""

from raffles import CATEGORIES, get_raffle
from store import create_entry, entries_for_phone

MAX_TICKETS = 10


def _main_menu() -> str:
    lines = [
        "CON Welcome to LuckyDraw Lottery",
        "Win cash, bikes, cars & more!",
        "",
        "1. Cash Prizes",
        "2. Motorbike Raffle",
        "3. Car Raffle",
        "4. Household Items",
        "5. My Entries",
    ]
    return "\n".join(lines)


def _category_menu(category_key: str) -> str:
    category = CATEGORIES[category_key]
    lines = [f"CON {category['title']}", ""]
    for i, raffle in enumerate(category["raffles"], start=1):
        lines.append(f"{i}. {raffle.name} - KES {raffle.price_kes}")
    lines.append("0. Back")
    return "\n".join(lines)


def _ticket_prompt(raffle) -> str:
    return (
        f"CON {raffle.name}\n"
        f"Prize: {raffle.prize}\n"
        f"Price: KES {raffle.price_kes}/ticket\n"
        f"Draw: {raffle.draw_date}\n"
        f"\n"
        f"Enter tickets (1-{MAX_TICKETS}):"
    )


def _confirm_prompt(raffle, tickets: int) -> str:
    total = raffle.price_kes * tickets
    return (
        f"CON Confirm purchase\n"
        f"{raffle.name}\n"
        f"{tickets} ticket(s) x KES {raffle.price_kes} = KES {total}\n"
        f"\n"
        f"1. Confirm\n"
        f"2. Cancel"
    )


def _my_entries(phone_number: str) -> str:
    entries = entries_for_phone(phone_number)
    if not entries:
        return "END You have no entries yet.\nDial again to buy a ticket!"

    lines = ["END Your entries:", ""]
    for entry in entries[-5:]:
        lines.append(f"{entry.entry_id}: {entry.raffle_name}")
        lines.append(f"  {entry.tickets} ticket(s), draw {entry.draw_date}")
    if len(entries) > 5:
        lines.append(f"...and {len(entries) - 5} more")
    return "\n".join(lines)


def handle_ussd(text: str, phone_number: str) -> str:
    """
    Route USSD input based on cumulative `text` from Africa's Talking.

    AT sends empty text on first dial, then appends each choice with *.
    Example: "" -> "1" -> "1*2" -> "1*2*3" -> "1*2*3*1"
    """
    parts = [p.strip() for p in text.split("*") if p.strip()]

    if not parts:
        return _main_menu()

    if parts[0] == "5":
        return _my_entries(phone_number)

    if parts[0] not in CATEGORIES:
        return "END Invalid option. Please dial again."

    category_key = parts[0]

    if len(parts) == 1:
        return _category_menu(category_key)

    if parts[1] == "0":
        return _main_menu()

    try:
        raffle_index = int(parts[1])
    except ValueError:
        return "END Invalid selection. Please dial again."

    raffle = get_raffle(category_key, raffle_index)
    if raffle is None:
        return "END Invalid raffle. Please dial again."

    if len(parts) == 2:
        return _ticket_prompt(raffle)

    try:
        tickets = int(parts[2])
    except ValueError:
        return f"CON Enter a number between 1 and {MAX_TICKETS}:"

    if tickets < 1 or tickets > MAX_TICKETS:
        return f"CON Invalid. Enter tickets (1-{MAX_TICKETS}):"

    if len(parts) == 3:
        return _confirm_prompt(raffle, tickets)

    if parts[3] == "2":
        return "END Purchase cancelled.\nThank you for visiting LuckyDraw!"

    if parts[3] != "1":
        return "CON Invalid option.\n1. Confirm\n2. Cancel"

    total = raffle.price_kes * tickets
    entry = create_entry(
        phone_number=phone_number,
        raffle_id=raffle.id,
        raffle_name=raffle.name,
        prize=raffle.prize,
        tickets=tickets,
        total_kes=total,
        draw_date=raffle.draw_date,
    )

    return (
        f"END Entry confirmed!\n"
        f"Ref: {entry.entry_id}\n"
        f"{raffle.name}: {tickets} ticket(s)\n"
        f"Total: KES {total}\n"
        f"Draw: {raffle.draw_date}\n"
        f"\n"
        f"(Test mode - no M-Pesa charge)\n"
        f"Good luck!"
    )
