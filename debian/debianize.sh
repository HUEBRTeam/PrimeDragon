#!/bin/bash

PKG_NAME="primedragon"

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/../"
DIR="/tmp/package/${PKG_NAME}"
APPDIR="${DIR}/var/www/primedragon/"
LIBDIR="${DIR}/usr/"
DEBIAN="${DIR}/DEBIAN"

rm -rf ${DIR}

mkdir -p ${DIR}
mkdir -p ${DEBIAN}
mkdir -p ${APPDIR}
mkdir -p ${LIBDIR}

G_REV=`git rev-parse --short=8 HEAD`
DATE=`date +"%Y%m%d%H%M%S"`
VERSION="1-git+${DATE}.${G_REV}~$1"

cat <<- EOF > ${DEBIAN}/control
Package: ${PKG_NAME}
Priority: optional
Maintainer: The Unknown <unknown@anonymous.com>
Architecture: i386
Description: The dragon has been released for Prime!
Version: ${VERSION}
Depends: apache2, libapache2-mod-php5, python, python-pip
EOF

DEB_PKG="${PKG_NAME}_${VERSION}_i386.deb"

cp postinst ${DEBIAN}

cp -rf ${REPO_DIR}/* ${APPDIR}
cp -rf ${REPO_DIR}/lib/x32/* ${LIBDIR}
rm -fr ${APPDIR}/*.pyc
rm -fr ${APPDIR}/lib/

dpkg-deb -b ${DIR} ./${DEB_PKG}

echo "Generated ${DEB_PKG}"

rm -fr ${DIR}

mkdir -p ${DIR}
mkdir -p ${DEBIAN}
mkdir -p ${APPDIR}
mkdir -p ${LIBDIR}

cat <<- EOF > ${DEBIAN}/control
Package: ${PKG_NAME}
Priority: optional
Maintainer: The Unknown <unknown@anonymous.com>
Architecture: amd64
Description: The dragon has been released for Prime!
Version: ${VERSION}
Depends: apache2, libapache2-mod-php5, python, python-pip
EOF

DEB_PKG="${PKG_NAME}_${VERSION}_amd64.deb"

cp postinst ${DEBIAN}

cp -rf ${REPO_DIR}/* ${APPDIR}
cp -rf ${REPO_DIR}/lib/x64/* ${LIBDIR}
rm -fr ${APPDIR}/*.pyc
rm -fr ${APPDIR}/lib/

dpkg-deb -b ${DIR} ./${DEB_PKG}

echo "Generated ${DEB_PKG}"

rm -fr ${DIR}/*
