from aqt import qt, browser, gui_hooks, Qt
from aqt.utils import saveSplitter, restoreSplitter
from aqt.browser.layout import BrowserLayout
from anki.consts import *
from .version import *

LBL = "sidebar-table"
NVER = "1.1.0"

#########################################################################
def move_to_side(browser: browser):
    """Move table to sidebar (inserting a splitter), saving/restoring splitter state"""

    # Remove table
    table = browser.table._view
    grid = browser.form.gridLayout
    switch = grid.itemAtPosition(0, 0).widget()
    search = grid.itemAtPosition(0, 1).widget()
    grid.removeWidget(switch)
    grid.removeWidget(search)

    # Create new layout and pane
    layout = qt.QVBoxLayout()
    layout.addWidget(switch)
    layout.addWidget(search)
    layout.addWidget(table)
    layout.setStretch(0, 0)
    layout.setStretch(1, 0)
    layout.setStretch(2, 100)
    layout.addStretch(1)
    layout.setContentsMargins(5, 0, 0, 5)
    pane = qt.QWidget(browser)
    pane.setLayout(layout)

    # Create new splitter and add to sidebar with pane
    sidebar_widget = browser.sidebarDockWidget.widget()
    splitter = qt.QSplitter(browser.sidebarDockWidget)
    splitter.setOrientation(Qt.Orientation.Vertical)
    splitter.addWidget(sidebar_widget)
    splitter.addWidget(pane)
    restoreSplitter(splitter, LBL)
    browser.sidebarDockWidget.setWidget(splitter)
    splitter.setHandleWidth(5)
    closeEvent = browser.closeEvent
    browser.closeEvent = lambda evt: (saveSplitter(splitter, LBL), closeEvent(evt))[1]

    # Hide empty top
    browser.form.splitter.widget(0).setHidden(True)
    browser.form.splitter.handle(1).setHidden(True)


#########################################################################
def move_to_top(browser: browser):
    """Move table to "normal" top position"""
    splitter = browser.sidebarDockWidget.widget()
    saveSplitter(splitter, LBL)
    sb = splitter.widget(0)
    switch = splitter.widget(1).layout().takeAt(0).widget()
    search = splitter.widget(1).layout().takeAt(0).widget()
    table = splitter.widget(1).layout().takeAt(0).widget()

    grid = browser.form.gridLayout
    grid.addWidget(switch, 0, 0)
    grid.addWidget(search, 0, 1)
    browser.form.verticalLayout_2.addWidget(table)
    browser.sidebarDockWidget.setWidget(sb)

    # Show top and restore layout
    browser.form.splitter.widget(0).setHidden(False)
    browser.form.splitter.handle(1).setHidden(False)

#########################################################################
def minimize_tags(browser):
    """Minimize tag editor"""
    browser.editor.web.eval('''(async () => {
        function min(pane) {
            if (pane.style.cssText.match(/--pane-size:\s*[1-9]/))
                document.querySelector('.horizontal-resizer').dispatchEvent(new MouseEvent('dblclick'))
        }
        await NoteEditor
        let pane = document.querySelector('.horizontal-resizer + div .pane[style*="--pane-size:"]')
        if (!pane) {
            const obs = new MutationObserver((muts, obs) => {
                pane = document.querySelector('.horizontal-resizer + div .pane[style*="--pane-size:"]')
                if (pane) {
                    obs.disconnect()
                    min(pane)
                }
            })
            obs.observe(document.body, {childList: true, subtree: true})
        } else min(pane)
    })()''')

#########################################################################
def toggle(browser):
    if browser.form.splitter.widget(0).isHidden():
        move_to_top(browser)
        CFG['State'] = 'top'
    else:
        move_to_side(browser)
        if CFG["Autominimize"] == True:
            minimize_tags(browser)
        CFG['State'] = 'side'
    mw.addonManager.writeConfig(__name__, CFG)


#########################################################################
def setup(browser: browser):
    if CFG["State"] == 'side':
        toggle(browser)


#########################################################################
def setup_menu(browser: browser):
    menu = browser.form.menuqt_accel_view
    a = menu.addAction('Toggle table position')
    a.triggered.connect(lambda _, browser=browser: toggle(browser))
    if CFG["Shortcut"]:
        a.setShortcut(qt.QKeySequence(CFG["Shortcut"]))


# Main ##################################################################
CFG = mw.addonManager.getConfig(__name__)
gui_hooks.browser_will_show.append(setup)
gui_hooks.browser_menus_did_init.append(setup_menu)

if strvercmp(NVER, get_version()) > 0: set_version(NVER)