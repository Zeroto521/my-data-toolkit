# Changelog

## [Version 0.0.20] (2022-12-30)

Highlights of this release:

Hightly support H3 (Hexagonal hierarchical geospatial indexing system) via `.to_h3` and `.H3.*`.

```python
>>> import dtoolkit.geoaccessor
>>> import pandas as pd
>>> df = pd.DataFrame({"x": [122, 100], "y": [55, 1]}).from_xy('x', 'y', crs=4326)
>>> df
     x   y                    geometry
0  122  55  POINT (122.00000 55.00000)
1  100   1   POINT (100.00000 1.00000)

# GeoDataFrame -> h3 cell

>>> df_with_h3 = df.to_h3(8)
>>> df_with_h3
                      x   y                    geometry
612845052823076863  122  55  POINT (122.00000 55.00000)
614269156845420543  100   1   POINT (100.00000 1.00000)

# Calculate h3 cell area

>>> df_with_h3.h3.area
612845052823076863    710781.770906
614269156845420543    852134.191671
dtype: float64

# h3 cell -> GeoDataFrame

>>> df_parent_cell = df_with_h3.h3.to_parent()
>>> df_parent_cell
                      x   y                    geometry
608341453197803519  122  55  POINT (122.00000 55.00000)
609765557230632959  100   1   POINT (100.00000 1.00000)
>>> df_parent_cell.h3.to_points()
                      x   y                    geometry
608341453197803519  122  55  POINT (122.00991 55.00606)
609765557230632959  100   1   POINT (100.00504 0.99852)
```

New features and improvements:

- {pr}`739`, {pr}`800`, {pr}`817`, {pr}`825`: New geoaccessor {meth}`~dtoolkit.geoaccessor.geoseries.to_h3` to convert geometry to h3 index.
- {pr}`778`: Speed up {meth}`~dtoolkit.accessor.series.textdistance_matrix`.
- {pr}`779`, {pr}`811`, {pr}`819`: New geoaccessor {obj}`~dtoolkit.geoaccessor.dataframe.H3` to handle h3's geohash.
- {pr}`784`: New accessor {meth}`~dtoolkit.accessor.series.to_zh`.
- {pr}`794`, {pr}`797`: New geoaccessor for GeoDataFrame {meth}`~dtoolkit.geoaccessor.geodataframe.xy`.
- {pr}`801`: New accessor for Series {meth}`~dtoolkit.accessor.series.invert_or_not`.
- {pr}`803`: New geoaccessor {meth}`~dtoolkit.geoaccessor.geoseries.select_geom_type`.
- {pr}`804`: New geoaccessor {meth}`~dtoolkit.geoaccessor.geoseries.radius`.
- {pr}`809`: New accessor for Index {meth}`~dtoolkit.accessor.index.len`.

Small bug-fix:

- {pr}`780`: Fix {meth}`~dtoolkit.geoaccessor.dataframe.to_geoframe`'s geometry is `GeoSeries`.
- {pr}`816`: Fix {meth}`~dtoolkit.geoaccessor.dataframe.to_geoframe` result CRS is missing.
- {pr}`822`: {meth}`~dtoolkit.geoaccessor.dataframe.to_geoframe` supports replacing old geometry.
- {pr}`824`: Fix inputting `GeoDataFrame` but {meth}`~dtoolkit.accessor.dataframe.repeat` return `DataFrame`.

API changes:

- {pr}`807`: {meth}`~dtoolkit.geoaccessor.geodataframe.get_coordinates` -> {meth}`~dtoolkit.geoaccessor.geodataframe.coordinates`.
- {pr}`814`: Drop keyword argument `drop`.

Documentation:

- {pr}`802`: Reorder methods via function first then name.
- {pr}`808`: Mark Series dtype.

Maintenance development:

- {pr}`774`: pre-commit hooks autoupdate.
- {pr}`798`: Remove pygeos dependency from dtoolkit.
- {pr}`805`: Remove `ci/env/311-latest-shapely2.yaml`.
- {pr}`806`: Compat pandas 2.x.
- {pr}`810`: Remove `dtoolkit.accessor.series._getattr_helper.py`.
- {pr}`812`: Add blank lines.
- {pr}`813`: Remove 0.0.19 version warning information.
- {pr}`818`: Simplify import shapely object ``from shapely.geometry import xxx`` -> ``from shapely import xxx``.

## [Version 0.0.19] (2022-12-11)

Highlights of this release:

- {pr}`574`, {pr}`752`, {pr}`757`, {pr}`758`: Supported python 3.11.
- {pr}`772`: Simplify importing `import dtoolkit` == `import dtoolkit.accessor`.

New features and improvements:

- {pr}`724`: New accessor for Series to calculate text distance {meth}`~dtoolkit.accessor.series.textdistance`.
- {pr}`745`: {meth}`~dtoolkit.geoaccessor.geodataframe.duplicated_geometry`'s `predicate` support to directly compare value.
- {pr}`748`: {meth}`~dtoolkit.geoaccessor.geoseries.xy` support to return DataFrame.
- {pr}`760`: {meth}`~dtoolkit.accessor.dataframe.repeat` support to use column as the input.
- {pr}`768`: New accessor {meth}`~dtoolkit.accessor.dataframe.change_axis_type`.

Small bug-fix:

