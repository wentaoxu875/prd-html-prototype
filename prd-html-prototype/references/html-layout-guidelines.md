# HTML Layout Guidelines

## Side-by-side layout for App/H5

Use a two-column shell on desktop: PRD content grows to fill available space, prototype iframe keeps a stable device width.

Recommended CSS pattern:

```css
.shell.mobile-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(390px, 430px);
  gap: 24px;
  align-items: start;
}
.prototype-frame.mobile {
  width: 100%;
  height: min(860px, calc(100vh - 96px));
  border: 1px solid #d7dce2;
  border-radius: 24px;
}
@media (max-width: 900px) {
  .shell.mobile-layout { grid-template-columns: 1fr; }
  .prototype-frame.mobile { height: 760px; }
}
```

## Stacked layout for Web PC

Use a vertical shell: PRD first, full-width prototype below. Keep the prototype iframe wide enough to represent a desktop product.

Recommended CSS pattern:

```css
.shell.web-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;
}
.prototype-frame.web {
  width: 100%;
  min-height: 720px;
  height: calc(100vh - 120px);
  border: 1px solid #d7dce2;
  border-radius: 8px;
}
```

## Content and interaction rules

- Put the actual PRD and iframe in the first viewport; do not create a marketing hero.
- Use semantic HTML headings and anchors for PRD navigation.
- Keep iframe `src` relative, usually `./prototype.html`.
- Avoid nested cards. Use sections, dividers, and compact panels only where they improve scanning.
- Ensure iframe has a visible title attribute for accessibility.
- If the prototype depends on multiple files, preserve its asset paths and copy the full asset folder.
