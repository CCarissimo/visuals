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
        self.play([
            g.edges[(1,2)].animate.set_color(YELLOW),
            g.edges[(2,4)].animate.set_color(YELLOW)])
        self.wait(0.5)
        self.play([
            g.edges[(1, 2)].animate.set_color(WHITE),
            g.edges[(2, 4)].animate.set_color(WHITE)])

        # highlight down path
        self.play([g.edges[(1, 3)].animate.set_color(YELLOW),
                   g.edges[(3, 4)].animate.set_color(YELLOW)])
        self.wait(0.5)
        self.play([g.edges[(1, 3)].animate.set_color(WHITE),
                   g.edges[(3, 4)].animate.set_color(WHITE)])

        # highlight cross path
        self.play([g.edges[(1, 2)].animate.set_color(YELLOW),
                   g.edges[(2, 3)].animate.set_color(YELLOW),
                   g.edges[(3, 4)].animate.set_color(YELLOW)])
        self.wait(0.5)
        self.play([g.edges[(1, 2)].animate.set_color(WHITE),
                   g.edges[(2, 3)].animate.set_color(WHITE),
                   g.edges[(3, 4)].animate.set_color(WHITE)])

        # single agent traverses a path
        self.play(Create(agent1))
        self.play(
            agent1.animate.scale(target_scale).move_to(g.vertices[1]),
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(
            agent1.animate.move_to(g.vertices[2]),
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(
            agent1.animate.move_to(g.vertices[4]),
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(
            agent1.animate.scale(2).move_to(end_point1),
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(agent1.animate.move_to(start_point1))


        # two agents traverse different paths
        self.play(Create(agent2))
        self.play(
            [agent1.animate.scale(target_scale).move_to(g.vertices[1]),
             agent2.animate.scale(target_scale).move_to(g.vertices[1])],
            run_time=0.5  # How long this animation takes
        )
        self.wait(0.5)
        self.play(
            [agent1.animate.move_to(g.vertices[2]),
             agent2.animate.move_to(g.vertices[2])],
            run_time=0.5  # How long this animation takes
        )
        self.play(agent2.animate.move_to(g.vertices[3]), run_time=0.5)
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
