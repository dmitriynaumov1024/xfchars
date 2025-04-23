#!/bin/bash

function exit_reason {
    echo "$2"
    exit $1
}

function exists {
    which "$1" >/dev/null
    return $?
}

exists python3 || exit_reason 1 "Python3 not found. Install python3 to proceed." 

function get_configs {
    # app name, version, revision was delegated to this
    python3 -B -c "import app.tui.info as ainfo; print(ainfo.APP_NAME, ainfo.APP_VERSION, ainfo.APP_REVISION, sep=';')"
}

function build {
    IFS=";" read APP_NAME APP_VERSION APP_REVISION

    export APP_NAME
    export APP_VERSION
    export APP_REVISION

    BUILD_DIR="./build/${APP_NAME}-${APP_VERSION}.${APP_REVISION}"
    TARGET_FS_PREFIX_LIB="/usr/lib/python3/dist-packages/${APP_NAME}"
    TARGET_FS_PREFIX_BIN="/usr/bin"
    DEBIAN_PREFIX="/DEBIAN"

    test -d ${BUILD_DIR} && rm -rf ${BUILD_DIR}

    mkdir -p "${BUILD_DIR}${DEBIAN_PREFIX}"
    mkdir -p "${BUILD_DIR}${TARGET_FS_PREFIX_LIB}"
    mkdir -p "${BUILD_DIR}${TARGET_FS_PREFIX_BIN}"

    cat ./deb/control.txt | envsubst > "${BUILD_DIR}${DEBIAN_PREFIX}/control"
    cp -r ./app/* "${BUILD_DIR}${TARGET_FS_PREFIX_LIB}/"
    cp ./bin/main.py "${BUILD_DIR}${TARGET_FS_PREFIX_BIN}/${APP_NAME}"
    chmod 755 "${BUILD_DIR}${TARGET_FS_PREFIX_BIN}/${APP_NAME}"

    dpkg-deb --build --root-owner-group ${BUILD_DIR}
}

get_configs | build
