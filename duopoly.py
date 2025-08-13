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

        # Add text above the agents, "Agent 1" and "Agent 2"
        agent1_text = Text("Agent 1", font_size=24, color=BLACK).next_to(agent1, UP)
        agent2_text = Text("Agent 2", font_size=24, color=BLACK).next_to(agent2, UP)
        self.play(Write(agent1_text), Write(agent2_text))
        self.wait(1)

        # q_table_values = np.round(np.random.random((2, 3)) + 1, decimals=1)
        # q_table_argmax = q_table_values.argmax(axis=1)

        # q_table = MathTable(
        #     q_table_values,
        #     include_outer_lines=True).scale(0.7)

        # q_table.move_to(np.array([-10,0,0]))

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

        # Add the label "price" to the y-axis, cenetered on the y-axis
        # set color to BLACK
        price_label = axes.get_y_axis_label("price", edge=UP, direction=LEFT, buff=0.2)
        axes_labels.add(price_label)
        axes_labels.set_color(BLACK)
        axes_labels.set_stroke(BLACK, 1)

        # Add the label "quantity" to the x-axis
        quantity_label = axes.get_x_axis_label("quantity", edge=RIGHT, direction=DOWN, buff=0.2)
        axes_labels.add(quantity_label)
        axes_labels.set_color(BLACK)
        axes_labels.set_stroke(BLACK, 1)
        
        # Create the demand curve

        demand_curve = axes.plot(lambda x: 10-x, color=BLACK)
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
            if p1.get_value() == p2.get_value():
                # if both prices are equal, create two rectangles side by side
                if p1.get_value() == p2.get_value():
                    # if both prices are equal, create two rectangles side by side
                    polygon = Polygon(
                        *[
                            axes.c2p(*i)
                            for i in self.get_rectangle_corners(
                                (0, 0), ((10 - p1.get_value())/2, p1.get_value())
                            )
                        ]
                    )
                    polygon.stroke_width = 1
                    polygon.set_fill(BLUE, opacity=0.8)

            else:
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
                    polygon.set_fill(BLUE, opacity=0.1)
            polygon.set_stroke(YELLOW_B)
            return polygon
        
        def get_player2_rectangle():
            if p1.get_value() == p2.get_value():
                # if both prices are equal, create two rectangles side by side
                polygon = Polygon(
                    *[
                        axes.c2p(*i)
                        for i in self.get_rectangle_corners(
                            ((10 - p2.get_value())/2, 0), (10 - p2.get_value(), p2.get_value())
                        )
                    ]
                )
                polygon.stroke_width = 1
                polygon.set_fill(RED, opacity=0.8)
            
            else:
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
                    polygon.set_fill(RED, opacity=0.1)
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

        # Prices compete to Nash Equilibrium
        self.play(p1.animate.set_value(3))
        self.play(p2.animate.set_value(3))
        self.wait(1)
        self.play(p1.animate.set_value(3))
        self.play(p2.animate.set_value(2))
        self.wait(1)
        self.play(p1.animate.set_value(1))
        self.play(p2.animate.set_value(2))
        self.wait(1)
        self.play(p1.animate.set_value(1))
        self.play(p2.animate.set_value(1))
        self.wait(1)

        # Add text below the graph
        nash_equilibrium = Text("Nash Equilibrium: prices = 1", font_size=36, color=BLACK).next_to(axes, DOWN, buff=1)
        self.play(FadeIn(nash_equilibrium))
        self.wait(2)
        self.play(FadeOut(nash_equilibrium))

        # Prices collude at Monopoly Price
        self.play(p1.animate.set_value(3))
        self.play(p2.animate.set_value(1))
        self.wait(1)
        self.play(p1.animate.set_value(3))
        self.play(p2.animate.set_value(3))
        self.wait(1)
        self.play(p1.animate.set_value(4))
        self.play(p2.animate.set_value(4))
        self.wait(1)
        self.play(p1.animate.set_value(5))
        self.play(p2.animate.set_value(5))
        self.wait(1)

        # Add text below the graph
        monopoly_price = Text("Monopoly price: maximum profit", font_size=36, color=BLACK).next_to(axes, DOWN, buff=1)
        self.play(FadeIn(monopoly_price))
        self.wait(2)
        self.play(FadeOut(monopoly_price))

        # Prices oscillate in Edgeworth Cycle
        # Add text below the graph
        edgeworth_cycle = Text("Edgeworth Cycle: prices oscillate", font_size=36, color=BLACK).next_to(axes, DOWN, buff=1)
        self.play(FadeIn(edgeworth_cycle))
        for price1, price2 in prices:
            # self.play([p1.animate.set_value(price1), p2.animate.set_value(price2)])
            self.play(p1.animate.set_value(price1))
            self.play(p2.animate.set_value(price2))
            self.wait(0.5)
        