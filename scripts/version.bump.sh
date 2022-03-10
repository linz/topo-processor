#!/bin/bash
#
# Version bump the repo and create a branch ready for pull request
#
set -e

git checkout master
git pull --rebase

# Validate that there are actually changes to be made, this will fail if nothing needs publishing
npm version -m 'release: %s' minor

CURRENT_VERSION=$(node -p "require('./package.json').version")
git checkout -b release/v${CURRENT_VERSION}

# This tag will be created once the pull request is merged
git tag -d v${CURRENT_VERSION}

# Write version to a file for Topo Processor to use
echo v${CURRENT_VERSION} | tee VERSION
