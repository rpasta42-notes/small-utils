#!/bin/bash

cd pywatch
./install.sh
cd ..

cd vivie-vim-view-saver
./install.sh
cd ..

cd bin
chmod a+x *
cp * /usr/bin
cd ..
