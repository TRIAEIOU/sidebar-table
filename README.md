# Sidebar table

![screenshot](https://github.com/TRIAEIOU/sidebar-table/blob/main/Screenshots/screenshot.jpg?raw=true)

[Anki](https://apps.ankiweb.net) addon ([Github](https://github.com/TRIAEIOU/sidebar-table)) to move the browser card/note table to the sidebar to maximize the editor area.

## Warning

On first run it may be that the note/card table is not visible, if so try to find the splitter position at the bottom of the sidebar (look for when the cursor changes to "splitter") to adjust the splitter position (it is remembered between sessions).

The addon is not super well tested (for instance I don't know what happens if you rotate the screen) but it shouldn't break anything, just disable the addon.

## Remarks

The implementation is some rather hacky monkey patching but simple enough. Will likely break sooner or later but should be fairly simple to correct.

The above screenshot is achieved with [Markdown input](https://ankiweb.net/shared/info/904999275) and [CSS Injector - Change default editor styles](https://ankiweb.net/shared/info/181103283) with the following CSS:

```css
/* editor.css */
div > div.editor-field {
  border-radius: unset;
  border: none !important;
  box-shadow: none !important;
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 5px;
}
div:not(:nth-child(1)) > .field-container {
  border-top: 1px solid var(--border);
}

.editor-toolbar .button-toolbar {
  border: none;
  padding: 7px 7px 0px 7px;
  margin: 0px;
}

.editor-field {
  --fg: #3b3b3b;
  --selected-bg: #ADD6FF80;
}
.night_mode .editor-field {
  --fg: #d4d4d4;
  --selected-bg: #ADD6FF26;
}

body {
  --fg: #3b3b3b;
  --canvas: #ffffff;
  --canvas-elevated: #ffffff;
  --border: #CECECE;
  --border-focus: 1px solid #3794ff;
}
body.night_mode {
  --fg: #858585;
  --canvas: #1e1e1e;
  --canvas-elevated: #1e1e1e;
  --border: #474747;
  --border-focus: 1px solid #3794ff;
}
```

and

```css
/* field.css */
anki-editable.night_mode {
  color: var(--fg);
  font-size: 18px;
}
```

## Changelog

- 23-04-18: Fix splitter handle and stretch.
- 23-04-22: Fix multi card/note select bug. Add logic that minimizes tag field on browser show.
