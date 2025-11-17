# PowerShell Script to Start the AI Trading Engine

# 1. Build and Start the Docker Containers
Write-Host "Building and starting the Docker containers..."
docker-compose -f trading_engine_v2/docker-compose.yml up --build -d

# 2. Check the Status of the Containers
Write-Host "Checking the status of the containers..."
docker-compose -f trading_engine_v2/docker-compose.yml ps

# 3. Instructions to Access the Application
Write-Host "The application is now running."
Write-Host "  - Backend API: http://localhost:8000"
Write-Host "  - Frontend: http://localhost:5173"

# 4. Instructions to Monitor the Logs
Write-Host "To monitor the logs, run the following command in a new terminal:"
Write-Host "  docker-compose -f trading_engine_v2/docker-compose.yml logs -f"
