import ConfigParser
from os.path import join
from utiltools.shellutils import expand_link


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

def parse_args():
   args = sys.argv

   if len(args) is not 2:
      return None

   if args[1] not in avail_cmd_args:
      return None

   return args[1]


def gen_new_conf():
   c = config = ConfigParser.ConfigParser()

   vim_view_path = expand_link('~/.vim/view/') + '/'
   default_track_extensions = ['*.py', '*.md', '.txt']
   default_track_paths = ['README.md'] #default directories/files to track


   c.add_section('VimSettings')
   c.add_section('ProjectConfig')
   c.add_section('ProjectSettings')

   c.set('VimSettings', 'ViewPath', vim_view_path)
   c.set('ProjectConfig', 'DataDir', '.vivie/')

   c.set('ProjectSettings', 'extensions_include',
