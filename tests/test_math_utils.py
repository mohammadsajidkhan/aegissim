from aegissim.utils.math_utils import AABB, ray_intersects_aabb_2d, sphere_intersects_aabb


def test_sphere_intersects_aabb():
    box = AABB("box", (0, 0, 0), (1, 1, 1))
    assert sphere_intersects_aabb((1.2, 0, 0), 0.3, box)
    assert not sphere_intersects_aabb((2.0, 0, 0), 0.3, box)


def test_ray_intersects_aabb_2d():
    box = AABB("box", (0, 5, 1), (1, 1, 2))
    hit = ray_intersects_aabb_2d((0, 0, 1), (0, 1), box, 10)
    assert hit is not None
    assert 3.9 < hit < 4.1
