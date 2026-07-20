#!/usr/bin/env python3
"""Render a small, dependency-free circuit JSON format to SVG."""

from __future__ import annotations

import argparse
import html
import json
import math
from pathlib import Path


def pt(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("points must be [x, y]")
    return float(value[0]), float(value[1])


def transform(a, b, along, normal=0):
    x1, y1 = a
    x2, y2 = b
    length = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    return x1 + ux * along - uy * normal, y1 + uy * along + ux * normal


def line(a, b, **attrs):
    extra = " ".join(f'{k.replace("_", "-")}="{html.escape(str(v))}"' for k, v in attrs.items())
    return f'<line x1="{a[0]:g}" y1="{a[1]:g}" x2="{b[0]:g}" y2="{b[1]:g}" {extra}/>'


def text_at(p, value, css="label"):
    return f'<text x="{p[0]:g}" y="{p[1]:g}" class="{css}">{html.escape(str(value))}</text>'


def component_svg(item):
    a, b = pt(item["from"]), pt(item["to"])
    length = math.dist(a, b)
    if length < 50:
        raise ValueError(f'{item.get("id", "component")}: length must be at least 50')
    if a[0] != b[0] and a[1] != b[1]:
        raise ValueError(f'{item.get("id", "component")}: only horizontal/vertical placement is supported')
    kind = item["type"]
    out = [f'<g id="{html.escape(str(item.get("id", kind)))}">']
    center = transform(a, b, length / 2)
    p1, p2 = transform(a, b, length * .36), transform(a, b, length * .64)
    out += [line(a, p1, **{"class": "wire"}), line(p2, b, **{"class": "wire"})]
    if kind == "resistor":
        corners = [transform(a, b, length*.36, -10), transform(a, b, length*.64, -10),
                   transform(a, b, length*.64, 10), transform(a, b, length*.36, 10)]
        out.append('<polygon class="symbol" points="' + " ".join(f"{x:g},{y:g}" for x, y in corners) + '"/>')
    elif kind == "capacitor":
        c1, c2 = transform(a, b, length*.46), transform(a, b, length*.54)
        out += [line(p1, c1, **{"class": "wire"}), line(c2, p2, **{"class": "wire"}),
                line(transform(a,b,length*.46,-16), transform(a,b,length*.46,16), **{"class":"symbol"}),
                line(transform(a,b,length*.54,-16), transform(a,b,length*.54,16), **{"class":"symbol"})]
    elif kind == "inductor":
        start, end = length*.36, length*.64
        steps = []
        for index in range(17):
            t = index / 16
            along = start + (end-start)*t
            normal = 10 * math.sin(t * 4 * math.pi)
            steps.append(transform(a, b, along, normal))
        out.append('<polyline class="symbol" points="' + " ".join(f"{x:g},{y:g}" for x,y in steps) + '"/>')
    elif kind in {"voltage_source", "current_source"}:
        radius = min(22, length*.14)
        out += [line(p1, transform(a,b,length/2-radius), **{"class":"wire"}),
                line(transform(a,b,length/2+radius), p2, **{"class":"wire"}),
                f'<circle class="symbol" cx="{center[0]:g}" cy="{center[1]:g}" r="{radius:g}"/>']
        if kind == "voltage_source":
            polarity = item.get("polarity", "+-")
            if polarity not in {"+-", "-+"}:
                raise ValueError(f'{item.get("id", "voltage_source")}: polarity must be +- or -+')
            out += [text_at(transform(a,b,length*.43,-4), polarity[0], "symbol-text"),
                    text_at(transform(a,b,length*.60,-4), polarity[1], "symbol-text")]
        else:
            start, end = transform(a,b,length*.42), transform(a,b,length*.58)
            out += [line(start,end,**{"class":"arrow current"}),]
    elif kind == "diode":
        left, right = transform(a,b,length*.42), transform(a,b,length*.58)
        tri = [transform(a,b,length*.42,-13), transform(a,b,length*.42,13), right]
        out += [line(p1,left,**{"class":"wire"}), line(right,p2,**{"class":"wire"}),
                '<polygon class="symbol" points="' + " ".join(f"{x:g},{y:g}" for x,y in tri) + '"/>',
                line(transform(a,b,length*.58,-14), transform(a,b,length*.58,14), **{"class":"symbol"})]
    elif kind == "switch":
        left, right = transform(a,b,length*.42), transform(a,b,length*.58)
        blade = transform(a,b,length*.57,-16)
        out += [line(p1,left,**{"class":"wire"}), line(right,p2,**{"class":"wire"}),
                f'<circle class="node" cx="{left[0]:g}" cy="{left[1]:g}" r="3"/>',
                f'<circle class="node" cx="{right[0]:g}" cy="{right[1]:g}" r="3"/>',
                line(left,blade,**{"class":"symbol"})]
    elif kind == "short":
        out = [f'<g id="{html.escape(str(item.get("id", kind)))}">', line(a,b,**{"class":"wire"})]
    else:
        raise ValueError(f"unsupported component type: {kind}")
    label = item.get("label", item.get("id", ""))
    value = item.get("value", "")
    offset = transform(a, b, length/2, -32)
    if label:
        out.append(text_at(offset, label))
    if value:
        out.append(text_at((offset[0], offset[1] + 15), value, "value"))
    out.append("</g>")
    return "".join(out)


def render(data):
    width, height = int(data.get("width", 640)), int(data.get("height", 360))
    if width < 100 or height < 100:
        raise ValueError("canvas must be at least 100 by 100")
    body = []
    if data.get("title"):
        body.append(text_at((width/2, 28), data["title"], "title"))
    for wire in data.get("wires", []):
        points = [pt(p) for p in wire["points"]]
        if len(points) < 2:
            raise ValueError("wire needs at least two points")
        body.append('<polyline class="wire" points="' + " ".join(f"{x:g},{y:g}" for x,y in points) + '"/>')
    for item in data.get("components", []):
        body.append(component_svg(item))
    for node in data.get("nodes", []):
        p = pt(node["at"])
        body.append(f'<circle class="node" cx="{p[0]:g}" cy="{p[1]:g}" r="4"/>')
        if node.get("label"):
            body.append(text_at((p[0]+7,p[1]-7), node["label"], "node-label"))
    for ann in data.get("annotations", []):
        a,b = pt(ann["from"]), pt(ann["to"])
        css = "arrow current" if ann.get("kind") == "current" else "arrow voltage"
        body.append(line(a,b,**{"class":css}))
        if ann.get("label"):
            body.append(text_at(((a[0]+b[0])/2+6,(a[1]+b[1])/2-6), ann["label"], css.split()[-1]+"-text"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="context-stroke"/></marker></defs>
<style>.wire,.symbol{{fill:none;stroke:#111;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}.node{{fill:#111}}text{{font-family:Arial,"Microsoft YaHei",sans-serif;font-size:14px;letter-spacing:0}}.label,.value,.node-label{{text-anchor:middle}}.value{{font-size:12px}}.title{{font-size:18px;font-weight:600;text-anchor:middle}}.symbol-text{{text-anchor:middle;font-size:14px}}.arrow{{stroke-width:2;marker-end:url(#arrow)}}.current{{stroke:#1565c0}}.voltage{{stroke:#c62828}}.current-text{{fill:#1565c0}}.voltage-text{{fill:#c62828}}</style>
<rect width="100%" height="100%" fill="white"/>{''.join(body)}</svg>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(data), encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
