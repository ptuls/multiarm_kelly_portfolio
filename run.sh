#!/usr/bin/env bash

# Runs the notebook server.
set -eu
set -o pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
IMAGE_NAME="kelly-multiarm"
# Note that this user is the default as defined in jupyter/base-notebook. Using anything else here
# will probably break things.
NB_USER="jovyan"

# Map the code into the container, so that restarting kernels will reload externally updated code.
HOST_CODE="${SCRIPT_DIR}/docker"
CONTAINER_CODE="/opt/conda/lib/python3.6/site-packages/app"


error() {
  local prog
  prog=$(basename "$0")
  echo "$(date '+[%Y-%m-%d %H:%M:%S]') ${prog} ERROR: $*" >&2
  exit 1
}


usage() {
  local prog
  prog=$(basename "$0")
  cat <<EOF
Usage: ${prog} [--build-only] [--entrypoint SCRIPT]

Builds a Docker container and runs the unit-tests, then a Jupyter
notebook server is run. If -s is set, executes and exports scheduled
notebooks rather than running the server. If -b is set, then we
only build and do not execute notebooks or run a Jupyter server.
EOF
}


build() {
  echo ${SCRIPT_DIR}
  pushd "${SCRIPT_DIR}/docker"
  make -f Makefile clean
  docker build -t "${IMAGE_NAME}" .
  docker run \
    --volume "${HOST_CODE}:${CONTAINER_CODE}" \
    "${IMAGE_NAME}" flake8 --ignore=E501 ${CONTAINER_CODE}
  popd
}

main() {
  if [[ "$*" == "--help" || "$*" == "-h" ]]; then
    usage
    exit
  fi

  local workdir="/home/${NB_USER}/work"
  local entrypoint=start-notebook.sh
  local build_only=false
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
      --help)
        usage
        exit 1
        ;;
      --entrypoint)
        entrypoint="$workdir/$2"
        shift
        ;;
      --build-only)
        build_only=true
        ;;
      *) error "unknown option $1" ;;
    esac
    shift
  done

  build

  if [[ "$build_only" = true ]]; then
    exit 0
  fi

  pushd "${SCRIPT_DIR}"
  docker run \
    --hostname localhost \
    --publish 8888:8888 \
    --user root \
    --env NB_UID="${UID}" \
    --env NB_USER="${NB_USER}" \
    --volume "${SCRIPT_DIR}:/home/${NB_USER}/work" \
    --volume "${HOST_CODE}:${CONTAINER_CODE}" \
    --workdir "${workdir}" \
    "${IMAGE_NAME}" ${entrypoint}
  popd
}

main "$@"
