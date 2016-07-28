'''A simple test bed for the leoBridge module.'''
import os
import sys

# Leo files.
files = [
    'c:/leo.repo/leo-editor/leo/test/unitTest.leo',
    'c:/leo.repo/leo-editor/leo/test/test.leo',
    'c:/xyzzy.xxx',
]

# Switches...
gui = 'nullGui'         # 'nullGui', 'qt',
kill_leo_output = False # True: kill all output produced by g.es_print.
loadPlugins = False     # True: attempt to load plugins.
readSettings = True     # True: read standard settings files.
silent = True           # True: don't print signon messages.
trace_sys_path = False  # True: trace imports here.
verbose = True          # True: verbose output.

# Import stuff...
dir_ = os.path.abspath('.')
if dir_ not in sys.path:
    if trace_sys_path: print('appending %s to sys.path' % dir_)
    sys.path.append(dir_)
if trace_sys_path:
    print('sys.path:...\n%s' % '\n'.join(sorted(sys.path)))
    print('sys.argv: %s %s' % (len(sys.argv), '\n'.join(sys.argv)))
if gui == 'qt':
    # Do this here to bypass leoQt g.in_bridge logic.
    import leo.core.leoQt as leoQt
import leo.core.leoBridge as leoBridge

controller = leoBridge.controller(
    gui=gui,
    loadPlugins=loadPlugins,
    readSettings=readSettings,
    silent=silent,
    verbose=verbose)
g = controller.globals()

# This kills all output from commanders.
if kill_leo_output:
    
    def do_nothing(*args, **keys):
        pass
        
    g.es_print = do_nothing
    
for path in files:
    if os.path.exists(path):
        c = controller.openLeoFile(path)
        if c:
            n = 0
            for p in c.all_positions():
                n += 1
            print('%s has %s nodes' % (c.shortFileName(), n))
    else:
        print('file not found: %s' % path)
