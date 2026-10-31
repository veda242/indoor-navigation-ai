"""Smoke test: the decision engine must act on the most urgent of several
detected obstacles, and still track every one of them (not just the primary),
so a closer-but-lower-priority obstacle never gets silently dropped."""
import numpy as np
from enhanced_decision import NavigationDecisionEngine


def test_closest_danger_wins_over_bigger_box():
    engine = NavigationDecisionEngine(frame_width=640, frame_height=480)
    depth_map = np.zeros((480, 640), dtype=np.float32)

    # A "person" far away (low depth = far) and a "chair" very close (high depth)
    depth_map[50:450, 0:200] = 0.1   # person region: far
    depth_map[50:450, 400:600] = 0.9  # chair region: very close

    detected = [
        ("person", 0, 50, 200, 450),
        ("chair", 400, 50, 600, 450),
    ]

    decision = engine.make_navigation_decision(detected, depth_map, frame=None)

    assert decision['obstacle_info']['label'] == 'chair', \
        "the close chair should be acted on, not the far person, regardless of box size"
    assert decision['obstacle_info']['other_objects_count'] == 1


def test_all_objects_tracked_in_environment_map():
    engine = NavigationDecisionEngine(frame_width=640, frame_height=480)
    depth_map = np.full((480, 640), 0.5, dtype=np.float32)

    detected = [
        ("chair", 0, 0, 50, 50),
        ("table", 200, 200, 250, 250),
        ("sofa", 400, 400, 450, 450),
    ]

    engine.make_navigation_decision(detected, depth_map, frame=None)

    assert engine.obstacle_analyzer.obstacle_history.get('chair', 0) == 1
    assert engine.obstacle_analyzer.obstacle_history.get('table', 0) == 1
    assert engine.obstacle_analyzer.obstacle_history.get('sofa', 0) == 1


if __name__ == "__main__":
    test_closest_danger_wins_over_bigger_box()
    test_all_objects_tracked_in_environment_map()
    print("OK")
