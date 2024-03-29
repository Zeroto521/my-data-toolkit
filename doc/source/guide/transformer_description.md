# Transformer and Pipeline Brief Description

![Real world Pipeline](https://cdn.pixabay.com/photo/2015/03/19/17/50/winter-681175_960_720.jpg)

> Image by [Robson Machado](https://pixabay.com/photos/winter-alaska-pipeline-oil-snow-681175/)

## What is Transformer?

The {class}`~dtoolkit.transformer.Transformer` is a protocol that defines the input port and output port.

It is just like a **pipe** in the real world.

![Transformer methods](../_static/transformer-method.svg)

Direction:

- `fit`, `transform` and `fit_transform` go forward.
- `inverse_transform` goes backward.

Minimal methods require:

- `transform` and `fit_transform` are necessary methods.
- `fit` and `inverse_transform` are optional method.

## What is Pipeline?

The {class}`~sklearn.pipeline.Pipeline` combines each port of {class}`~dtoolkit.transformer.Transformer` into a stream.

You could control the **direction** of the stream to go forward or backward.
And you could stop the stream where you want and check its **internal**.

It is just like a real **pipeline** in the real world.

![Pipeline](https://raw.githubusercontent.com/rasbt/python-machine-learning-book/master/code/ch06/images/06_01.png)

> From [Python Machine Learning Book Chapter 6](https://nbviewer.org/github/rasbt/python-machine-learning-book/blob/master/code/ch06/ch06.ipynb)

## What transformer does?

{class}`dtoolkit.transformer` does two things:

- Let {class}`~pandas.DataFrame` as the basic data structure of {class}`~dtoolkit.transformer.Transformer`.
- Transform all methods / algorithms into {class}`~dtoolkit.transformer.Transformer`.

### DataFrame in and DataFrame out

{class}`sklearn.base.TransformerMixin` let `array-like` in `array-like` out.

As if there has a pipeline `[DropColumnTF, DropRowTF, Map, MapColumnTF]`.
If we put a {class}`~pandas.DataFrame` into this pipeline and want to debug and check the preprocessing data. However, it is hard to trace the data changing. There is only left data itself, other information is missing.

It is important to keep trace the data changing. So {class}`dtoolkit.transformer` would keep the {class}`~pandas.DataFrame` unchanged in stream, let {class}`~pandas.DataFrame` in and {class}`~pandas.DataFrame` out.

![Transformer architecture](../_static/transformer-architecture.svg)

### Engineering of Data Preprocessing

{class}`dtoolkit.transformer` could handle what a mess codes of data preprocessing codes.

A surprise comes here. It can face to the engineering of data preprocessing.

- {class}`~pandas.DataFrame` gives a good view to show the data.
- {class}`~dtoolkit.transformer.Transformer` contains the processing or transforming methods.
- {class}`~sklearn.pipeline.Pipeline` as the manager to control the running.

![DToolKit for transformer](../_static/transformer-with-pipeline.svg)

## What's Next - Future Features

There are two articles about some future features of `Transformer` and `Pipeline`.

- {ref}`Automated Pipeline: AutoML`
- {ref}`Data Visual Modeling: Workflow`
