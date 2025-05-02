import pytest
from django.core.exceptions import ValidationError
from account.validators import validate_phone

class TestPhoneValidator:
    @pytest.mark.parametrize("valid_number", [
        '+998912345678',
        '+998935678901',
        '+998997654321'
    ])
    def test_valid_phone_numbers(self, valid_number):
        assert validate_phone(valid_number) is None

    @pytest.mark.parametrize("invalid_number,error_message", [
        ('998912345678', "Telefon raqam: 13 ta belgidan iborat bolishi kerak"),
        ('+99891234567', "Telefon raqam: 13 ta belgidan iborat bolishi kerak"),
        ('+992912345678', "Telefon raqam: 13 ta belgidan iborat bolishi kerak"),
        ('+abcdefghijk', "Telefon raqam: 13 ta belgidan iborat bolishi kerak"),
        (None, "Telefon raqam: 13 ta belgidan iborat bolishi kerak"),
        ('', "Telefon raqam: 13 ta belgidan iborat bolishi kerak")
    ])
    def test_invalid_phone_numbers(self, invalid_number, error_message):
        with pytest.raises(ValidationError) as excinfo:
            validate_phone(invalid_number)
        assert error_message in str(excinfo.value)