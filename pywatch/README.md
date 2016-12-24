Usage: `./pywatch.py <path> <extensions> <exec> [-d] &`

`<extensions> = ".py|.js|etc..."`
`extensions` is the extension types you want to monitor

`-d` is optional argument which prints the files that changed

`path` is location of the dir to monitor

`exec` is the command you want to run when something changes


###Example 1 for compiling latex:
`./pywatch.py src "tex" "make" -d`

###Example 2:
./watch.sh content:
```
#!/bin/bash
make
```

`./pywatch src ".py|.cpp" ./watch.sh &`

Only dependency for this script is pyinotify. To install it
run "sudo pip install pyinotify" (and if you don't want to
install it globally, it's recommended to use python
virtual environment (http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Explanation:
This script recursively watches for changes in <path>
of files with one of the <extensions> and automatically
triggers exec whenever a file changes

TODO:
   - possibly exclude .git directory with exclude_filter
   - add a timer and don't kill gunicorn more than once every second
   - Issue: when modifying code with vim, on_event is called twice
   - Check what happens when a bunch of files get changed at the same time, for example when installing new app.

