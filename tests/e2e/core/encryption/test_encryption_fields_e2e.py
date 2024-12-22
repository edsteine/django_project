import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.e2e
def test_encrypted_field_e2e(client, valid_encryption_key):# type: ignore
    """Test the end-to-end encryption and decryption in a user-facing API."""
    # Assuming you have a model with the EncryptedCharField and a corresponding serializer
    response = client.post(reverse('model-create'), {'encrypted_field': 'Sensitive Info'})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['encrypted_field'] != 'Sensitive Info'  # Ensure data is encrypted

    # Simulate retrieving the data
    response = client.get(reverse('model-detail', args=[response.data['id']]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['encrypted_field'] == 'Sensitive Info'  # Ensure data can be decrypted
