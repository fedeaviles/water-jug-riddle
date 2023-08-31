# stdlib
from collections import deque

# flask
from flask import render_template, request

# local
from app.main import bp


def bfs(x_jug_cap, y_jug_cap, z_to_measure):
    """
    Solves the water jug riddle using BFS algorithm.

    Args:
        x_jug_cap (int): Capacity of the X-gallon jug.
        y_jug_cap (int): Capacity of the Y-gallon jug.
        z_to_measure (int): Amount of water to measure.

    Returns:
        list or None: List of actions to achieve the measurement, or None if no solution.
    """

    def generate_new_state(x_state, y_state, action, new_action):
        """
        Generates a new state with an added action to the list.

        Args:
            x_state (int): Current amount of water in X-gallon jug.
            y_state (int): Current amount of water in Y-gallon jug.
            action (list): List of previous actions.
            new_action (str): New action to be added.

        Returns:
            tuple: New state after adding the new action.
        """
        # Convert x_state to descriptive string
        x_description = (
            "Empty"
            if x_state == 0
            else "Full"
            if x_state == x_jug_cap
            else "Partially Full"
        )

        # Convert y_state to descriptive string
        y_description = (
            "Empty"
            if y_state == 0
            else "Full"
            if y_state == y_jug_cap
            else "Partially Full"
        )

        return (
            x_state,
            y_state,
            action
            + [
                {
                    "x_state": x_description,
                    "y_state": y_description,
                    "action": new_action,
                }
            ],
        )

    def transfer(state, from_jug, to_jug):
        """
        Transfer water from one jug to another.

        Args:
            state (tuple): Current state of the jugs.
            from_jug (int): Index of the jug to transfer from.
            to_jug (int): Index of the jug to transfer into.

        Returns:
            tuple: New state after transfering water.
        """
        amount_transfered = min(state[from_jug], y_jug_cap - state[to_jug])
        x_amount = state[0] - amount_transfered if from_jug == 0 else state[0]
        y_amount = state[1] + amount_transfered if to_jug == 1 else state[1]
        return generate_new_state(
            x_amount,
            y_amount,
            state[2],
            "Transfer X to Y" if from_jug == 0 else "Transfer Y to X",
        )

    visited = set()

    # Initial states of the jugs
    queue = deque(
        [(0, 0, [{"x_state": "Empty", "y_state": "Empty", "action": "Start"}])]
    )

    while queue:
        current_state = queue.popleft()
        if current_state[:2] in visited:
            continue
        visited.add(current_state[:2])

        if current_state[0] == z_to_measure or current_state[1] == z_to_measure:
            # Return the list of actions
            return current_state[2]

        x_amount, y_amount, action = current_state
        new_states = [
            generate_new_state(x_jug_cap, y_amount, action, "Fill X"),
            generate_new_state(x_amount, y_jug_cap, action, "Fill Y"),
            generate_new_state(0, y_amount, action, "Empty X"),
            generate_new_state(x_amount, 0, action, "Empty Y"),
            transfer(current_state, 0, 1),
            transfer(current_state, 1, 0),
        ]
        queue.extend(new_states)

    return None


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        x = int(request.form.get("x"))
        y = int(request.form.get("y"))
        z = int(request.form.get("z"))

        solution_steps = bfs(x, y, z)
        return render_template("index.html", solution_steps=solution_steps)

    return render_template("index.html")
