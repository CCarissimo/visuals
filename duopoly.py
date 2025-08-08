from manim import *
import numpy as np


class Duopoly(MovingCameraScene):

    def get_rectangle_corners(self, bottom_left, top_right):
        return [
            (top_right[0], top_right[1]),
            (bottom_left[0], top_right[1]),
            (bottom_left[0], bottom_left[1]),
            (top_right[0], bottom_left[1]),
        ]

    def construct(self):
        
        # setup agents as squares
        agent1 = Square(side_length=2, color=BLUE, fill_opacity=0.5)
        agent2 = Square(side_length=2, color=RED, fill_opacity=0.5)
        start_point1 = np.array([-5, 2, 0])
        start_point2 = np.array([5, 2, 0])
        agent1.move_to(start_point1)
        agent2.move_to(start_point2)
        target_scale = 2
        end_point1 = np.array([5, 2, 0])
        end_point2 = np.array([5, -2, 0])

        self.add(agent1)
        self.add(agent2)

        # self.play(
        #     self.camera.frame.animate.set_width(30)
        # )
        # self.wait(1)

        # Q table

        q_table_values = np.round(np.random.random((2, 3)) + 1, decimals=1)
        q_table_argmax = q_table_values.argmax(axis=1)

        q_table = MathTable(
            q_table_values,
            include_outer_lines=True).scale(0.7)

        q_table.move_to(np.array([-10,0,0]))

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=10,
            axis_config={"color": GREEN},
            # x_axis_config={
            #     "numbers_to_include": np.arange(-10, 10.01, 2),
            #     "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            # },
            tips=False,
        ).scale(0.5)
        axes_labels = axes.get_axis_labels()

        demand_curve = axes.plot(lambda x: 10-x, color=YELLOW)
        demand_label = axes.get_graph_label(
            demand_curve, "demand", x_val=8, direction=3*UP
        )

        plot = VGroup(axes, demand_curve)
        labels = VGroup(axes_labels, demand_label)
        self.add(plot, labels)

        # self.play(Create(plot, labels))

        p1 = ValueTracker(3)
        p2 = ValueTracker(5)
        
        cycle = np.hstack([np.flip(np.arange(2, 9, 2)), np.flip(np.arange(2, 9, 2))])
        # prices = list(zip(np.random.randint(1, 10, size=10), np.random.randint(1, 10, size=10)))
        prices = list(zip(cycle, cycle-1))
        print(prices)

        def get_player1_rectangle():
            polygon = Polygon(
                *[
                    axes.c2p(*i)
                    for i in self.get_rectangle_corners(
                        (0, 0), (10 - p1.get_value(), p1.get_value())
                    )
                ]
            )
            polygon.stroke_width = 1
            if p1.get_value() < p2.get_value():
                polygon.set_fill(BLUE, opacity=0.8)
            else:
                polygon.set_fill(BLUE, opacity=0.3)
            polygon.set_stroke(YELLOW_B)
            return polygon
        
        def get_player2_rectangle():
            polygon = Polygon(
                *[
                    axes.c2p(*i)
                    for i in self.get_rectangle_corners(
                        (0, 0), (10 - p2.get_value(), p2.get_value())
                    )
                ]
            )
            polygon.stroke_width = 1
            if p1.get_value() > p2.get_value():
                polygon.set_fill(RED, opacity=0.8)
            else:
                polygon.set_fill(RED, opacity=0.3)
            polygon.set_stroke(YELLOW_B)
            return polygon
        
        polygon1 = always_redraw(get_player1_rectangle)
        polygon2 = always_redraw(get_player2_rectangle)

        self.play(Create(polygon1))
        self.play(Create(polygon2))
        self.wait(1)

        self.play(p1.animate.set_value(4))
        self.play(p2.animate.set_value(3))
        self.wait(1)

        for price1, price2 in prices:
            # self.play([p1.animate.set_value(price1), p2.animate.set_value(price2)])
            self.play(p1.animate.set_value(price1))
            self.play(p2.animate.set_value(price2))
            self.wait(0.5)
        
        