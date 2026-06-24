# figma-mcp-go serializer patch notes

The IR extractor can preserve vector fills/strokes when they exist in raw output. For better fidelity, patch the plugin serializer to export more style fields from every visible scene node.

Add these fields when available:

```ts
if ("visible" in node && node.visible === false) base.visible = false;
if ("opacity" in node && node.opacity !== 1) base.opacity = node.opacity;
if ("blendMode" in node && node.blendMode !== "PASS_THROUGH") base.blendMode = node.blendMode;

if ("cornerRadius" in node && !isMixed(node.cornerRadius)) {
  base.styles.cornerRadius = node.cornerRadius;
}

if ("topLeftRadius" in node && !isMixed(node.topLeftRadius)) {
  base.styles.topLeftRadius = node.topLeftRadius;
  base.styles.topRightRadius = node.topRightRadius;
  base.styles.bottomRightRadius = node.bottomRightRadius;
  base.styles.bottomLeftRadius = node.bottomLeftRadius;
}

if ("strokeWeight" in node && !isMixed(node.strokeWeight)) {
  base.styles.strokeWeight = node.strokeWeight;
}

if ("strokeAlign" in node && !isMixed(node.strokeAlign)) {
  base.styles.strokeAlign = node.strokeAlign;
}

if ("effects" in node && !isMixed(node.effects) && node.effects?.length) {
  base.styles.effects = node.effects;
}

if ("layoutMode" in node) {
  base.layout = {
    mode: node.layoutMode,
    wrap: node.layoutWrap,
    itemSpacing: node.itemSpacing,
    primaryAxisAlignItems: node.primaryAxisAlignItems,
    counterAxisAlignItems: node.counterAxisAlignItems,
    paddingTop: node.paddingTop,
    paddingRight: node.paddingRight,
    paddingBottom: node.paddingBottom,
    paddingLeft: node.paddingLeft
  };
}
```

Why this matters:

- Without `cornerRadius`, rounded inputs/buttons/cards will be approximated.
- Without `effects`, shadows are lost.
- Without `opacity`, overlays may be too dark or too light.
- Without layout fields, agents infer flex/grid from coordinates only.
