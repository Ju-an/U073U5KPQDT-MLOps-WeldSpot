import os
import re
from unittest.mock import mock_open, patch

import pytest
from sklearn.metrics import roc_auc_score

from options import CLASS_NAMES
from service.metric_monitoring import analyze_classes

# Test data
test_input_files = [
    "A0Z_1-0.9_0-0.1_0-0.2_0-0.3_0-0.4_0-0.5_0-0.6.jpg",
    "A3Z_0-0.2_1-0.8_0-0.3_1-0.7_0-0.4_1-0.6_0-0.5.jpg",
    "B1Z_1-0.7_0-0.3_1-0.6_0-0.4_1-0.5_0-0.2_1-0.8.jpg",
    "B3Z_0-0.4_1-0.6_0-0.5_1-0.5_0-0.3_1-0.7_0-0.2.jpg",
    "C1A_1-0.7_1-0.3_1-0.6_1-0.1_1-0.5_1-0.2_0-0.8.jpg",
    "C1Z_0-0.4_0-0.4_0-0.6_0-0.9_0-0.4_1-0.9_0-0.2.jpg",
]

expected_class_metrics = {
    "Background": {
        "actuals": [1, 0, 1, 0, 1, 0],
        "predictions": [0.9, 0.2, 0.7, 0.4, 0.7, 0.4],
        "TP": 3,
        "FP": 0,
        "TN": 3,
        "FN": 0,
    },
    "Bad Welding": {
        "actuals": [0, 1, 0, 1, 1, 0],
        "predictions": [0.1, 0.8, 0.3, 0.6, 0.3, 0.4],
        "TP": 2,
        "FP": 0,
        "TN": 3,
        "FN": 1,
    },
    "Crack": {
        "actuals": [0, 0, 1, 0, 1, 0],
        "predictions": [0.2, 0.3, 0.6, 0.5, 0.6, 0.6],
        "TP": 2,
        "FP": 1,
        "TN": 3,
        "FN": 0,
    },
    "Excess Reinforcement": {
        "actuals": [0, 1, 0, 1, 1, 0],
        "predictions": [0.3, 0.7, 0.4, 0.5, 0.1, 0.9],
        "TP": 1,
        "FP": 1,
        "TN": 2,
        "FN": 2,
    },
    "Good Welding": {
        "actuals": [0, 0, 1, 0, 1, 0],
        "predictions": [0.4, 0.4, 0.5, 0.3, 0.5, 0.4],
        "TP": 0,
        "FP": 0,
        "TN": 4,
        "FN": 2,
    },
    "Porosity": {
        "actuals": [0, 1, 0, 1, 1, 1],
        "predictions": [0.5, 0.6, 0.2, 0.7, 0.2, 0.9],
        "TP": 3,
        "FP": 0,
        "TN": 2,
        "FN": 1,
    },
    "Splatters": {
        "actuals": [0, 0, 1, 0, 0, 0],
        "predictions": [0.6, 0.5, 0.8, 0.2, 0.8, 0.2],
        "TP": 1,
        "FP": 2,
        "TN": 3,
        "FN": 0,
    },
}

expected_renamed_files = [
    "A0Z_1_0_0_0_0_0_0.jpg",
    "A3Z_0_1_0_1_0_1_0.jpg",
    "B1Z_1_0_1_0_1_0_1.jpg",
    "B3Z_0_1_0_1_0_1_0.jpg",
    "C1A_1_1_1_1_1_1_0.jpg",
    "C1Z_0_0_0_0_0_1_0.jpg",
]

expected_class_aucs = {
    class_name: roc_auc_score(metrics["actuals"], metrics["predictions"])
    for class_name, metrics in expected_class_metrics.items()
}


def test_analyze_classes():

    class_metrics, class_aucs, renames = analyze_classes(test_input_files)

    assert class_metrics == expected_class_metrics
    assert class_aucs == expected_class_aucs

    expected_pairs = list(zip(test_input_files, expected_renamed_files))
    assert renames == expected_pairs
