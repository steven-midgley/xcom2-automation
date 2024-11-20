from stable_baselines3 import PPO


def test_model():
    """Test the trained model."""
    model = PPO.load("trained_model")  # Load the trained model
    # Assuming you have an environment to test the model
    obs = model.env.reset()  # Reset the environment to start a new episode
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, reward, done, info = model.env.step(action)
        print(f"Reward: {reward}")


if __name__ == "__main__":
    test_model()
