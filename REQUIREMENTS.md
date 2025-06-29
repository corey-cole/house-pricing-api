# Requirements

This requirements file was used to vibe-code the bootstrap of the sample application.  It may be useful to review for anyone looking to replicate, but is not generally intended for human consumption.

## Background
This is a FastAPI application that hosts machine learning models for inference. It includes endpoints for health checks, model inventory, and prediction.  It is anticipated that the project will undergo multiple revisions, so ensure that endpoints have a prefix identifying the version (e.g. "/v1" or "/v2").  All the endpoints in this initial implementation are under "/v1".

Inference may take some time, so when prediction is called for use the `multiprocessing` module from the Python standard library to enable prediction for each item under the request.

## Input/Output
Request shape:
```json
{
    "1": {
        "LotArea": 12345,
        "YearBuilt": 1999,
        "InteriorArea": 1234,
        "ModelDate": "2025-06-29"
    },
    "2": {
        "LotArea": 12345,
        "YearBuilt": 1899,
        "InteriorArea": 1234,
        "ModelDate": "2025-06-15"
    }
}
```

Response shape:
```json
{
    "1": {
        "SalePrice": 100000,
        "ModelDate": "2025-06-27"
    },
    "2": {
        "SalePrice": 85000,
        "ModelDate": "2025-06-10"
    }
}
```

## Monitoring 

In addition to standard Prometheus monitoring, the application should include FastAPI instrumentation.  It should also include a custom metric to track each individual subrequest from the prediction endpoint.  These custom metrics should track the count of subrequests, the duration of subrequests, and the number of subrequest successes and failures.

## Testing

The application has a suite of Pytest unit tests, and code coverage is determined via the `pytest-cov` library.