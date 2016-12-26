#!/usr/bin/env python3

import sh, sys
from utiltools import shellutils
from utiltools.shellutils import file_exists, read_file
from utiltools.shellutils import expand_link

conf_path = '.vivie.conf'
data_dir = '.vivie/'
avail_cmd_args = ['setup', 'snapshot', 'help', 'status']

vim_view_path = expand_link('~/.vim/view/') + '/'

full_home_path = expand_link('~')

def usage():
   #convert available arguments to string
   cmd_args_str = ''
   for arg in avail_cmd_args:
      cmd_args_str += arg + '|'

   cmd_args_str = cmd_args_str[:-1]

   print('usage: %s [%s]', sys.args[0], cmd_args_str)

def print_help():
   usage()
   print('\tsetup = clone vim view from repo folder')
   print('\tsnapshot = copy vim view files into repo folder')

def path_to_vim(path):
   return path.replace('/', '=+') + '='

def path_from_vim(path):
   return path.replace('=+', '/')[:-1]

def parse_args():
   args = sys.argv

   if len(args) is not 2:
      return None

   if args[1] not in avail_cmd_args:
      return None

   return args[1]

def take_snapshot(file_lst):
   for local_fpath in file_lst:
      print('snapshotting:', local_fpath)
      local_fpath = expand_link(local_fpath).replace(full_home_path, '~')
      print('after cleanup:', local_fpath)

      view_fname = path_to_vim(local_fpath)

      view_fpath = vim_view_path + view_fname
      view_localdest = data_dir + view_fname

      sh.rm('-Rf', view_localdest)
      sh.cp(view_fpath, view_localdest)

def run_setup(file_lst):
   for local_fpath in file_lst:
      print('setting up:', local_fpath)
      local_fpath = expand_link(local_fpath).replace(full_home_path, '~')

      view_fname = path_to_vim(local_fpath)
      #print(view_fname)

      view_dest_path = vim_view_path + view_fname
      view_local_path = data_dir + view_fname
      sh.cp(view_local_path, view_dest_path)

def main():
   #list of paths to track
   to_track_lst = None

   if not file_exists(conf_path):
      err_str = "can't find %s. " % (conf_path, )
      print("doesn't look like .vivie folder:", err_str)
      sys.exit(1)
   else:
      to_track_str = read_file(conf_path)
      to_track_lst = to_track_str.split('\n')[:-1]

   if not file_exists(data_dir):
      sh.mkdir(data_dir)

   cmd = parse_args()

   if cmd == 'help':
      print_help()
   elif cmd == 'setup':
      run_setup(to_track_lst)
   elif cmd == 'snapshot':
      take_snapshot(to_track_lst)
   elif cmd == 'status':
      pass

main()


