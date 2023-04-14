from aqt import qt, browser, gui_hooks, Qt
from aqt.utils import saveSplitter, restoreSplitter
from anki.consts import *

LABEL = "sidebar-table"

#########################################################################
def move(browser: browser):
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
        self.sidebar_table["container"].setVisible(self.singleCard)

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

    tablew =  browser.table._view.parent()
    splitter = qt.QSplitter(browser.sidebarDockWidget)
    splitter.setOrientation(Qt.Orientation.Vertical)
    sbw = browser.sidebarDockWidget.widget()
    splitter.addWidget(sbw)
    splitter.addWidget(tablew)
    restoreSplitter(splitter, LABEL)
    browser.sidebarDockWidget.setWidget(splitter)
    browser.sidebar_table = { # custom prop to store info
        "container": tablew,
        "splitter": splitter
    }
    browser.on_all_or_selected_rows_changed = lambda: on_all_or_selected_rows_changed(browser)
    closeEvent = browser.closeEvent
    browser.closeEvent = lambda evt: (saveSplitter(splitter, LABEL), closeEvent(evt))[1]

# Main ##################################################################
gui_hooks.browser_will_show.append(move)
