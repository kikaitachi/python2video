#!/usr/bin/env bash

SCRIPT_DIR=$(realpath -m "$(dirname $0)")
FILE_NAME=${1}

"${SCRIPT_DIR}/python2trace.py" "${FILE_NAME}" | "${SCRIPT_DIR}/trace2video.py" "${FILE_NAME}"
