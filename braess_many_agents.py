from manim import *
import numpy as np


class BraessNetwork(MovingCameraScene):

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
        target_scale = 2
        end_point1 = np.array([5, 2, 0])
        end_point2 = np.array([5, -2, 0])

        self.add(g)
        self.add(agent1)
        self.add(agent2)

        self.play(
            self.camera.frame.animate.set_width(30)
        )
        self.wait(1)

        n_agents = 30
        agents = [Square(side_length=0.3, color=BLUE, fill_opacity=0.5) for i in range(n_agents)]
        start_points = [np.array([-10, y, 0]) for y in np.linspace(-8, 8, n_agents)]
        end_points = [np.array([10, y, 0]) for y in np.linspace(-8, 8, n_agents)]

        for i, square in enumerate(agents):
            square.move_to(start_points[i])

        self.play([Create(square) for square in agents]+[FadeOut(agent1), FadeOut(agent2)])

        self.play([agent.animate.scale(target_scale).move_to(g.vertices[1]) for agent in agents], run_time=0.5)

        up_indices = int(n_agents/2)
        down_indices = n_agents

        self.play(
            [agent.animate.move_to(g.vertices[2]) for agent in agents[0:up_indices]] + \
            [agent.animate.move_to(g.vertices[3]) for agent in agents[up_indices:n_agents]],
            run_time=0.5
        )

        self.play(
            [agent.animate.move_to(g.vertices[4]) for agent in agents[0:up_indices]] + \
            [agent.animate.move_to(g.vertices[4]) for agent in agents[up_indices:n_agents]],
            run_time=0.5
        )

        self.play([agent.animate.scale(0.5).move_to(end_points[i]) for i, agent in enumerate(agents)], run_time=0.5)
        self.wait(1)
        self.play([agent.animate.move_to(start_points[i]) for i, agent in enumerate(agents)], run_time=0.5)
        self.wait(1)
