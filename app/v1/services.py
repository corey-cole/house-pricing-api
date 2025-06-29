import random
import time
from datetime import date
from typing import Union

from ..core.monitoring import SUBREQUEST_COUNTER, SUBREQUEST_DURATION_SECONDS
from .schemas import HouseData, Prediction, PredictionError

# Placeholder for model version
MODEL_VERSION = "v0.1.0"


def predict_price(house_data_tuple: tuple[str, HouseData]) -> tuple[str, Union[Prediction, PredictionError]]:
    """
    Placeholder function to simulate a prediction.
    This function is designed to be run in a separate process.
    """
    request_id, house_data = house_data_tuple
    status = "success"
    start_time = time.time()
    try:
        # Simulate ML model inference time
        time.sleep(random.uniform(0.05, 0.2))  # noqa: S311

        # Dummy prediction logic
        if house_data.YearBuilt < 1800:
            raise ValueError("Model cannot handle houses built before 1800")

        sale_price = int(
            (house_data.LotArea * 10)
            + (house_data.InteriorArea * 50)
            - (date.today().year - house_data.YearBuilt) * 100
        )

        prediction = Prediction(SalePrice=max(50000, sale_price), ModelDate=date.today())
        return request_id, prediction
    except Exception as e:
        status = "failure"
        return request_id, PredictionError(error=str(e))
    finally:
        duration = time.time() - start_time
        SUBREQUEST_DURATION_SECONDS.observe(duration)
        SUBREQUEST_COUNTER.labels(model_version=MODEL_VERSION, status=status).inc()
