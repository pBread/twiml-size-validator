from typing import Literal
import random
import string

from faker import Faker

fake = Faker()


def escape_xml(text: str) -> str:

    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def get_byte_length(text: str) -> int:
    return len(text.encode("utf-8"))


def generate_payload(bytes_target: int, compressibility: str) -> str:
    """Generate a payload of the specified byte length and compressibility type.

    Args:
        bytes_target: Target size in bytes
        compressibility: Type of payload to generate

    Returns:
        Generated payload string

    Raises:
        ValueError: If compressibility type is invalid
    """
    match compressibility:
        case "random":
            return _make_random(bytes_target)
        case "maximally":
            return _make_maximally(bytes_target)
        case "lipsum":
            return _make_lipsum(bytes_target)
        case _:
            raise ValueError(f"Invalid compressibility type: {compressibility}")


def _make_random(bytes_target: int) -> str:
    """Generate random random data.

    Args:
        bytes_target: Target size in bytes

    Returns:
        Random string from 64-character alphabet
    """
    alphabet = string.ascii_letters + string.digits + "-_"

    result = ""
    for _ in range(bytes_target):
        result += random.choice(alphabet)

    return result


def _make_maximally(bytes_target: int) -> str:
    """Generate maximally compressible data (repeated pattern).

    Args:
        bytes_target: Target size in bytes

    Returns:
        Repeated 'A' pattern
    """
    return "A" * bytes_target


def _make_lipsum(bytes_target: int) -> str:
    """Generate realistic mixed content with moderate compressibility.

    Args:
        bytes_target: Target size in bytes

    Returns:
        Mixed realistic content
    """
    result = ""
    current_bytes = 0

    # Product categories and adjectives for commerce-like data
    products = [
        "Laptop",
        "Smartphone",
        "Headphones",
        "Camera",
        "Tablet",
        "Watch",
        "Speaker",
        "Monitor",
    ]
    adjectives = [
        "premium",
        "affordable",
        "innovative",
        "reliable",
        "sleek",
        "powerful",
        "compact",
        "professional",
    ]

    while current_bytes < bytes_target:
        chunk = ""
        content_type = random.random()

        if content_type < 0.3:
            # Lorem ipsum style sentences
            chunk = f"{fake.sentence()} "
        elif content_type < 0.5:
            # Product information
            product = random.choice(products)
            adjective = random.choice(adjectives)
            price = f"${random.randint(50, 2000)}.{random.randint(0, 99):02d}"
            chunk = f"{product} is {adjective} and costs {price}. "
        elif content_type < 0.7:
            # Person profiles
            chunk = (
                f"{fake.name()} from {fake.city()}, "
                f"{fake.country()} works as a {fake.job()}. "
            )
        else:
            # Company announcements
            words = " ".join(fake.words(5))
            recent_date = fake.date_between(start_date="-30d", end_date="today")
            chunk = (
                f"On {recent_date.strftime('%a %b %d %Y')}, "
                f"{fake.company()} announced {words}. "
            )

        chunk = escape_xml(chunk)
        chunk_bytes = get_byte_length(chunk)

        # If adding this chunk would exceed target, trim it to fit exactly
        if current_bytes + chunk_bytes > bytes_target:
            remaining_bytes = bytes_target - current_bytes
            # Find the longest substring that fits
            for i in range(len(chunk), 0, -1):
                trimmed = chunk[:i]
                if get_byte_length(trimmed) <= remaining_bytes:
                    result += trimmed
                    current_bytes = bytes_target  # We're done
                    break
            break
        else:
            result += chunk
            current_bytes += chunk_bytes

    return result
