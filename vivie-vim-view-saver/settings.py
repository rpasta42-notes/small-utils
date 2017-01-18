import configparser, argparse, sys
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


def gen_arg_parser():

   init_help = '''main actions:
      init              init new project
      setup             setup project data in system
      snapshot          take snapshot of current project
      status            print current status of project
   '''

   p = parser = argparse.ArgumentParser(
      'vivie',
      formatter_class=argparse.RawTextHelpFormatter, epilog=init_help)

   p.add_argument('--conf-path', nargs='?',
                  help='give explicit conf file location')


   p.add_argument('action', nargs='?', choices=['init', 'setup', 'snapshot', 'status'])

   #p.add_argument('init', nargs='?', help='init new project')
   #p.add_argument('setup', nargs='?', help='setup project data in system')
   #p.add_argument('snapshot', nargs='?', help='take snapshot of current project')
   #p.add_argument('status', nargs='?', help='print current status of project')

   return parser

def gen_new_conf(project_name, default_path='.vivie.conf'):
   c = config = configparser.ConfigParser()

   c.add_section('VimSettings')
   vim_view_path = expand_link('~/.vim/view/') + '/'
   c.set('VimSettings', 'ViewPath', vim_view_path)

   c.add_section('ProjectSettings')
   c.set('ProjectSettings', 'DataDir', '.vivie/')
   c.set('ProjectSettings', 'ProjectName', project_name)
   c.set('ProjectSettings', 'TrackByDefault', 'false') #False)

   c.add_section('TrackingConfig')
   include_tracking = ['*.py', '*.md', '*.txt', 'README.md']
   c.set('TrackingConfig', 'include', ','.join(include_tracking))
   c.set('TrackingConfig', 'exclude', ','.join(['.vivie/', '*.swp']))


   conf_file = open(default_path, 'w')
   config.write(conf_file)
   conf_file.close()




