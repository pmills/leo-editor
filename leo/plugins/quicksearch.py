#@+leo-ver=5-thin
#@+node:ville.20090314215508.4: * @file quicksearch.py
#@+<< docstring >>
#@+node:ville.20090314215508.5: ** << docstring >> (quicksearch.py)
''' Adds a fast-to-use search widget, like the "Find in files" feature of many editors.

Just load the plugin, activate "Nav" tab, enter search text and press enter.

Usage
=====

The pattern to search for is, by default, a case *insensitive* fnmatch pattern
(e.g. foo*bar), because they are typically easier to type than regexps. If you
want to search for a regexp, use 'r:' prefix, e.g. r:foo.*bar.

Regexp matching is case sensitive; if you want to do a case-insensitive regular
expression search (or any kind of case-sensitive search in the first place), do it
by searching for "r:(?i)Foo". (?i) is a standard feature of Python regular expression
syntax, as documented in

The search can be confined to several options:
- All: regular search for all nodes
- Subtree: current node and it's children
- File: only search under a node with an @<file> directive
- Chapter: only search under a node with an @chapter directer
- Node: only search currently selected node

http://docs.python.org/library/re.html#regular-expression-syntax

Commands
========

This plugin defines the following commands that can be bound to keys:

- find-quick:
  Opens the Nav tab.

- find-quick-selected:
  Opens the Nav tab with the selected text as the search string.

- focus-to-nav:
  Puts focus in Nav tab.

- find-quick-test-failures:
  Lists nodes in c.db.get('unittest/cur/fail')

- find-quick-timeline:
  Lists all nodes in reversed gnx order, basically newest to oldest, creation wise,
  not modification wise.

- find-quick-changed:
  Lists all nodes that are changed (aka "dirty") since last save.  Handy when
  you want to see why a file's marked as changed.

- go-anywhere
  Nav bar does live search on headline. Press enter to force search of bodies.

  Once the hits are shown, you can navigate them by pressing up/down while
  focus is still in line editor & you can keep on typing (sort of like
  sublime text).

  **Clever**: spaces in search string are replaced with * wild card. So if
  you search for, say "file txt", it will search for "file*txt", matching
  e.g. @file readme.txt.

- history:
  Lists nodes from c.nodeHistory.

- marked-list:
  List all marked nodes.

'''
#@-<< docstring >>
# Ville M. Vainio <vivainio@gmail.com>.
#@+<< imports >>
#@+node:ville.20090314215508.7: ** << imports >>
import leo.core.leoGlobals as g
import itertools
from collections import OrderedDict

# Fail gracefully if the gui is not qt.
g.assertUi('qt')
from leo.core.leoQt import QtCore,QtConst,QtGui,QtWidgets,isQt5
if isQt5:
    QApplication = QtWidgets.QApplication
else:
    QApplication = QtGui.QApplication

from leo.core import leoNodes
    # Uses leoNodes.PosList.
import fnmatch
import re
from leo.plugins import threadutil
    # Bug fix. See: https://groups.google.com/forum/?fromgroups=#!topic/leo-editor/PAZloEsuk7g
from leo.plugins import qt_quicksearch_sub as qt_quicksearch
#@-<< imports >>
#@+others
#@+node:ville.20090314215508.8: ** init
def init ():
    '''Return True if the plugin has loaded successfully.'''
    ok = g.app.gui.guiName() == "qt"
    if ok:
        g.registerHandler('after-create-leo-frame',onCreate)
        g.plugin_signon(__name__)
    return ok

#@+node:ville.20090314215508.9: ** onCreate
def onCreate (tag, keys):

    c = keys.get('c')
    if not c: return

    install_qt_quicksearch_tab(c)

#@+node:tbrown.20111011152601.48461: ** show_unittest_failures
def show_unittest_failures(event):
    c = event.get('c')
    fails = c.db.get('unittest/cur/fail')
    # print(fails)
    nav = c.frame.nav
    #print nav

    nav.scon.clear()
    if fails:
        for gnx, stack in fails:
            pos = None
            # sucks
            for p in c.all_positions():
                if p.gnx == gnx:
                    pos = p.copy()
                    break

            def mkcb(pos, stack):
                def focus():
                    g.es(stack)
                    c.selectPosition(pos)
                return focus

            it = nav.scon.addGeneric(pos.h, mkcb(pos,stack))
            it.setToolTip(stack)

    c.k.simulateCommand('focus-to-nav')
