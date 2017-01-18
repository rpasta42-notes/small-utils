

def path_to_vim(path):
   return path.replace('/', '=+') + '='

def path_from_vim(path):
   return path.replace('=+', '/')[:-1]


def get_path_matches(paths, patterns, antipatterns=[]):
   from fnmatch import fnmatch
   ret = []
   for path in paths:

      bad = False
      for antip in antipatterns:
         if fnmatch(path, antip):
            continue

      for pattern in patterns:
         if fnmatch(path, pattern):
            ret.append(path)
   return ret


