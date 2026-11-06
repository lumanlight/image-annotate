---
name: image-annotate
description: 让智能体自己画图或给图片动笔——从零画手绘插画/示意图/流程图（rough.js 抖动线条，吃 JSON 场景出 PNG），或精确标注截图（数字步骤/圈框/箭头/高亮/放大镜/打码）。自带渲染脚本与中文字体配置，任何工作区直接可用。Use when 画图, 画画, 画个, 画一张, 插画, 示意图, 流程图, 草图, 手绘, 涂描, 标注图片, 圈出来, 加箭头, 图片上写字, draw, sketch, diagram, annotate image.
---

# image-annotate — 智能体画图 / 标注图片

> **一句话**：要「出图」就找这里。**从零画**（手绘插画/示意图/流程图）用 `scripts/sketch`；
> **在已有图上标**（圈按钮/加箭头/打码）用 `scripts/annotate`。都能吃 JSON 吐 PNG。

**本技能自包含**：`scripts/`（程序）+ `venv/`（依赖）+ 本说明书都在一起，任何工作区都能直接用，
不依赖任何仓库路径。下面的 `scripts/...` 都是相对**本技能目录**（加载时会告诉你 base directory）。

## 0. 四个坑（违反就出事）

1. **一律走 `scripts/` 下的封装**，别裸调 ainotate / 别自己 pip install。封装已配好中文字体、输出目录、venv 解释器。
2. **中文必须走封装**（它设 `AINOTATE_FONT=NotoSansCJK.ttc:2` 与 CJK fontFamily）；裸调会**豆腐块**。
3. **坐标＝图片真实像素**，别照缩略预览目测。`scripts/annotate info x.png` 拿真实尺寸。sketch 已固定 `auto_fit=False`。
4. **一个形状一个轮廓**：rough 不合并图形，别用一堆圆堆「树冠/云」→ 会像棒棒糖；有机形状用**一条闭合 `polygon`**（配方见 `references/drawing-recipes.md`）。

## 1. 三十秒上手

> 输出位置：`scripts/sketch` 第 2 个参数写哪就出在哪；`scripts/annotate` 默认出到 `./image-annotate-out/`（当前目录，可写），也可用 `AINOTATE_OUTPUT_DIR` 指定。

**A. 从零画一张**（手绘风）：
```bash
BD="<本技能目录>"        # = 加载本技能时给的那个 base directory
cat > /tmp/s.json <<'JSON'
{"w":600,"h":400,"bg":"#fdf6e3","items":[
 {"type":"circle","x":480,"y":90,"diameter":80,"stroke":"#e8590c","strokeWidth":3,"roughness":1.4,"fill":"#ffd43b"},
 {"type":"rect","x":120,"y":200,"w":220,"h":140,"stroke":"#495057","strokeWidth":3,"roughness":1.3,"fill":"#fff9db"},
 {"type":"polygon","points":[[100,200],[230,110],[360,200]],"stroke":"#c92a2a","strokeWidth":3,"roughness":1.3,"fill":"#ffa8a8"},
 {"type":"text","x":150,"y":370,"text":"手绘小房子","size":28,"color":"#495057"}]}
JSON
"$BD/scripts/sketch" /tmp/s.json ./house.png         # 出到当前目录
```

**B. 标一张截图**（截图来源不限：系统截图工具、浏览器截屏、或用户给的文件）：
```bash
cat > /tmp/a.json <<'JSON'
{"input":"SHOT","marks":[
 {"type":"step","n":1,"rect":[360,138,880,184],"label":"改用户名"},
 {"type":"arrow","rect":[360,400,510,452],"label":"点保存"}]}
JSON
sed -i "s|SHOT|$PWD/shot.png|" /tmp/a.json
"$BD/scripts/annotate" annotate /tmp/a.json --json     # 默认出到 ./image-annotate-out/
```

坐标必须按**图片真实像素**写，先量：
```bash
"$BD/scripts/annotate" info shot.png     # 真实尺寸
"$BD/scripts/annotate" grid shot.png     # 叠坐标网格
```

## 2. 从零画（sketch）

```bash
"$BD/scripts/sketch" scene.json out.png     # 有 bg_image 时叠在图上
```