#@+node:tbrown.20111011152601.48462: ** install_qt_quicksearch_tab (Creates commands)
def install_qt_quicksearch_tab(c):

    # tabw = c.frame.top.tabWidget
    wdg = LeoQuickSearchWidget(c, mode="nav")
    c.frame.log.createTab("Nav", widget = wdg)
    # tabw.addTab(wdg, "QuickSearch")

    def focus_quicksearch_entry(event):
        c.frame.log.selectTab('Nav')
        wdg.ui.lineEdit.selectAll()
        wdg.ui.lineEdit.setFocus()

    def focus_to_nav(event):
        c.frame.log.selectTab('Nav')
        wdg.ui.listWidget.setFocus()

    def find_selected(event):
        text = c.frame.body.wrapper.getSelectedText()
        if text.strip():
            wdg.ui.lineEdit.setText(text)
            wdg.returnPressed()
            focus_to_nav(event)
        else:
            focus_quicksearch_entry(event)

    def nodehistory(event):
        c.frame.log.selectTab('Nav')
        wdg.scon.doNodeHistory()

    def show_dirty(event):
        c.frame.log.selectTab('Nav')
        wdg.scon.doChanged()

    def timeline(event):
        c.frame.log.selectTab('Nav')
        wdg.scon.doTimeline()

    c.k.registerCommand(
        'find-quick',None,focus_quicksearch_entry)
    c.k.registerCommand(
        'find-quick-selected','Ctrl-Shift-f',find_selected)
    c.k.registerCommand(
        'focus-to-nav', None,focus_to_nav)
    c.k.registerCommand(
        'find-quick-test-failures', None,show_unittest_failures)
    c.k.registerCommand(
        'find-quick-timeline', None, timeline)
    c.k.registerCommand(
        'find-quick-changed', None, show_dirty)
    c.k.registerCommand(
        'history', None, nodehistory)

    @g.command('marked-list')
    def showmarks(event):
        """ List marked nodes in nav tab """
        #c.frame.log.selectTab('Nav')
        wdg.scon.doShowMarked()

    @g.command('go-anywhere')
    def find_popout_f(event):
        c = event['c']
        w = LeoQuickSearchWidget(c, mode="popout", parent = c.frame.top)
        topgeo = c.frame.top.geometry()
        wid = topgeo.width()
        w.setGeometry(wid/2,0, wid/2, 500)
        #w.setParent(c.frame.top)
        #w.setWindowFlags(QtConst.FramelessWindowHint)
        w.show()
        w.setFocus(QtConst.OtherFocusReason)
        #w.setGeometry(100,0,800,500)
        c._popout = w

    c.frame.nav = wdg

    # make activating this tab activate the input box
    def activate_input(idx, c=c):
        wdg = c.frame.nav
        tab_widget = wdg.parent().parent()
        if (tab_widget and
            hasattr(tab_widget, 'currentWidget') and
            tab_widget.currentWidget() == wdg
        ):
            wdg.ui.lineEdit.selectAll()
            wdg.ui.lineEdit.setFocus()

    # Careful: we may be unit testing.
    if wdg and wdg.parent():
        tab_widget = wdg.parent().parent()
        tab_widget.currentChanged.connect(activate_input)
