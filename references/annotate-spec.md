# annotate 标注 spec（全量要点）

`bin/annotate annotate spec.json --json`（在**已有图片**上标）；`--draft` 只出临时文件、`--debug` 画真实 rect/label 框调坐标用。

## 顶层字段

| 字段 | 说明 |
|---|---|
| `input` | 图片路径（**不是 `image`**，这是最容易踩的坑） |
| `name` | 落盘文件名标签（可选） |
| `scale` | 坐标→图片像素的缩放；`annotate` 用图片像素时＝1（默认） |
| `crop` | 裁剪：`"auto"`（默认框住所有 mark）或 `[x1,y1,x2,y2]` |
| `frame` | 加外框：`{"chrome":"browser","bg":"ocean"}` 等（做教程/文档时用） |
| `look` | 配色主题，默认橙 |
| `marks` | 标注列表 |

## marks（一次 ≤6 个，标签 1–4 个词）

| type | 作用 | 主要字段 |
|---|---|---|
| `step` | 数字徽章 + 轮廓 | `n`,`rect`/`target`,`label` |
| `box` | 圈一个东西 | `rect`,`label` |
| `arrow` | 箭头指向 | `rect`,`label`,`label_at` |
| `highlight` | 区域高亮 | `rect` |
| `spotlight` | 压暗其余、突出区域 | `rect` |
| `magnify` | 放大镜 | `rect` |
| `text` | 自由文字 | `at:[x,y]`,`text` |
| `click` | 点击涟漪 | `rect`/`target` |
| `keys` | 键帽 | `keys:["⌘","K"]` |
| `redact` | **实心打码**（敏感信息用它） | `rect` |
| `blur`/`pixelate` | 仅装饰（**可逆，别藏密钥**） | `rect` |

- `rect`：`[x1,y1,x2,y2]` 或 `{x,y,w,h}`。
- 定位也可用 `target`（`{"text":"保存"}` 走 OCR，需自行安装 tesseract；`{"selector"}` 等只在截图工具里用）。
- 标签被压/放不下：报 `no room for label` → 缩短 label / 加 `"label_at":[x,y]` 指空白 / 裁大图。

## 校准坐标的正确姿势

```bash
bin/annotate info shot.png              # 真实像素尺寸（预览是缩放的，别目测）
bin/annotate grid shot.png              # 叠坐标网格
bin/annotate zoom shot.png x1 y1 x2 y2  # 局部放大+细网格
```
全量字段与所有预设见上游 ainotate 文档；上游是 ainotate（AGPL-3.0）。
