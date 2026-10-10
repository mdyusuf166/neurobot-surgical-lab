"""NeuroBot DQN environment.

An abstract grid-navigation benchmark for reinforcement learning.
This is not a surgical or medical simulator.
"""

from dataclasses import dataclass

WIDTH = 12
HEIGHT = 9

START = (1, 7)
GOAL = (10, 1)

ACTIONS = (
    (0, -1),  # Up
    (1, 0),   # Right
    (0, 1),   # Down
    (-1, 0),  # Left
)

OBSTACLES = frozenset({
    (4, 2), (4, 3), (4, 4),
    (7, 4), (7, 5), (7, 6),
    (2, 2), (3, 2),
    (9, 3), (9, 4),
})


@dataclass
class StepResult:
    observation: list[float]
    reward: float
    terminated: bool
    truncated: bool
    info: dict


class GridNavigationEnv:
    observation_size = 8
    action_size = 4

    def __init__(self, max_steps: int = 160):
        if max_steps < 1:
            raise ValueError("max_steps must be positive")

        self.max_steps = max_steps
        self.reset()

    def reset(self) -> list[float]:
        self.position = START
        self.steps = 0
        return self.observe()

    def observe(self) -> list[float]:
        x, y = self.position

        blocked = []
        for dx, dy in ACTIONS:
            nx, ny = x + dx, y + dy

            is_blocked = (
                nx < 0
                or nx >= WIDTH
                or ny < 0
                or ny >= HEIGHT
                or (nx, ny) in OBSTACLES
            )
            blocked.append(float(is_blocked))

        return [
            x / (WIDTH - 1),
            y / (HEIGHT - 1),
            (GOAL[0] - x) / (WIDTH - 1),
            (GOAL[1] - y) / (HEIGHT - 1),
            *blocked,
        ]

    def step(self, action: int) -> StepResult:
        if not isinstance(action, int) or not 0 <= action < 4:
            raise ValueError("action must be an integer from 0 to 3")

        dx, dy = ACTIONS[action]
        x, y = self.position
        next_position = (x + dx, y + dy)

        self.steps += 1

        outside = (
            next_position[0] < 0
            or next_position[0] >= WIDTH
            or next_position[1] < 0
            or next_position[1] >= HEIGHT
        )

        if outside or next_position in OBSTACLES:
            reward = -0.25
            event = "blocked"
        else:
            self.position = next_position
            reward = -0.02
            event = "move"

        terminated = self.position == GOAL

        if terminated:
            reward = 2.0
            event = "goal"

        truncated = (
            self.steps >= self.max_steps
            and not terminated
        )

        return StepResult(
            observation=self.observe(),
            reward=reward,
            terminated=terminated,
            truncated=truncated,
            info={
                "event": event,
                "success": terminated,
                "position": self.position,
                "steps": self.steps,
            },
        )
