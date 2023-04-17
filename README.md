# Sidebar table

![screenshot](https://github.com/TRIAEIOU/sidebar-table/blob/main/Screenshots/screenshot.jpg?raw=true)

Anki addon to move the browser card/note table to the sidebar to maximize the editor area.

## Remarks

The implementation is some rather hacky monkey patching but simple enough. Will likely break sooner or later but should be fairly simple to correct.

The above screenshot is achieved with [Markdown input](https://ankiweb.net/shared/info/904999275) and [CSS Injector - Change default editor styles](https://ankiweb.net/shared/info/181103283) with the following CSS:

```css
/* editor.css */
body.night_mode {
  --fg: #858585;
  --canvas: #1e1e1e;
  --canvas-elevated: #1e1e1e;
  --border: #474747;
  --border-focus: 1px solid #3794ff;
}
.night_mode .editor-field {
  border-radius: unset;
  border: none;
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 5px;
  --fg: #d4d4d4;
  --selected-bg: #ADD6FF26;
}
.night_mode div:not(:nth-child(1)) > .field-container {
  border-top: 1px solid var(--border);
}

.night_mode .editor-toolbar {
  border: none;
  padding: 2px 0 0 0;
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