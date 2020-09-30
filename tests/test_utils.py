from django.test import TestCase

from drfaddons.utils import validate_email
from drfaddons.utils import validate_mobile


class TestUtils(TestCase):
    def test_validate_email(self):
        valid_email = "user@django.com"
        invalid_email = "user"

        self.assertTrue(validate_email(valid_email))
        self.assertFalse(validate_email(invalid_email))

    def test_validate_mobile(self):
        valid_mobile = "1234567890"
        invalid_mobile = "1234567"

        self.assertTrue(validate_mobile(valid_mobile))
        self.assertFalse(validate_mobile(invalid_mobile))
