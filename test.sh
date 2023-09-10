#!/bin/bash
set -e

./reset.sh

pytest

pushd client
  yarn test --run
popd

pushd behave
  behave
popd
