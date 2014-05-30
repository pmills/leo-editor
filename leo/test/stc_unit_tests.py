# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20140527115626.17955: * @file ../test/stc_unit_tests.py
#@@first
#@+others
#@+node:ekr.20140527073639.16704: ** @testsetup
# Common setup code for all unit tests.
# **Note**: Only included for "all" and "marked" *local* runs.
trace = False
do_gc = True
    # Takes about 0.5 sec. per test.
    # Can be done at end of test.
if c.isChanged():
    c.save()
import ast
import gc
import leo.core.leoSTC as stc
import time
import imp
imp.reload(stc) # Takes about 0.003 sec.
u = stc.Utils()
u.update_run_count(verbose=True)
t2 = time.clock()
if do_gc:
    gc.collect()
if trace:
    print('@testsetup gc.collect: %s %s' % (
        (do_gc,g.timeSince(t2))))
#@+node:ekr.20140527073639.16706: ** @test DataTraverser
#@+others
#@+node:ekr.20140527125017.17956: *3* check_class_names
def check_class_names(defs_d,refs_d):
    aList = [ 
    #@+<< non-pep8 class names >>
    #@+node:ekr.20140528065727.17958: *4* << non-pep8 class names >>
    # converted by hand:
    # 'chapter',
    # 'chapterController',
    # 'command',
    # 'leoFrame',
    # 'leoLog',
    # 'node', # -> LeoNode in plugins/leo_interface.py.
    # 'nodeIndices',
    # 'shadowController',
    'abbrevCommandsClass',
    'anchor_htmlParserClass',
    'atFile',
    'atShadowTestCase',
    'baseEditCommandsClass',
    'baseFileCommands',
    'baseLeoCompare',
    'baseLeoPlugin',
    'baseNativeTreeWidget',
    'baseTangleCommands',
    'baseTextWidget',
    'bridgeController',
    'bufferCommandsClass',
    'cScanner',
    'cSharpScanner',
    'cacher',
    'chapterCommandsClass',
    'controlCommandsClass',
    'debugCommandsClass',
    'def_node',
    'editBodyTestCase',
    'editCommandsClass',
    'editFileCommandsClass',
    'elispScanner',
    'emergencyDialog',
    'fileCommands',
    'fileLikeObject',
    'goToLineNumber',
    'helpCommandsClass',
    'htmlParserClass',
    'htmlScanner',
    'importExportTestCase',
    'iniScanner',
    'invalidPaste',
    'jEditColorizer',
    'javaScanner',
    'keyHandlerClass',
    'keyHandlerCommandsClass',
    'killBufferCommandsClass',
    'killBuffer_iter_class',
    'leoBody',
    'leoCommandsClass',
    'leoCompare',
    'leoFind',
    'leoGui',
    'leoImportCommands',
    'leoKeyEvent',
    'leoMenu',
    'leoQLineEditWidget',
    'leoQScintillaWidget',
    'leoQTextEditWidget',
    'leoQtBaseTextWidget',
    'leoQtBody',
    'leoQtColorizer',
    'leoQtEventFilter',
    'leoQtFrame',
    'leoQtGui',
    'leoQtHeadlineWidget',
    'leoQtLog',
    'leoQtMenu',
    'leoQtMinibuffer',
    'leoQtSpellTab',
    'leoQtSyntaxHighlighter',
    'leoQtTree',
    'leoQtTreeTab',
    'leoTree',
    'leoTreeTab',
    'linkAnchorParserClass',
    'link_htmlparserClass',
    'macroCommandsClass',
    'markerClass',
    'nodeHistory',
    'nullBody',
    'nullColorizer',
    'nullFrame',
    'nullGui',
    'nullIconBarClass',
    'nullLog',
    'nullMenu',
    'nullObject',
    'nullScriptingControllerClass',
    'nullStatusLineClass',
    'nullTree',
    'part_node',
    'pascalScanner',
    'phpScanner',
    'posList',
    'poslist',
    'pythonScanner',
    'qtIconBarClass',
    'qtMenuWrapper',
    'qtSearchWidget',
    'qtStatusLineClass',
    'qtTabBarWrapper',
    'readLinesClass',
    'rectangleCommandsClass',
    'recursiveImportController',
    'redirectClass',
    'registerCommandsClass',
    'root_attributes',
    'rstCommands',
    'rstScanner',
    'runTestExternallyHelperClass',
    'saxContentHandler',
    'saxNodeClass',
    'scanUtility',
    'searchCommandsClass',
    'searchWidget',
    'sourcereader',
    'sourcewriter',
    'spellCommandsClass',
    'spellTabHandler',
    'stringTextWidget',
    'tangleCommands',
    'tst_node',
    'undoer',
    'unitTestGui',
    'ust_node',
    'vimoutlinerScanner',
    'xmlScanner',
    #@-<< non-pep8 class names >>
    ]
    ambiguous,undefined = [],[]
    for s in aList:
        aSet = defs_d.get(s,set())
        n = len(sorted(aSet))
        if n == 0:
            undefined.append(s)
        elif n > 1:
            ambiguous.append(s)
        s2 = g.pep8_class_name(s)
        aSet = defs_d.get(s2,set())
        if len(sorted(aSet)) > 1:
            g.trace('conflict',s,s2)
    print('undefined...\n  %s' % '\n  '.join(sorted(undefined)))
    print('ambiguous...\n')
    for s in sorted(ambiguous):
        aSet = defs_d.get(s,set())
        # print('%20s %s' % (s,sorted(aSet)))
        print('%3s %s' % (len(sorted(aSet)),s))
