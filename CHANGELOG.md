# Changelog

## [Version 0.0.11] (2022-1-25)

Small bug-fix:

- Fix jupyter notebook can't render ({pr}`438`).

New features and improvements:

- Simplify `OneHotEncoder` examples and inputs ({pr}`434`).
- `FeatureUnion` would merge all into one DataFrame and the index would use the common part ({pr}`433`).

Maintenance development:

- Simplify linting workflow ({pr}`437`).

## [Version 0.0.10] (2022-1-21)

Use `main` replace of `master` as the base branch ({issue}`412`, {pr}`413`).

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

Use `squash merge` to keep a cleaning git commit history ({issue}`386`).

Highlights of this release:

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

Contribuing development:

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

- Update pre-commit commit message ({pr}`371`).
- Enable labeled 'auto-merged' PR could merge master branch into PR ({pr}`368`, {pr}`370`, {pr}`372`, {pr}`375`).
- Github action runner update ({pr}`365`, {pr}`366`, {pr}`367`, {pr}`369`, {pr}`383`).
- Auto update github action runner ({pr}`360`, {pr}`364`).
- Pre-commit hooks auto update ({pr}`359`).
- Let git choose the default branch ({pr}`376`).

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

Now DToolKit supports py3.9, works with Python >= 3.7 ({pr}`211`).

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
