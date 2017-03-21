#!/bin/bash

cd pywatch
./install.sh
cd ..

cd vivie-vim-view-saver
./install.sh
cd ..

cd bin
sudo chmod a+x *
sudo cp * /usr/bin
cd ..
