from aegissim.config import load_config


def test_load_default_config():
    cfg = load_config("config/default.toml")
    assert cfg.window.width > 0
    assert cfg.sensors.lidar_rays == 32
