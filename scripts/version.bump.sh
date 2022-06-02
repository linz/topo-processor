#!/bin/bash
#
# Version bump the repo and create a branch ready for pull request
#
set -e

git checkout master
git pull --rebase

# Validate that there are actually changes to be made, this will fail if nothing needs publishing
npm version -m 'release: %s' minor

# Set the version environment variable
CURRENT_VERSION=$(node -p "require('./package.json').version")

# Bump the version in Poetry pyproject.toml file
poetry version ${CURRENT_VERSION}

# Write version to a file for Topo Processor to use
echo v${CURRENT_VERSION} | tee VERSION

# Commit the changed files
git commit -a --amend --no-edit

# Checkout a new release branch
git checkout -b release/v${CURRENT_VERSION}

# This tag will be created once the pull request is merged
git tag -d v${CURRENT_VERSION}
