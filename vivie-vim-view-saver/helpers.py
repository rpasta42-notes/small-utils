

def path_to_vim(path):
   return path.replace('/', '=+') + '='

def path_from_vim(path):
   return path.replace('=+', '/')[:-1]


def get_path_matches(paths, patterns):
   from fnmatch import fnmatch
   ret = []
   for path in paths:
      for pattern in patterns:
         if fnmatch(path, pattern):
            ret.append(path)
   return ret


