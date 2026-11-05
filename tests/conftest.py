import os
import tempfile

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def temp_csv_file():
    """Provide the shared integration-test CSV fixture."""
    data = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5],
            "category": ["A", "B", "A", "C", "B"],
            "value": [10.5, 20.3, 15.7, np.nan, 25.0],
            "count": [100, 200, 150, 175, 225],
            "date": [
                "2023-01-01",
                "2023-01-02",
                "2023-01-03",
                "2023-01-04",
                "2023-01-05",
            ],
        }
    )
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as file:
        data.to_csv(file.name, index=False)
        path = file.name
    yield path
    if os.path.exists(path):
        os.unlink(path)
