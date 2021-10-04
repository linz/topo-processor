# Topo Processor

[![GitHub Actions Status](https://github.com/linz/topo-processor/workflows/Build/badge.svg)](https://github.com/linz/topo-processor/actions)
[![Alerts](https://badgen.net/lgtm/alerts/g/linz/topo-processor?icon=lgtm&labelColor=2e3a44&label=Alerts&color=3dc64b)](https://lgtm.com/projects/g/linz/topo-processor/context:python)
[![Dependabot Status](https://badgen.net/dependabot/linz/topo-processor?icon=dependabot&labelColor=2e3a44&color=blue)](https://dependabot.com)
[![License](https://badgen.net/github/license/linz/processor-aerial-imagery?labelColor=2e3a44&label=License)](https://github.com/linz/topo-processor/blob/master/LICENSE)
[![Conventional Commits](https://badgen.net/badge/Commits/conventional?labelColor=2e3a44&color=EC5772)](https://conventionalcommits.org)
[![Code Style](https://badgen.net/badge/Code%20Style/black?labelColor=2e3a44&color=000000)](https://github.com/psf/black)

## Description

The Topo Processor is a collection of small components that can be combined together to create a pipeline.

These components include transforming data into cloud optimised formats like [COG](https://www.cogeo.org/) and the creation of [STAC](http://stacspec.org/) metadata.

## Installation

### Requirements

#### Poetry

Follow the [Poetry installation guide](https://python-poetry.org/docs/).

#### Docker

Follow the [Docker Engine installation guide (Ubuntu)](https://docs.docker.com/engine/install/ubuntu/).

### Recommended

- [node](https://nodejs.org/en/about/)
- [pretty-json-log](https://npmjs.com/package/pretty-json-log)

### Use poetry to install

```shell
poetry shell

poetry install
```

## Usage

### Upload

```shell
# Run in a virtual environment (poetry shell).
./upload --source source_path --datatype data.type --target target_folder
```

```shell
# For help:
./upload --help
```

```shell
# To see all logs in a tidy format, use pretty-json-log:
./upload --source source_path --datatype data.type --target target_folder --verbose | pjl
```

The following source and target combinations can be used:

| Source        | Target        |
| ------------- |:-------------:|
| s3            | s3            |
| s3            | local         |
| local         | local         |
| local         | s3            |
