from manim import *
import random


class QLearningAnimation(MovingCameraScene):

    def action_loop(self, table_object, data, target):
        """
        Animate the action loop for the Q-learning agent.
        """
        # Create an arrow pointing to the first entry in the table
        arrow = Arrow(
            start=table_object.get_entries()[0].get_center() + DOWN * 2,
            end=table_object.get_entries()[0].get_center() + DOWN * 0.5,
            color=GOLD,
            max_stroke_width_to_length_ratio=5
        )
        self.play(Create(arrow))
        self.wait(0.5)
        # Move the arrow to the second entry in the table
        self.play(
            arrow.animate.move_to(table_object.get_entries()[1].get_center() + DOWN * 1.25)
        )
        self.wait(0.5)

        # Get the string values of the entries in the table, and compare them as floats to get the largest one
        first_entry = table_object.get_entries()[0]
        second_entry = table_object.get_entries()[1]
        first_value = data[0][0]
        second_value = data[0][1]
        if first_value > second_value:
            chosen_entry = first_entry
            chosen_value = first_value
            chosen_action = 0
        else:
            chosen_entry = second_entry
            chosen_value = second_value
            chosen_action = 1
        
        # Highlight the chosen entry with a surrounding rectangle
        chosen_entry_box = SurroundingRectangle(chosen_entry, color=GREEN, buff=0.3)
        self.play(Create(chosen_entry_box))
        self.wait(0.5)

        # Animate the box to move to the target
        self.play(
            chosen_entry_box.animate.move_to(target.get_center()),
        )
        self.wait(0.5)

        # Create a single number at the center of the target to represent the reward, as a random float between 0 and 1
        reward_value = random.uniform(0, 1)
        reward_number = Text(f"{reward_value:.1f}").set_color(GREEN).move_to(target.get_center())
        self.play(Write(reward_number))
        self.wait(0.5)

        # Animate the reward number to move to the chosen entry in the table
        self.play(
            reward_number.animate.move_to(chosen_entry.get_center()),
            chosen_entry_box.animate.move_to(chosen_entry.get_center())
        )

        # Change the value of the chosen entry in the table to the average of the entry and the reward number
        new_value = (chosen_value + reward_value) / 2
        data[0][chosen_action] = new_value

        new_entry = Text(f"{new_value:.1f}").set_color(BLACK)
        new_entry.move_to(chosen_entry.get_center())
        self.play(
            ReplacementTransform(chosen_entry, new_entry),
            FadeOut(reward_number),
            FadeOut(chosen_entry_box)
        )
        self.wait(1)

        return data


    def construct(self):
        # make sure to set the colors of things to BLACK, because we have a white background
        # Our agent will play a game with two actions: "A" and "B"
        
        # Create a vector to represent Q-values
        table = Matrix([["Q_a", "Q_b"]]).set_color(BLACK)

        # Create a square to represent the agent
        square = Square().set_color(BLUE)

        # Animate the creation of the square, and transform it into the vector
        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, table))  # interpolate the square into the vector
        # self.play(FadeOut(square))  # fade out animation

        # Add a label to the vector to represent the agent
        agent_label = Text("Agent").next_to(table, UP * 4).set_color(BLACK)
        self.play(Write(agent_label))
        self.wait(1)

        # Create a circle to represent the environment, to the right of the square
        circle = Circle(radius=1.5, color=BLACK).shift(RIGHT * 6)

        # Animate the creation of the circle
        self.play(
            Create(circle),
            self.camera.frame.animate.move_to((table.get_center() + circle.get_center()) / 2).set_width(17)
        )

        # Add a label to the circle to represent the environment
        env_label = Text("Environment").next_to(circle, UP).set_color(BLACK)
        self.play(Write(env_label))
        self.wait(1)

        # Create two labels for the actions, and place them above the vector
        # set color to BLACK
        action_a_label = Text(" a ").next_to(table.get_left(), UP * 3 + RIGHT * 2).set_color(BLACK)
        action_b_label = Text(" b ").next_to(table.get_right(), UP * 3 + LEFT * 2).set_color(BLACK)

        # Change the values of the table to real numbers
        agent1_data = [[0.5, 0.8]] 
        new_values = [[f"{val:.2f}" for val in row] for row in agent1_data]
        q_values = Matrix(new_values).set_color(BLACK) # create a new table with the new values
        q_values.move_to(table.get_center())

        # Animate the transition from the old table to the new table, and add the action labels
        self.play(ReplacementTransform(square, q_values),
            Write(action_a_label),
            Write(action_b_label)
            )
        self.wait(1)
        

        # Change the color of the first entry in the table to green, and then reset it to black
        first_entry = q_values.get_entries()[0]

        arrow = Arrow(start=first_entry.get_center() + DOWN * 2, end=first_entry.get_center() + DOWN * 0.5, color=GOLD, max_stroke_width_to_length_ratio=5)

        self.play(first_entry.animate.set_color(GREEN), 
                  Create(arrow)
                  )
        self.wait(1)
        self.play(first_entry.animate.set_color(BLACK))

        # Change the color of the second entry in the table to green, and then reset it to black
        # and move the arrow to point to the second entry
        
        second_entry = q_values.get_entries()[1]

        self.play(
            second_entry.animate.set_color(GREEN), 
            arrow.animate.move_to(second_entry.get_center() + DOWN * 1.25)
            )
        self.wait(1)
        self.play(second_entry.animate.set_color(BLACK))

        # Add a box around the second entry to highlight it
        second_entry_box = SurroundingRectangle(action_b_label, color=GREEN, buff=0.3)
        self.play(
            Create(second_entry_box), 
            FadeOut(arrow)
            )
        self.wait(1)

        # Animate the box to move to the circle
        self.play(
            second_entry_box.animate.move_to(circle.get_center()),
        )
        self.wait(1)

        # Create a single number at the center of the circle to represent the reward
        reward_number = Text("1.0").set_color(GREEN).move_to(circle.get_center())
        self.play(Write(reward_number))
        self.wait(1)

        # Below the agent, create a new equation to represent the stateless Q-learning update rule
        q_update_rule = MathTex(
            "Q(a) = Q(a) + \\alpha (", "r", "+ \\gamma \\max Q(a') - Q(a))",
            font_size=36
        ).next_to(q_values, DOWN * 8).set_color(BLACK)
        self.play(Write(q_update_rule))
        self.wait(1)

        # Change a new matrix with the new second entry in the table to the average of the entry and the reward number
        new_agent_1_data = [[0.5, 0.9]]  # new data for the agent
        new_q_values = [[f"{val:.2f}" for val in row] for row in new_agent_1_data]
        new_q_table = Matrix(new_q_values).set_color(BLACK).move_to(q_values.get_center())

        # Animate the reward number to move to the second entry in the table
        self.play(
            reward_number.animate.move_to(q_update_rule[1].get_center()),
            second_entry_box.animate.move_to(q_update_rule[1].get_center())
        )

        self.play(
            ReplacementTransform(q_values, new_q_table),
            FadeOut(reward_number),
            FadeOut(second_entry_box)
        )

        self.wait(1)


        # Zoom out the camera to center the circle
        self.play(
            self.camera.frame.animate.set_width(20).move_to(circle.get_center())
        )

        # Create a new q_table for a new agent on the right side of the circle
        agent2_data = [[0.7, 0.4]]  # new data for the second agent
        new_q_values = [[f"{val:.2f}" for val in row] for row in agent2_data]
        agent2_table = Matrix(new_q_values).set_color(BLACK).move_to(
            circle.get_center() + RIGHT * (circle.get_center()-new_q_table.get_center()))

        # Add a label to the new agent, Agnent 2, and change the old agent label to Agent 1
        agent_2_label = Text("Agent 2").next_to(agent2_table, UP * 4).set_color(BLACK)
        agent_1_label = Text("Agent 1").next_to(q_values, UP * 4).set_color(BLACK)

        self.play(
            Write(agent_2_label),
            ReplacementTransform(agent_label, agent_1_label),
            Create(agent2_table)
        )
        self.wait(1)

        # Create a new environment label for the circle, Game
        game_label = Text("Game").next_to(circle, UP).set_color(BLACK)
        self.play(ReplacementTransform(env_label, game_label))

        self.wait(1)

        # Animate both agents taking actions 3 times each
        # for _ in range(3):
        #     agent1_data = self.action_loop(q_values, agent1_data, circle)
        #     agent2_data = self.action_loop(agent2_table, agent2_data, circle)
        # self.wait(1)
