class ShortCodeEncoder:
    """Encode/decode short codes using base62."""

    # Base62 alphabet: 0-9, A-Z, a-z
    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    BASE = len(ALPHABET)
    ALPHABET_MAP = {char: i for i, char in enumerate(ALPHABET)}

    @staticmethod
    def encode(num: int) -> str:
        """Encode a number to a short code using base62."""
        if num < 0:
            raise ValueError("Number must be non-negative")

        if num == 0:
            return ShortCodeEncoder.ALPHABET[0]

        result = []
        while num > 0:
            num, remainder = divmod(num, ShortCodeEncoder.BASE)
            result.append(ShortCodeEncoder.ALPHABET[remainder])

        return "".join(reversed(result))

    @staticmethod
    def decode(short_code: str) -> int:
        """Decode a short code back to a number."""
        num = 0
        for char in short_code:
            try:
                index = ShortCodeEncoder.ALPHABET_MAP[char]
                num = num * ShortCodeEncoder.BASE + index
            except KeyError:
                raise ValueError(f"Invalid character in short code: {char}") from None

        return num


encoder = ShortCodeEncoder()