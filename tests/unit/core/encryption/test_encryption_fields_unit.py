# import pytest
# from api.core.encryption.encryption_fields import EncryptedCharField

# @pytest.mark.unit
# def test_encrypted_char_field_init(valid_encryption_key):
#     """Test if the encryption key is correctly validated during initialization."""
#     field = EncryptedCharField(max_length=255)
#     assert field.key is not None

# @pytest.mark.unit
# def test_encryption_failure(encrypted_char_field):
#     """Test the encryption failure case."""
#     with pytest.raises(ValueError):
#         encrypted_char_field.get_prep_value(None)

# @pytest.mark.unit
# def test_decryption_failure(encrypted_char_field):
#     """Test the decryption failure case."""
#     with pytest.raises(ValueError):
#         encrypted_char_field.from_db_value(None, None, None)
