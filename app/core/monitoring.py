from prometheus_client import Counter, Histogram

# Custom metric to track sub-request count for predictions
SUBREQUEST_COUNTER = Counter(
    "prediction_subrequest_count",
    "Count of prediction sub-requests",
    ["model_version", "status"],
)

# Custom metric to track sub-request duration for predictions
SUBREQUEST_DURATION_SECONDS = Histogram(
    "prediction_subrequest_duration_seconds",
    "Duration of prediction sub-requests",
)
