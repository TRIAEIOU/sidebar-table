from aqt import qt, browser, gui_hooks, Qt
from aqt.utils import saveSplitter, restoreSplitter
from anki.consts import *
from .version import *

LABEL = "sidebar-table"
NVER = "1.0.2"

#########################################################################
def move(browser: browser):
    """Move table to sidebar (inserting a splitter), saving/restoring splitter state"""
    # Direct copy from [browser.py](https://github.com/ankitects/anki/blob/8abcb77d9536da10a00cbe15f3149bb00c6deee0/qt/aqt/browser/browser.py#L536)
    # Only change is how to get a hold of the widget holding the table (marked below)
    def on_all_or_selected_rows_changed(self) -> None:
        """Called after the selected or all rows (searching, toggling mode) have
        changed. Update window title, card preview, context actions, and editor.
        """
        if self._closeEventHasCleanedUp:
            return

        self.updateTitle()
        # if there is only one selected card, use it in the editor
        # it might differ from the current card
        self.card = self.table.get_single_selected_card()
        self.singleCard = bool(self.card)

        # Modification: replace `self.form.splitter.widget(1).setVisible(self.singleCard)` with
        self.form.fieldsArea.parent().setVisible(self.singleCard)

        if self.singleCard:
            self.editor.set_note(self.card.note(), focusTo=self.focusTo)
            self.focusTo = None
            self.editor.card = self.card
        else:
            self.editor.set_note(None)
        self._renderPreview()
        self._update_row_actions()
        self._update_selection_actions()
        gui_hooks.browser_did_change_row(self)

    # Remove table parent widget and reorder the layout
    table = browser.table._view
    root =  table.parent()
    grid = browser.form.gridLayout
    switch = grid.itemAtPosition(0, 0).widget()
    search = grid.itemAtPosition(0, 1).widget()
    grid.removeWidget(switch)
    grid.removeWidget(search)
    layout = root.layout()
    layout.removeItem(grid)
    layout.addWidget(switch)
    layout.addWidget(search)
    layout.removeWidget(table)
    layout.addWidget(table)
    layout.setStretch(0, 0)
    layout.setStretch(1, 0)
    layout.setStretch(2, 100)
    layout.addStretch(1)

    # Create new splitter and add to sidebar
    splitter = qt.QSplitter(browser.sidebarDockWidget)
    splitter.setOrientation(Qt.Orientation.Vertical)
    splitter.addWidget(browser.sidebarDockWidget.widget())
    splitter.addWidget(root)
    root.setMinimumHeight(0)
    restoreSplitter(splitter, LABEL)
    browser.sidebarDockWidget.setWidget(splitter)
    splitter.setHandleWidth(5)
    browser.on_all_or_selected_rows_changed = lambda: on_all_or_selected_rows_changed(browser)
    closeEvent = browser.closeEvent
    browser.closeEvent = lambda evt: (saveSplitter(splitter, LABEL), closeEvent(evt))[1]

    # Ensure tag field is minimized
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
    })()
    ''')

# Main ##################################################################
gui_hooks.browser_will_show.append(move)

if strvercmp(NVER, get_version()) > 0: set_version(NVER)