- {pr}`576`: Fix `DataFrame.append`'s FutureWarning.
- {pr}`765`: Fix sklearn pipeline visualization can't print `OneHotEncoder`.
- {pr}`776`: After v0.0.17 github release page don't have tarball file anymore.

API changes:

- {pr}`762`: Drop `columns` arguments for `error_report`.

Documentation:

- {pr}`755`: Update `installtation` documentation.
- {pr}`766`: Some patches to documentation.

Maintenance development:

- {pr}`726`, {pr}`790`: Compat sklearn 1.2
- {pr}`737`: Leave TODO marks for deleting pygeos.
- {pr}`742`, {pr}`754`, {pr}`767`: pre-commit hooks autoupdate.
- {pr}`744`, {pr}`750`: versioneer autoupdate.
- {pr}`746`: All envs will get daily test.
- {pr}`747`: Set a env to test that dtoolkit works with only base dependencies.
- {pr}`749`: Use `.is_monotonic_increasing` replace `.is_monotonic`.
- {pr}`751`, {pr}`756`, {pr}`773`, {pr}`781`, {pr}`787`, {pr}`795`: Compat shapely 2.x.
- {pr}`753`, {pr}`759`: Lint codes.
- {pr}`763`: Simplify versioneer updating CI.
- {pr}`764`: versioneer updating only works on main branch.
- {pr}`770`: Minimal environments only test base features.
- {pr}`775`: Remove `set-output` from github actions yaml files.
- {pr}`777`, {pr}`785`, {pr}`786`, {pr}`788`: Autoupdate actions.
- {pr}`791`: Compat with pandas 2.x.

## [Version 0.0.18] (2022-10-14)

New features and improvements:

- {pr}`721`: New accessor for `Series` to convert datetime type, {meth}`~dtoolkit.accessor.series.to_datetime`.
- {pr}`715`: New accessor {meth}`~dtoolkit.accessor.series.equal` to compare pandas-object with other.
- {pr}`712`: Support use `DataFrame`'s column as the distance for {meth}`~dtoolkit.geoaccessor.geodataframe.geobuffer`.
- {pr}`711`, {pr}`713`: New geoaccessor for GeoSeries to return tuple of coordinates `(x, y)`, {meth}`~dtoolkit.geoaccessor.geoseries.xy`.
- {pr}`701`, {pr}`704`, {pr}`705`, {pr}`706`: New geoaccessor to generate great circle distances matrix, {meth}`~dtoolkit.geoaccessor.geoseries.geodistance_matrix`.
- {pr}`699`, {pr}`702`, {pr}`707`, {pr}`735`: New geoaccessor to calculate two coordinates distance on earth, {meth}`~dtoolkit.geoaccessor.geoseries.geodistance`.
- {pr}`696`: New geoaccessor to handle China webmap offset problem, {meth}`~dtoolkit.geoaccessor.geoseries.cncrs_offset`.
- {pr}`691`, {pr}`703`: New geoaccessor to filter geometry via spatial relationship, {meth}`~dtoolkit.geoaccessor.geoseries.filter_geometry`.
- {pr}`688`: New accessor {meth}`~dtoolkit.accessor.dataframe.weighted_mean` for DataFrame.
- {pr}`685`: Let `Pipeline`'s `fit_predict` and `predict` support outputting `DataFrame`.
- {pr}`680`, {pr}`682`: New geoaccessor to check Polygon whether having hole, {meth}`~dtoolkit.geoaccessor.geoseries.has_hole`.
- {pr}`679`: New geoaccessor to count the hole number of `Polygon`, {meth}`~dtoolkit.geoaccessor.geoseries.hole_counts`.
- {pr}`668`: Add a new option `dropna` for {meth}`~dtoolkit.accessor.series.values_to_dict` to handle nan value.
- {pr}`667`: New accessor {meth}`~dtoolkit.accessor.series.dropna_index`.

API changes:

- {pr}`694`, {pr}`695`: `pygeos` isn't an optional dependency anymore.
- {pr}`665`: Drop {meth}`~dtoolkit.geoaccessor.geoseries.utm_crs`.

Small bug-fix:

- {pr}`714`, {pr}`716`: Fix {meth}`~dtoolkit.accessor.dataframe.decompose` can't collapse `dict`.
- {pr}`692`: Reset non-monotonic index.

Documentation:

