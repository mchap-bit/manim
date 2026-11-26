from logo.logo import Thumbnail
from manimlib.mobject.value_tracker import ValueTracker
from manimlib.mobject.geometry import (
    Dot,
    DashedLine,
    RegularPolygon,
)
from unittest.mock import call, patch

def build_scene():
    scene = Thumbnail()
    scene.setup_axes()
    return scene


def build_marker(scene, graph):
    with patch("logo.logo.Tex") as tex_factory:
        marker = scene.create_graph_marker(
            ValueTracker(1),
            graph,
            "a",
            "f(a)",
        )

    assert tex_factory.call_args_list == [call("a"), call("f(a)")]
    return marker


def test_get_x_value():
    scene = build_scene()

    tracker = ValueTracker(3.5)

    assert scene.get_x_value(tracker) == 3.5


def test_create_marker_triangle():
    scene = build_scene()

    triangle = scene.create_marker_triangle(0)

    assert isinstance(triangle, RegularPolygon)


def test_create_graph_marker_returns_expected_keys():
    scene = build_scene()

    graph = scene.get_graph(lambda x: x)
    marker = build_marker(scene, graph)

    assert set(marker.keys()) == {
        "x_label",
        "y_label",
        "input_triangle",
        "output_triangle",
        "v_line",
        "h_line",
        "dot",
    }


def test_create_graph_marker_types():
    scene = build_scene()

    graph = scene.get_graph(lambda x: x)
    marker = build_marker(scene, graph)

    assert isinstance(marker["dot"], Dot)
    assert isinstance(marker["v_line"], DashedLine)
    assert isinstance(marker["h_line"], DashedLine)