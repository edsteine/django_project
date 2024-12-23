# # tests/unit/test_encryption_config.py
# import pytest
# from unittest.mock import patch
# from api.core.encryption.encryption_config import ENCRYPTION_KEY, ENCRYPTION_ALGORITHM, logger

# @patch('api.core.encryption.encryption_config.env_variables.str')
# def test_encryption_config_validation(mock_env_vars):
#     mock_env_vars.side_effect = ["", ""]  # Simulate missing keys

#     with pytest.raises(ValueError):
#         # Running the logic that should raise the ValueError when keys are missing
#         from api.core.encryption.encryption_config import ENCRYPTION_KEY, ENCRYPTION_ALGORITHM
