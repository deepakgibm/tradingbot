# Local Setup Instructions

This guide provides instructions for setting up and running the Upstox Intraday Trading Bot on your local machine.

## Prerequisites

- Python 3.11 or higher
- Node.js and npm
- Git

## Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    You will need to set up environment variables for your Upstox API credentials. The application will need to be configured to read these from a `.env` file or directly from your environment.

    ```
    UPSTOX_API_KEY=your_api_key
    UPSTOX_API_SECRET=your_api_secret
    UPSTOX_REDIRECT_URI=http://localhost:8000/auth/callback
    ```

5.  **Run the backend server:**
    ```bash
    python main.py
    ```
    The backend server will be running at `http://localhost:8000`.

## Frontend Setup

1.  **Navigate to the client directory:**
    In a new terminal, from the root of the project, run:
    ```bash
    cd client
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend development server:**
    ```bash
    npm run dev
    ```
    The frontend application will be accessible at `http://localhost:5173` (or another port if 5173 is in use).

## Configuration

Adjust the trading strategy parameters by editing the `config.py` file. This includes settings for capital, risk management, and technical indicator thresholds.

## Running the Bot

1.  Ensure both the backend and frontend servers are running.
2.  Open your browser and navigate to the frontend URL.
3.  You will be prompted to log in with your Upstox account to authorize the application.
4.  Once authorized, you can start the bot from the dashboard.
