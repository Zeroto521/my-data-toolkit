import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.index import H3 as i_H3
from dtoolkit.geoaccessor.series.h3 import H3Base


@register_dataframe_accessor("h3")
@doc(i_H3, klass="DataFrame")
class H3(H3Base):
    def __init__(self, df: pd.DataFrame, /):
        self.data = df

        self._freeze()

    @doc(H3Base.to_int, klass="DataFrame")
    def to_int(self) -> pd.DataFrame:

        return super().to_int()

    @doc(H3Base.to_str, klass="DataFrame")
    def to_str(self) -> pd.DataFrame:

        return super().to_str()

    @doc(H3Base.to_center_child, klass="DataFrame")
    def to_center_child(self, resolution: int = None) -> pd.DataFrame:

        return super().to_center_child(resolution)

    @doc(H3Base.to_children, klass="DataFrame")
    def to_children(self, resolution: int = None) -> pd.DataFrame:

        return super().to_children(resolution)

    @doc(H3Base.to_parent, klass="DataFrame")
    def to_parent(self, resolution: int = None) -> pd.DataFrame:

        return super().to_parent(resolution)
