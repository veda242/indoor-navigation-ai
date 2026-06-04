def get_depth_distance(depth_map, x1, y1, x2, y2):
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    region = depth_map[
        max(0, center_y - 5):center_y + 5,
        max(0, center_x - 5):center_x + 5
    ]

    return region.mean()


def make_decision(obj, frame_width, depth_map):
    label, x1, y1, x2, y2 = obj

    depth_value = get_depth_distance(depth_map, x1, y1, x2, y2)

    # Distance (normalized)
    if depth_value > 0.6:
        distance = "VERY CLOSE"
    elif depth_value > 0.3:
        distance = "CLOSE"
    else:
        distance = "FAR"

    center_x = (x1 + x2) // 2

    if center_x < frame_width // 3:
        suggestion = "move right"
    elif center_x < 2 * frame_width // 3:
        suggestion = "stop or move carefully"
    else:
        suggestion = "move left"

    return label, distance, suggestion