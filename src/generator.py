import random
import string
from typing import Literal

from faker import Faker

fake = Faker()

CompressibilityType = Literal["incompressible", "maximally", "lipsum"]


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


def generate_payload(bytes_target: int, compressibility: CompressibilityType) -> str:
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
        case "incompressible":
            return _make_incompressible(bytes_target)
        case "maximally":
            return _make_maximally(bytes_target)
        case "lipsum":
            return _make_lipsum(bytes_target)
        case _:
            raise ValueError(f"Invalid compressibility type: {compressibility}")


def _make_incompressible(bytes_target: int) -> str:
    """Generate incompressible random data.

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
    return result
