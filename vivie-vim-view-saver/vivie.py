#!/usr/bin/env python3

import sh


def translate_path_to_vim(path):
   return path.replace('/', '=+') + '='

def translate_path_from_vim(path):
   return path.replace('=+', '/')[:-1]


#sh.mkdir(
x = sh.ls('-a')

