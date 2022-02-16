# Topo Processor

[![GitHub Actions Status](https://github.com/linz/topo-processor/workflows/Build/badge.svg)](https://github.com/linz/topo-processor/actions)
[![Alerts](https://badgen.net/lgtm/alerts/g/linz/topo-processor?icon=lgtm&labelColor=2e3a44&label=Alerts&color=3dc64b)](https://lgtm.com/projects/g/linz/topo-processor/context:python)
[![Dependabot Status](https://badgen.net/dependabot/linz/topo-processor?icon=dependabot&labelColor=2e3a44&color=blue)](https://dependabot.com)
[![License](https://badgen.net/github/license/linz/processor-aerial-imagery?labelColor=2e3a44&label=License)](https://github.com/linz/topo-processor/blob/master/LICENSE)
[![Conventional Commits](https://badgen.net/badge/Commits/conventional?labelColor=2e3a44&color=EC5772)](https://conventionalcommits.org)
[![Code Style](https://badgen.net/badge/Code%20Style/black?labelColor=2e3a44&color=000000)](https://github.com/psf/black)

## Description

The Topo Processor is a collection of small components that can be combined together to create a pipeline. It can be run on a local workstation or using AWS Batch.

These components include transforming data into cloud optimised formats like [COG](https://www.cogeo.org/) and the creation of [STAC](http://stacspec.org/) metadata.

## Installation

### Requirements ro run Topo Processor locally:

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

## Configuration

The global user configuration is defined by environment variables, example environment variables are found in the `.env` file.

### Requirements ro run Topo Processor using AWS Batch:

#### Software

```shell
yarn

yarn build
```

#### AWS Batch Stack deployment

**_NOTE:_** [AWS deployment is done automatically through GitHub Actions.](#aws-deployment--ci--cd)

To deploy the Batch via CDK locally:



On the AWS account you are logged into

```shell
yarn build

npx cdk deploy
```

### AWS Roles

To allow the system to perform cross account AWS request, you'll need to config AWS roles inside of a AWS SSM parameter.

This configuration parameter can be referenced via `$LINZ_SSM_BUCKET_CONFIG_NAME`

## Usage

### AWS Batch Job Submission

**_NOTE:_** Only the `upload` command is implemented to run on AWS Batch at the moment. Currently the job submission is restricted to only one job.

**_NOTE:_** You may need to set the `AWS_REGION` environment variable to your region.

```shell
node ./build/infra/src/submit.js
```

### Upload command

**_NOTE:_** In its developing phase for using the `LDS Cache`, the `upload` command will be restricted to a run per `survey` and only for the `Historical Imagery` layer.

The user has to specify the survey path (where the data is) as a `--source` and it will be validated against the latest version of metadata. The `--datatype` has to be `historical.imagery`. The user also have to specify a target folder for the output.

```shell
# Run in a virtual environment (poetry shell):
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

| Source | Target |
| ------ | :----: |
| s3     |   s3   |
| s3     | local  |
| local  | local  |
| local  |   s3   |

### Validate

**_NOTE:_** This command is currently only implemented for `Historical Imagery`. Other layers will come later.

This command runs a validation against a layer. It gets the layer last version metadata and generates the corresponding STAC objects on the fly. Then, it runs a JSON schema validation (using [jsonschema-rs](https://github.com/Stranger6667/jsonschema-rs)) for the `Items` and `Collections`. It outputs the errors and their recurrences grouped by JSON schemas as:

```json
"errors": {"https://stac.linz.govt.nz/v0.0.11/aerial-photo/schema.json": {"'aerial-photo:run' is a required property": 4, "'aerial-photo:sequence_number' is a required property": 10}
```

To validate another version than the latest one, specify the metadata csv file wanted to be validated by using the `--metadata` argument.

The following command have to be run in a virtual environment (poetry shell):

```shell
# Run default:
./validate
```

```shell
# Run against a specific version (can be a s3 or local file):
./validate --metadata s3://bucket/layer_id/metadata_file.csv
```

```shell
# Run against the `Items` only:
./validate --item
```

```shell
# Run against the `Collections` only:
./validate --collection
```

```shell
# For help:
./validate --help
```

```shell
# To see all logs in a tidy format, use pretty-json-log:
./validate --verbose | pjl
```

```shell
# To record the output in an external file:
./validate | tee output.file
```


## AWS Deployment / CI / CD

CI/CD is used to deploy into AWS, to trigger a deployment create a new "release:" commit and merge it to master

A helpful utility script is in `./scripts/version.bump.sh` to automate this process

```bash
./scripts/version.bump.sh
# Push branch release/v:versionNumber
git push
# Create the pull request
gh pr create
# Merge to master
```
