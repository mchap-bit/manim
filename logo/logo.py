from manim.manimlib.animation.creation import DrawBorderThenFill, ShowCreation, Write
from manim.manimlib.animation.growing import GrowFromCenter
from manim.manimlib.constants import DOWN, LEFT, TAU, WHITE
from manim.manimlib.mobject.geometry import DashedLine, Dot
from manim.manimlib.mobject.geometry import RegularPolygon
from manim.manimlib.mobject.svg.tex_mobject import Tex
from manim.manimlib.mobject.value_tracker import ValueTracker
from manimlib.imports import *

NEW_BLUE = "#68a8e1"

class Thumbnail(GraphScene):
    CONFIG = {
        "y_max": 8,
        "y_axis_height": 5,
    }

    def construct(self):
        self.show_function_graph()

    def get_x_value(self,input_tracker):
        return input_tracker.get_value()

    def get_y_value(self, input_tracker, graph):
        return graph.underlying_function(self.get_x_value(input_tracker))

    def get_x_point(self, input_tracker):
        return self.coords_to_point(self.get_x_value(input_tracker), 0)

    def get_y_point(self, input_tracker, graph):
        return self.coords_to_point(0, self.get_y_value(input_tracker, graph))

    def get_graph_point(self, input_tracker, graph):
        return self.coords_to_point(
            self.get_x_value(input_tracker),
            self.get_y_value(input_tracker, graph)
        )

    def get_v_line(self, input_tracker, graph):
        return DashedLine(
            self.get_x_point(input_tracker), 
            self.get_graph_point(input_tracker, graph), 
            stroke_width=2
        )

    def get_h_line(self, input_tracker, graph):
        return DashedLine(
            self.get_graph_point(input_tracker, graph), 
            self.get_y_point(input_tracker, graph), 
            stroke_width=2
        )

    def create_marker_triangle(self, start_angle):
        triangle = RegularPolygon(n=3, start_angle=start_angle)
        triangle.set_fill(WHITE, 1)
        triangle.set_stroke(width=0)
        triangle.scale(0.1)
        return triangle

    def create_graph_marker(self, input_tracker, graph, x_text, y_text):
        x_label = Tex(x_text)
        y_label = Tex(y_text)

        input_triangle = self.create_marker_triangle(start_angle=TAU / 4)
        output_triangle = self.create_marker_triangle(start_angle=0)

        v_line = self.get_v_line(input_tracker, graph)
        h_line = self.get_h_line(input_tracker, graph)

        dot = Dot(color=WHITE)

        x_label.next_to(v_line, DOWN)
        y_label.next_to(h_line, LEFT)

        input_triangle.next_to(v_line, DOWN, buff=0)
        output_triangle.next_to(h_line, LEFT, buff=0)

        dot.move_to(self.get_graph_point(input_tracker, graph))

        return {
            "x_label": x_label,
            "y_label": y_label,
            "input_triangle": input_triangle,
            "output_triangle": output_triangle,
            "v_line": v_line,
            "h_line": h_line,
            "dot": dot
        }

    def animate_marker(self, marker):
        return [
            DrawBorderThenFill(marker["input_triangle"]),
            Write(marker["x_label"]),
            ShowCreation(marker["v_line"]),
            GrowFromCenter(marker["dot"]),
            ShowCreation(marker["h_line"]),
            Write(marker["y_label"]),
            DrawBorderThenFill(marker["output_triangle"]),
        ]
    
    def show_function_graph(self):
        self.setup_axes(animate=False)
        def func(x):
            return 0.1 * (x + 3-5) * (x - 3-5) * (x-5) + 5

        def rect(x):
            return 2.775*(x-1.5)+3.862
        recta = self.get_graph(rect,x_min=-1,x_max=5)
        graph = self.get_graph(func,x_min=0.2,x_max=9)
        graph.set_color(NEW_BLUE)
        input_tracker_p1 = ValueTracker(1.5)
        input_tracker_p2 = ValueTracker(3.5)

        # 
        marker_p1 = self.create_graph_marker(input_tracker_p1, graph, "a", "f(a)")
        # 
        marker_p2 = self.create_graph_marker(input_tracker_p2, graph, "b", "f(b)")

        #
        self.play(
            ShowCreation(graph),
        )
        # Animacion del punto a
        self.add_foreground_mobject(marker_p1["dot"])
        self.add_foreground_mobject(marker_p2["dot"])

        self.play(
            *self.animate_marker(marker_p1),
            *self.animate_marker(marker_p2),
            run_time=0.5
        )

        self.add(
            marker_p2["input_triangle"],
            marker_p2["x_label"],
            marker_p2["dot"],
            marker_p2["v_line"],
            marker_p2["h_line"],
            marker_p2["output_triangle"],
            marker_p2["y_label"],
        )
        ###################
        pendiente_recta = self.get_secant_slope_group(
            1.9, recta, dx = 1.4,
            df_label = None,
            dx_label = None,
            dx_line_color = PURPLE,
            df_line_color= ORANGE,
            )
        grupo_secante = self.get_secant_slope_group(
            1.5, graph, dx = 2,
            df_label = None,
            dx_label = None,
            dx_line_color = "#942357",
            df_line_color= "#3f7d5c",
            secant_line_color = RED,
        )


        self.add(
            marker_p2["input_triangle"],
            marker_p2["dot"],
            marker_p2["v_line"],
            marker_p2["h_line"],
            marker_p2["output_triangle"],
        )
        self.play(FadeIn(grupo_secante))

        kwargs = {
            "x_min" : 4,
            "x_max" : 9,
            "fill_opacity" : 0.75,
            "stroke_width" : 0.25,
        }
        self.graph=graph
        iteraciones=6


        self.rect_list = self.get_riemann_rectangles_list(
            graph, iteraciones,start_color=PURPLE,end_color=ORANGE, **kwargs
        )
        flat_rects = self.get_riemann_rectangles(
            self.get_graph(lambda x : 0), dx = 0.5,start_color=invert_color(PURPLE),end_color=invert_color(ORANGE),**kwargs
        )
        rects = self.rect_list[0]
        self.transform_between_riemann_rects(
            flat_rects, rects, 
            replace_mobject_with_target_in_scene = True,
            run_time=0.9
        )

        # adding manim
        picture = Group(*self.mobjects)
        picture.scale(0.6).to_edge(LEFT, buff=SMALL_BUFF)
        manim = TexText("Manim").set_height(1.5) \
                                    .next_to(picture, RIGHT) \
                                    .shift(DOWN * 0.7)
        self.add(manim)
