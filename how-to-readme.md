# How to Run the AI Trading Engine Locally

This document provides a detailed guide to setting up and running the AI Trading Engine application on your local machine.

## 1. Code Flow and Architecture

The application is a full-stack trading bot that combines a Python FastAPI backend with a React frontend.

### Backend

The backend is located in the `trading_engine_v2` directory and is built with FastAPI. It consists of the following key modules:

-   **`api/main.py`**: The main FastAPI application, which defines all the API endpoints.
-   **`upstox_client.py`**: A client for interacting with the Upstox API.
-   **`feature_store.py`**: A module for calculating and storing technical indicators.
-   **`risk_manager.py`**: A module for managing risk and position sizing.
-   **`backtester.py`**: An event-driven simulator for backtesting trading strategies.
-   **`model_interface.py`**: An interface for machine learning models.

### Frontend

The frontend is located in the `client` directory and is built with React, TypeScript, and Vite. It includes a comprehensive set of components and pages for interacting with the trading engine.

-   **`src/components`**: Reusable components for building the UI.
-   **`src/pages`**: The main pages of the application, such as the dashboard, strategy builder, and settings.
-   **`src/App.tsx`**: The main application component, which handles routing and the overall layout.

## 2. Local Setup and Execution

To run the application locally, you will need to have the following prerequisites installed:

-   Python 3.10+
-   Node.js and npm
-   Docker and Docker Compose (optional, for containerized deployment)

### Step 1: Set Up the Backend

1.  **Navigate to the `trading_engine_v2` directory:**

    ```bash
    cd trading_engine_v2
    ```

2.  **Install the Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file** with the following content:

    ```
    UPSTOX_API_KEY=your_api_key
    UPSTOX_API_SECRET=your_api_secret
    UPSTOX_ACCESS_TOKEN=your_access_token
    ```

4.  **Start the backend server:**

    ```bash
    uvicorn api.main:app --host 0.0.0.0 --port 8000
    ```

### Step 2: Set Up the Frontend

1.  **Navigate to the `client` directory:**

    ```bash
    cd client
    ```

2.  **Install the JavaScript dependencies:**

    ```bash
    npm install
    ```

3.  **Start the frontend development server:**

    ```bash
    npm run dev
    ```

### Step 3: Access the Application

Once both the backend and frontend servers are running, you can access the application in your web browser at `http://localhost:5173`.

## 3. Running the End-to-End Tests

To run the end-to-end tests, you will need to have Playwright installed:

```bash
pip install pytest-playwright
```

Then, with both the backend and frontend servers running, you can run the tests with the following command:

```bash
pytest
```

## 4. Running with GPU Acceleration

To run the application with GPU acceleration, you will need to have a compatible NVIDIA GPU and the NVIDIA Container Toolkit installed.

Once you have the prerequisites installed, you can build and run the application with the `Dockerfile.gpu` using the following commands:

```bash
docker build -t trading-engine-gpu -f trading_engine_v2/Dockerfile.gpu .
docker run -p 8000:8000 --gpus all trading-engine-gpu
```