#@+node:ekr.20140527083058.16708: *3* report
def report():
    '''Report ambiguous symbols.'''
    n = 0
    for s in sorted(defs_d.keys()):
        aSet = defs_d.get(s)
        aList = sorted(aSet)
        if len(aList) > 1:
            n += 1
            # g.trace('multiple defs',s)
    return n
#@-others
project_name = 'leo'
flags = (
    'check',
    'print',
    'report',
    # 'skip',
    # 'stats',
)
files = [
    # r'c:\leo.repo\leo-editor\leo\core\leoApp.py',
    # r'c:\leo.repo\leo-editor\leo\core\leoFileCommands.py',
] or u.project_files(project_name)
if g.app.runningAllUnitTests and (len(files) > 1 or 'skip' in flags):
    self.skipTest('slow test')
# Pass 0
t = time.time()
root_d = u.p0(files,project_name,False)
p0_time = u.diff_time(t)
# DataTraverser
t = time.time()
defs_d, refs_d = {},{}
dt = stc.DataTraverser(defs_d,refs_d)
for fn in sorted(files):
    dt(fn,root_d.get(fn))
dt_time = u.diff_time(t)
if 'check' in flags:
    check_class_names(defs_d,refs_d)
if 'print' in flags:
    print('parse: %s' % p0_time)
    print('   DT: %s' % dt_time)
    print('defs: %s refs: %s: ambiguous: %s' % (
        len(sorted(defs_d.keys())),
        len(sorted(refs_d.keys())),
        report(),
    ))
    if 'stats' in flags:
        dt.print_stats()
