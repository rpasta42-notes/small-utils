import configparser, argparse, sys
from os.path import join
from utiltools.shellutils import expand_link

default_conf_path = '.vivie.conf'

from utiltools.shellutils import file_exists
from utiltools.shellutils import get_abs_path_relative_to


def find_conf_path(conf_fname):
   su_get_path = get_abs_path_relative_to
   conf_path = su_get_path(conf_fname, '.')

   while conf_path != '/':
      test_path = join(conf_path, conf_fname)
      if file_exists(test_path):
         return test_path

      conf_path = su_get_path(conf_path) #, '..')
   return None

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


def gen_arg_parser():

   init_help = '''main actions:
      init              init new project
      setup             setup project data in system
      snapshot          take snapshot of current project
      status            print current status of project
   '''

   p = parser = argparse.ArgumentParser(
         'vivie', epilog=init_help,
         formatter_class=argparse.RawTextHelpFormatter)

   p.add_argument('-c', '--conf-path', nargs='?', default=default_conf_path,
                  help='give explicit conf file location')

   p.add_argument('-p', '--project-name', nargs='?', help='name of new project (use with init only')

   choices=['init', 'setup', 'snapshot', 'status']
   p.add_argument('action', nargs='?', choices=choices)

   return parser

def gen_new_conf(project_name, conf_path=default_conf_path):
   c = config = configparser.ConfigParser()

   c.add_section('VimSettings')
   vim_view_path = '~/.vim/view/' #expand_link('~/.vim/view/') + '/'
   c.set('VimSettings', 'ViewPath', vim_view_path)

   c.add_section('ProjectSettings')
   c.set('ProjectSettings', 'DataDir', '.vivie/')
   c.set('ProjectSettings', 'ProjectName', project_name)
   c.set('ProjectSettings', 'TrackByDefault', 'false') #False)

   c.add_section('TrackingConfig')
   include_tracking = ['*.py', '*.md', '*.txt', '*.jsx', 'README.md']
   c.set('TrackingConfig', 'Include', ','.join(include_tracking))
   c.set('TrackingConfig', 'Exclude', ','.join(['*node_modules*', '.vivie/', '*.swp', '.git/']))

   conf_file = open(conf_path, 'w')
   config.write(conf_file)
   conf_file.close()
   return config


def parse_conf(conf_path):
   settings = configparser.ConfigParser()
   settings.read(conf_path)

   #print(conf.sections())

   ret = get_conf_data(settings)
   #print(ret)
   return ret

def get_conf_data(conf):
   return {
      'vim-view-path' : conf.get('VimSettings', 'ViewPath'),
      'data-dir' : conf.get('ProjectSettings', 'DataDir'),
      'project-name' : conf.get('ProjectSettings', 'ProjectName'),
      'track-by-default' : conf.getboolean('ProjectSettings',
                                           'TrackByDefault'),
      'include' : conf.get('TrackingConfig', 'Include').split(','),
      'exclude' : conf.get('TrackingConfig', 'Exclude').split(','),
   }


