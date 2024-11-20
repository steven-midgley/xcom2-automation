XCOM 2 Automation with Reinforcement Learning

This project automates XCOM 2 gameplay by leveraging machine learning to autonomously complete in-game actions. Using PyAutoGUI for in-game control, OpenCV and Tesseract for screen capture and OCR, and a reinforcement learning model (via Stable Baselines3), the project aims to automate gameplay without manual intervention.

Objectives

    •	Automated Gameplay: The system will interact with XCOM 2 by simulating mouse clicks, movement, and various in-game actions (e.g., movement, attacking, using items) based on a trained machine learning model.
    •	Screen Capture & OCR: The project will use OpenCV and Tesseract to capture and interpret the game screen, extracting information like health, unit positions, and available actions.
    •	Reinforcement Learning: A custom reinforcement learning model will be used to make real-time decisions on movement, combat, and strategy based on the game state.
    •	Self-Learning: The model will continue to improve as it interacts with the game, learning better strategies through training.

Features

    •	Game Interaction: Automates in-game actions like moving units, attacking enemies, and interacting with objects.
    •	Screen Detection: Uses OCR to extract relevant game data such as health, unit positions, and enemy visibility.
    •	Reinforcement Learning: Stable Baselines3 is used to train the agent for decision-making based on game states.
    •	Offline Execution: All operations are run locally on the machine without a web interface or external backend.

Technologies Used

    •	Backend: Python for scripting the interactions and controlling the game.
    •	Game Interaction: PyAutoGUI for simulating mouse movements and clicks, OpenCV for screen capture, and Tesseract for OCR to read game data.
    •	Machine Learning: Stable Baselines3 for reinforcement learning, TensorFlow for deep learning model training and evaluation.
    •	Dependencies: The project leverages libraries like OpenCV, PyAutoGUI, Tesseract, and Stable Baselines3.

Getting Started

Prerequisites

    •	Python 3.9 or higher
    •	Conda for environment management (recommended)

Installation

    1.	Clone the repository:
    •	Use git clone to copy the project locally.
    2.	Create the Conda environment:
    •	Use the provided environment.yml to install the necessary dependencies.
    3.	Activate the environment:
    •	Run the conda activate xcom2-automation command to use the environment.
    4.	Install additional dependencies:
    •	If needed, run pip install -r requirements.txt for additional requirements.

Running the Automation

Once the environment is set up and the game is running, execute the automation scripts for interacting with the game and performing actions. The reinforcement learning model will be responsible for making decisions based on the game state captured through the screen.

Training and Testing the Model

    •	Training: The train_model.py script is used for training the reinforcement learning model.
    •	Testing: The test_rl_model.py script will test the performance of the trained model in different mission scenarios.

Contributing

Feel free to fork the repository and submit pull requests. Ensure your code follows the structure of the project and includes relevant tests for any changes made.

License

This project is licensed under the MIT License – see the LICENSE file for details.
