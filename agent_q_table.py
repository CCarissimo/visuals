from manim import *


class DefaultTemplate(Scene):
    def construct(self):
        table = Matrix([["Q_a", "Q_b", "Q_c"]]).set_color(BLACK)

        square = Square().set_color(BLACK)  # create a square
        # square.flip(RIGHT)  # flip horizontally
        # square.rotate(-3 * TAU / 8)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, table))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
