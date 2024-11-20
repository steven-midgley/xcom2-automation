from stable_baselines3 import PPO
from xcom2_env import XCOM2Env


def create_rl_model(env):
    """Create and return a reinforcement learning model using Stable Baselines3 (PPO)."""
    model = PPO("MlpPolicy", env, verbose=1)
    return model
