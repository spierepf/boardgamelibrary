#!/bin/bash
set -e

pytest

pushd client
  yarn test --run
popd

pushd behave
  behave
popd
