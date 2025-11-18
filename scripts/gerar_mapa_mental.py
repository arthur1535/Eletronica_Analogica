from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring


SVG_NS = "http://www.w3.org/2000/svg"


NODE_STYLE = {
    "stroke": "#1f4b99",
    "fill": "#f0f4ff",
    "stroke-width": "2",
    "rx": "10",
    "ry": "10",
}

TEXT_STYLE = {
    "fill": "#0f172a",
    "font-size": "14",
    "font-family": "DejaVu Sans, Arial, sans-serif",
    "text-anchor": "middle",
    "dominant-baseline": "middle",
}

ARROW_STYLE = {
    "stroke": "#1f4b99",
    "fill": "none",
    "stroke-width": "2",
    "marker-end": "url(#arrowhead)",
}


NODE_DATA = [
    (3, 1.5, 220, 80, "Ceifadores\n(limitadores)"),
    (7, 1.5, 220, 80, "Grampeadores\n(clampers)"),
    (2, 3.2, 200, 90, "Série\n- polarizado\n- não polarizado"),
    (4, 3.2, 200, 90, "Paralelo\n- polarizado\n- não polarizado"),
    (6, 3.2, 220, 90, "Direção\n- para cima\n- para baixo"),
    (8, 3.2, 220, 90, "Polarização\n- com fonte de bias\n- sem bias"),
    (
        2,
        5.1,
        230,
        110,
        "Efeitos práticos\n- proteção de entrada\n- recorte assimétrico\n- queda direta V_D",
    ),
    (
        4,
        5.1,
        230,
        110,
        "Análise por regiões\n- diodo ON/OFF\n- ondas senoidal, triangular, quadrada",
    ),
    (
        6,
        5.1,
        230,
        110,
        "Carga R≫RC\n- capacitor mantém carga\n- desloca nível DC",
    ),
    (8, 5.1, 230, 110, "Aplicações\n- redefinição de nível\n- multiplicadores de tensão"),
]

ARROWS = [
    ((3, 1.9), (2, 2.7)),
    ((3, 1.9), (4, 2.7)),
    ((2, 4.2), (2, 4.7)),
    ((4, 4.2), (4, 4.7)),
    ((7, 1.9), (6, 2.7)),
    ((7, 1.9), (8, 2.7)),
    ((6, 4.2), (6, 4.7)),
    ((8, 4.2), (8, 4.7)),
]


def create_svg(width=1000, height=720):
    svg = Element("svg", attrib={"xmlns": SVG_NS, "width": str(width), "height": str(height)})

    defs = SubElement(svg, "defs")
    marker = SubElement(
        defs,
        "marker",
        attrib={
            "id": "arrowhead",
            "markerWidth": "10",
            "markerHeight": "7",
            "refX": "8",
            "refY": "3.5",
            "orient": "auto",
            "markerUnits": "strokeWidth",
        },
    )
    SubElement(marker, "path", attrib={"d": "M0,0 L10,3.5 L0,7 z", "fill": "#1f4b99"})

    SubElement(
        svg,
        "text",
        attrib={
            "x": str(width / 2),
            "y": "35",
            "fill": "#1f4b99",
            "font-size": "20",
            "font-family": TEXT_STYLE["font-family"],
            "text-anchor": "middle",
        },
    ).text = "Mapa mental: ceifadores e grampeadores"

    for cx, cy, w, h, label in NODE_DATA:
        x = cx * 100
        y = cy * 100
        rect_attrib = {
            "x": str(x - w / 2),
            "y": str(y - h / 2 + 40),
            "width": str(w),
            "height": str(h),
            **NODE_STYLE,
        }
        SubElement(svg, "rect", attrib=rect_attrib)

        text = SubElement(
            svg,
            "text",
            attrib={
                "x": str(x),
                "y": str(y + 40),
                **TEXT_STYLE,
            },
        )
        for i, line in enumerate(label.split("\n")):
            tspan = SubElement(
                text,
                "tspan",
                attrib={
                    "x": str(x),
                    "dy": str(16 if i else 0),
                },
            )
            tspan.text = line

    for start, end in ARROWS:
        x1, y1 = (start[0] * 100, start[1] * 100 + 40)
        x2, y2 = (end[0] * 100, end[1] * 100 + 40)
        SubElement(
            svg,
            "line",
            attrib={
                "x1": str(x1),
                "y1": str(y1),
                "x2": str(x2),
                "y2": str(y2),
                **ARROW_STYLE,
            },
        )

    return svg


def save_svg(path: Path):
    svg_element = create_svg()
    path.write_bytes(tostring(svg_element))


def main():
    output_path = Path("docs/img/mapa_mental_ceifadores_grampeadores.svg")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_svg(output_path)
    print(f"SVG salvo em {output_path.resolve()}")


if __name__ == "__main__":
    main()