#@+node:jlunz.20151027094647.1: ** class OrderedDefaultDict
class OrderedDefaultDict(OrderedDict):
    '''
    Credit:  http://stackoverflow.com/questions/4126348/
    how-do-i-rewrite-this-function-to-implement-ordereddict/4127426#4127426
    '''
    def __init__(self, *args, **kwargs):
        if not args:
            self.default_factory = None
        else:
            if not (args[0] is None or callable(args[0])):
                raise TypeError('first argument must be callable or None')
            self.default_factory = args[0]
            args = args[1:]
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)

    def __missing__ (self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = default = self.default_factory()
        return default

    def __reduce__(self):  # optional, for pickle support
        args = (self.default_factory,) if self.default_factory else ()
        return self.__class__, args, None, None, self.items()
#@+node:ekr.20111015194452.15716: ** class QuickSearchEventFilter
class QuickSearchEventFilter(QtCore.QObject):

    #@+others
    #@+node:ekr.20111015194452.15718: *3*  ctor (leoQtEventFilter)
    def __init__(self,c,w, lineedit):

        # Init the base class.
        QtCore.QObject.__init__(self)

        self.c = c
        self.listWidget = w
        self.lineEdit = lineedit
    #@+node:ekr.20111015194452.15719: *3* eventFilter
    def eventFilter(self,obj,event):

        # g.trace()
        eventType = event.type()
        ev = QtCore.QEvent
        # QLineEdit generates ev.KeyRelease only on Windows,Ubuntu
        # kinds = [ev.KeyPress,ev.KeyRelease]
        if eventType == ev.KeyRelease:
            #print "key event"
            lw = self.listWidget
            k = event.key()
            moved = False
            if k == QtConst.Key_Up:
                lw.setCurrentRow(lw.currentRow()-1)
                moved = True
            if k == QtConst.Key_Down:
                lw.setCurrentRow(lw.currentRow()+1)
                moved = True
            if k == QtConst.Key_Return:
                lw.setCurrentRow(lw.currentRow()+1)
                moved = True

            if moved:
                self.lineEdit.setFocus(True)
                self.lineEdit.deselect()
            #self.w.onKeyPress(event)

        return False
    #@-others
#@+node:ville.20121223213319.3670: ** dumpfocus
def dumpfocus():
    f = QtGui.QApplication.instance().focusWidget()
    g.es("Focus: " + f)
    print("Focus: " + f)
#@+node:ville.20090314215508.2: ** class LeoQuickSearchWidget (QWidget)
class LeoQuickSearchWidget(QtWidgets.QWidget):

    """ 'Find in files'/grep style search widget """

    #@+others
    #@+node:ekr.20111015194452.15695: *3*  ctor
    def __init__(self,c, mode = "nav", parent=None):

        QtWidgets.QWidget.__init__(self, parent)

        self.ui = qt_quicksearch.Ui_LeoQuickSearchWidget()
        self.ui.setupUi(self)

        # set to True after return is pressed in nav mode, to disable live updates until field is cleaned again
        self.frozen = False
        w = self.ui.listWidget
        u = self.ui
        cc = QuickSearchController(c,w,u)
        self.scon = cc

        if mode == "popout":
            self.setWindowTitle("Go anywhere")
            if 1:
                self.ui.lineEdit.returnPressed.connect(self.selectAndDismiss)
            else:
                self.connect(self.ui.lineEdit,
                    QtCore.SIGNAL("returnPressed()"),
                    self.selectAndDismiss)
            threadutil.later(self.ui.lineEdit.setFocus)
        else:
            if 1:
                self.ui.lineEdit.returnPressed.connect(self.returnPressed)
            else:
                self.connect(self.ui.lineEdit,
                    QtCore.SIGNAL("returnPressed()"),
                    self.returnPressed)
        if 1:
            self.ui.lineEdit.textChanged.connect(self.liveUpdate)
        else:
            self.connect(self.ui.lineEdit,
                QtCore.SIGNAL("textChanged(QString)"),
                self.liveUpdate)

        self.ev_filter = QuickSearchEventFilter(c,w, self.ui.lineEdit)
        self.ui.lineEdit.installEventFilter(self.ev_filter)
        self.c = c
    #@+node:ekr.20111015194452.15696: *3* returnPressed
    def returnPressed(self):

        self.scon.freeze()
        t = g.u(self.ui.lineEdit.text())
        if not t.strip():
            return

        if t == g.u('m'):
            self.scon.doShowMarked()
        else:
            self.scon.doSearch(t)

        if self.scon.its:
            self.ui.listWidget.blockSignals(True) # don't jump to first hit
            self.ui.listWidget.setFocus()
            self.ui.listWidget.blockSignals(False) # ok, respond if user moves

    def selectAndDismiss(self):
        self.hide()

    #@+node:ville.20121118193144.3622: *3* liveUpdate
    def liveUpdate(self):

        t = g.u(self.ui.lineEdit.text())
        if not t.strip():
            if self.scon.frozen:
                self.scon.freeze(False)
                self.scon.clear()
            return

        if len(t) < 3:
            return

        if self.scon.frozen:
            return

        if t == g.u('m'):
            self.scon.doShowMarked()
            return

        self.scon.worker.set_input(t)




    #@-others
#@+node:ekr.20111014074810.15659: ** matchLines
def matchlines(b, miter):

    res = []
    for m in miter:
        st, en = g.getLine(b, m.start())
        li = b[st:en].strip()
        res.append((li, (m.start(), m.end() )))
    return res

#@+node:ville.20090314215508.12: ** class QuickSearchController
class QuickSearchController(object):

    #@+others
    #@+node:ekr.20111015194452.15685: *3* __init__
    def __init__(self,c,listWidget,ui):
        self.c = c
        self.lw = w = listWidget # A QListWidget.
        self.its = {} # Keys are id(w),values are tuples (p,pos)
        self.worker = threadutil.UnitWorker()
        self.widgetUI = ui
        self.fileDirectives = ["@clean", "@file", "@asis", "@edit",
                               "@auto", "@auto-md", "@auto-org",
                               "@auto-otl", "@auto-rst"]

        self.frozen = False
        def searcher(inp):
            #print("searcher", inp)
            if self.frozen:
                return
            exp = inp.replace(" ", "*")
            res =  self.bgSearch(exp)
            return res

        def dumper():
            # always run on ui thread
            if self.frozen:
                return
            out = self.worker.output
            #print("dumper")
            self.throttler.add(out)

        def throttledDump(lst):
            """ dumps the last output """
            #print "Throttled dump"
            # we do get called with empty list on occasion
            if not lst:
                return
            if self.frozen:
                return
            hm,bm = lst[-1]
            self.clear()
            self.addHeadlineMatches(hm)
            self.addBodyMatches(bm)

        self.throttler = threadutil.NowOrLater(throttledDump)

        self.worker.set_worker(searcher)
        #self.worker.set_output_f(dumper)
        self.worker.resultReady.connect(dumper)
        self.worker.start()

        if 1: # Compatible with PyQt5
            # we want both single-clicks and activations (press enter)
            w.itemActivated.connect(self.onActivated)
            w.itemPressed.connect(self.onSelectItem)
            w.currentItemChanged.connect(self.onSelectItem)
        else:
            pass
            # # we want both single-clicks and activations (press enter)
            # w.connect(w,
                # QtCore.SIGNAL("itemActivated(QListWidgetItem*)"),
                # self.onActivated)
            # w.connect(w,
                # QtCore.SIGNAL("itemPressed(QListWidgetItem*)"),
                # self.onSelectItem)
            # w.connect(w,
                # QtCore.SIGNAL("currentItemChanged(QListWidgetItem*,QListWidgetItem *)"),
                # self.onSelectItem)
            # # Doesn't work.
    #@+node:ville.20121120225024.3636: *3* freeze
    def freeze(self, val = True):
        self.frozen = val

    #@+node:ekr.20111015194452.15689: *3* addBodyMatches
    def addBodyMatches(self, poslist):
        lineMatchHits = 0
        for p in poslist:
            it = QtWidgets.QListWidgetItem(p.h, self.lw)
            f = it.font()
            f.setBold(True)
            it.setFont(f)
            self.its[id(it)] = (p, None)
            ms = matchlines(p.b, p.matchiter)
            for ml, pos in ms:
                lineMatchHits += 1
                it = QtWidgets.QListWidgetItem("    "+ml, self.lw)
                self.its[id(it)] = (p,pos)
        return lineMatchHits
    #@+node:jlunz.20151027092130.1: *3* addParentMatches
    def addParentMatches(self, parent_list):
        lineMatchHits = 0
        for parent_key, parent_value in parent_list.items():
            if g.isString(parent_key):
                it = QtWidgets.QListWidgetItem(parent_key, self.lw)
            else:
                it = QtWidgets.QListWidgetItem(parent_key.h, self.lw)
            f = it.font()
            f.setItalic(True)
            it.setFont(f)
            self.its[id(it)] = (parent_key, None)
            for p in parent_value:
                it = QtWidgets.QListWidgetItem("    "+p.h, self.lw)
                f = it.font()
                f.setBold(True)
                it.setFont(f)
                self.its[id(it)] = (p, None)
                if hasattr(p,"matchiter"): #p might be not have body matches
                    ms = matchlines(p.b, p.matchiter)
                    for ml, pos in ms:
                        lineMatchHits += 1
                        it = QtWidgets.QListWidgetItem("    "+"    "+ml, self.lw)
                        self.its[id(it)] = (p,pos)
        return lineMatchHits

    #@+node:ekr.20111015194452.15690: *3* addGeneric
    def addGeneric(self, text, f):
        """ Add generic callback """
        it = id(QtWidgets.QListWidgetItem(text, self.lw))
        self.its[id(it)] = f
        return it
    #@+node:ekr.20111015194452.15688: *3* addHeadlineMatches
    def addHeadlineMatches(self, poslist):

        for p in poslist:
            it = QtWidgets.QListWidgetItem(p.h, self.lw)
            f = it.font()
            f.setBold(True)
            it.setFont(f)
            self.its[id(it)] = (p,None)
    #@+node:ekr.20111015194452.15691: *3* clear
    def clear(self):

        self.its = {}
        self.lw.clear()

    #@+node:ekr.20111015194452.15693: *3* doNodeHistory
    def doNodeHistory(self):

        nh = leoNodes.PosList(po[0] for po in self.c.nodeHistory.beadList)
        nh.reverse()
        self.clear()
        self.addHeadlineMatches(nh)
    #@+node:tbrown.20120220091254.45207: *3* doTimeline
    def doTimeline(self):

        c = self.c
        timeline = [p.copy() for p in c.all_unique_positions()]
        timeline.sort(key=lambda x: x.gnx, reverse=True)
        self.clear()
        self.addHeadlineMatches(timeline)
    #@+node:tbrown.20131204085704.57542: *3* doChanged
    def doChanged(self):

        c = self.c
        changed = [p.copy() for p in c.all_unique_positions() if p.isDirty()]
        self.clear()
        self.addHeadlineMatches(changed)
    #@+node:ekr.20111015194452.15692: *3* doSearch
    def doSearch(self, pat):
        hitBase = False
        self.clear()

        if not pat.startswith('r:'):
            hpat = fnmatch.translate('*'+ pat + '*').replace(r"\Z(?ms)","")
            bpat = fnmatch.translate(pat).rstrip('$').replace(r"\Z(?ms)","")
            flags = re.IGNORECASE
        else:
            hpat = pat[2:]
            bpat = pat[2:]
            flags = 0
        combo = self.widgetUI.comboBox.currentText()
        if combo == "All":
            hNodes = self.c.all_positions()
            bNodes = self.c.all_positions()
        elif combo == "Subtree":
            hNodes = self.c.p.self_and_subtree()
            bNodes = self.c.p.self_and_subtree()
        elif combo == "File":
            found = False
            node = self.c.p
            while not found and not hitBase:
                h = node.h
                if h: h=h.split()[0]
                if h in self.fileDirectives:
                    found = True
                else:
                    if node.level() == 0:
                        hitBase = True
                    else:
                        node = node.parent()
            hNodes = node.self_and_subtree()
            bNodes = node.self_and_subtree()
        elif combo == "Chapter":
            found = False
            node = self.c.p
            while not found and not hitBase:
                h = node.h
                if h: h=h.split()[0]
                if h == "@chapter":
                    found = True
                else:
                    if node.level() == 0:
                        hitBase = True
                    else:
                        node = node.parent()
            if hitBase: 
                # If I hit the base then revert to all positions 
                # this is basically the "main" chapter
                hitBase = False #reset
                hNodes = self.c.all_positions()
                bNodes = self.c.all_positions()
            else:
                hNodes = node.self_and_subtree()
                bNodes = node.self_and_subtree()

        else:
            hNodes = [self.c.p]
            bNodes = [self.c.p]

        if not hitBase:
            hm = self.find_h(hpat, hNodes, flags)
            bm = self.find_b(bpat, bNodes, flags)
            bm_keys = [match.key() for match in bm]
            numOfHm = len(hm) #do this before trim to get accurate count
            hm = [match for match in hm if match.key() not in bm_keys]

            if self.widgetUI.showParents.isChecked():
                parents = OrderedDefaultDict(lambda: [])
                for nodeList in [hm,bm]:
                    for node in nodeList:
                        if node.level() == 0:
                            parents["Root"].append(node)
                        else:
                            parents[node.parent()].append(node)
                lineMatchHits = self.addParentMatches(parents)
            else:
                self.addHeadlineMatches(hm)
                lineMatchHits = self.addBodyMatches(bm)

            hits = numOfHm + lineMatchHits
            self.lw.insertItem(0, "{} hits".format(hits))
        else:
            if combo == "File":
                self.lw.insertItem(0, "External file directive not found "+
                                      "during search")
    #@+node:ville.20121118193144.3620: *3* bgSearch
    def bgSearch(self, pat):

        #self.clear()

        if self.frozen:
            return

        if not pat.startswith('r:'):
            hpat = fnmatch.translate('*'+ pat + '*').replace(r"\Z(?ms)","")
            # bpat = fnmatch.translate(pat).rstrip('$').replace(r"\Z(?ms)","")
            flags = re.IGNORECASE
        else:
            hpat = pat[2:]
            # bpat = pat[2:]
            flags = 0
        combo = self.widgetUI.comboBox.currentText()
        if combo == "All":
            hNodes = self.c.all_positions()
        elif combo == "Subtree":
            hNodes = self.c.p.self_and_subtree()
        else:
            hNodes = [self.c.p]
        hm = self.find_h(hpat, hNodes, flags)
        # self.addHeadlineMatches(hm)
        # bm = self.c.find_b(bpat, flags)
        # self.addBodyMatches(bm)
        return hm, []
        # self.lw.insertItem(0, "%d hits"%self.lw.count())
    #@+node:jlunz.20150826091415.1: *3* find_h
    def find_h(self, regex, nodes, flags=re.IGNORECASE):
        """ Return list (a PosList) of all nodes where zero or more characters at
        the beginning of the headline match regex
        """

        pat = re.compile(regex, flags)
        res = leoNodes.PosList()
        for p in nodes:
            m = re.match(pat, p.h)
            if m:
                pc = p.copy()
                pc.mo = m
                res.append(pc)
        return res
    #@+node:jlunz.20150826091424.1: *3* find_b
    def find_b(self, regex, nodes, flags=re.IGNORECASE | re.MULTILINE):
        """ Return list (a PosList) of all nodes whose body matches regex
        one or more times.

        """
        pat = re.compile(regex, flags)
        res = leoNodes.PosList()
        for p in nodes:
            m = re.finditer(pat, p.b)
            t1, t2 = itertools.tee(m, 2)
            try:
                if g.isPython3:
                    t1.__next__()
                else:
                    t1.next()
            except StopIteration:
                continue
            pc = p.copy()
            pc.matchiter = t2
            res.append(pc)
        return res
    #@+node:ekr.20111015194452.15687: *3* doShowMarked
    def doShowMarked(self):

        self.clear()
        c = self.c
        pl = leoNodes.PosList()
        for p in c.all_positions():
            if p.isMarked():
                pl.append(p.copy())
        self.addHeadlineMatches(pl)
    #@+node:ekr.20111015194452.15700: *3* Event handlers
    #@+node:ekr.20111015194452.15686: *4* onSelectItem
    def onSelectItem(self, it, it_prev=None):

        c = self.c

        tgt = self.its.get(it and id(it))

        if not tgt: return

        # if Ctrl key is down, delete item and
        # children (based on indent) and return
        modifiers = QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            row = self.lw.row(it)
            init_indent = len(it.text()) - len(str(it.text()).lstrip())
            self.lw.blockSignals(True)
            while row < self.lw.count():
                self.lw.item(row).setHidden(True)
                row += 1
                cur = self.lw.item(row)
                indent = len(cur.text()) - len(str(cur.text()).lstrip())
                if indent <= init_indent:
                    break
            self.lw.setCurrentRow(row)
            self.lw.blockSignals(False)
            return

        # generic callable
        if callable(tgt):
            tgt()
        elif len(tgt) == 2:
            p, pos = tgt
            if hasattr(p,'v'): #p might be "Root"
                if not c.positionExists(p):
                    g.es(
                        "Node moved or deleted.\nMaybe re-do search.",
                        color='red'
                    )
                    return
                c.selectPosition(p)
                if pos is not None:
                    st, en = pos
                    w = c.frame.body.wrapper
                    w.setSelectionRange(st,en)
                    w.seeInsertPoint()

                self.lw.setFocus()
    #@+node:tbrown.20111018130925.3642: *4* onActivated
    def onActivated (self,event):

        c = self.c

        c.bodyWantsFocusNow()
    #@-others
#@-others
#@@language python
#@@tabwidth -4
#@-leo