- {pr}`732`: Add description for {meth}`~dtoolkit.accessor.series.jenks_bin`.
- {pr}`723`, {pr}`729`: Add sub-title for reference apis.
- {pr}`719`: Fix [`transformer_quickstart.ipynb` rendering](https://my-data-toolkit.readthedocs.io/en/v0.0.18/guide/transformer_quickstart.html).
- {pr}`709`: Update `toposimplify` example.
- {pr}`697`: Simplify doc link via `klass` variable.
- {pr}`693`: Reforce pydata-sphinx-theme to v0.9.0.
- {pr}`689`: Update author information.
- {pr}`686`: Correct link.
- {pr}`553`: Add description for `pipeline`.

Maintenance development:

- {pr}`730`, {pr}`731`: Simplify codes (directly select DataFrame, rename Series, and add `/` for method to only receive positional argument).
- {pr}`720`: Add comment for why updating the version of dependencies.
- {pr}`717`: Compat Python 3.7 / 3.8 which requires pandas >= 1.2.
- {pr}`710`, {pr}`727`: Lint codes (includes {meth}`~dtoolkit.accessor.dataframe.top_n`, {meth}`~dtoolkit.util._decorator.warning`, and {meth}`~dtoolkit.accessor.series.filter_in`).
- {pr}`700`: Simplify CodeQL CI.
- {pr}`687`: Add new pre-commit hooks.
- {pr}`684`: Use official `concurrency` instead of `cancel.yaml`.
- {pr}`678`, {pr}`698`, {pr}`718`, {pr}`722`: pre-commit hooks autoupdate.
- {pr}`677`: Update workflow-run-cleaner option.
- {pr}`675`, {pr}`676`: New CI to remove old extra workflow runs.
- {pr}`673`: Merge two test CIs.
- {pr}`672`: Small patch to release CI.
- {pr}`671`: Don't lint versioneer.
- {pr}`666`: Merge 'sdist' and 'release' two CIs.
- {pr}`664`: use `*.size` replace `len(*)`.
- {pr}`663`: Update {meth}`~dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups` description and simplify its logic.
- {pr}`661`: Update {meth}`~dtoolkit.accessor.series.to_series` description  and simplify its logic.
- {pr}`660`: Set `sdist` default job name.
- {pr}`658`, {pr}`690`, {pr}`708`: versioneer autoupdate.

## [Version 0.0.17] (2022-8-15)

Highlights of this release:

- Speed up geoaccessor {meth}`~dtoolkit.geoaccessor.geoseries.geobuffer` via `UTM` CRS ({pr}`638`).
- Require minimal Python 3.8+ ({pr}`554`).
- {meth}`~dtoolkit.accessor.series.eval` and {meth}`~dtoolkit.accessor.series.query` work for Series now ({pr}`492`, {pr}`551`).

New features and improvements:

- New geoaccessor compute geographic area {meth}`~dtoolkit.geoaccessor.geoseries.geoarea` ({pr}`640`).
- A syntactic sugar to parallelize multi-jobs {meth}`~dtoolkit.util.parallelize` ({pr}`635`, {pr}`641`).
- New geoaccessor to label / drop duplicate geometry: {meth}`~dtoolkit.geoaccessor.geoseries.duplicated_geometry_groups`, {meth}`~dtoolkit.geoaccessor.geoseries.duplicated_geometry`, and {meth}`~dtoolkit.geoaccessor.geoseries.drop_duplicates_geometry` ({pr}`631`, {pr}`632`).
- New accessor for Series {meth}`~dtoolkit.accessor.series.swap_index_values` ({pr}`630`).
- New accessor group by index {meth}`~dtoolkit.accessor.series.groupby_index` ({pr}`625`).
- New geoaccessor for GeoDataFrame {meth}`~dtoolkit.geoaccessor.geoseries.toposimplify` ({pr}`624`, {pr}`649`, {pr}`651`).
- {meth}`~dtoolkit.accessor.dataframe.to_series` gets only `value_column` also return Series from DataFrame ({pr}`620`).
- New accessor for Series {meth}`~dtoolkit.accessor.series.jenks_bin` and {meth}`~dtoolkit.accessor.series.jenks_breaks` ({pr}`618`, .{pr}`629`)
- New accessor for Series {meth}`~dtoolkit.accessor.series.filter_in` ({pr}`614`).
- New geoaccessor for GeoDataFrame {meth}`~dtoolkit.geoaccessor.series.to_geoseries` ({pr}`609`).
- New geoaccessor remove active geometry {meth}`~dtoolkit.geoaccessor.geodataframe.drop_geometry` ({pr}`599`).
- New geoaccessor for Series {meth}`~dtoolkit.geoaccessor.series.from_wkt` ({pr}`596`).
- New geoaccessor get coordinates from addresses {meth}`~dtoolkit.geoaccessor.series.geocode` and get addresses from coordinates {meth}`~dtoolkit.geoaccessor.geoseries.reverse_geocode` ({pr}`591`, {pr}`594`, {pr}`643`, {pr}`636`, {pr}`652`).
- New `level` option for Index accessor {meth}`~dtoolkit.accessor.index.to_set` ({pr}`586`).
- Speed up Series accessor {meth}`~dtoolkit.accessor.series.to_set` ({pr}`585`).
- New geoaccessor {meth}`~dtoolkit.geoaccessor.dataframe.from_wkb` ({pr}`584`, {pr}`598`).
- New geoaccessor {meth}`~dtoolkit.geoaccessor.series.to_geoframe` ({pr}`568`, {pr}`642`, {pr}`646`).

Small bug-fix:

- Avoid GeoDataFrame constructor mutating the original (inputting) DataFrame ({pr}`644`).
- Avoid {meth}`~dtoolkit.accessor.dataframe.fillna_regression` mutating the original dataframe ({pr}`622`).
- Compat with sklearn 1.2 stricter class parameters checking ({pr}`602`).
- {meth}`~dtoolkit.geoaccessor.geodataframe.geobuffer` uses the active geometry to generate buffers ({pr}`583`).
- Hook accessor method's attrs into both class and instance ({pr}`580`).

API changes:

- Add deprecated warning for {meth}`~dtoolkit.geoaccessor.geoseries.utm_crs` ({pr}`637`, {pr}`645`).
- Remove warning message and drop `inplace` option ({pr}`555`).
- Use positional-only arguments (`/`) to limit `name` ({pr}`435`).

Documentation:

- Add Raises part for documentation ({pr}`623`).
- Apply singular file name style to `/doc/*` ({pr}`613`).
- Remove title '.dev0' and '.post0' suffixes ({pr}`587`).
- Beautify the format of inputting dictionary ({pr}`577`).

Maintenance development:

- Set timeout for updating versioneer CI ({pr}`657`).
- `drop_inf/get_inf_range` returns `set` instead of `list` ({pr}`656`).
- Remove 'fkirc/skip-duplicate-actions' ({pr}`655`).
- Rename arguments of methods ({pr}`647`).
- Remove 'geopy' from `*-minmal.yaml` env ({pr}`621`).
- Use `cut` as {meth}`~dtoolkit.accessor.series.bin`'s alias ({pr}`619`).
- Use `topn` as {meth}`~dtoolkit.accessor.series.top_n`'s alias ({pr}`617`).
- Follow `Series.nlargest(n=5, keep='first')` API ({pr}`616`).
- Follow `numpy.repeat(repeats, axis)` API ({pr}`615`).
- Set only positional parameter (`/`) for `(geo)accessor` ({pr}`612`).
- Add `environment.yaml` at root path for user ({pr}`611`).
- Use `pandas.testing.assert_*_equal` replace `(Series|DataFrame).equals` in testing ({pr}`607`, {pr}`608`).
- Use function style rather than OOP ({pr}`606`, {pr}`633`, {pr}`648`, {pr}`653`).
- Singular style file name ({pr}`605`).
- Correct file name ({pr}`604`).
- Rename yaml file `*.yml` -> `*.yaml` ({pr}`603`).
- `(Geo)DataFrame` geoaccessor don't return `(Geo)Series` anymore ({pr}`601`).
- Set default coding style via EditorConfig ({pr}`600`).
- Suit actions/setup-python@v4 new changing ({pr}`581`).
- pre-commit hooks autoupdate ({pr}`579`, {pr}`595`, {pr}`610`, {pr}`627`, {pr}`634`, {pr}`639`).
- Autoupdate actions ({pr}`578`, {pr}`592`, {pr}`628`).
- Move `dtoolkit.transformer.pipeline` into `dtoolkit.pipeline` ({pr}`563`).

Typing annotations:

- Use `Hashable` replace `str | int` ({pr}`582`).
- Use `Literal` ({pr}`505`).

## [Version 0.0.16] (2022-5-30)

New features and improvements:

- New accessor {meth}`~dtoolkit.accessor.dataframe.fillna_regression` ({pr}`556`, {pr}`567`).
- New `unique` option for {meth}`~dtoolkit.accessor.dataframe.values_to_dict` ({pr}`548`).
- Speed up {meth}`~dtoolkit.util._exception.find_stack_level` ({pr}`546`).
- {meth}`~dtoolkit.accessor.dataframe.filter_in`'s `how` only works on `condition` `DataFrame`'s columns ({pr}`545`).
- {meth}`~dtoolkit.accessor.series.to_set` speeds up especial to large data ({pr}`542`, {pr}`543`).
- {meth}`~dtoolkit.accessor.dataframe.drop_inf`'s `inf` option supports `+` and `-` ({pr}`539`).
- New accessor {meth}`~dtoolkit.accessor.dataframe.boolean` for `DataFrame` ({pr}`537`, {pr}`538`).
- New `complement` option for {meth}`~dtoolkit.accessor.dataframe.filter_in` ({pr}`533`).
- New `Index` method {meth}`~dtoolkit.accessor.index.to_set` ({pr}`529`).
- New method {meth}`~dtoolkit.accessor.dataframe.decompose` for `DataFrame` ({pr}`488`, {pr}`573`).

API changes:

- Add deprecated warning for {mod}`dtoolkit.transformer.pipeline` ({pr}`558`).
- Split {mod}`dtoolkit.transformer` scripts into sub-pakcages ({pr}`557`).
- Drop `inplace` for {meth}`~dtoolkit.accessor.dataframe.drop_inf` ({pr}`540`).
- Drop `generic` package ({pr}`535`).
- Drop `inplace` option of {meth}`~dtoolkit.accessor.dataframe.filter_in` ({pr}`518`, {pr}`531`, {pr}`559`).

Documentation:

- Adjust the sequence of methods ({pr}`565`).
- Index `._decorator` and `_exception` method ({pr}`532`).

Maintenance development:

- Don't skip dist when `ci/**` path files changing ({pr}`570`).
- Remove `TYPE_CHECKING` blocks ({pr}`566`).
- Remove `__future__` useless line importing ({pr}`564`).
- Simplify {meth}`~dtoolkit.accessor.register_method_factory` ({pr}`552`).
- Correct name `excepted` -> `expected` ({pr}`547`).
- Complete the accessor subpackage test suitcase ({pr}`544`).
- Move `collapse` from `_util` into `expand` ({pr}`541`).
- Lint importing ({pr}`536`).
- Test {meth}`~dtoolkit.util._decorator.deprecated_kwargs` ({pr}`534`).

## [Version 0.0.15] (2022-5-13)

New features and improvements:

- New decorator {meth}`~dtoolkit.util._decorator.deprecated_kwargs` ({pr}`525`).
- Add `to_list` option for {meth}`~dtoolkit.accessor.series.cols` ({pr}`523`).
- Add the index register method {meth}`~dtoolkit.accessor.register_index_method`, support register method into {class}`~pandas.Index` ({pr}`507`).

API changes:

- Add version information for warning ({pr}`528`).
- Add `DeprecationWarning` for dropping `axis` option of {meth}`~dtoolkit.accessor.dataframe.filter_in` ({pr}`522`).
- Add `DeprecationWarning` for dropping `generic` package ({pr}`521`).
- Add `DeprecationWarning` for dropping `inplace` option of {meth}`~dtoolkit.accessor.dataframe.filter_in` ({pr}`519`).
- Drop {meth}`unique_counts` method ({pr}`512`).

Maintenance development:

- Add single quote via `!r` for f-string ({pr}`520`).
- Add changelog link at PyPI page ({pr}`517`).
- Use `build` new distuils and add `pyproject.toml` configuration ({pr}`516`).
- pre-commit hooks autoupdate ({pr}`515`, {pr}`524`).
- Remove warning message ({pr}`513`, {pr}`514`, {pr}`526`).

## [Version 0.0.14] (2022-5-1)

New features and improvements:

- Replace `.shape` with `.__len__`, 1.6x speed up than older method ({pr}`506`).
- New method {meth}`~dtoolkit.accessor.series.to_set` ({pr}`503`).
- New option `to_list` for {meth}`~dtoolkit.accessor.dataframe.values_to_dict` ({pr}`500`).
- New decorator {meth}`dtoolkit.util._decorator.deprecated_alias` ({pr}`498`).
- New option `order` for {meth}`~dtoolkit.accessor.dataframe.values_to_dict` ({pr}`495`).
- Return the error place is first happening via `stacklevel` option({pr}`490`).
- New method {meth}`~dtoolkit.geoaccessor.dataframe.from_wkt` ({pr}`486`).
- New method {meth}`~dtoolkit.accessor.dataframe.drop_or_not` ({pr}`485`).
- New decorator `warning` ({pr}`484`).

API changes:

- Drop {meth}`~dtoolkit.accessor.dataframe.unique_counts`, use {meth}`pandas.DataFrame.nunique` instead ({pr}`502`)
- Rename {meth}`~dtoolkit.accessor.dataframe.values_to_dict`'s argument from `few_as_key` to `asscending` ({pr}`499`).
- Rename accessor name, `get_attr` -> `getattr`, `lens` -> `len` ({pr}`487`).
- Simplify {meth}`~dtoolkit.accessor.dataframe.bin`'s parameters via `*args` and `**kwargs` ({pr}`481`).

Documentation:

- Add {meth}`~dtoolkit.accessor.dataframe.top_n`'s new example about returning values ({pr}`489`).
- Adjust API reference sequences ({pr}`478`).

Maintenance development:

- Autoupdate actions ({pr}`494`, {pr}`496`, {pr}`497`, {pr}`504`, {pr}`510`).
- Autoupdate pre-commit hooks ({pr}`493`, {pr}`501`, {pr}`508`).
- Use `pd.concat` replace `pd.DataFrame.append` ({pr}`491`).
- Update black version ({pr}`483`).
- Split package to scripts, `dataframe.py` -> `dataframe/`, `series.py` -> `series/`, `geodataframe.py` -> `geodataframe/`, `geoseries.py` -> `geoseries/`, `generic.py` -> `generic/` ({pr}`475`, {pr}`480`, {pr}`482`).

## [Version 0.0.13] (2022-4-2)

New features and improvements:

- Use `.loc[:, wrong_keys]` instead of `.get(wrong_keys)` ({pr}`473`).
- New method {meth}`~dtoolkit.accessor.dataframe.values_to_dict` ({pr}`470`).
- New method {meth}`~dtoolkit.accessor.dataframe.unique_counts` ({pr}`469`).
- {meth}`~dtoolkit.accessor.dataframe.to_series` could convert two or more columns DataFrame ({pr}`468`).

API changes:

- Array in array out ({pr}`460`).
- `OneHotEncoder`'s `fit_transform` use inputting's index ({pr}`458`).
- Let `Pipeline`'s `fit_transform` supports `Series` ({pr}`457`).
- Drop `dtoolkit.transformer.MinMaxScaler`({pr}`451`).

Small bug-fix:

- Fix jupyter notebook can't render ({pr}`438`).

Documentation:

- Rename sphinx project name from 'dtoolkit' to 'my data toolkit' ({pr}`454`).
- Add 'feature' section at documentation homepage ({pr}`452`).

Maintenance development:

- Update versioneer ({pr}`471`).
- Autoupdate pre-commit hooks ({pr}`464`).
- Autoupdate actions ({pr}`462`, {pr}`463`, {pr}`472`).
- Yaml file uses list item replace `[]` ({pr}`461`).
- Group test suits ({pr}`459`).
- Handle `GeoSeries` FutureWarning ({pr}`456`).
- Move all data to conftest.py ({pr}`453`).

Typing annotations:

- Specific `None` type using ({pr}`467`).
- Specific `None` type ({pr}`466`).
- Add `Number` and `IntOrStr` annotation constants ({pr}`465`).

## [Version 0.0.12] (2022-2-11)

Highlights of this release:

- Specific pandas minimal version to each python version ({pr}`440`).
- One column data pipeline supports return `Series` ({pr}`431`).

API changes:

- Add `DeprecationWarning` for {class}`dtoolkit.transformer.MinMaxScaler` ({pr}`449`).

Documentation:

- New documentation, [Register a Method as the Original Attribute of Pandas Object](https://my-data-toolkit.readthedocs.io/en/v0.0.12/guide/tips_about_accessor.html) ({pr}`445`).
- Correct jupyter link ({pr}`444`).

Maintenance development:

- Add `extras_require` ({pr}`446`).
- Update pre-commit hooks ({pr}`442`, {pr}`448`).
- Set `setup.cfg` version attribute ({pr}`441`).
- Compat sklearn 1.0 ({pr}`250`).

## [Version 0.0.11] (2022-1-25)

New features and improvements:

- Simplify `OneHotEncoder` examples and inputs ({pr}`434`).
- `FeatureUnion` would merge all into one DataFrame and the index would use the common part ({pr}`433`).

Small bug-fix:

- Fix jupyter notebook can't render ({pr}`438`).

Maintenance development:

- Simplify linting workflow ({pr}`437`).

## [Version 0.0.10] (2022-1-21)

Highlights of this release:

- Use `main` replace of `master` as the base branch ({issue}`412`, {pr}`413`).

New features and improvements:

- Add `number` and `other` option for {meth}`~dtoolkit.accessor.series.lens` ({pr}`406`).

Documentation:

- Fix Readthedocs running excessive memory consumption ({pr}`436`).
- Update installation documentation ({pr}`419`).
- New documentation, [Tips About Accessing Element Attributes of `Series`](https://my-data-toolkit.readthedocs.io/en/v0.0.11/guide/tips_about_getattr.html) ({pr}`408`).
- Use jupyter replace markdown ({pr}`405`, {pr}`409`, {pr}`410`, {pr}`414`).
- Remove warning for `Series.lens` ({pr}`399`).

Maintenance development:

- Cancel any previous runs that are not completed ({pr}`426`).
- Add skip check job ({pr}`425`).
- Use mamba to speed up building env ({pr}`422`, {pr}`427`, {pr}`436`).
- Test `register_*_method` positional arguments ({pr}`420`).
- Simplify CI jobs ({pr}`416`, {pr}`423`, {pr}`424`)
- Add some new pre-commit hooks ({pr}`407`).
- Contained 'rc' tag would be as 'pre-release' ({pr}`404`).
- Rename `ci/envs/*` to `ci/env/*` ({pr}`403`).
- Add skip check avoid frequently creating versioneer's autoupdating PR ({pr}`397`).

## [Version 0.0.9] (2022-1-10)

Highlights of this release:

- Use `squash merge` to keep a cleaning git commit history ({issue}`386`).
- {meth}`~dtoolkit.accessor.register_series_method` and {meth}`~dtoolkit.accessor.register_dataframe_method` support alias ({pr}`392`).

New features and improvements:

- {meth}`~dtoolkit.geoaccessor.dataframe.points_from_xy` would return `GeoSeries` if df only has one column ({pr}`385`).
- New accessor method {meth}`~dtoolkit.accessor.dataframe.to_series` ({pr}`380`).
- New accessor method {meth}`~dtoolkit.accessor.series.get_attr` ({pr}`379`, {pr}`394`, {pr}`398`).

API changes:

- Call {meth}`~dtoolkit.accessor.series.lens` via `Series.len` ({pr}`394`).

Maintenance development:

- Draft github-action release then add changelog by manually ({pr}`396`).
- Fix words, a -> an ({pr}`387`).
- Pre-commit hooks autoupdate ({pr}`384`).

Contributing development:

- Add pull request template ({pr}`361`).

Documentation:

- Correct sphinx method link ({pr}`390`).

## [Version 0.0.8] (2022-1-1)

Highlights of this release:

- Publish to PyPI ({pr}`363`).
- Change PyPI project name from `dtoolkit` to `my-data-toolkit` ({pr}`382`).

API changes:

- Remove {meth}`~dtoolkit.geoaccessor.tool.geographic_buffer` ({pr}`348`).

Maintenance development:

- Let git choose the default branch ({pr}`376`).
- Update pre-commit commit message ({pr}`371`).
- Enable labeled 'auto-merged' PR could merge master branch into PR ({pr}`368`, {pr}`370`, {pr}`372`, {pr}`375`).
- Github action runner update ({pr}`365`, {pr}`366`, {pr}`367`, {pr}`369`, {pr}`383`).
- Auto update github action runner ({pr}`360`, {pr}`364`).
- Pre-commit hooks auto update ({pr}`359`).

Documentation:

- Correct package name, `MinMaxScaler` -> `OneHotEncoder` ({pr}`374`).
- Shorten package path, `dtoolkit.accessor.register` -> `dtoolkit.accessor` ({pr}`373`).

New contributors:

- {user}`dependabot`
- {user}`web-flow`

## [Version 0.0.7] (2021-12-30)

Highlights of this release:

- {meth}`~dtoolkit.geoaccessor.geoseries.geobuffer` at least x1.3 faster than before ({pr}`341`, {pr}`342`, {pr}`347`, {pr}`350`, {pr}`357`).

New features and improvements:

- Extend {meth}`~dtoolkit.accessor.series.lens` function range ({pr}`356`).
- New geoaccessor method {meth}`~dtoolkit.geoaccessor.geoseries.utm_crs` ({pr}`346`).

API changes:

- Add `DeprecationWarning` for {meth}`~dtoolkit.geoaccessor.tool.geographic_buffer` ({pr}`341`).

Maintenance development:

- Simplify {meth}`~dtoolkit.accessor.dataframe.repeat` codes ({pr}`353`).
- Use `add_prefix` to simplify {meth}`~dtoolkit.accessor.series.expand` ({pr}`352`).
- Use `add_prefix` to simplify {meth}`~dtoolkit.accessor.series.top_n` ({pr}`351`).
- Import uncommon packages at inner of method ({pr}`343`, {pr}`344`).
- Tag event also trigger to release to `test.pypi.org` ({pr}`340`).

Typing annotations:

- Specific `Any` type ({pr}`355`).
- Use `TYPE_CHECKING` mark ({pr}`354`).
- Specific the type of `list` element ({pr}`349`).
- Correct {meth}`~dtoolkit.accessor.series.cols` return type ({pr}`345`).

## [Version 0.0.6] (2021-12-13)

Highlights of this release:

- Now DToolKit supports python 3.10 ({pr}`228`, {pr}`326`, {pr}`327`, {pr}`330`, {pr}`338`).

New features and improvements:

- Add `columns` argument for {meth}`~dtoolkit.accessor.series.error_report` ({pr}`328`).
- New method {meth}`~dtoolkit.geoaccessor.dataframe.points_from_xy` ({pr}`316`).

Bug fixes:

- Fix version number showing at sphinx home page ({pr}`318`).

Maintenance development:

- Publish to test.pypi.org only when event is 'push' ({pr}`337`).
- pre-commit autoupdate ({pr}`324`).
- Update commit message of bot ({pr}`321`).
- Add workflow to automatically update versioneer ({pr}`319`, {pr}`333`).

Documentation:

- Documentation pathch ({pr}`329`).

## [Version 0.0.5] (2021-12-6)

Highlights of this release:

- Remove test from release package ({pr}`307`).
- Use `TAG[.postDIST[.dev0]]` version style ({pr}`299`, {pr}`300`, {pr}`306`).
- Simplify methods of importing {mod}`dtoolkit.accessor` and {mod}`dtoolkit.geoaccessor` ({pr}`294`, {pr}`295`, {pr}`297`, {pr}`303`).

New features and improvements:

- Add new method for Series, {meth}`~dtoolkit.accessor.series.error_report` ({pr}`304`).
- Let {meth}`~dtoolkit.accessor.series.expand` support sub-element type is list-like ({pr}`283`).
- Add new accessor {meth}`~dtoolkit.accessor.series.lens` ({pr}`282`).

API changes:

- Remove {mod}`toolkit.geogarphy` ({pr}`277`).

Maintenance development:

- Let CI fetch all git history to get correct version ({pr}`312`).
- Add yaml file checker ({pr}`302`).
- Update versioneer ({pr}`296`).
- Bump version of pre-commit repos ({pr}`292`).
- Publish to TestPyPI ({pr}`291`).
- Gather information into setup.cfg ({pr}`298`).
- Create codeql analysis CI ({pr}`287`).
- Add `.PHONY` into Makefile to avoid name conflict ({pr}`285`).
- Adjust tests CI ({pr}`284`, {pr}`288`, {pr}`290`, {pr}`293`, {pr}`310`, {pr}`311`).

Documentation:

- Redirect py-modindex.html to reference.html ({pr}`314`).
- Update Readme file ({pr}`313`).
- Add documentation for generating geographic buffer methods ({pr}`308`).
- Complete {meth}`~dtoolkit.accessor.series.top_n`'s documentation ({pr}`305`).

New contributors:

- {user}`pre-commit-ci`

## [Version 0.0.4] (2021-11-8)

Highlights of this release:

- Let GeoPandas also has Pandas accessor function ({pr}`261`, {pr}`265`, {pr}`266`, {pr}`268`, {pr}`271`, {pr}`273`, {pr}`275`, {pr}`276`, {pr}`280`, {pr}`281`).
- DToolKit requires Pandas >= 1.1.3 to support Python 3.9 ({pr}`254`).

New features and improvements:

- New accessor {meth}`~dtoolkit.accessor.series.expand` ({pr}`252`, {pr}`279`).
- Let {meth}`~dtoolkit.accessor.dataframe.top_n` default return is index not tuple ({pr}`248`).
- Add a new option `element` for {meth}`~dtoolkit.accessor.dataframe.top_n`, now support to control return data structure ({pr}`247`).

API changes:

- Add `DeprecationWarning` for {mod}`toolkit.geogarphy` ({pr}`274`).
- Keep snake name style, `dropinf` -> `drop_inf` and `filterin` -> `filter_in` ({pr}`249`, {pr}`253`).

Maintenance development:

- Only publish `.tar` file ({pr}`246`).
- Use `artifact` to save sdist to fix different CI jobs that can't exchange data problems ({pr}`242`).

Documentation:

- Use `sphinx.ext.autosectionlabel` to add anchor ({pr}`272`).
- Start to use IPython Sphinx Directive ({pr}`258`, {pr}`259`, {pr}`260`).
- Drop python module index html page ({pr}`256`).
- Small patches to documentation ({pr}`245`, {pr}`251`, {pr}`255`, {pr}`257`, {pr}`262`, {pr}`263`, {pr}`267`, {pr}`286`).
- Fix these doc doesn't exist in dtoolkit ({pr}`244`).
- Fix documentation building environment ({pr}`243`).

## [Version 0.0.3] (2021-10-21)

New features and improvements:

- Add new accessor method {meth}`~dtoolkit.accessor.dataframe.top_n` ({pr}`217`, {pr}`218`, {pr}`219`).
- Add new series accessor method {meth}`~dtoolkit.accessor.series.bin` ({pr}`213`, {pr}`216`).

Documentation:

- Add a new documentation about `Workflow`, see [Automated `Pipeline`: `AutoML`](https://my-data-toolkit.readthedocs.io/en/v0.0.3/guide/automl.html) ({pr}`236`, {pr}`237`).
- Add a new documentation about `AutoML`, see [`Transformer` and `Pipeline` Brief Description](https://my-data-toolkit.readthedocs.io/en/v0.0.3/guide/transformer_description.html) ({pr}`235`, {pr}`237`).
- Update the description of dtoolkit ({pr}`234`, {pr}`241`).
- Add an introduction for {meth}`~dtoolkit.transformer` ({pr}`232`, {pr}`233`).
- Generate sphinx python model index, see [py-modindex](https://my-data-toolkit.readthedocs.io/en/v0.0.3/py-modindex.html) ({pr}`231`).
- Add an introduction for {meth}`~dtoolkit.geography.geographic_buffer`, see [What is the Geographic Buffer?](https://my-data-toolkit.readthedocs.io/en/v0.0.3/guide/geographic_buffer.html) ({pr}`229`).
- Let class method doc could show ({pr}`226`).
- Add `CHANGELOG.md` file ({pr}`222`).
- Change API URL, from `reference/api/geography/dtoolkit.geography.geographic_buffer.html` to `reference/api/dtoolkit.geography.geographic_buffer.html` ({pr}`225`).
- Remove extra `*` in example's doc ({pr}`215`, {pr}`227`).

Maintenance development:

- New CI pipeline ({pr}`238`, {pr}`239`, {pr}`240`).
- Add auto releases workflows ({pr}`224`).
- Use versioneer to control software version ({pr}`223`).
- Support geopandas >= 0.9.0 ({pr}`220`, {pr}`221`).

## [Version 0.0.2] (2021-9-2)

Highlights of this release:

- Now DToolKit supports py3.9, works with Python >= 3.7 ({pr}`211`).

New features and improvements:

- Add {meth}`~dtoolkit.transformer._util.transform_series_to_frame` function series to dataframe, keep the data structure in the pipeline data stream is still **DataFrame** ({pr}`202`).
- Make a generic array to frame transform function ({pr}`193`, {pr}`198`).
- Simplify base {class}`~dtoolkit.transformer.base.Transformer`, move `Transformer`'s `__init__` and `fit` to {class}`~dtoolkit.transformer.base.MethodTF` ({pr}`192`).
- Let {meth}`~dtoolkit.transformer.MethodTF.update_invargs` could could use the old arguments when new are empty ({pr}`191`).

API changes:

- Move {meth}`~dtoolkit.transformer._util.isin` to `dtoolkit/accessor/_util.py` ({pr}`200`).
- Drop `istype` ({pr}`189`).

Bug fixes:

- Fix error typing cause vscode plugin can't show function's documentation ({pr}`203`, {pr}`205`).
- Fix `pip show dtoolkit` error homepage name ({pr}`201`).

Typing annotations:

- Add `OneDimArray` and `TwoDimArray` typing ({pr}`209`).
- Add `GeoSeriesOrGeoFrame` typing ({pr}`207`).
- Add `SeriesOrFrame` typing ({pr}`206`).
- Specific {meth}`~dtoolkit.transformer.make_union` input is a list of {class}`~dtoolkit.transformer.Transformer` ({pr}`199`).
- Rich {meth}`~dtoolkit.transformer.MethodTF.transform`'s annotations ({pr}`197`).
- Fix {meth}`~dtoolkit.util.multi_if_else`' `if_condition_return` parameter annotation ({pr}`195`).
- Rremove `PandasType` and `GeoPandasType` ({pr}`190`).
- Fix {meth}`dtoolkit.transformer._util.isin`'s annotation ({pr}`188`).
- Let {meth}`dtoolkit.transformer._util.isin`'s `axis` could accept `str` type ({pr}`188`).

Documentation:

- `dropinf`'s `inf` could be any `inf`, not only `np.inf` ({pr}`197`).
- Update `README.md` contents ({pr}`185`).

Maintenance development:

- Use single name style whatever script or folder ({pr}`210`).
- Use absolute path to import parent level folder script ({pr}`204`).
- Drop useless comments in test files, these comments are overtime ({pr}`187`).
- Simplify `setup.py` contents ({pr}`185`).

[Version 0.0.20]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.19...v0.0.20
[Version 0.0.19]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.18...v0.0.19
[Version 0.0.18]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.17...v0.0.18
[Version 0.0.17]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.16...v0.0.17
[Version 0.0.16]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.15...v0.0.16
[Version 0.0.15]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.14...v0.0.15
[Version 0.0.14]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.13...v0.0.14
[Version 0.0.13]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.12...v0.0.13
[Version 0.0.12]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.11...v0.0.12
[Version 0.0.11]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.10...v0.0.11
[Version 0.0.10]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.9...v0.0.10
[Version 0.0.9]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.8...v0.0.9
[Version 0.0.8]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.7...v0.0.8
[Version 0.0.7]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.6...v0.0.7
[Version 0.0.6]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.5...v0.0.6
[Version 0.0.5]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.4...v0.0.5
[Version 0.0.4]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.3...v0.0.4
[Version 0.0.3]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.2...v0.0.3
[Version 0.0.2]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.1...v0.0.2
