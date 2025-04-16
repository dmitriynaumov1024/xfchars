#!/bin/bash

APP_NAME="xfchars"
APP_VERSION="1.0"
APP_REVISION="1"
BUILD_DIR="./build/${APP_NAME}-${APP_VERSION}-${APP_REVISION:-1}"
TARGET_FS_PREFIX_LIB="/usr/lib/python3/dist-packages/${APP_NAME}"
TARGET_FS_PREFIX_BIN="/usr/bin"
DEBIAN_PREFIX="/DEBIAN"

test -d ${BUILD_DIR} && rm -rf ${BUILD_DIR}

mkdir -p "${BUILD_DIR}${DEBIAN_PREFIX}"
mkdir -p "${BUILD_DIR}${TARGET_FS_PREFIX_LIB}"
mkdir -p "${BUILD_DIR}${TARGET_FS_PREFIX_BIN}"

cp ./deb/control.txt "${BUILD_DIR}${DEBIAN_PREFIX}/control"
cp -r ./app/* "${BUILD_DIR}${TARGET_FS_PREFIX_LIB}/"
cp ./bin/main.py "${BUILD_DIR}${TARGET_FS_PREFIX_BIN}/${APP_NAME}"
chmod 755 "${BUILD_DIR}${TARGET_FS_PREFIX_BIN}/${APP_NAME}"

dpkg-deb --build --root-owner-group ${BUILD_DIR}
