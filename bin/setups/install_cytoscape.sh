#!/bin/bash
# -*- coding: utf-8 -*-
VERSION="3.5.0"
_VERSION=${VERSION//./_} #3.4.0 => 3_4_0

PWD=`sudo pwd`
cd `dirname $0`

wget -P ../tmp/ http://chianti.ucsd.edu/cytoscape-"$VERSION"/Cytoscape_"$_VERSION"_unix.sh > /dev/null 2>&1
sudo bash ../tmp/Cytoscape_"$_VERSION"_unix.sh

echo "Apps -> App Manager -> check CyREST -> install"

cd $PWD

exit 0
