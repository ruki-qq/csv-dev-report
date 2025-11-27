from pytest import raises as pt_raises

from core import convert_to_number, is_numeric


class TestIsNumeric:
    """Tests for is_numeric function."""

    def test_is_numeric_with_integer_string(self):
        assert is_numeric("42") is True
        assert is_numeric("0") is True
        assert is_numeric("100") is True

    def test_is_numeric_with_float_string(self):
        assert is_numeric("3.14") is True
        assert is_numeric("0.5") is True
        assert is_numeric("99.99") is True

    def test_is_numeric_with_negative_numbers(self):
        assert is_numeric("-10") is True
        assert is_numeric("-3.14") is True
        assert is_numeric("-0.5") is True

    def test_is_numeric_with_zero(self):
        assert is_numeric("0") is True
        assert is_numeric("0.0") is True
        assert is_numeric("-0") is True

    def test_is_numeric_with_non_numeric_string(self):
        assert is_numeric("abc") is False
        assert is_numeric("hello") is False
        assert is_numeric("test123") is False

    def test_is_numeric_with_empty_string(self):
        assert is_numeric("") is False

    def test_is_numeric_with_whitespace(self):
        assert is_numeric("  ") is False
        assert is_numeric("\n") is False
        assert is_numeric("\t") is False

    def test_is_numeric_with_special_characters(self):
        assert is_numeric("$100") is False
        assert is_numeric("10%") is False
        assert is_numeric("#5") is False

    def test_is_numeric_with_mixed_content(self):
        """Test with mixed numeric and non-numeric."""

        assert is_numeric("123abc") is False
        assert is_numeric("12.34.56") is False
        assert is_numeric("1 2 3") is False

    def test_is_numeric_with_actual_numbers(self):
        assert is_numeric(42) is True
        assert is_numeric(3.14) is True
        assert is_numeric(-10) is True


class TestConvertToNumber:
    """Tests for convert_to_number function."""

    def test_convert_integer_string(self):
        result = convert_to_number("42")

        assert result == 42
        assert isinstance(result, int)

    def test_convert_float_string(self):
        result = convert_to_number("3.14")

        assert result == 3.14
        assert isinstance(result, float)

    def test_convert_zero(self):
        result = convert_to_number("0")

        assert result == 0
        assert isinstance(result, int)

    def test_convert_negative_integer(self):
        result = convert_to_number("-10")

        assert result == -10
        assert isinstance(result, int)

    def test_convert_negative_float(self):
        result = convert_to_number("-2.5")

        assert result == -2.5
        assert isinstance(result, float)

    def test_convert_large_numbers(self):
        result = convert_to_number("1000000")
        assert result == 1000000
        assert isinstance(result, int)

        result = convert_to_number("999.999")
        assert result == 999.999
        assert isinstance(result, float)

    def test_convert_small_decimals(self):
        result = convert_to_number("0.001")

        assert result == 0.001
        assert isinstance(result, float)

    def test_convert_invalid_string_raises_error(self):
        """Test that invalid string raises ValueError."""

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("abc")

    def test_convert_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("")

    def test_convert_whitespace_raises_error(self):
        """Test that whitespace raises ValueError."""

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("   ")

    def test_convert_special_characters_raises_error(self):
        """Test that special characters raise ValueError."""

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("$100")

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("10%")

    def test_convert_mixed_content_raises_error(self):
        """Test that mixed content raises ValueError."""

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("123abc")

        with pt_raises(ValueError, match="Cannot convert value"):
            convert_to_number("12.34.56")

    def test_convert_preserves_type_int(self):
        """Test that integers without decimal point return int."""

        result = convert_to_number("100")
        assert isinstance(result, int)

    def test_convert_preserves_type_float(self):
        """Test that numbers with decimal point return float."""

        result = convert_to_number("100.0")
        assert isinstance(result, float)
