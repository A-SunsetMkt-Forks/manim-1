"""Functions determining transformation paths between sets of points."""

from __future__ import annotations

__all__ = [
    "straight_path",
    "path_along_arc",
    "clockwise_path",
    "counterclockwise_path",
]


from typing import TYPE_CHECKING

import numpy as np

from ..constants import OUT
from ..utils.bezier import interpolate
from ..utils.space_ops import normalize, rotation_matrix

if TYPE_CHECKING:
    from manim.typing import (
        PathFuncType,
        Point3D_Array,
        Point3DLike_Array,
        Vector3DLike,
    )


STRAIGHT_PATH_THRESHOLD = 0.01


def straight_path() -> PathFuncType:
    """Simplest path function. Each point in a set goes in a straight path toward its destination.

    Examples
    --------

    .. manim :: StraightPathExample

        class StraightPathExample(Scene):
            def construct(self):
                colors = [RED, GREEN, BLUE]

                starting_points = VGroup(
                    *[
                        Dot(LEFT + pos, color=color)
                        for pos, color in zip([UP, DOWN, LEFT], colors)
                    ]
                )

                finish_points = VGroup(
                    *[
                        Dot(RIGHT + pos, color=color)
                        for pos, color in zip([ORIGIN, UP, DOWN], colors)
                    ]
                )

                self.add(starting_points)
                self.add(finish_points)
                for dot in starting_points:
                    self.add(TracedPath(dot.get_center, stroke_color=dot.get_color()))

                self.wait()
                self.play(
                    Transform(
                        starting_points,
                        finish_points,
                        path_func=utils.paths.straight_path(),
                        run_time=2,
                    )
                )
                self.wait()

    """
    return interpolate


def path_along_circles(
    arc_angle: float, circles_centers: Point3DLike_Array, axis: Vector3DLike = OUT
) -> PathFuncType:
    """This function transforms each point by moving it roughly along a circle, each with its own specified center.

    The path may be seen as each point smoothly changing its orbit from its starting position to its destination.

    Parameters
    ----------
    arc_angle
        The angle each point traverses around the quasicircle.
    circles_centers
        The centers of each point's quasicircle to rotate around.
    axis
        The axis of rotation.

    Examples
    --------

    .. manim :: PathAlongCirclesExample

        class PathAlongCirclesExample(Scene):
            def construct(self):
                colors = [RED, GREEN, BLUE]

                starting_points = VGroup(
                    *[
                        Dot(LEFT + pos, color=color)
                        for pos, color in zip([UP, DOWN, LEFT], colors)
                    ]
                )

                finish_points = VGroup(
                    *[
                        Dot(RIGHT + pos, color=color)
                        for pos, color in zip([ORIGIN, UP, DOWN], colors)
                    ]
                )

                self.add(starting_points)
                self.add(finish_points)
                for dot in starting_points:
                    self.add(TracedPath(dot.get_center, stroke_color=dot.get_color()))

                circle_center = Dot(3 * LEFT)
                self.add(circle_center)

                self.wait()
                self.play(
                    Transform(
                        starting_points,
                        finish_points,
                        path_func=utils.paths.path_along_circles(
                            2 * PI, circle_center.get_center()
                        ),
                        run_time=3,
                    )
                )
                self.wait()

    """
    unit_axis = normalize(axis, fall_back=OUT)

    def path(
        start_points: Point3D_Array, end_points: Point3D_Array, alpha: float
    ) -> Point3D_Array:
        detransformed_end_points = circles_centers + np.dot(
            end_points - circles_centers, rotation_matrix(-arc_angle, unit_axis).T
        )
        rot_matrix = rotation_matrix(alpha * arc_angle, unit_axis)
        return circles_centers + np.dot(
            interpolate(start_points, detransformed_end_points, alpha)
            - circles_centers,
            rot_matrix.T,
        )

    return path


