# import pytest
# from api.core.encryption.encryption_fields import EncryptedCharField
# from django.db import models

# @pytest.mark.factory
# def test_factory_usage():
#     """Test creating instances with the factory."""
#     class TestModel(models.Model):
#         encrypted_field = EncryptedCharField(max_length=255)

#     instance = TestModel.objects.create(encrypted_field="Sensitive Data")
#     assert instance.encrypted_field != "Sensitive Data"
