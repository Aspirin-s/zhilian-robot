# Project initialization script

Write-Host "Zhilian Robot - Initializing..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. Create backend .env file
Write-Host "[1/4] Configuring backend environment..." -ForegroundColor Yellow
if (!(Test-Path "backend\.env")) {
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "Created backend/.env" -ForegroundColor Green
} else {
    Write-Host "backend/.env already exists" -ForegroundColor Green
}

# 2. Create Python virtual environment
Write-Host ""
Write-Host "[2/4] Creating Python virtual environment..." -ForegroundColor Yellow
Set-Location backend
if (!(Test-Path "venv")) {
    python -m venv venv
    Write-Host "Python virtual environment created" -ForegroundColor Green
} else {
    Write-Host "Python virtual environment already exists" -ForegroundColor Green
}

# 3. Install Python dependencies
Write-Host ""
Write-Host "[3/4] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "Please wait, this may take a few minutes..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
Write-Host "Python dependencies installed" -ForegroundColor Green

# 4. Install frontend dependencies
Set-Location ..\frontend
Write-Host ""
Write-Host "[4/4] Installing frontend dependencies..." -ForegroundColor Yellow
Write-Host "Please wait, this may take a few minutes..." -ForegroundColor Yellow
npm install
Write-Host "Frontend dependencies installed" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Initialization completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit backend/.env to configure database connections and API keys"
Write-Host "2. Start database services (Neo4j, MongoDB, Redis, MySQL)"
Write-Host "3. Run scripts/start.ps1 to start the application"
Write-Host ""
Write-Host "Or use Docker for one-click deployment:" -ForegroundColor Yellow
Write-Host "docker-compose up -d" -ForegroundColor Cyan
