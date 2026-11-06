#!/usr/bin/env python3
"""Rough.js 手绘风格渲染器：JSON 场景 -> SVG -> PNG。
- 不指定 bg_image 时：在纯色/白底画布上画手绘图形（示意图、圈注草图）
- 指定 bg_image 时：在已有图片（如截图）上叠加手绘圈/箭头/文字（手工涂描感）

场景: {"w":1000,"h":620,"bg":"#ffffff","bg_image":"shot.png","items":[ ... ]}
item: rect{x,y,w,h,stroke,fill,strokeWidth,roughness} | circle{x,y,d,...}
      | ellipse{x,y,w,h,...} | line{x1,y1,x2,y2,...} | polygon{points:[[x,y]..]}
      | text{x,y,text,size,color,align}
颜色可写名字: orange/red/green/blue/gray 或 #rrggbb。
"""
import json, sys
from rough import canvas, Options
import cairosvg
from PIL import Image

NAMED = dict(orange="#e8590c", red="#c92a2a", green="#2f9e44", blue="#1971c2", gray="#495057")

def _col(v, default=None):
    if v is None:
        return default
    return NAMED.get(v, v)

def opt(d, **over):
    return Options(stroke=_col(d.get("stroke", "orange")),
                   strokeWidth=d.get("strokeWidth", 3),
                   roughness=d.get("roughness", 2.0),
                   fill=_col(d.get("fill"), "none"),
                   bowing=d.get("bowing", 1.0), **over)

def build(scene, W, H):
    c = canvas(W, H)
    for it in scene.get("items", []):
        t = it.get("type")
        if t == "rect":
            c.rectangle(x=it["x"], y=it["y"], w=it["w"], h=it["h"], options=opt(it))
        elif t == "circle":
            c.circle(x=it["x"], y=it["y"],
                     diameter=it.get("diameter", it.get("d", 60)), options=opt(it))
        elif t == "ellipse":
            c.ellipse(x=it["x"], y=it["y"], w=it["w"], h=it["h"], options=opt(it))
        elif t == "line":
            c.line(it["x1"], it["y1"], it["x2"], it["y2"], options=opt(it))
        elif t == "polygon":
            c.polygon([tuple(p) for p in it["points"]], options=opt(it))
        elif t == "text":
            o = opt(it, fontSize=it.get("size", 22),
                    fontFamily="Noto Sans CJK SC, Noto Sans CJK JP, sans-serif")
            o.fill = _col(it.get("color"), "#1b1f24")
            c.text(it["x"], it["y"], it["text"], options=o)
    # auto_fit=False 关键：默认 True 会把所有图形缩放平移到铺满画布，
    # 叠在截图/图上时坐标就全乱了。必须关掉，坐标即像素坐标。
    return c.as_svg(W, H, auto_fit=False)

def main():
    if len(sys.argv) < 3:
        print("usage: sketch_render.py scene.json out.png", file=sys.stderr); sys.exit(2)
    scene = json.load(open(sys.argv[1], encoding="utf-8"))
    bg_image = scene.get("bg_image")
    if bg_image:
        base = Image.open(bg_image).convert("RGBA")
        W, H = base.size
    else:
        W, H = scene.get("w", 1000), scene.get("h", 620)
        base = None
    svg = build(scene, W, H)
    marks = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=W, output_height=H)
    layer = Image.open(__import__("io").BytesIO(marks)).convert("RGBA")
    if base is not None:
        out = Image.alpha_composite(base, layer)
    else:
        out = Image.new("RGBA", (W, H), scene.get("bg", "#ffffff"))
        out = Image.alpha_composite(out, layer)
    out.convert("RGB").save(sys.argv[2])
    print(sys.argv[2])

if __name__ == "__main__":
    main()
