# import pytest
# from django.db import models
# from api.core.encryption.encryption_fields import EncryptedCharField

# @pytest.mark.integration
# def test_encrypted_char_field_integration(db, valid_encryption_key):
#     """Test if the encrypted field interacts correctly with the database."""
#     class TestModel(models.Model):
#         encrypted_field = EncryptedCharField(max_length=255)

#     test_obj = TestModel.objects.create(encrypted_field="Sensitive Data")
#     assert test_obj.encrypted_field != "Sensitive Data"  # Ensure data is encrypted

#     retrieved_obj = TestModel.objects.get(id=test_obj.id)
#     assert retrieved_obj.encrypted_field == "Sensitive Data"  # Ensure data can be decrypted
