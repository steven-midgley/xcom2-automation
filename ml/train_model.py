from xcom2_env import XCOM2Env
from rl_model import create_rl_model


def train_model():
    """Train the RL model on the XCOM2 environment."""
    env = XCOM2Env()  # Create the custom environment
    model = create_rl_model(env)
    model.learn(total_timesteps=10000)  # Train the model for 10,000 timesteps
    model.save("trained_model")  # Save the trained model
    print("Model training complete.")


if __name__ == "__main__":
    train_model()
