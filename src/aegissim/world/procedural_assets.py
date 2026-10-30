from __future__ import annotations

from panda3d.core import (
    CardMaker,
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    NodePath,
)


def make_floor(width: float, depth: float) -> NodePath:
    cm = CardMaker("warehouse_floor_card")
    cm.setFrame(-width / 2.0, width / 2.0, -depth / 2.0, depth / 2.0)
    floor = NodePath(cm.generate())
    floor.setP(-90)
    floor.setColor(0.18, 0.18, 0.19, 1)
    floor.setTwoSided(True)
    return floor


def make_box(name: str, scale: tuple[float, float, float], color: tuple[float, float, float, float]) -> NodePath:
    sx, sy, sz = scale
    hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0

    vertices = [
        (-hx, -hy, -hz), ( hx, -hy, -hz), ( hx,  hy, -hz), (-hx,  hy, -hz),
        (-hx, -hy,  hz), ( hx, -hy,  hz), ( hx,  hy,  hz), (-hx,  hy,  hz),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]

    fmt = GeomVertexFormat.getV3n3c4()
    vdata = GeomVertexData(name, fmt, Geom.UHStatic)
    vertex = GeomVertexWriter(vdata, "vertex")
    normal = GeomVertexWriter(vdata, "normal")
    color_writer = GeomVertexWriter(vdata, "color")

    # Flat normals by duplicating vertices per face.
    tri = GeomTriangles(Geom.UHStatic)
    idx = 0
    for face in faces:
        pts = [vertices[i] for i in face]
        ux, uy, uz = (pts[1][0] - pts[0][0], pts[1][1] - pts[0][1], pts[1][2] - pts[0][2])
        vx, vy, vz = (pts[2][0] - pts[1][0], pts[2][1] - pts[1][1], pts[2][2] - pts[1][2])
        nx, ny, nz = (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)
        length = max((nx * nx + ny * ny + nz * nz) ** 0.5, 1e-8)
        n = (nx / length, ny / length, nz / length)
        for p in pts:
            vertex.addData3(*p)
            normal.addData3(*n)
            color_writer.addData4(*color)
        tri.addVertices(idx, idx + 1, idx + 2)
        tri.addVertices(idx, idx + 2, idx + 3)
        idx += 4

    geom = Geom(vdata)
    geom.addPrimitive(tri)
    node = GeomNode(name)
    node.addGeom(geom)
    np = NodePath(node)
    np.setColor(*color)
    return np
