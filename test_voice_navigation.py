"""Smoke test: emergency_stop must be cooled down, the queue must cap backlog,
and emergency messages must name the obstacle so a blind user gets directions."""
from unittest.mock import patch

with patch("subprocess.run"):
    from voice_navigation import VoiceNavigationSystem


def test_emergency_stop_has_cooldown():
    vs = VoiceNavigationSystem()
    for _ in range(50):
        vs.emergency_stop(obstacle_label="chair", position="on your left")
    assert vs.voice_queue.qsize() <= 1, "emergency_stop should not flood the queue when called every frame"


def test_emergency_stop_names_obstacle_and_position():
    vs = VoiceNavigationSystem()
    vs.emergency_stop(obstacle_label="chair", position="on your left")
    assert "chair" in vs.feedback_history[-1]['message']
    assert "on your left" in vs.feedback_history[-1]['message']


def test_queue_drops_when_backed_up():
    vs = VoiceNavigationSystem()
    for i in range(10):
        vs.say(f"message {i}")
    assert vs.voice_queue.qsize() <= 2, "say() should drop messages once the queue is backed up"


if __name__ == "__main__":
    test_emergency_stop_has_cooldown()
    test_emergency_stop_names_obstacle_and_position()
    test_queue_drops_when_backed_up()
    print("OK")