### scene 格式（速查，全量见 references/scene-grammar.md）
```json
{"w":900,"h":600,"bg":"#fdf6e3","bg_image":"可选-底图.png","items":[
  {"type":"rect","x":100,"y":100,"w":200,"h":120,"stroke":"blue","strokeWidth":3,"roughness":1.3,"fill":"#d0ebff"},
  {"type":"circle","x":400,"y":200,"diameter":80,"stroke":"red","fill":"#ffd43b"},
  {"type":"ellipse","x":600,"y":150,"w":160,"h":70,"stroke":"gray","fill":"#ffffff"},
  {"type":"line","x1":10,"y1":10,"x2":200,"y2":60,"stroke":"green"},
  {"type":"polygon","points":[[1,2],[3,4],[5,6]],"stroke":"green","fill":"#b2f2bb"},
  {"type":"text","x":50,"y":500,"text":"中文没问题","size":28,"color":"#333"}]}
```
- 颜色：`orange/red/green/blue/gray` 或 `#rrggbb`；样式键 `stroke fill strokeWidth roughness bowing`。
- `roughness`：0=规整，1.2–2=自然手绘，>2.5 很潦草；`strokeWidth`≈3 像马克笔。
- `circle` 直径用 `diameter`（`d` 也兼容）；`rect` 用 `x,y,w,h`；`ellipse` 的 x,y 是**中心**。
- 箭头 = `line` + `polygon`(三角头)；没有内置箭头对象。

### 画完必须验收（闭环）
画完用 `read_image` 看一眼：比例、堆叠、中文有没有豆腐。不对就改 JSON 数值重跑。**一次画对几乎不可能，迭代 2–3 版正常**。见 references/drawing-recipes.md。

## 3. 标注截图（annotate）

```bash
"$BD/scripts/annotate" info shot.png          # 真实像素尺寸
"$BD/scripts/annotate" grid shot.png          # 叠坐标网格量坐标
"$BD/scripts/annotate" zoom shot.png x1 y1 x2 y2
"$BD/scripts/annotate" annotate spec.json --json     # 落盘；--draft 只出临时文件
```
mark 类型：`step`数字 · `box`圈 · `arrow`指 · `highlight`高亮 · `spotlight`压暗其余 · `magnify`放大镜 · `text`自由文字 · `click`涟漪 · `keys`键帽 · `redact`**实心打码(敏感信息)** · `blur/pixelate`仅装饰。`rect`=[x1,y1,x2,y2] 或 {x,y,w,h}；一次 ≤6 个 mark；全量见 references/annotate-spec.md。

## 4. 报错对号入座

| 报错 / 现象 | 先做什么 |
|---|---|
| 中文变方块 | 没走 `scripts/annotate` 封装 |
| `Read-only file system` | 输出目录不可写 → 显式给输出路径，或设 `AINOTATE_OUTPUT_DIR=$PWD/xx` |
| `missing 'input'` | 标注 spec 根字段是 `input` 不是 `image` |
| `rect lies mostly outside` | 用了预览尺寸 → `annotate info` 拿真实像素 |
| `no room for label 'X'` | label 写短 / 加 `label_at:[x,y]` / 裁大图 |
| 图形跑到别处/巨大 | 自己写了代码却漏了 `auto_fit=False` |
| `No module named rough/ainotate` | 换了机器没建 venv → 跑 `bash setup.sh` |
| 树冠/云像棒棒糖 | 别堆圆，改用闭合 `polygon` |

## 5. 换机器 / 重建环境

`venv/` 是机器与架构相关的，**不能跨机器拷贝**。新机器需先满足：
- **系统依赖**：`libcairo2`（cairosvg 渲染必需）、`fonts-noto-cjk`（中文不变豆腐块）
  ```bash
  sudo apt-get install -y libcairo2 fonts-noto-cjk
  ```
- **uv**（可选）：`curl -LsSf https://astral.sh/uv/install.sh | sh`
  没有 uv 也能跑，`setup.sh` 会退回标准库 `python3 -m venv` + pip。

然后：
```bash
bash "$BD/setup.sh"        # 会先 preflight 检查 libcairo2/字体，再按 requirements.txt 重建 venv（约 5 秒）
```
`setup.sh` 缺系统依赖时会明确报出该装哪个 apt 包，不会静默装完却渲染失败。

## 6. 参考索引

| 想知道 | 文件（相对本技能目录） |
|---|---|
| scene 全量语法（每类 item 字段、单位、坑） | `references/scene-grammar.md` |
| 常见画法配方（太阳/云/树/房子/流程图/有机形状） | `references/drawing-recipes.md` |
| 标注 spec 全量字段（所有 mark、placement、crop、frame、privacy） | `references/annotate-spec.md` |

## 7. 什么时候别用

- 只裁剪/缩放/转格式：`python -c "from PIL import Image..."` 足够。
- 要矢量设计稿/图层精修：Inkscape/Krita 的活。
- 敏感信息外发：`redact` 才是真打码，`blur` 可逆。
- 网页一条龙（开网页→找元素→标）：需 playwright，未装，先截图再标。
