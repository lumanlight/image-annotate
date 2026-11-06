# sketch 场景语法（全量）

`bin/sketch scene.json out.png` —— 读 JSON 场景，用 rough（Rough.js 手绘风）渲染成 PNG。

## 顶层字段

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `w` | int | 1000 | 画布宽（有 `bg_image` 时忽略，用底图尺寸） |
| `h` | int | 620 | 画布高（同上） |
| `bg` | color | `#ffffff` | 画布背景色（无 `bg_image` 时生效） |
| `bg_image` | path | — | 底图（截图/照片）。给了就把图形**叠**在它上面 |
| `items` | array | — | 图形列表，按顺序绘制（后面的盖住前面的） |

**坐标单位＝图片像素**（封装已固定 `as_svg(...,auto_fit=False)`；早期 bug 会缩放铺满画布，见 P-145）。

## item 通用

| 键 | 说明 |
|---|---|
| `type` | `rect` / `circle` / `ellipse` / `line` / `polygon` / `text` |
| `stroke` | 描边色：`orange` `red` `green` `blue` `gray` 或 `#rrggbb` |
| `fill` | 填充色（同上）；不写＝`none`（只描边） |
| `strokeWidth` | 线宽，默认 3（≈马克笔） |
| `roughness` | 抖动强度，默认 2.0。0=规整，1.2–2=自然，>2.5 很潦草 |
| `bowing` | 线条弯曲度，默认 1.0 |

## 各类型字段

```jsonc
{"type":"rect",    "x":100,"y":100,"w":200,"h":120, ...}          // 左上角 + 宽高
{"type":"circle",  "x":400,"y":200,"diameter":80, ...}            // 圆心 + 直径（d 也兼容）
{"type":"ellipse", "x":600,"y":150,"w":160,"h":70, ...}           // 圆心 + 总宽高
{"type":"line",    "x1":10,"y1":10,"x2":200,"y2":60, ...}         // 两点
{"type":"polygon", "points":[[x1,y1],[x2,y2],...], ...}           // 折线/闭合面；多用于有机形状
{"type":"text",    "x":50,"y":500,"text":"中文","size":28,"color":"#333"}  // 基线左下起笔
```

`text` 的 `color` 走 `fill`；字体已固定 `Noto Sans CJK SC`（中文不会豆腐）；`size` 默认 22。

## 单位与坑

- `ellipse` / `circle` 的 `x,y` 是**几何中心**；`rect` 的 `x,y` 是**左上角**。
- `diameter` 是**直径不是半径**。给 ~10px 的小图标画圈用 `diameter:16`。
- rough **不合并图形**：别用一串圆堆「云/树冠」，会像棒棒糖；有机轮廓用一条闭合 `polygon`。
- 没有内置「箭头」对象：箭头 = `line` + `polygon`(三角头)。要现成箭头就用 `bin/annotate` 的 `arrow`。

## 渐变填充（rough 支持，进阶）

`fill` 可传颜色数组做渐变停靠点（`[{"offset":0,"color":"#fff"},...]`），少用；一般纯色足够。
