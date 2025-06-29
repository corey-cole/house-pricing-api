import multiprocessing
from typing import Any, Dict

from fastapi import APIRouter, HTTPException

from .schemas import PredictionRequest, PredictionResponse
from .services import predict_price

router = APIRouter()


@router.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}


@router.get("/inventory")
def model_inventory() -> Dict[str, Any]:
    # Placeholder for model inventory
    return {"models": ["xgboost-v1.0", "random-forest-v2.1"]}


@router.post("/predict", response_model=PredictionResponse)
def predict(request_data: PredictionRequest) -> PredictionResponse:
    """
    Receives a batch of house data items and returns predictions.
    Uses multiprocessing to parallelize predictions and handles
    individual prediction errors gracefully.
    """
    items_to_process = list(request_data.items())

    if not items_to_process:
        return PredictionResponse(root={})

    with multiprocessing.Pool() as pool:
        # Exceptions in predict_price are caught and returned as PredictionError objects
        results = pool.map(predict_price, items_to_process)

    response_data = dict(results)
    return PredictionResponse(root=response_data)