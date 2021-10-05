# Changelog

## [Version 0.0.2] (2021-9-2)

Now DToolKit supports py3.9, works with Python >= 3.7 (#211).

New features and improvements:

- Add `transform_series_to_frame` function series to dataframe, keep the data structure in the pipeline data stream is still **DataFrame** (#202).
- Make a generic array to frame transform function (#193, #198).
- Simplify base `Transformer`, move `Transformer`'s `__init__` and `fit` to `MethodTF` (#192).
- Let `update_invargs` could could use the old arguments when new are empty (#191).

API changes:

- Move `isin` to `dtoolkit/accessor/_util.py` (#200).
- Drop `istype` (#189).

Bug fixes:

- Fix error typing cause vscode plugin can't show function's documentation (#203, #205).
- Fix `pip show dtoolkit` error homepage name (#201).

Typing annotations:

- Add `OneDimArray` and `TwoDimArray` typing (#209).
- Add `GeoSeriesOrGeoFrame` typing (#207).
- Add `SeriesOrFrame` typing (#206).
- Specific `make_union` input is a list of `Transformer` (#199).
- Rich `transform`'s annotations (#197).
- Fix `multi_if_else`' `if_condition_return` parameter annotation (#195).
- Rremove `PandasType` and `GeoPandasType` (#190).
- Fix `isin`'s annotation (#188).
- Let `isin`'s `axis` could accept `str` type (#188).

Documentation:

- `inf` could be any `inf`, not only `np.inf` (#197).
- Update README.md contents (#185).

Maintenance development:

- Use single name style whatever script or folder (#210).
- Use absolute path to import parent level folder script (#204).
- Drop useless comments in test files, these comments are overtime (#187).
- Simplify setup.py contents (#185).

[Version 0.0.2]: https://github.com/Zeroto521/my-data-toolkit/compare/v0.0.1...v0.0.2
