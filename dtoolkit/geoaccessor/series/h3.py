import geopandas as gpd
import pandas as pd
from pandas.api.extensions import register_series_accessor
from pandas.core.base import NoNewAttributesMixin
from pandas.util._decorators import doc

from dtoolkit._typing import SeriesOrFrame
from dtoolkit.geoaccessor.index import H3 as i_H3


class H3Base(NoNewAttributesMixin):
    @property
    @doc(i_H3.area)
    def area(self) -> pd.Series:

        return self.data.index.h3.area

    # TODO: Available only for h3 release 4.
    # @property
    # @doc(i_H3.edge)
    # def edge(self) -> pd.Series:

    #     return self.data.index.h3.edge

    @property
    @doc(i_H3.resolution)
    def resolution(self) -> pd.Series:

        return self.data.index.h3.resolution

    @property
    @doc(i_H3.is_valid)
    def is_valid(self) -> pd.Series:

        return self.data.index.h3.is_valid

    @property
    @doc(i_H3.is_pentagon)
    def is_pentagon(self) -> pd.Series:

        return self.data.index.h3.is_pentagon

    @property
    @doc(i_H3.is_res_class_III)
    def is_res_class_III(self) -> pd.Series:

        return self.data.index.h3.is_res_class_III

    @doc(klass="Series or DataFrame")
    def to_int(self) -> SeriesOrFrame:
        """
        Converts hexadecimal string H3 cell index to 64-bit integer.

        Returns
        -------
        {klass}
            With new H3 cell as the its index.

        See Also
        --------
        h3.str_to_int
        dtoolkit.geoaccessor.series.H3.to_str
        dtoolkit.geoaccessor.dataframe.H3.to_int

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=['88143541bdfffff', '886528b2a3fffff'])
        >>> s
        88143541bdfffff    a
        886528b2a3fffff    b
        dtype: object
        >>> s.h3.to_int()
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> df = pd.DataFrame(
        ...     {{'label': ['a', 'b']}},
        ...     index=['88143541bdfffff', '886528b2a3fffff'],
        ... )
        >>> df
                        label
        88143541bdfffff     a
        886528b2a3fffff     b
        >>> df.h3.to_int()
                           label
        612845052823076863     a
        614269156845420543     b
        """

        return self.data.set_axis(self.data.index.h3.to_int())

    @doc(klass="Series or DataFrame")
    def to_str(self) -> SeriesOrFrame:
        """
        Converts 64-bit integer H3 cell index to hexadecimal string.

        Returns
        -------
        {klass}
            With new H3 cell as the its index.

        See Also
        --------
        h3.int_to_str
        dtoolkit.geoaccessor.series.H3.to_int
        dtoolkit.geoaccessor.dataframe.H3.to_str

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.to_str()
        88143541bdfffff    a
        886528b2a3fffff    b
        dtype: object
        >>> df = pd.DataFrame(
        ...     {{'label': ['a', 'b']}},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_str()
                        label
        88143541bdfffff     a
        886528b2a3fffff     b
        """

        return self.data.set_axis(self.data.index.h3.to_str())

    @doc(klass="Series or DataFrame")
    def to_center_child(self, resolution: int = None) -> SeriesOrFrame:
        """
        Get the center child of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        {klass}
            With new H3 center child cell.

        See Also
        --------
        h3.cell_to_center_child
        dtoolkit.geoaccessor.series.H3.to_children
        dtoolkit.geoaccessor.dataframe.H3.to_center_child

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.to_center_child()
        617348652448612351    a
        618772756470956031    b
        dtype: object
        >>> df = pd.DataFrame(
        ...     {{'label': ['a', 'b']}},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_center_child()
                           label
        617348652448612351     a
        618772756470956031     b
        """

        return self.data.set_axis(self.data.index.h3.to_center_child(resolution))

    @doc(klass="Series or DataFrame")
    def to_children(self, resolution: int = None) -> SeriesOrFrame:
        """
        Get the children of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        {klass}
            With new H3 children cells.

        See Also
        --------
        h3.cell_to_children
        dtoolkit.geoaccessor.series.H3.to_center_child
        dtoolkit.geoaccessor.series.H3.to_parent
        dtoolkit.geoaccessor.dataframe.H3.to_children

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.to_children()
        617348652448612351    a
        617348652448874495    a
        617348652449136639    a
        617348652449398783    a
        617348652449660927    a
        617348652449923071    a
        617348652450185215    a
        618772756470956031    b
        618772756471218175    b
        618772756471480319    b
        618772756471742463    b
        618772756472004607    b
        618772756472266751    b
        618772756472528895    b
        dtype: object
        >>> df = pd.DataFrame(
        ...     {{'label': ['a', 'b']}},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_children()
                           label
        617348652448612351     a
        617348652448874495     a
        617348652449136639     a
        617348652449398783     a
        617348652449660927     a
        617348652449923071     a
        617348652450185215     a
        618772756470956031     b
        618772756471218175     b
        618772756471480319     b
        618772756471742463     b
        618772756472004607     b
        618772756472266751     b
        618772756472528895     b
        """
        from pandas._libs.reshape import explode

        # BUG: `GeoDataFrame.repeat` will return `DataFrame` not `GeoDataFrame`
        index, counts = explode(self.data.index.h3.to_children(resolution).to_numpy())
        return self.data.repeat(counts).set_axis(index)

    @doc(klass="Series or DataFrame")
    def to_parent(self, resolution: int = None) -> SeriesOrFrame:
        """
        Get the parent of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``-1`` .

        Returns
        -------
        {klass}
            With new H3 parent cell.

        See Also
        --------
        h3.cell_to_parent
        dtoolkit.geoaccessor.series.H3.to_children
        dtoolkit.geoaccessor.dataframe.H3.to_parent

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd

        Series Example.

        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.to_parent()
        608341453197803519    a
        609765557230632959    b
        dtype: object

        DataFrame Example.

        >>> df = pd.DataFrame(
        ...     {{'label': ['a', 'b']}},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_parent()
                           label
        608341453197803519     a
        609765557230632959     b
        """

        return self.data.set_axis(self.data.index.h3.to_parent(resolution))

    def to_points(self) -> gpd.GeoDataFrame:
        """
        Return the center :obj:`~shapely.Point` of H3 cell.

        Returns
        -------
        GeoDataFrame
            With H3 cell as the its index.

        See Also
        --------
        h3.cell_to_latlng
        dtoolkit.geoaccessor.series.H3.to_polygons
        dtoolkit.geoaccessor.dataframe.H3.to_points
        dtoolkit.geoaccessor.geodataframe.to_h3

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(
        ...     ['a', 'b'],
        ...     index=[612845052823076863, 614269156845420543],
        ...     name='label',
        ... )
        >>> s
        612845052823076863    a
        614269156845420543    b
        Name: label, dtype: object
        >>> s.h3.to_points()
                           label                    geometry
        612845052823076863     a  POINT (121.99637 55.00331)
        614269156845420543     b    POINT (99.99611 0.99919)
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_points()
                           label                    geometry
        612845052823076863     a  POINT (121.99637 55.00331)
        614269156845420543     b    POINT (99.99611 0.99919)
        """

        if isinstance(self.data, pd.Series) and self.data.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.data.__class__.__name__!r}.",
            )

        return self.data.to_geoframe(geometry=self.data.index.h3.to_points())

    def to_polygons(self) -> gpd.GeoDataFrame:
        """
        Return :obj:`~shapely.Polygon` to describe the cell boundary.

        Returns
        -------
        GeoDataFrame
            With H3 cell as the its index.

        See Also
        --------
        h3.cell_to_boundary
        dtoolkit.geoaccessor.series.H3.to_points
        dtoolkit.geoaccessor.dataframe.H3.to_polygons
        dtoolkit.geoaccessor.geodataframe.to_h3

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(
        ...     ['a', 'b'],
        ...     index=[612845052823076863, 614269156845420543],
        ...     name='label'
        ... )
        >>> s
        612845052823076863    a
        614269156845420543    b
        Name: label, dtype: object
        >>> s.h3.to_polygons()
                           label                                           geometry
        612845052823076863     a  POLYGON ((121.98797 55.00408, 121.99122 54.999...
        614269156845420543     b  POLYGON ((100.00035 0.99630, 100.00080 1.00141...
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_polygons()
                           label                                           geometry
        612845052823076863     a  POLYGON ((121.98797 55.00408, 121.99122 54.999...
        614269156845420543     b  POLYGON ((100.00035 0.99630, 100.00080 1.00141...
        """

        if isinstance(self.data, pd.Series) and self.data.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.data.__class__.__name__!r}.",
            )

        return self.data.to_geoframe(geometry=self.data.index.h3.to_polygons())


@register_series_accessor("h3")
@doc(i_H3, klass="Series")
class H3(H3Base):
    def __init__(self, s: pd.Series, /):
        self.data = s

        self._freeze()

    @doc(H3Base.to_int, klass="Series")
    def to_int(self) -> pd.Series:

        return super().to_int()

    @doc(H3Base.to_str, klass="Series")
    def to_str(self) -> pd.Series:

        return super().to_str()

    @doc(H3Base.to_center_child, klass="Series")
    def to_center_child(self, resolution: int = None) -> pd.Series:

        return super().to_center_child(resolution)

    @doc(H3Base.to_children, klass="Series")
    def to_children(self, resolution: int = None) -> pd.Series:

        return super().to_children(resolution)

    @doc(H3Base.to_parent, klass="Series")
    def to_parent(self, resolution: int = None) -> pd.Series:

        return super().to_parent(resolution)
