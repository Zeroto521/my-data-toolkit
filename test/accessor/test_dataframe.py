from test.accessor.conftest import d

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest

from dtoolkit.accessor.dataframe import drop_inf  # noqa
from dtoolkit.accessor.dataframe import filter_in  # noqa
from dtoolkit.accessor.dataframe import repeat  # noqa
from dtoolkit.accessor.dataframe import to_series  # noqa
from dtoolkit.accessor.dataframe import top_n  # noqa


class TestDropinf:
    @pytest.mark.parametrize(
        "df, axis, how, inf, subset, expt",
        [
            (
                d,
                0,
                "any",
                "all",
                None,
                d,
            ),
            (
                d.append({"a": np.inf}, ignore_index=True),
                0,
                "any",
                "all",
                None,
                d,
            ),
            (
                d.append({"a": np.inf}, ignore_index=True),
                1,
                "any",
                "all",
                None,
                d.append({"a": np.inf}, ignore_index=True).drop(columns=["a"]),
            ),
            (
                d.append({"a": np.inf}, ignore_index=True),
                0,
                "all",
                "all",
                None,
                d.append({"a": np.inf}, ignore_index=True),
            ),
            (
                d.append({"a": np.inf, "b": -np.inf}, ignore_index=True),
                0,
                "all",
                "all",
                None,
                d,
            ),
            (
                d.append({"b": -np.inf}, ignore_index=True),
                0,
                "any",
                "neg",
                None,
                d,
            ),
            (
                d.append({"b": -np.inf}, ignore_index=True),
                0,
                "any",
                "pos",
                None,
                d.append({"b": -np.inf}, ignore_index=True),
            ),
            (
                d.append({"b": -np.inf}, ignore_index=True),
                0,
                "any",
                "all",
                ["b"],
                d,
            ),
            (
                d.append({"b": -np.inf}, ignore_index=True),
                0,
                "any",
                "all",
                ["a", "b"],
                d,
            ),
            (
                d.append({"b": -np.inf}, ignore_index=True),
                0,
                "any",
                "all",
                ["a", "b"],
                d,
            ),
        ],
    )
    def test_work(self, df, axis, how, inf, subset, expt):
        res = df.drop_inf(axis=axis, how=how, inf=inf, subset=subset)

        assert res.equals(expt)

    @pytest.mark.parametrize(
        "error, axis, how, subset",
        [
            (ValueError, (0, 1), "any", None),
            (ValueError, 0, "whatever", None),
            (TypeError, 0, None, None),
            (KeyError, 0, "any", ["c"]),
        ],
    )
    def test_error(self, error, axis, how, subset):
        with pytest.raises(error):
            d.drop_inf(axis=axis, how=how, subset=subset)

    def test_inplace_is_true(self):
        self_d = d.copy(True)
        self_d = self_d.append(
            {
                "a": np.inf,
                "b": -np.inf,
            },
            ignore_index=True,
        )
        res = self_d.drop_inf(inplace=True)

        assert res is None
        assert self_d.equals(d)


class TestFilterIn:
    def setup_method(self):
        self.d = d.copy(True)
        self.condition = {"a": [0, 1], "b": [2]}

    def test_work(self):
        res = self.d.filter_in(self.condition)

        assert res["a"].isin([0, 1]).any()  # 0 and 1 in a
        assert (~res["a"].isin([2])).all()  # 2 not in a
        assert res["b"].isin([2]).any()  # 2 in a
        assert (~res["b"].isin([0, 1])).all()  # 0 and not in a

    def test_inplace_is_true(self):
        res = self.d.filter_in(self.condition, inplace=True)

        assert res is None
        assert self.d.equals(d) is False

    def test_issue_145(self):
        # test my-data-toolkit#145
        df = pd.DataFrame(
            {
                "legs": [2, 4, 2],
                "wings": [2, 0, 0],
            },
            index=["falcon", "dog", "cat"],
        )
        res = df.filter_in({"legs": [2]})

        expected = pd.DataFrame(
            {
                "legs": [2, 2],
                "wings": [2, 0],
            },
            index=["falcon", "cat"],
        )

        assert res.equals(expected)


