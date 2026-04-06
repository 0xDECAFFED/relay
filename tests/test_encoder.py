import pytest

from app.core.encoder import encoder


class TestShortCodeEncoder:
    """Test cases for the short code encoder (base62)."""

    def test_encode_zero(self):
        """Test encoding of zero."""
        assert encoder.encode(0) == "0"

    def test_encode_small_number(self):
        """Test encoding of small numbers."""
        result = encoder.encode(1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_encode_large_number(self):
        """Test encoding of large numbers."""
        result = encoder.encode(999999999)
        assert isinstance(result, str)
        # Base62 should be shorter than decimal representation
        assert len(result) < len("999999999")

    def test_encode_roundtrip(self):
        """Test that encoding and decoding roundtrip correctly."""
        test_values = [0, 1, 100, 9999, 999999999, 1234567890]
        for value in test_values:
            encoded = encoder.encode(value)
            decoded = encoder.decode(encoded)
            assert decoded == value

    def test_decode_invalid_code(self):
        """Test decoding of invalid short codes."""
        with pytest.raises(ValueError):
            encoder.decode("!!!")

    def test_decode_empty_string(self):
        """Test decoding empty string."""
        result = encoder.decode("")
        assert result == 0

    def test_consistent_encoding(self):
        """Test that encoding the same number produces the same result."""
        num = 12345
        encoded1 = encoder.encode(num)
        encoded2 = encoder.encode(num)
        assert encoded1 == encoded2

    def test_base62_alphabet(self):
        """Test that output only contains base62 characters."""
        result = encoder.encode(123456789)
        valid_chars = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        assert all(c in valid_chars for c in result)