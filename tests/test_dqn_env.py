
from neurobot.dqn_env import GridNavigationEnv, GOAL, START


def test_reset_returns_valid_observation():
    env = GridNavigationEnv()
    observation = env.reset()

    assert env.position == START
    assert len(observation) == env.observation_size
    assert env.action_size == 4


def test_right_action_moves_agent():
    env = GridNavigationEnv()
    env.reset()

    result = env.step(1)

    assert result.info["position"] == (2, 7)
    assert result.info["event"] == "move"
    assert result.reward == -0.02


def test_blocked_action_does_not_move_agent():
    env = GridNavigationEnv()
    env.reset()

    # At (1, 7), moving left reaches (0, 7), which is valid.
    # Moving up is also valid, so use a boundary-specific setup.
    env.position = (0, 0)

    result = env.step(0)

    assert result.info["position"] == (0, 0)
    assert result.info["event"] == "blocked"
    assert result.reward == -0.25


def test_episode_truncates_at_step_limit():
    env = GridNavigationEnv(max_steps=2)

    first = env.step(1)
    second = env.step(1)

    assert not first.truncated
    assert second.truncated
    assert not second.terminated


def test_invalid_action_raises_error():
    env = GridNavigationEnv()

    try:
        env.step(4)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid action should raise ValueError")
