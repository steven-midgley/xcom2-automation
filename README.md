XCOM 2 Automation with Reinforcement Learning

This project automates XCOM 2 gameplay using PyAutoGUI for in-game control, OpenCV and Tesseract for screen detection and OCR, and FastAPI for backend communication. It also leverages reinforcement learning (via Stable Baselines3) to autonomously make decisions during gameplay.

Features

    • Automated Gameplay: Control in-game actions like moving units, attacking enemies, and using items.
    • Screen Detection: Capture and process game screen to extract useful data like health and unit positions using OpenCV and OCR via Tesseract.
    • Decision-Making: Use reinforcement learning (using Stable Baselines3) for dynamic decision-making like moving to cover, attacking enemies, and more.
    • Web Interface: A simple web interface built with FastAPI for real-time game control and monitoring.

Technologies Used

    • Backend: Python, and FastAPI for API communication.
    • Game Interaction: PyAutoGUI for controlling game actions and OpenCV for image recognition.
    • Machine Learning: Stable Baselines3 for reinforcement learning models, TensorFlow or PyTorch for model training and evaluation.
    • OCR: Tesseract and pytesseract for reading game data from the screen.
    • Frontend: Simple HTML, CSS, and JavaScript for the user interface.

Getting Started

Prerequisites

    • Python 3.9 or higher
    • Conda for environment management (recommended)

Installation

1.  Clone the repo:

        git clone <repo-url>
        cd xcom2-automation

2.  Create the Conda environment:

        conda env create -f environment.yml

3.  Activate the environment:

        conda activate xcom2-automation

4.  Run the backend server:

        uvicorn backend.server:app --reload

5.  Access the frontend:

    Open index.html in a browser or set up a simple HTTP server to view the interface.

/xcom2-automation
│
├── /backend # Backend for handling game interaction and API communication
│ ├── /automation # PyAutoGUI and game interaction scripts
│ ├── /api # API layer for frontend communication
│ ├── /utils # Helper functions for backend logic
│ ├── server .py # Entry point for running the backend
│ └── environment.yml # Backend dependencies
│
├── /frontend # Frontend for live demo and controls
│ ├── /assets # Static assets (CSS, images, etc.)
│ ├── /js # JavaScript for frontend logic
│ ├── index.html # Main HTML for frontend interface
│ └── README.md # Frontend documentation
│
├── /scripts # Utility scripts for setup, training, and deployment
│ ├── setup.py # Dependency setup
│ ├── run_training.py # Script for training reinforcement learning models
│ └── deploy_model.py # Deploy trained model into the automation loop
│
├── LICENSE # License for the project
├── README.md # Project overview and instructions
└── .gitignore # Git ignore file for unnecessary

Usage

1. Start the Backend:

   - Ensure the backend server is running by using FastAPI

2. Use the Web Interface:

   - The frontend interface allows you to control and monitor the game. Use buttons for actions like move, attack, and heal

3. Monitor Game State:

   - The web interface displays real-time game state (e.g., health, unit positions), which is captured by the backend

4. Reinforcement Learning:

   - The reinforcement learning model makes decisions about in-game actions. You can train or evaluate the model using run_training.py.

Contributing

Feel free to fork this repository and submit pull requests. Please ensure your code adheres to existing project structure and includes relevant tests.

License

This project is licensed under the MIT License – see the LICENSE file for details.
