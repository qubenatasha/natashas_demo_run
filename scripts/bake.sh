#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $NATASHAS_DEMO_RUN_DOCKER_IMAGE_LOCAL

docker build -t $NATASHAS_DEMO_RUN_DOCKER_IMAGE_LOCAL:$NATASHAS_DEMO_RUN_IMAGE_VERSION . 
