"""Local USSD flow tests without Africa's Talking."""

from ussd_handler import handle_ussd

PHONE = "+254712345678"


def simulate(steps: list[str]) -> None:
    print(f"\n--- Flow: {' -> '.join(steps) or 'initial dial'} ---")
    if not steps:
        print("text=''")
        print(handle_ussd("", PHONE))
        print()
        return
    for i in range(len(steps)):
        text = "*".join(steps[: i + 1])
        response = handle_ussd(text, PHONE)
        print(f"text={text!r}")
        print(response)
        print()


def main() -> None:
    simulate([])
    simulate(["1"])
    simulate(["1", "1"])
    simulate(["1", "1", "2"])
    simulate(["1", "1", "2", "1"])
    simulate(["5"])


if __name__ == "__main__":
    main()