class TestRepeat:
    def setup_method(self):
        self.d = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    @pytest.mark.parametrize(
        "repeats, axis, expected",
        [
            (1, 0, pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
            (1, 1, pd.DataFrame({"a": [1, 2], "b": [3, 4]})),
            (
                2,
                0,
                pd.DataFrame(
                    {
                        "a": [1, 1, 2, 2],
                        "b": [3, 3, 4, 4],
                    },
                    index=[0, 0, 1, 1],
                ),
            ),
            (
                2,
                1,
                pd.DataFrame(
                    [
                        [1, 1, 3, 3],
                        [2, 2, 4, 4],
                    ],
                    columns=["a", "a", "b", "b"],
                ),
            ),
            (
                [1, 2],
                1,
                pd.DataFrame(
                    [
                        [1, 3, 3],
                        [2, 4, 4],
                    ],
                    columns=["a", "b", "b"],
                ),
            ),
        ],
    )
    def test_work(self, repeats, axis, expected):
        result = self.d.repeat(repeats, axis=axis)

        assert result.equals(expected)

    @pytest.mark.parametrize("axis", [-1, 3, None])
    def test_error(self, axis):
        with pytest.raises(ValueError):
            self.d.repeat(2, axis)


class TestTopN:
    @pytest.mark.parametrize(
        "n, largest, keep, prefix, delimiter, element, excepted",
        [
            (
                1,
                True,
                "first",
                "top",
                "_",
                "both",
                {
                    "top_1": [
                        ("b", 3),
                        ("a", 3),
                        ("c", 3),
                    ],
                },
            ),
            (  # test 'n'
                2,
                True,
                "first",
                "top",
                "_",
                "both",
                {
                    "top_1": [("b", 3), ("a", 3), ("c", 3)],
                    "top_2": [("c", 2), ("b", 2), ("a", 2)],
                },
            ),
            (  # test 'largest'
                1,
                False,
                "first",
                "top",
                "_",
                "both",
                {
                    "top_1": [("a", 1), ("c", 1), ("b", 1)],
                },
            ),
            (  # test 'prefix' and 'delimiter'
                1,
                True,
                "first",
                "largest",
                "-",
                "both",
                {
                    "largest-1": [
                        ("b", 3),
                        ("a", 3),
                        ("c", 3),
                    ],
                },
            ),
            (  # test 'element'
                2,
                True,
                "first",
                "top",
                "_",
                "index",
                {
                    "top_1": ["b", "a", "c"],
                    "top_2": ["c", "b", "a"],
                },
            ),
            (  # test 'element'
                2,
                True,
                "first",
                "top",
                "_",
                "value",
                {
                    "top_1": [3, 3, 3],
                    "top_2": [2, 2, 2],
                },
            ),
        ],
    )
    def test_single_index_work(
        self,
        n,
        largest,
        keep,
        prefix,
        delimiter,
        element,
        excepted,
    ):
        df = pd.DataFrame(
            {
                "a": [1, 3, 2],
                "b": [3, 2, 1],
                "c": [2, 1, 3],
            },
        )

        result = df.top_n(
            n=n,
            largest=largest,
            keep=keep,
            prefix=prefix,
            delimiter=delimiter,
            element=element,
        )

        excepted = pd.DataFrame(excepted)
        assert result.equals(excepted)

    @pytest.mark.parametrize(
        "n, keep, excepted",
        [
            (
                1,
                "first",
                {
                    "top_1": [("c", 3), ("a", 3)],
                },
            ),
            (
                1,
                "all",
                {
                    "top_1": [("c", 3), ("a", 3)],
                    "top_2": [np.nan, ("b", 3)],
                    "top_3": [np.nan, ("c", 3)],
                },
            ),
        ],
    )
    def test_duplicate_dataframe(self, n, keep, excepted):
        df = pd.DataFrame(
            {
                "a": [1, 3],
                "b": [2, 3],
                "c": [3, 3],
            },
        )

        result = df.top_n(n=n, keep=keep, element="both")
        excepted = pd.DataFrame(excepted)

        assert result.equals(excepted)

    @pytest.mark.parametrize(
        "df, n, excepted",
        [
            (
                {
                    ("a1", "a2"): [1, 3],
                    ("b1", "b2"): [2, 3],
                    ("c1", "c2"): [3, 3],
                },
                1,
                {
                    "top_1": [
                        (("c1", "c2"), 3),
                        (("a1", "a2"), 3),
                    ],
                },
            ),
            (
                {
                    ("a1", "a2"): [1, 3],
                    ("b1", "b2"): [2, 2],
                    ("c1", "c2"): [3, 1],
                },
                2,
                {
                    "top_1": [
                        (("c1", "c2"), 3),
                        (("a1", "a2"), 3),
                    ],
                    "top_2": [
                        (("b1", "b2"), 2),
                        (("b1", "b2"), 2),
                    ],
                },
            ),
        ],
    )
    def test_multi_index(self, df, n, excepted):
        df = pd.DataFrame(df)
        result = df.top_n(n=n, element="both")
        excepted = pd.DataFrame(excepted)

        assert result.equals(excepted)

    def test_element_error(self):
        df = pd.DataFrame(
            {
                "a": [1, 3, 2],
                "b": [3, 2, 1],
                "c": [2, 1, 3],
            },
        )

        with pytest.raises(ValueError):
            df.top_n(1, element="whatever")


class TestToSeries:
    @pytest.mark.parametrize(
        "df, name, excepted",
        [
            (
                pd.DataFrame({"a": [1, 2]}),
                None,
                pd.Series([1, 2], name="a"),
            ),
            # dataframe -> dataframe
            (
                pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
                None,
                pd.DataFrame({"a": [1, 2], "b": [3, 4]}),
            ),
            # name is not None
            (
                pd.DataFrame({"a": [1, 2]}),
                "b",
                pd.Series([1, 2], name="b"),
            ),
            # the columns of df are default
            (
                pd.DataFrame([1, 2]),
                None,
                pd.Series([1, 2], name=0),
            ),
            # geodataframe -> geodataframe
            (
                gpd.GeoDataFrame({"a": [1, 2], "b": [3, 4]}),
                None,
                gpd.GeoDataFrame({"a": [1, 2], "b": [3, 4]}),
            ),
            # geodataframe -> geodataframe
            (
                gpd.GeoDataFrame.from_features(
                    {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {"col1": "name1"},
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": (1.0, 2.0),
                                },
                            },
                            {
                                "type": "Feature",
                                "properties": {"col1": "name2"},
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": (2.0, 1.0),
                                },
                            },
                        ],
                    },
                ),
                None,
                gpd.GeoDataFrame.from_features(
                    {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {"col1": "name1"},
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": (1.0, 2.0),
                                },
                            },
                            {
                                "type": "Feature",
                                "properties": {"col1": "name2"},
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": (2.0, 1.0),
                                },
                            },
                        ],
                    },
                ),
            ),
            # geodataframe -> geoseries
            (
                gpd.GeoDataFrame({"a": [1, 2]}),
                None,
                pd.Series([1, 2], name="a"),
            ),
            # geodataframe -> geoseries
            (
                gpd.GeoDataFrame.from_features(
                    {
                        "type": "FeatureCollection",
                        "features": [
                            {
                                "type": "Feature",
                                "properties": {},
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": (1.0, 2.0),
                                },
                            },
                            {
                                "type": "Feature",
                                "properties": {},
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": (2.0, 1.0),
                                },
                            },
                        ],
                    },
                ),
                None,
                gpd.GeoSeries.from_wkt(
                    [
                        "POINT (1 2)",
                        "POINT (2 1)",
                    ],
                    name="geometry",
                ),
            ),
        ],
    )
    def test_work(self, df, name, excepted):
        result = df.to_series(name)

        assert result.equals(excepted)
