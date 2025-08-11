"""Main application for TwiML payload size testing."""

from generator import generate_payload, get_byte_length


def main():

    # Test different payload types
    test_configs = [
        ("random", 1000),
        ("maximally", 1000),
        ("lipsum", 1000),
    ]

    print("TwiML Payload Generator Test")
    print("=" * 40)

    for compressibility, size in test_configs:
        print(f"\nTesting {compressibility} payload ({size} bytes):")
        print("-" * 30)

        payload = generate_payload(size, compressibility)
        actual_size = get_byte_length(payload)

        print(f"Target size: {size} bytes")
        print(f"Actual size: {actual_size} bytes")
        print(f"Preview: {payload[:100]}{'...' if len(payload) > 100 else ''}")

        if compressibility == "lipsum":
            print(
                f"Full content preview:\n{payload[:500]}{'...' if len(payload) > 500 else ''}"
            )


if __name__ == "__main__":
    main()
