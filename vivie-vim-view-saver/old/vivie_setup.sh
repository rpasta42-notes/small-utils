#!/bin/bash

#echo everything
set -x


mkdir -p ~/.vim/view


view_dir_path=$(eval echo "~/.vim/view/")

notes_n=1
view_name="~=+orgs=+rpasta42-personal=+mynotes=+numbered=+$notes_n.txt="
notes_view_path=${view_dir_path}/${view_name}
rm $notes_view_path
cp numbered/${notes_n}.txt.vim $notes_view_path
