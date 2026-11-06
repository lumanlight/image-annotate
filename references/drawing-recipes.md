# 常见画法配方（copy-paste 起手）

原则：**先搭大件（背景/地平线/主体），再补细节（门窗/高光），最后文字**。
坐标先估，画完 `read_image` 看，再改数值迭代 2–3 版是正常的。

## 有机形状（树冠 / 云 / 花瓣）—— 用正弦扰动的闭合多边形

不要堆圆。用一条闭合 polygon，半径带 n 瓣起伏：

```python
import math, json
def blob(cx, cy, rx, ry, lobes=5, amp=0.10, n=22):
    pts=[]
    for i in range(n):
        th = 2*math.pi*i/n
        wob = 1.0 + amp*math.sin(lobes*th) + 0.05*math.sin(3*th+1.1)
        pts.append([round(cx+rx*wob*math.cos(th),1), round(cy+ry*wob*math.sin(th),1)])
    return pts
# item: {"type":"polygon","points":blob(645,268,100,92),"stroke":"#2b8a3e","fill":"#b2f2bb","roughness":2.2}
```

## 太阳

```jsonc
{"type":"circle","x":765,"y":100,"diameter":92,"stroke":"#e8590c","strokeWidth":3.5,"roughness":1.4,"fill":"#ffd43b"}
```
射线＝从圆外 8–10px 起、再往外 26px 的短线，8 个方向（0/45/90/...）：
```python
for k in range(8):
    a=math.radians(45*k); r0=58; r1=88
    {"type":"line","x1":cx+r0*cos,"y1":cy+r0*sin,"x2":cx+r1*cos,"y2":cy+r1*sin,...}
```

## 云 —— 几个圆「连成一片」+ 一条底线

单独几颗圆会像眼睛；要让圆心在**同一条水平带**、互相重叠，再在底部拉一条横线封口：
```jsonc
[{"type":"circle","x":140,"y":138,"diameter":52,"stroke":"#ced4da","fill":"#fff"},
 {"type":"circle","x":182,"y":122,"diameter":72,"stroke":"#ced4da","fill":"#fff"},
 {"type":"circle","x":232,"y":124,"diameter":66,"stroke":"#ced4da","fill":"#fff"},
 {"type":"circle","x":272,"y":140,"diameter":50,"stroke":"#ced4da","fill":"#fff"},
 {"type":"line","x1":120,"y1":162,"x2":290,"y2":162,"stroke":"#ced4da"}]
```

## 房子

```jsonc
// 屋顶（三角）、墙、门、门把、窗（田字）、烟囱
{"type":"polygon","points":[[150,302],[310,172],[470,302]],"stroke":"#c92a2a","fill":"#ffa8a8","roughness":1.3}
{"type":"rect","x":175,"y":302,"w":270,"h":173,"stroke":"#495057","fill":"#fff9db","roughness":1.3}
{"type":"rect","x":272,"y":390,"w":74,"h":85,"stroke":"#6b3f1d","fill":"#c0986a"}          // 门
{"type":"rect","x":205,"y":336,"w":66,"h":58,"stroke":"#1971c2","fill":"#d0ebff"}          // 窗
{"type":"line","x1":238,"y1":336,"x2":238,"y2":394,"stroke":"#1971c2"}                     // 窗棂竖
{"type":"line","x1":205,"y1":365,"x2":271,"y2":365,"stroke":"#1971c2"}                     // 窗棂横
```
烟囱贴在**屋顶斜坡**上（x 略偏屋脊右），底部被屋顶盖住才自然。

## 流程图 / 框图（常用形状速成）

```jsonc
// 处理框
{"type":"rect","x":80,"y":60,"w":180,"h":80,"stroke":"blue","fill":"#d0ebff","roughness":1.2}
// 判断菱形（用多边形）
{"type":"polygon","points":[[380,40],[470,100],[380,160],[290,100]],"stroke":"orange","fill":"#ffe8cc"}
// 连线箭头（line + 三角头）
{"type":"line","x1":260,"y1":100,"x2":360,"y2":100,"stroke":"gray"}
{"type":"polygon","points":[[360,94],[378,100],[360,106]],"stroke":"gray","fill":"gray","roughness":0.5}
// 起始/结束（圆角可用椭圆近似）
{"type":"ellipse","x":380,"y":230,"w":160,"h":60,"stroke":"green","fill":"#d3f9d8"}
// 流程文字
{"type":"text","x":120,"y":108,"text":"读取数据","size":20,"color":"#333"}
```

## 排线/阴影

rough 的 `fill` 自动带排线（hatch）质感——这就是"手绘"味的来源。
要更"铅笔"，把 `roughness` 调到 2.2–2.8、`strokeWidth` 调细到 2。

## 验收清单（画完必看）

1. `read_image` 打开成品；
2. 大件比例对不对（太阳别太靠边、树别压房顶、地平线别穿主体）；
3. 中文有没有豆腐、被线挡住；
4. 有机形状是否成形（不是棒棒糖）；
5. 不对就改 JSON 数值重跑——**列坐标改，比"描述一遍"快**。
