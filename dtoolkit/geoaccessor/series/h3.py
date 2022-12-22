from dataclasses import dataclass
from functools import wraps
from typing import Hashable

import geopandas as gpd
import pandas as pd
from pandas.api.extensions import register_series_accessor
from pandas.util._decorators import doc
from pandas._libs.reshape import explode

from dtoolkit.accessor.series import len as s_len
from dtoolkit.geoaccessor.index import h3 as i_h3
from dtoolkit.geoaccessor.series.to_geoframe import to_geoframe


@register_series_accessor("h3")
@dataclass
class h3:
    """
    Hexagonal hierarchical geospatial indexing system.

    A little magic binding H3 for Series.

    Raises
    ------
    ModuleNotFoundError
        If don't have module named 'h3'.

    TypeError
        If the dtype of Index is not string or int64.

    Notes
    -----
    Based on :obj:`~pandas.Series` style, APIs are designed as follows:

    - Remove the prefix ``h3_`` of the original H3 API.
      e.g. :meth:`h3.h3_to_geo` → :meth:`~dtoolkit.geoaccessor.series.h3.to_points`

    - Use ``to_`` prefix for the conversion between H3 cell int and str.
      e.g. :meth:`h3.h3_to_string` → :meth:`~dtoolkit.geoaccessor.series.h3.to_str`

    - Use ``is_`` prefix for the validation of H3 cell.
      e.g. :meth:`h3.h3_is_valid` → :meth:`~dtoolkit.geoaccessor.series.h3.is_valid`
    """

    s: pd.Series

    @property
    @doc(i_h3.area)
    def area(self) -> pd.Series:

        return self.s.index.h3.resolution.area

    # TODO: Available only for h3 release 4.
    # @property
    # @doc(i_h3.edge)
    # def edge(self) -> pd.Series:

    #     return self.s.index.h3.edge

    @property
    @doc(i_h3.resolution)
    def resolution(self) -> pd.Series:

        return self.s.index.h3.resolution

    @property
    @doc(i_h3.resolution)
    def is_valid(self) -> pd.Series:

        return self.s.index.h3.is_valid

    @property
    @doc(i_h3.resolution)
    def is_pentagon(self) -> pd.Series:

        return self.s.index.h3.is_pentagon

    @property
    @doc(i_h3.resolution)
    def is_res_class_III(self) -> pd.Series:

        return self.s.index.h3.is_res_class_III

    def to_int(self) -> pd.Series:
        """
        Converts 64-bit integer H3 cell index to hexadecimal string.

        Returns
        -------
        Series(int64)
            With new H3 cell as the its index.

        Raises
        ------
        TypeError
            If the Series dtype is not string.

        See Also
        --------
        h3.str_to_int
        dtoolkit.geoaccessor.index.h3.to_int
        dtoolkit.geoaccessor.series.h3.to_str

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
        """

        return self.s.set_axis(self.s.index.h3.to_int())

    def to_str(self) -> pd.Series:
        """
        Converts hexadecimal string H3 cell index to 64-bit integer.

        Returns
        -------
        Series(string)
            With new H3 cell as the its index.

        Raises
        ------
        TypeError
            If the Series dtype is not int64.

        See Also
        --------
        h3.int_to_str
        dtoolkit.geoaccessor.index.h3.to_str
        dtoolkit.geoaccessor.series.h3.to_int

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
        """

        return self.s.set_axis(self.s.index.h3.to_str())

    def to_center_child(self, resolution: int = None) -> pd.Series:
        """
        Get the center child of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        Series
            With new H3 center child cell.

        See Also
        --------
        h3.cell_to_center_child
        dtoolkit.geoaccessor.index.h3.to_center_child
        dtoolkit.geoaccessor.series.h3.to_children

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
        """

        return self.s.set_axis(self.s.index.h3.to_center_child(resolution))

    def to_children(self, resolution: int = None) -> pd.Series:
        """
        Get the children of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        Series
            With new H3 children cells.

        See Also
        --------
        h3.cell_to_children
        dtoolkit.geoaccessor.index.h3.to_children
        dtoolkit.geoaccessor.series.h3.to_center_child
        dtoolkit.geoaccessor.series.h3.to_parent

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.to_children(drop=False, partent=None)
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
        """
        # TODO: Use `cell_to_children` instead of `h3_to_children`
        # While h3-py release 4, `cell_to_children` is not available.
        values, counts = explode(self.s.index.h3.to_children(resolution).to_numpy())
        return self.s.repeat(counts).set_axis(values)

    def to_parent(self, resolution: int = None) -> pd.Series:
        """
        Get the parent of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``-1`` .

        Returns
        -------
        Series
            With new H3 parent cell.

        See Also
        --------
        h3.cell_to_parent
        dtoolkit.geoaccessor.index.h3.to_parent
        dtoolkit.geoaccessor.series.h3.to_children

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> s = pd.Series(['a', 'b'], index=[612845052823076863, 614269156845420543])
        >>> s
        612845052823076863    a
        614269156845420543    b
        dtype: object
        >>> s.h3.to_parent(drop=False, children=None)
        608341453197803519    a
        609765557230632959    b
        """

        return self.s.set_axis(self.s.index.h3.to_parent(resolution))

    def to_points(self) -> gpd.GeoDataFrame:
        """
        Return the center :obj:`~shapely.Point` of H3 cell.

        Returns
        -------
        GeoDataFrame

        Raises
        ------
        ValueError
            If name of Series is None.

        See Also
        --------
        h3.cell_to_latlng
        dtoolkit.geoaccessor.index.h3.to_points
        dtoolkit.geoaccessor.series.h3.to_polygons

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
        >>> s.h3.to_points()
                            label                    geometry
        612845052823076863      a  POINT (121.99637 55.00331)
        614269156845420543      b    POINT (99.99611 0.99919)
        """

        if self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.s.__class__.__name__!r}.",
            )

        return to_geoframe(self.s, geometry=self.s.index.h3.to_points())

    def to_polygons(self, drop: bool = False) -> gpd.GeoDataFrame:
        """
        Return :obj:`~shapely.Polygon` to describe the cell boundary.

        Parameters
        ----------
        drop : bool, default False
            Whether to drop the original H3 cell index column.

        Returns
        -------
        GeoSeries or GeoDataFrame
            If True, return a GeoSeries with the original H3 cell index column dropped.

        Raises
        ------
        ValueError
            If ``drop=False`` and the original H3 cell index column is not named.

        See Also
        --------
        h3.cell_to_boundary
        dtoolkit.geoaccessor.series.h3.to_points

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
        612845052823076863      a  POLYGON ((121.98797 55.00408, 121.99122 54.999...
        614269156845420543      b  POLYGON ((100.00035 0.99630, 100.00080 1.00141...
        """

        if self.s.name is None:
            raise ValueError(
                "to keep the original data requires setting the 'name' of "
                f"{self.s.__class__.__name__!r}.",
            )

        return to_geoframe(self.s, geometry=self.s.index.h3.to_polygons())
