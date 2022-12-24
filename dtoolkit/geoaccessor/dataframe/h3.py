import geopandas as gpd
import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
from pandas.core.base import NoNewAttributesMixin
from pandas.util._decorators import doc

from dtoolkit.geoaccessor.dataframe.to_geoframe import to_geoframe
from dtoolkit.geoaccessor.index import H3 as i_H3


@register_dataframe_accessor("h3")
@doc(i_H3, klass="DataFrame")
class H3(NoNewAttributesMixin):
    def __init__(self, df: pd.DataFrame, /):
        self.df = df

        self._freeze()

    @property
    @doc(i_H3.area)
    def area(self) -> pd.Series:

        return self.df.index.h3.area

    # TODO: Available only for h3 release 4.
    # @property
    # @doc(i_H3.edge)
    # def edge(self) -> pd.Series:

    #     return self.df.index.h3.edge

    @property
    @doc(i_H3.resolution)
    def resolution(self) -> pd.Series:

        return self.df.index.h3.resolution

    @property
    @doc(i_H3.resolution)
    def is_valid(self) -> pd.Series:

        return self.df.index.h3.is_valid

    @property
    @doc(i_H3.resolution)
    def is_pentagon(self) -> pd.Series:

        return self.df.index.h3.is_pentagon

    @property
    @doc(i_H3.resolution)
    def is_res_class_III(self) -> pd.Series:

        return self.df.index.h3.is_res_class_III

    def to_int(self) -> pd.DataFrame:
        """
        Converts 64-bit integer H3 cell index to hexadecimal string.

        Returns
        -------
        DataFrame
            With new H3 cell as the its index.

        Raises
        ------
        TypeError
            If the Series dtype is not string.

        See Also
        --------
        h3.str_to_int
        dtoolkit.geoaccessor.series.H3.to_int
        dtoolkit.geoaccessor.dataframe.H3.to_str

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
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

        return self.df.set_axis(self.df.index.h3.to_int())

    def to_str(self) -> pd.DataFrame:
        """
        Converts hexadecimal string H3 cell index to 64-bit integer.

        Returns
        -------
        DataFrame
            With new H3 cell as the its index.

        Raises
        ------
        TypeError
            If the Series dtype is not int64.

        See Also
        --------
        h3.int_to_str
        dtoolkit.geoaccessor.series.H3.to_str
        dtoolkit.geoaccessor.dataframe.H3.to_int

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
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

        return self.df.set_axis(self.df.index.h3.to_str())

    def to_center_child(self, resolution: int = None) -> pd.DataFrame:
        """
        Get the center child of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        DataFrame
            With new H3 center child cell.

        See Also
        --------
        h3.cell_to_center_child
        dtoolkit.geoaccessor.series.H3.to_center_child
        dtoolkit.geoaccessor.dataframe.H3.to_children

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
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

        return self.df.set_axis(self.df.index.h3.to_center_child(resolution))

    def to_children(self, resolution: int = None) -> pd.DataFrame:
        """
        Get the children of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``+1`` .

        Returns
        -------
        DataFrame
            With new H3 children cells.

        See Also
        --------
        h3.cell_to_children
        dtoolkit.geoaccessor.series.H3.to_children
        dtoolkit.geoaccessor.dataframe.H3.to_center_child
        dtoolkit.geoaccessor.dataframe.H3.to_parent

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> df.h3.to_children()
                           label
        617348652448874495     a
        617348652448612351     a
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

        # TODO: Use `cell_to_children` instead of `h3_to_children`
        # While h3-py release 4, `cell_to_children` is not available.
        h3, counts = explode(self.df.index.h3.to_children(resolution).to_numpy())
        return self.df.repeat(counts).set_axis(h3)

    def to_parent(self, resolution: int = None) -> pd.DataFrame:
        """
        Get the parent of cell.

        Parameters
        ----------
        resolution : int, optional
            The resolution for the children. If None, then use the current
            ``resolution`` of cell ``-1`` .

        Returns
        -------
        DataFrame
            With new H3 parent cell.

        See Also
        --------
        h3.cell_to_parent
        dtoolkit.geoaccessor.series.H3.to_parent
        dtoolkit.geoaccessor.dataframe.H3.to_children

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
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

        return self.df.set_axis(self.df.index.h3.to_parent(resolution))

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
        dtoolkit.geoaccessor.series.H3.to_points
        dtoolkit.geoaccessor.dataframe.H3.to_polygons

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
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
        612845052823076863      a  POINT (121.99637 55.00331)
        614269156845420543      b    POINT (99.99611 0.99919)
        """

        return to_geoframe(self.df, geometry=self.df.index.h3.to_points())

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
        dtoolkit.geoaccessor.series.H3.to_polygons
        dtoolkit.geoaccessor.dataframe.H3.to_points

        Examples
        --------
        >>> import dtoolkit.geoaccessor
        >>> import pandas as pd
        >>> df = pd.DataFrame(
        ...     {'label': ['a', 'b']},
        ...     index=[612845052823076863, 614269156845420543],
        ... )
        >>> df
                           label
        612845052823076863     a
        614269156845420543     b
        >>> s.h3.to_polygons()
                            label                                           geometry
        612845052823076863      a  POLYGON ((121.98797 55.00408, 121.99122 54.999...
        614269156845420543      b  POLYGON ((100.00035 0.99630, 100.00080 1.00141...
        """

        return to_geoframe(self.df, geometry=self.df.index.h3.to_polygons())
