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
            vertex_config={"radius": 0.2, "fill_opacity": 0.8, "color": BLACK},
            edge_config={"color": BLACK},
        )

        # setup agents as squares
        # agent1 = Square(side_length=2, color=BLUE, fill_opacity=0.5)
        # agent2 = Square(side_length=2, color=RED, fill_opacity=0.5)
        # start_point1 = np.array([-5, 2, 0])
        # start_point2 = np.array([-5, -2, 0])
        # agent1.move_to(start_point1)
        # agent2.move_to(start_point2)
        # target_scale = 2
        # end_point1 = np.array([5, 2, 0])
        # end_point2 = np.array([5, -2, 0])

        self.add(g)
        # self.add(agent1)
        # self.add(agent2)

        self.camera.frame.set_width(30)

        # self.play(
        #     self.camera.frame.animate.set_width(30)
        # )
        self.wait(1)

        n_agents = 16
        start_points = [np.array([-10, y, 0]) for y in np.linspace(-8, 8, n_agents)]
        colors = [GREEN, BLUE, RED]

        # Q vectors

        q_table_values = np.round(np.random.random((n_agents, 3)) + 1, decimals=1)
        q_table_argmax = q_table_values.argmax(axis=1)

        q_vectors = [Matrix([["Q_a", "Q_b", "Q_c"]]) for i in range(n_agents)]
        
        for i, vec in enumerate(q_vectors):
            vec.move_to(start_points[i]).set_color(BLACK)

        self.add(*q_vectors)
        self.play(FadeIn(*q_vectors))
        self.wait(1)

        # Agents

        # agents = [Square(side_length=0.5, color=colors[q_table_argmax[i]], fill_opacity=0.5) for i in range(n_agents)]
        # for i, agent in enumerate(agents):
        #     agent.move_to(start_points[i])

        # animations = [Transform(q_vectors[i], agents[i]) for i in range(n_agents)]

        # self.play(AnimationGroup(*animations))
        
        # self.wait(1)

        # zoom out camera
        self.play(self.camera.frame.animate.set_width(50))
        
        q_values = np.round(np.random.random((3, 3)) + 1, decimals=1)
        q_table = Matrix(q_values).set_color(BLACK)
        q_table.move_to(start_points[0])

        bottom_3_vectors = Group(q_vectors[0], q_vectors[1], q_vectors[2])

        self.play(Transform(bottom_3_vectors, q_table), run_time=1)
        self.wait(1)

        self.play([FadeOut(*q_vectors), q_table.animate.move_to(np.array([-10,0,0]))])
        self.wait(1)

        # shift camera to the left
        self.play(self.camera.frame.animate.shift(LEFT * 10))

        