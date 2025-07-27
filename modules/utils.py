# modules/utils.py

import os
import pandas as pd
from datetime import datetime

def save_output_report(data, filename="report.csv"):
    """
    Saves the output verification result to a CSV file in the output folder.
    """
    os.makedirs("output", exist_ok=True)
    filepath = os.path.join("output", filename)

    # If file already exists, append timestamp to filename
    if os.path.exists(filepath):
        base, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join("output", f"{base}_{timestamp}{ext}")

    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)

    return filepath
