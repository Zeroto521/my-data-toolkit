# What is the Geographic Buffer?

:::{note}
This tutorial requires basic **GIS** (Geographic Information System) knowledge.
:::

## What is the Buffer?

:::{note}
All buffer of geometries are created on **2D plane**.
:::

A simple graph could show this.

![Buffer](https://desktop.arcgis.com/en/arcmap/latest/tools/analysis-toolbox/GUID-267CF0D1-DB92-456F-A8FE-F819981F5467-web.png)

> From [ArcGIS analysis-toolbox Buffer](https://desktop.arcgis.com/en/arcmap/latest/tools/analysis-toolbox/buffer.htm)

The graph shows the buffer generation of three basic kinds of geometries.

- Point
- Line
- Polygon

And the graph also shows the way to deal with the overlapping relationship of multi-buffers.

## Latitude, Longitude and Earth

This section comes to introduce CRS (Coordinate Reference Systems).

Simply say CRS shows a mapping relationship between 3D ellipsoid Earth and 2D plane.

![CRS](https://docs.qgis.org/2.8/en/_images/projection_families.png)

Some CRSs we have already met, the GPS coordniate references, used in online map:

- `EPSG:4326`: {math}`(120°, 50°)`, spherical reference
- `EPSG:3857`: {math}`(13358338.90m, 6446275.84m)`, projection plane reference

## Non Geographic Buffer

The method of {meth}`geopandas.GeoSeries.buffer` created buffer is not a really buffer in the map.

### Steps to Generate Buffer

Let us select two `EPSG:4326` coordinates and show their buffer on map.

- {math}`(122, 50)`
- {math}`(100, 1)`

Then let us generate {math}`500km` buffers for those two points.

With the following steps:

1. Transform spherical coordinates to projection plane coordinates from `EPSG:4326` to `EPSG:3857`.
2. Generate {math}`500km` buffer via {meth}`~geopandas.GeoSeries.buffer`.
3. Transform CRS back from `EPSG:3857` to `EPSG:4326`.
4. Display on the map.

![Points buffer](../_static/points-buffer.png)

The green one is the non geographic buffer, and the blue one is the geographic buffer.

As we see the green one's diameter is less than {math}`1000km`.

### Problem of Non Geographic Buffer

The following GIF could tell us why the green one is smaller than the blue one.

![Proportions of apparent size and real size (animated)](https://upload.wikimedia.org/wikipedia/commons/e/ee/Worlds_animate.gif)

> From [WikiPedia Mercator Projection](https://en.wikipedia.orgwiki/Mercator_projection)

The [EPSG:3857](https://proj.org/operations/projections/merc.html) is a cylindrical map projection, that cause the area which closes to the equator is the same as real.

## Geographic Buffer

### Use Local Projection CRS

A idea to fix this is to use local projection CRS.
Local projection CRS means build projection CRS for each point.

The Steps to generate buffer would be following.

1. Transform each point of these geometries from default CRS to local projection CRS.
2. Transform them back to default CRS.
3. Do dissolve operation for generated buffers from geometry points.

In this way, it could totally describe the all points in Earth.

However, it would be so **slow** to get such great **precision**. And hard to vectorize this algorithm, because of different local projection CRS.

![Azimuthal Equidistant projection](https://proj.org/_images/aeqd.png)

> From [PROJ Coordinate operations](https://proj.org/operations/projections/aeqd.html)

### Use UTM CRS

Another idea to fix this is to use Universal Transerse Mercator (UTM) projection CRS.

One projection would lose precision, much would slow down. The UTM CRS is a good balance between precision and speed.

It divides into sixty zones across the globe. The speed depends on the geometries where they are.
It would be as quick as a normal speed if the zone of geometries is the same.

![Universal Transerse Mercator](https://proj.org/_images/utm_zones.png)

> From [PROJ Coordinate operations](https://proj.org/operations/projections/utm.html)

That is what the {meth}`~dtoolkit.geoaccessor.geoseries.geobuffer` method does.

What's next? Try to use it.
