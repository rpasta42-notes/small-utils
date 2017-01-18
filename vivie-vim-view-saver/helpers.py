

def path_to_vim(path):
   return path.replace('/', '=+') + '='

def path_from_vim(path):
   return path.replace('=+', '/')[:-1]

