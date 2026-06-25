# PodsReunion Assets

## Logo

- `logo/logo-master.svg` is the production master mark. It uses `currentColor`, so set its color with CSS.
- `logo/logo-white.svg` is the fixed white variant for dark backgrounds and exports.
- `logo/original-linear-upload.svg` is the original SVG uploaded to Linear.
- `logo/references/` keeps PNG reference exports from the Linear issue comments.

## Favicons

The favicon and app icon exports live in `favicons/`.

Use these paths in HTML:

```html
<link rel="icon" type="image/png" sizes="16x16" href="/static/assets/favicons/favicon-16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/static/assets/favicons/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="96x96" href="/static/assets/favicons/favicon-96x96.png">
<link rel="shortcut icon" href="/static/assets/favicons/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/static/assets/favicons/apple-icon-180x180.png">
<link rel="manifest" href="/static/assets/favicons/manifest.json">
<meta name="msapplication-config" content="/static/assets/favicons/browserconfig.xml">
```

## AirPods Case Images

- `airpods/cases/web/` stores less glossy case images for product UI usage.
- `airpods/cases/original/` stores untouched source images named by model number.
- `airpods/cases/README.md` documents the taxonomy names and usage notes.

## AirPods Product Images

- `airpods/products/web/` stores less glossy product images for product UI usage.
- `airpods/products/original/` stores untouched source images named by product generation and view.
- `airpods/products/comparisons/` stores review-only comparison sheets.
- `airpods/products/README.md` documents the earbuds-only and with-case image naming convention.

## AirPods Earbud Images

- `airpods/earbuds/` stores one folder per AirPods model.
- Each model folder contains `og.png`, `right.png`, and `left.png`.
- `right.png` is the cleaned UI asset; `left.png` is the horizontal mirror used for left-side presentation.
- `airpods/earbuds/README.md` documents the screenshot-to-model mapping.
