# Changelog

## [Version 0.0.3] (2021-??-??)

New features and improvements:

- Add new series accessor method `bin` ({pr}`213`, {pr}`216`).
- Add new accessor method `top_n` ({pr}`217`, {pr}`218`, {pr}`219`)

Documentation:

- Let class method doc could show ({pr}`226`).
- Add changelog file ({pr}`222`).
- Change API URL, from `reference/api/geography/dtoolkit.geography.geographic_buffer.html` to `reference/api/dtoolkit.geography.geographic_buffer.html` ({pr}`225`).
- Remove extra `*` in example's doc ({pr}`215`, {pr}`227`).

Maintenance development:

- Add auto releases workflows ({pr}`224`).
- Use versioneer to control software version ({pr}`223`).
- Support geopandas >= 0.9.0 ({pr}`220`, {pr}`221`).

## [Version 0.0.2] (2021-9-2)

Now DToolKit supports py3.9, works with Python >= 3.7 ({pr}`211`).

New features and improvements:

- Add `transform_series_to_frame` function series to dataframe, keep the data structure in the pipeline data stream is still **DataFrame** ({pr}`202`).
- Make a generic array to frame transform function ({pr}`193`, {pr}`198`).
- Simplify base `Transformer`, move `Transformer`'s `__init__` and `fit` to `MethodTF` ({pr}`192`).
- Let `update_invargs` could could use the old arguments when new are empty ({pr}`191`).

API changes:

- Move `isin` to `dtoolkit/accessor/_util.py` ({pr}`200`).
- Drop `istype` ({pr}`189`).

Bug fixes:

- Fix error typing cause vscode plugin can't show function's documentation ({pr}`203`, {pr}`205`).
- Fix `pip show dtoolkit` error homepage name ({pr}`201`).

Typing annotations:

- Add `OneDimArray` and `TwoDimArray` typing ({pr}`209`).
- Add `GeoSeriesOrGeoFrame` typing ({pr}`207`).
- Add `SeriesOrFrame` typing ({pr}`206`).
- Specific `make_union` input is a list of `Transformer` ({pr}`199`).
- Rich `transform`'s annotations ({pr}`197`).
- Fix `multi_if_else`' `if_condition_return` parameter annotation ({pr}`195`).
- Rremove `PandasType` and `GeoPandasType` ({pr}`190`).
- Fix `isin`'s annotation ({pr}`188`).
- Let `isin`'s `axis` could accept `str` type ({pr}`188`).

Documentation:

- `inf` could be any `inf`, not only `np.inf` ({pr}`197`).
- Update README.md contents ({pr}`185`).

Maintenance development:

- Use single name style whatever script or folder ({pr}`210`).
- Use absolute path to import parent level folder script ({pr}`204`).
- Drop useless comments in test files, these comments are overtime ({pr}`187`).
- Simplify setup.py contents ({pr}`185`).

[Version 0.0.3]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.2...v0.0.3
[Version 0.0.2]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.1...v0.0.2
