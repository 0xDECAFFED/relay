import base64
import binascii


class ShortCodeEncoder:
    """Encode/decode short codes using base64."""

    @staticmethod
    def encode(num: int) -> str:
        """Encode a number to a short code using base64."""
        if num < 0:
            raise ValueError("Number must be non-negative")

        # Convert number to bytes, then to base64
        num_bytes = num.to_bytes((num.bit_length() + 7) // 8, byteorder="big")
        encoded = base64.urlsafe_b64encode(num_bytes).decode("utf-8")

        # Remove padding
        return encoded.rstrip("=")

    @staticmethod
    def decode(short_code: str) -> int:
        """Decode a short code back to a number."""
        # Add padding if needed
        padding = 4 - (len(short_code) % 4)
        if padding != 4:
            short_code += "=" * padding

        # Decode from base64
        try:
            num_bytes = base64.urlsafe_b64decode(short_code)
            return int.from_bytes(num_bytes, byteorder="big")
        except (binascii.Error, ValueError) as e:
            raise ValueError(f"Invalid short code: {short_code}") from e


encoder = ShortCodeEncoder()