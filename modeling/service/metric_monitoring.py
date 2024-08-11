import os
import re

from sklearn.metrics import roc_auc_score

from options import CLASS_NAMES, CLASS_THRESHOLD, RAW_PATH


def analyze_classes(files):
    class_metrics = {
        class_name: {
            "actuals": [],
            "predictions": [],
            "TP": 0,
            "FP": 0,
            "TN": 0,
            "FN": 0,
        }
        for class_name in CLASS_NAMES
    }

    renames = []

    for file in files:
        match = re.match(r"^(.*?)(_.*?\.jpg)$", file)
        if not match:
            continue

        identifier, class_conf_pairs = match.groups()
        class_conf_pairs = class_conf_pairs[1:-4].split(
            "_"
        )  # Remove leading underscore and .jpg

        new_filename_parts = [identifier]
        for i, pair in enumerate(class_conf_pairs):
            actual, confidence = pair.split("-")
            actual = int(actual)
            confidence = float(confidence)
            class_name = CLASS_NAMES[i]

            # Update confusion matrix
            if actual == 1:
                if confidence >= CLASS_THRESHOLD:
                    class_metrics[class_name]["TP"] += 1
                else:
                    class_metrics[class_name]["FN"] += 1
            else:
                if confidence >= CLASS_THRESHOLD:
                    class_metrics[class_name]["FP"] += 1
                else:
                    class_metrics[class_name]["TN"] += 1

            # Store predictions and actual values for AUC calculation
            class_metrics[class_name]["predictions"].append(confidence)
            class_metrics[class_name]["actuals"].append(actual)

            new_filename_parts.append(str(actual))

        new_filename = "_".join(new_filename_parts) + ".jpg"
        renames.append((file, new_filename))

    # Calculate AUC for each class
    class_aucs = {}
    for class_name, metrics in class_metrics.items():
        if (
            len(set(metrics["actuals"])) > 1
        ):  # AUC is undefined if there is only one class in actuals
            class_aucs[class_name] = roc_auc_score(
                metrics["actuals"], metrics["predictions"]
            )
        else:
            class_aucs[class_name] = None

    return class_metrics, class_aucs, renames


def drift_detection():
    files = os.listdir(RAW_PATH)
    if not files:
        return None, None
    class_metrics, class_aucs, renames = analyze_classes(files)
    # Check if there is drift in any class
    for class_name, auc in class_aucs.items():
        if auc is not None and auc < CLASS_THRESHOLD:
            return class_metrics, class_name
    # Rename files
    for old_name, new_name in renames:
        os.rename(os.path.join(RAW_PATH, old_name), os.path.join(RAW_PATH, new_name))
    return class_metrics, None
