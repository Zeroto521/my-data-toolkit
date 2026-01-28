import numpy as np
import dtoolkit.geoaccessor
import pandas as pd
import shapely

df = pd.DataFrame(
    {
        "x": [114.21892734521, 128.543, 1],
        "y": [29.575429778924, 37.065, 1],
    },
).from_xy("x", "y", crs=4326)

data = df.geometry
print(shapely.has_z(np.array(data)).any())
# print(df.cncrs_offset(from_crs="bd09", to_crs="gcj02"))
print(shapely.get_coordinates(data, include_z=True))