#@+node:ekr.20140528102444.17997: ** @test replace class names
'''Replace only unambiguously defined non-pep8 class names.'''
replace = True # True: actually make the replacements.
aList = [
#@+<< non-pep8 class names >>
#@+node:ekr.20140528102444.19375: *3* << non-pep8 class names >>
'abbrevCommandsClass',
'anchor_htmlParserClass',
'atFile',
'atShadowTestCase',
'baseEditCommandsClass',
'baseFileCommands',
'baseLeoCompare',
'baseLeoPlugin',
'baseNativeTreeWidget',
'baseTangleCommands',
'baseTextWidget',
'bridgeController',
'bufferCommandsClass',
'cScanner',
'cSharpScanner',
'cacher',
'chapterCommandsClass',
'controlCommandsClass',
'debugCommandsClass',
'def_node',
'editBodyTestCase',
'editCommandsClass',
'editFileCommandsClass',
'elispScanner',
'emergencyDialog',
'fileCommands',
'fileLikeObject',
'goToLineNumber',
'helpCommandsClass',
'htmlParserClass',
'htmlScanner',
'importExportTestCase',
'iniScanner',
'invalidPaste',
'jEditColorizer',
'javaScanner',
'keyHandlerClass',
'keyHandlerCommandsClass',
'killBufferCommandsClass',
'killBuffer_iter_class',
'leoBody',
'leoCommandsClass',
'leoCompare',
'leoFind',
'leoGui',
'leoImportCommands',
'leoKeyEvent',
'leoMenu',
'leoQLineEditWidget',
'leoQScintillaWidget',
'leoQTextEditWidget',
'leoQtBaseTextWidget',
'leoQtBody',
'leoQtColorizer',
'leoQtEventFilter',
'leoQtFrame',
'leoQtGui',
'leoQtHeadlineWidget',
'leoQtLog',
'leoQtMenu',
'leoQtMinibuffer',
'leoQtSpellTab',
'leoQtSyntaxHighlighter',
'leoQtTree',
'leoQtTreeTab',
'leoTree',
'leoTreeTab',
'linkAnchorParserClass',
'link_htmlparserClass',
'macroCommandsClass',
'markerClass',
'nodeHistory',
'nullBody',
'nullColorizer',
'nullFrame',
'nullGui',
'nullIconBarClass',
'nullLog',
'nullMenu',
'nullObject',
'nullScriptingControllerClass',
'nullStatusLineClass',
'nullTree',
'part_node',
'pascalScanner',
'phpScanner',
'posList',
'poslist',
'pythonScanner',
'qtIconBarClass',
'qtMenuWrapper',
'qtSearchWidget',
'qtStatusLineClass',
'qtTabBarWrapper',
'readLinesClass',
'rectangleCommandsClass',
'recursiveImportController',
'redirectClass',
'registerCommandsClass',
'root_attributes',
'rstCommands',
'rstScanner',
'runTestExternallyHelperClass',
'saxContentHandler',
'saxNodeClass',
'scanUtility',
'searchCommandsClass',
'searchWidget',
'sourcereader',
'sourcewriter',
'spellCommandsClass',
'spellTabHandler',
'stringTextWidget',
'tangleCommands',
'tst_node',
'undoer',
'unitTestGui',
'ust_node',
'vimoutlinerScanner',
'xmlScanner',
#@-<< non-pep8 class names >>
]
if 0: # not needed when @testsetup exists.
    import leo.core.leoSTC as stc
    import time
    import imp
    imp.reload(stc) # Takes about 0.003 sec.
u = stc.Utils()
#@+others
#@+node:ekr.20140528102444.19376: *3* class ReplaceController
class ReplaceController:
    #@+others
    #@+node:ekr.20140530134300.17617: *4*  ctor
    def __init__(self,c,files):
        self.c = c
        self.changed = set()
        self.files_d = {} # Keys are full paths, values are file contents.
        self.files = files
    #@+node:ekr.20140528102444.19379: *4* check_new_name
    def check_new_name(self,new_name):
        '''Verify that s is found nowhere in Leo.'''
        for fn in self.files:
            s = self.files_d.get(fn)
            if s.count(new_name) > 0:
                g.trace('****',new_name,'exists in',g.shortFileName(fn))
                return False
        return True
            
    #@+node:ekr.20140528102444.19380: *4* load_files
    def load_files(self):
        for fn in self.files:
            assert g.os_path_exists(fn),fn
            f = open(fn,'r')
            s = f.read()
            f.close()
            self.files_d[fn] = s
            assert s,fn
        
    #@+node:ekr.20140528102444.19378: *4* replace_class_name
    def replace_class_name(self,old_name,new_name):
        assert old_name != new_name,old_name
        if not self.check_new_name(new_name):
            return
        for fn in self.files:
            s = self.files_d.get(fn)
            i = s.count(old_name)
            if i > 0:
                self.changed.add(fn)
                self.files_d[fn] = s.replace(old_name,new_name)
                print('%2s instances of %s in %s' % (
                    i,old_name,g.shortFileName(fn)))
    #@+node:ekr.20140528102444.19377: *4* run
    def run(self,aList):
        self.load_files()
        for s in aList:
            self.replace_class_name(s,g.pep8_class_name(s))
        self.write_files()
    #@+node:ekr.20140530134300.17616: *4* write_files
    def write_files(self):
        '''Write all changed files.'''
        if replace:
            for fn in sorted(self.changed):
                if replace:
                    print('writing: %s' % fn)
                    f = open(fn,'w')
                    s = self.files_d.get(fn)
                    f.write(s)
                    f.close()
        else:
            print('changed, not written:...\n%s' % (
                '\n'.join(sorted(self.changed))))
    #@-others
#@-others
files = u.project_files('leo')
ReplaceController(c,files).run(aList)
#@-others
#@@language python
#@@tabwidth -4
#@-leo