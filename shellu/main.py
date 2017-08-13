#!/usr/bin/python3

#sudo pip3 install sexpdata

import sys

from utiltools import shellutils as shutil
from sexpdata import loads, dumps
import json
import sh

fname = '/tmp/shellu'

if not shutil.file_exists(fname):
   shutil.write_file(fname, '{}')


def get_dict_sexps():
   ret = {}

   data = shutil.read_file(fname)
   sexps_data = json.loads(data)

   for binding in sexps_data:
      ret[binding[0]] = binding[1]

   return ret

def get_dict():
   ret = {}
   with open(fname, 'r') as f:
      data = f.read()
      lines = data.split('\n')

      for line in lines:
         binding = line.split(' ')
         ret[binding[0]] = binding[1]
   return ret

def write_dict(d):

   ret = ''
   for key in d:
      line = key + ' ' + d[key] + '\n'
      ret += line

   with open(fname, 'w') as f:
      f.write(ret)

def write_dict_sexps(d):
   exp = []
   for key in d:
      exp.append([key, d[key]])

   sexps = json.dumps(exp)

   shutil.write_file(fname, sexps)

def set(arg, val):
   d = get_dict()
   d[arg] = val
   write_dict(d)


def calc_val(val):

   if type(val) is list and len(val) == 1:
      val = val[0]

   if type(val) == str:
      #if val == '[]':
      #   return []
      if val[0] == '{' or val[0] == '[':
         val = val.replace('\'', '"')
         #print(val)
         return json.loads(val)
      if val[0:3] == 'py:':
         return eval(val[3:])
   return val


#if index is not None, then val is None and last item in index is val
def set_sexps(arg, val, indices=None, is_append=False):
   val = calc_val(val)

   d = get_dict_sexps()

   to_set = d
   index = arg
   prev_to_set = d
   prev_index = arg

   if indices is not None:
      #to_set = d[arg]
      for j in indices: #i in range(0, len(indices-1)):
         if type(to_set) != dict and type(to_set) != list:
            print_d('CANNOT SET THIS INDEX')
            prev_to_set[prev_index] = {}
            to_set = prev_to_set[prev_index]
            #break

         prev_to_set = to_set
         prev_index = index

         to_set = to_set[index]
         index = int(j) #indices[i]

   if type(to_set) != dict and type(to_set) != list:
      print_d('CANNOT SET THIS INDEX')
      prev_to_set[prev_index] = []
      to_set = prev_to_set[prev_index]
      #break

   if is_append:
      if type(val) is list:
         to_set[index] = to_set[index] + val
      else:
         to_set[index].append(val)
   else:
      to_set[index] = val

   write_dict_sexps(d)

def unset_sexps(v):
   d = get_dict_sexps()
   if v in d:
      del d[v]
   write_dict_sexps(d)

def list_bindings():
   d = get_dict_sexps()
   for key in d:
      print('%s - %s' % (key, d[key]))


def check(key, index=None, d=None, is_print=True):
   if d is None:
      d = get_dict()

   if index == None:
      if key in d:
         print_('1', is_print)
         return 1
      else:
         print_d('index doesn\'t exist')
         print_('0', is_print)
         return 0

   if type(index) is not int:
      print_d('index is not int')
      print_('0', is_print)
      return 0

   val = d[key]
   if type(val) is not list:
      print_d('index is not list')
      print_('0', is_print)
      return 0

   if len(val) <= index:
      print_d('index too large')
      print_('0', is_print)
      return 0

   print_('1', is_print)
   return 1


def get(key, index=None):
   d = get_dict_sexps()
   #print(d)

   if check(key, index=index, d=d, is_print=False) == 0:
      return

   val = d[key]

   if type(index) is int:
      ret = val[index]
   else:
      ret = val
      if type(ret) is list and len(ret) == 1:
         ret = ret[0]

   print(ret)
   return ret


def print_d(msg):
   DEBUG = True
   if DEBUG:
      print(msg)

def print_(s, should_print):
   if should_print:
      print(s)

def usage(is_bad=True):

   usage_str = '''
      {n} list\n
      {n} set [name] "val" "val2"\n
      {n} get [name] [index]\n
      {n} unset [name]\n
      {n} eval [cmd]\n
      {n} set-index [name] [i] [i2] [val]\n
      {n} set-many [name1] [val1] [name2] [val2]
   '''.format(n=sys.argv[0])

   print(usage_str)

   if is_bad:
      print('bad args')
      sys.exit(-1)


def main():

   if len(sys.argv) == 2 and sys.argv[1] == 'list':
      list_bindings()
      return

   if len(sys.argv) < 3:
      usage()

   args = sys.argv
   if args[1] == 'set':

      if len(args) < 4:
         usage()

      set_sexps(args[2], args[3:])
      get(args[2])

   elif args[1] == 'set-index':

      if len(args) < 5:
         usage()

      set_sexps(args[2], args[-1], indices=args[3:-1])

      get(args[2])

   elif args[1] == 'append':
      if len(args) < 4:
         usage()

      set_sexps(args[2], args[3:], is_append=True)

      get(args[2])

   elif args[1] == 'append-index':
      if len(args) < 5:
         usage()

      set_sexps(args[2], args[-1], indices=args[3:-1], is_append=True)

      get(args[2])


   elif args[1] == 'set-many':

      if len(args) < 4:
         usage()

      i = 2
      while i+1 < len(args):
         set_sexps(args[i], [args[i+1]])
         i += 2

      list_bindings()

   elif args[1] == 'unset':
      if len(args) != 3:
         usage()
      unset_sexps(args[2])

   elif args[1] == 'get':
      if len(args) == 3:
         get(args[2])
      elif len(args) == 4:
         get(args[2], index=int(args[3]))

   elif args[1] == 'eval':
      ret = eval(args[2])
      print(ret)
      return ret

main()


