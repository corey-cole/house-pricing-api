import json

import pytest
from pydantic import ValidationError

from app.v1.schemas import PredictionRequest
from tests import TEST_DATA_DIR

SAMPLE_DATA_PATH = TEST_DATA_DIR / "sample-data.json"


@pytest.fixture
def valid_payload() -> dict:
    """Load valid sample data from the JSON file."""
    with open(SAMPLE_DATA_PATH, "r") as f:
        return json.load(f)


def test_prediction_request_valid(valid_payload):
    """Tests that a valid payload is correctly parsed."""
    request = PredictionRequest.model_validate(valid_payload)
    assert "1" in request.root
    assert "2" in request.root
    assert request.root["1"].LotArea == 12345


def test_prediction_request_invalid_year(valid_payload):
    """Tests that a year outside the valid range raises a ValidationError."""
    valid_payload["1"]["YearBuilt"] = 1799
    with pytest.raises(ValidationError) as excinfo:
        PredictionRequest.model_validate(valid_payload)
    assert "YearBuilt" in str(excinfo.value)
    assert "Input should be greater than 1800" in str(excinfo.value)


def test_prediction_request_missing_field(valid_payload):
    """Tests that a missing required field raises a ValidationError."""
    del valid_payload["1"]["LotArea"]
    with pytest.raises(ValidationError) as excinfo:
        PredictionRequest.model_validate(valid_payload)
    assert "LotArea" in str(excinfo.value)
    assert "Field required" in str(excinfo.value)


def test_prediction_request_invalid_type(valid_payload):
    """Tests that a field with an incorrect type raises a ValidationError."""
    valid_payload["1"]["InteriorArea"] = "not-an-int"
    with pytest.raises(ValidationError) as excinfo:
        PredictionRequest.model_validate(valid_payload)
    assert "InteriorArea" in str(excinfo.value)
    assert "Input should be a valid integer" in str(excinfo.value)


def test_prediction_request_empty_payload():
    """Tests that an empty payload is valid."""
    request = PredictionRequest.model_validate({})
    assert len(request.root) == 0