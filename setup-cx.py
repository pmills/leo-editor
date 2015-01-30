from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], 
    includes = ['atexit'],
    include_files = [('leo/', '')])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('launchLeo.py', base=base, targetName = 'leo-cx.exe')
]

options = {
    'build_exe': {
        'includes': 'atexit',
    }
}


setup(name='Leo Editor',
      version = '5.0cx01',
      description = 'Leonine Outline Editor',
      options = dict(build_exe = buildOptions),
      executables = executables)
      

