from stable_baselines3 import PPO
from xcom2_env import XCOM2Env


def evaluate_model():
    """Evaluate the trained model."""
    env = XCOM2Env()  # Create the environment
    model = PPO.load("trained_model")  # Load the trained model

    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action, _states = model.predict(state)
        state, reward, done, info = env.step(action)
        total_reward += reward

    print(f"Total Reward: {total_reward}")


if __name__ == "__main__":
    evaluate_model()