def path_along_arc(arc_angle: float, axis: Vector3DLike = OUT) -> PathFuncType:
    """This function transforms each point by moving it along a circular arc.

    Parameters
    ----------
    arc_angle
        The angle each point traverses around a circular arc.
    axis
        The axis of rotation.

    Examples
    --------

    .. manim :: PathAlongArcExample

        class PathAlongArcExample(Scene):
            def construct(self):
                colors = [RED, GREEN, BLUE]

                starting_points = VGroup(
                    *[
                        Dot(LEFT + pos, color=color)
                        for pos, color in zip([UP, DOWN, LEFT], colors)
                    ]
                )

                finish_points = VGroup(
                    *[
                        Dot(RIGHT + pos, color=color)
                        for pos, color in zip([ORIGIN, UP, DOWN], colors)
                    ]
                )

                self.add(starting_points)
                self.add(finish_points)
                for dot in starting_points:
                    self.add(TracedPath(dot.get_center, stroke_color=dot.get_color()))

                self.wait()
                self.play(
                    Transform(
                        starting_points,
                        finish_points,
                        path_func=utils.paths.path_along_arc(TAU * 2 / 3),
                        run_time=3,
                    )
                )
                self.wait()

    """
    if abs(arc_angle) < STRAIGHT_PATH_THRESHOLD:
        return straight_path()
    unit_axis = normalize(axis, fall_back=OUT)

    def path(
        start_points: Point3D_Array, end_points: Point3D_Array, alpha: float
    ) -> Point3D_Array:
        vects = end_points - start_points
        centers = start_points + 0.5 * vects
        if arc_angle != np.pi:
            centers += np.cross(unit_axis, vects / 2.0) / np.tan(arc_angle / 2)
        rot_matrix = rotation_matrix(alpha * arc_angle, unit_axis)
        return centers + np.dot(start_points - centers, rot_matrix.T)

    return path


def clockwise_path() -> PathFuncType:
    """This function transforms each point by moving clockwise around a half circle.

    Examples
    --------

    .. manim :: ClockwisePathExample

        class ClockwisePathExample(Scene):
            def construct(self):
                colors = [RED, GREEN, BLUE]

                starting_points = VGroup(
                    *[
                        Dot(LEFT + pos, color=color)
                        for pos, color in zip([UP, DOWN, LEFT], colors)
                    ]
                )

                finish_points = VGroup(
                    *[
                        Dot(RIGHT + pos, color=color)
                        for pos, color in zip([ORIGIN, UP, DOWN], colors)
                    ]
                )

                self.add(starting_points)
                self.add(finish_points)
                for dot in starting_points:
                    self.add(TracedPath(dot.get_center, stroke_color=dot.get_color()))

                self.wait()
                self.play(
                    Transform(
                        starting_points,
                        finish_points,
                        path_func=utils.paths.clockwise_path(),
                        run_time=2,
                    )
                )
                self.wait()

    """
    return path_along_arc(-np.pi)


def counterclockwise_path() -> PathFuncType:
    """This function transforms each point by moving counterclockwise around a half circle.

    Examples
    --------

    .. manim :: CounterclockwisePathExample

        class CounterclockwisePathExample(Scene):
            def construct(self):
                colors = [RED, GREEN, BLUE]

                starting_points = VGroup(
                    *[
                        Dot(LEFT + pos, color=color)
                        for pos, color in zip([UP, DOWN, LEFT], colors)
                    ]
                )

                finish_points = VGroup(
                    *[
                        Dot(RIGHT + pos, color=color)
                        for pos, color in zip([ORIGIN, UP, DOWN], colors)
                    ]
                )

                self.add(starting_points)
                self.add(finish_points)
                for dot in starting_points:
                    self.add(TracedPath(dot.get_center, stroke_color=dot.get_color()))

                self.wait()
                self.play(
                    Transform(
                        starting_points,
                        finish_points,
                        path_func=utils.paths.counterclockwise_path(),
                        run_time=2,
                    )
                )
                self.wait()

    """
    return path_along_arc(np.pi)


def spiral_path(angle: float, axis: Vector3DLike = OUT) -> PathFuncType:
    """This function transforms each point by moving along a spiral to its destination.

    Parameters
    ----------
    angle
        The angle each point traverses around a spiral.
    axis
        The axis of rotation.

    Examples
    --------

    .. manim :: SpiralPathExample

        class SpiralPathExample(Scene):
            def construct(self):
                colors = [RED, GREEN, BLUE]

                starting_points = VGroup(
                    *[
                        Dot(LEFT + pos, color=color)
                        for pos, color in zip([UP, DOWN, LEFT], colors)
                    ]
                )

                finish_points = VGroup(
                    *[
                        Dot(RIGHT + pos, color=color)
                        for pos, color in zip([ORIGIN, UP, DOWN], colors)
                    ]
                )

                self.add(starting_points)
                self.add(finish_points)
                for dot in starting_points:
                    self.add(TracedPath(dot.get_center, stroke_color=dot.get_color()))

                self.wait()
                self.play(
                    Transform(
                        starting_points,
                        finish_points,
                        path_func=utils.paths.spiral_path(2 * TAU),
                        run_time=5,
                    )
                )
                self.wait()

    """
    if abs(angle) < STRAIGHT_PATH_THRESHOLD:
        return straight_path()
    unit_axis = normalize(axis, fall_back=OUT)

    def path(
        start_points: Point3D_Array, end_points: Point3D_Array, alpha: float
    ) -> Point3D_Array:
        rot_matrix = rotation_matrix((alpha - 1) * angle, unit_axis)
        return start_points + alpha * np.dot(end_points - start_points, rot_matrix.T)

    return path
