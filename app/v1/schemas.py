from datetime import date
from typing import Union

from pydantic import BaseModel, Field, PositiveInt, RootModel


class HouseData(BaseModel):
    LotArea: PositiveInt
    YearBuilt: int = Field(..., gt=1800, lt=date.today().year + 2)
    InteriorArea: PositiveInt
    ModelDate: date


class PredictionRequest(RootModel[dict[str, HouseData]]):
    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def items(self):
        return self.root.items()


class Prediction(BaseModel):
    SalePrice: PositiveInt
    ModelDate: date


class PredictionError(BaseModel):
    error: str


class PredictionResponse(RootModel[dict[str, Union[Prediction, PredictionError]]]):
    pass
