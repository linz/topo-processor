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

### Requirements to run Topo Processor locally:

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

### Requirements to run Topo Processor using AWS Batch:

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

To allow the system to perform cross account AWS requests, you'll need to config AWS roles inside of an AWS SSM parameter.

This configuration parameter can be referenced via `$LINZ_SSM_BUCKET_CONFIG_NAME`

## Usage

### AWS Batch Job Submission

**_NOTE:_** Only the `upload` command is implemented to run on AWS Batch. Currently the job submission is restricted to only one job per survey.

**_NOTE:_** You may need to set the `AWS_REGION` environment variable to your region.

```shell
# Passing survey IDs as argument
node ./build/infra/src/submit.js surveyId1 surveyId3 [...]

# Passing S3 folder as argument
node ./build/infra/src/submit.js s3://my-bucket/backup2/surveyId1/ s3://my-bucket/backup4/surveyId3/ [...]
```

### `upload`

**_NOTE:_** The `upload` command is restricted to a run per `survey` and only for the `Historical Imagery` layer. To run multiple surveys, please refere to `AWS Batch` described above.

| Argument                    |                                           Description                                           |
| --------------------------- | :---------------------------------------------------------------------------------------------: |
| `-s` or `--source`          | The source of the data to import. Can be a `survey ID` or a path (local or `s3`) to the survey. |
| `-d` or `--datatype`        |        The datatype of the upload. _Only `imagery.historic` is available at the moment._        |
| `-t` or `--target`          |                   The target local directory path or `s3` path of the upload.                   |
| `-cid` or `--correlationid` |              OPTIONAL. The `correlation ID` of the batch job. _`AWS Batch` only._               |
| `-m` or `--metadata`        |                        OPTIONAL. The metadata file (local or `s3`) path.                        |
| `-f` or `--footprint`       |               TESTING PURPOSE. The footprint metadata file (local or `s3`) path.                |
| `--force`                   |   Flag to force the upload even if some data are invalid (some items might not be uploaded).    |
| `-v` or `--verbose`         |                                   Flag to display trace logs.                                   |

The user has to specify the survey id or path (where the data is) as a `--source` and it will be validated against the latest version of metadata. A metadata file path can also be specified by using `--metadata` if the LDS cache version one is not wanted. The `--datatype` has to be `imagery.historic`. The user also has to specify a target folder for the output.

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

### `add` (Geostore)

This command allows to add a survey to the [Geostore](https://github.com/linz/geostore) by using the [Geostore API](https://github.com/linz/geostore/blob/master/USAGE.md).

**_Prerequisites:_** The survey has to be processed by the `upload` command first. The output files of the `upload` is what will be exported to the `Geostore`.

| Argument              |                      Description                       |
| --------------------- | :----------------------------------------------------: |
| `-s`, `--source` TEXT |     The s3 path to the survey to export [required]     |
| `-r`, `--role` TEXT   | The ARN role to access to the source bucket [required] |
| `-c`, `--commit`      |  Use this flag to commit the creation of the dataset   |
| `-v`, `--verbose`     |           Use verbose to display debug logs            |

```bash
poetry run add -s "s3://bucket/survey-path/" -r "arn:aws:iam::123456789:role/read-role"
```

### `status` (Geostore)

This is to follow the current upload status to the `Geostore` for a particular `dataset` version. You may have to run it several times as the status gets updated.

| Argument                     |                                   Description                                    |
| ---------------------------- | :------------------------------------------------------------------------------: |
| `-a`, `--execution-arn` TEXT | The execution ARN received from the Geostore after invoking an upload [required] |
| `-v`, `--verbose`            |                        Use verbose to display debug logs                         |

**_NOTE:_** The command to run is given in the logs after calling successfully the `add` command:

```json
"info": "To check the export status, run the following command 'poetry run status -arn arn:aws:states:ap-southeast-2:632223577832:execution:ABCD'"
```

### `list` (Geostore)

It gives you the information for one or all the datasets created on the `Geostore`.

| Argument                |                                         Description                                          |
| ----------------------- | :------------------------------------------------------------------------------------------: |
| `-s`, `--survey` TEXT   |                                     The survey to filter                                     |
| `-d`, `--datatype` TEXT | The datatype of the upload. _Only `imagery.historic` is available at the moment._ [required] |
| `-v`, `--verbose`       |                              Use verbose to display debug logs                               |

```bash
poetry run list [-s ID123ABC]
```

### `delete` (Geostore)

Delete a dataset from the `Geostore`. Only if the dataset does not contain any version. To delete a dataset which contains a version, contact the **Geostore** support.

| Argument                  |                       Description                       |
| ------------------------- | :-----------------------------------------------------: |
| `-d`, `--dataset-id` TEXT |           The dataset id to delete [required]           |
| `-c`, `--commit`          | Use this flag to commit the suppression of the dataset. |
| `-v`, `--verbose`         |            Use verbose to display debug logs            |

```bash
poetry run delete -d ID123ABC [--commit]
```

### `validate`

**_NOTE:_** This command is currently only implemented for `Historical Imagery`. Other layers will come later.

This command runs a validation against a layer. It gets the layer last version metadata and generates the corresponding STAC objects on the fly. Then, it runs a JSON schema validation (using [jsonschema-rs](https://github.com/Stranger6667/jsonschema-rs)) for the `Items` and `Collections`. It outputs the errors and their recurrences grouped by JSON schemas as:

```json
"errors": {"https://stac.linz.govt.nz/v0.0.11/aerial-photo/schema.json": {"'aerial-photo:run' is a required property": 4, "'aerial-photo:sequence_number' is a required property": 10}
```

To validate another version than the latest one, specify the metadata csv file wanted to be validated by using the `--metadata` argument.

The following command have to be run in a virtual environment (poetry shell):

```shell
# Run default:
poetry run validate
```

```shell
# Run against a specific version (can be a s3 or local file):
poetry run validate --metadata s3://bucket/layer_id/metadata_file.csv
```

```shell
# Run against the `Items` only:
poetry run validate --item
```

```shell
# Run against the `Collections` only:
poetry run validate --collection
```

```shell
# For help:
poetry run validate --help
```

```shell
# To see all logs in a tidy format, use pretty-json-log:
poetry run validate --verbose | pjl
```

```shell
# To record the output in an external file:
poetry run validate | tee output.file
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
