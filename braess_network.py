from manim import *
import numpy as np


class BraessNetwork(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2), (2, 3), (1, 3), (2, 4), (3, 4)]

        vertex_positions = {
            1: np.array([-4, 0, 0]),  # Vertex 1 at top-left-ish
            2: np.array([0, 2, 0]),  # Vertex 2 at top-right-ish
            3: np.array([0, -2, 0]),  # Vertex 3 at bottom-left-ish
            4: np.array([4, 0, 0])  # Vertex 4 at bottom-right-ish
        }

        g = DiGraph(
            vertices,
            edges,
            layout = vertex_positions,
            vertex_config={"radius": 0.2, "fill_opacity": 0.8, "color": BLUE},
            edge_config={"stroke_width": 2, "color": BLACK}
        )

        # setup agents as squares
        agent1 = Square(side_length=2, color=BLUE, fill_opacity=0.5)
        agent2 = Square(side_length=2, color=RED, fill_opacity=0.5)
        start_point1 = np.array([-5, 2, 0])
        start_point2 = np.array([-5, -2, 0])
        agent1.move_to(start_point1)
        agent2.move_to(start_point2)
        target_scale = 0.5
        end_point1 = np.array([5, 2, 0])
        end_point2 = np.array([5, -2, 0])

        # self.add(g)
        self.play(Create(g))
        self.wait()

        # highlight up path
        up_path = Group(g.edges[(1, 2)], g.edges[(2, 4)])

        # add path costs as text above the edges
        edge12_cost = Text("x", font_size=28, color=BLACK).move_to(g.edges[(1, 2)]).shift(UP*0.4)
        edge24_cost = Text("1", font_size=28, color=BLACK).move_to(g.edges[(2, 4)]).shift(UP*0.4)

        self.play(up_path.animate.set_color(GREEN), Write(edge12_cost), Write(edge24_cost))
        self.wait(0.5)
        self.play(up_path.animate.set_color(BLACK))
        
        up_path_2 = up_path.copy()
        self.play(up_path_2.animate.scale(0.25).move_to(LEFT*3 + UP*3))
        up_text = Text("Up", font_size=23, color=BLACK).next_to(up_path_2, UP)
        self.play(FadeIn(up_text))

        # highlight down path
        down_path = Group(g.edges[(1, 3)], g.edges[(3, 4)])

        # add down path costs as text above the edges
        edge13_cost = Text("1", font_size=28, color=BLACK).move_to(g.edges[(1, 3)]).shift(DOWN*0.4)
        edge34_cost = Text("x", font_size=28, color=BLACK).move_to(g.edges[(3, 4)]).shift(DOWN*0.4)

        self.play(down_path.animate.set_color(GREEN), Write(edge13_cost), Write(edge34_cost))
        self.wait(0.5)
        self.play(down_path.animate.set_color(BLACK))

        down_path_2 = down_path.copy()
        self.play(down_path_2.animate.scale(0.25).move_to(RIGHT*3 + UP*3))
        down_text = Text("Down", font_size=23, color=BLACK).next_to(down_path_2, UP)
        self.play(FadeIn(down_text))

        # highlight cross path
        cross_path = Group(g.edges[(1, 2)], g.edges[(2, 3)], g.edges[(3, 4)])

        # add cross path costs as text above the edges
        edge23_cost = Text("0", font_size=28, color=BLACK).move_to(g.edges[(2, 3)]).shift(RIGHT*0.4)

        self.play(cross_path.animate.set_color(GREEN), Write(edge23_cost))
        self.wait(0.5)
        self.play(cross_path.animate.set_color(BLACK))

        cross_path_2 = cross_path.copy()
        self.play(cross_path_2.animate.scale(0.25).move_to(UP*3))
        cross_text = Text("Cross", font_size=23, color=BLACK).next_to(cross_path_2, UP)
        self.play(FadeIn(cross_text))
        
        self.wait(0.5)

        # two agents traverse the same path
        self.play(Create(agent1), Create(agent2))
        self.play(
            [agent1.animate.scale(target_scale).move_to(g.vertices[1]),
             agent2.animate.scale(target_scale).move_to(g.vertices[1])],
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)

        og_edge12_cost = edge12_cost.copy()
        edit_edge12_cost = Text("1", font_size=28, color=GREEN).move_to(g.edges[(1, 2)]).shift(UP*0.4)
        self.play(
            [agent1.animate.move_to(g.vertices[2]),
             agent2.animate.move_to(g.vertices[2]),
             Transform(edge12_cost, edit_edge12_cost)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(
            [agent1.animate.move_to(g.vertices[4]),
             agent2.animate.move_to(g.vertices[4])],    
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(
            [agent1.animate.scale(2).move_to(end_point1),
             agent2.animate.scale(2).move_to(end_point2)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(2)
        self.play([agent1.animate.move_to(start_point1), 
        agent2.animate.move_to(start_point2),
        Transform(edge12_cost, og_edge12_cost)], run_time=0.5)


        # two agents traverse different paths
        self.play(
            [agent1.animate.scale(target_scale).move_to(g.vertices[1]),
             agent2.animate.scale(target_scale).move_to(g.vertices[1])],
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        og_edge12_cost = edge12_cost.copy()
        edit_edge12_cost = Text("1/2", font_size=28, color=GREEN).move_to(g.edges[(1, 2)]).shift(UP*0.4)
        self.play(
            [agent1.animate.move_to(g.vertices[2]),
             agent2.animate.move_to(g.vertices[3]),
             Transform(edge12_cost, edit_edge12_cost)],
            run_time=0.5  # How long this animation takes
        )
        # self.play(agent2.animate.move_to(g.vertices[3]), run_time=0.5)
        # self.wait(0.5)
        og_edge34_cost = edge34_cost.copy()
        edit_edge34_cost = Text("1/2", font_size=28, color=GREEN).move_to(g.edges[(3, 4)]).shift(DOWN*0.4)
        self.play(
            [agent1.animate.move_to(g.vertices[4]),
             agent2.animate.move_to(g.vertices[4]),
             Transform(edge34_cost, edit_edge34_cost)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(2)

        # Add text below network
        social_optimum = Text("Social Optimum: average = 1.5", font_size=36, color=BLACK).next_to(g, DOWN, buff=1)
        self.play(FadeIn(social_optimum))
        self.wait(2)

        self.play(
            [agent1.animate.scale(2).move_to(end_point1),
             agent2.animate.scale(2).move_to(end_point2),
             Transform(edge12_cost, og_edge12_cost),
             Transform(edge34_cost, og_edge34_cost),
             FadeOut(social_optimum)],
            run_time=0.5  # How long this animation takes
        )

        # two agents traverse cross path
        self.play(
            [agent1.animate.scale(target_scale).move_to(g.vertices[1]),
             agent2.animate.scale(target_scale).move_to(g.vertices[1])],
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        og_edge12_cost = edge12_cost.copy()
        edit_edge12_cost = Text("1", font_size=28, color=GREEN).move_to(g.edges[(1, 2)]).shift(UP*0.4)
        self.play(
            [agent1.animate.move_to(g.vertices[2]),
             agent2.animate.move_to(g.vertices[2]),
             Transform(edge12_cost, edit_edge12_cost)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        
        self.play(
            [agent1.animate.move_to(g.vertices[3]),
             agent2.animate.move_to(g.vertices[3])],
            run_time=0.5  # How long this animation takes
        )

        og_edge34_cost = edge34_cost.copy()
        edit_edge34_cost = Text("1", font_size=28, color=GREEN).move_to(g.edges[(3, 4)]).shift(DOWN*0.4)
        self.play(
            [agent1.animate.move_to(g.vertices[4]),
             agent2.animate.move_to(g.vertices[4]),
             Transform(edge34_cost, edit_edge34_cost)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(2)

        # add text below network
        nash_equilibrium = Text("Nash Equilibrium: average = 2", font_size=36, color=BLACK).next_to(g, DOWN, buff=1)
        self.play(FadeIn(nash_equilibrium))
        self.wait(2)

        self.play(
            [agent1.animate.scale(2).move_to(end_point1),
             agent2.animate.scale(2).move_to(end_point2)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(2)

        # Reset agents to start positions
        self.play(
            [agent1.animate.move_to(start_point1), 
             agent2.animate.move_to(start_point2),
             Transform(edge12_cost, og_edge12_cost),
             Transform(edge34_cost, og_edge34_cost),
             FadeOut(nash_equilibrium)],
            run_time=0.5  # How long this animation takes
        )
        self.wait(1)
