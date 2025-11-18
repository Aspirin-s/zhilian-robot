# 快速启动脚本 - Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   智链机器人 - 项目启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python
Write-Host "检查Python环境..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python已安装: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python未安装,请先安装Python 3.8+" -ForegroundColor Red
    exit 1
}

# 检查Node.js
Write-Host "检查Node.js环境..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js已安装: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js未安装,请先安装Node.js 16+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "选择启动方式:" -ForegroundColor Cyan
Write-Host "1. 启动后端服务"
Write-Host "2. 启动前端服务"
Write-Host "3. 同时启动前后端(推荐)"
Write-Host "4. 使用Docker启动"
Write-Host "5. 初始化项目环境"
Write-Host ""

$choice = Read-Host "请输入选项(1-5)"

switch ($choice) {
    "1" {
        Write-Host "`n启动后端服务..." -ForegroundColor Green
        Set-Location backend
        
        # 检查虚拟环境
        if (!(Test-Path "venv")) {
            Write-Host "创建Python虚拟环境..." -ForegroundColor Yellow
            python -m venv venv
        }
        
        # 激活虚拟环境
        .\venv\Scripts\Activate.ps1
        
        # 安装依赖
        Write-Host "安装依赖..." -ForegroundColor Yellow
        pip install -r requirements.txt
        
        # 启动服务
        Write-Host "启动后端服务..." -ForegroundColor Green
        python main.py
    }
    
    "2" {
        Write-Host "`n启动前端服务..." -ForegroundColor Green
        Set-Location frontend
        
        # 检查node_modules
        if (!(Test-Path "node_modules")) {
            Write-Host "安装依赖..." -ForegroundColor Yellow
            npm install
        }
        
        # 启动服务
        Write-Host "启动前端服务..." -ForegroundColor Green
        npm run dev
    }
    
    "3" {
        Write-Host "`n同时启动前后端服务..." -ForegroundColor Green
        
        # 启动后端
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python main.py"
        
        # 等待2秒
        Start-Sleep -Seconds 2
        
        # 启动前端
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"
        
        Write-Host "`n服务已在新窗口中启动!" -ForegroundColor Green
        Write-Host "后端地址: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "前端地址: http://localhost:3000" -ForegroundColor Cyan
    }
    
    "4" {
        Write-Host "`n使用Docker启动..." -ForegroundColor Green
        
        # 检查Docker
        $dockerVersion = docker --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ Docker未安装,请先安装Docker Desktop" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "启动Docker容器..." -ForegroundColor Yellow
        docker-compose up -d
        
        Write-Host "`nDocker容器已启动!" -ForegroundColor Green
        Write-Host "前端地址: http://localhost" -ForegroundColor Cyan
        Write-Host "后端地址: http://localhost:8000" -ForegroundColor Cyan
    }
    
    "5" {
        Write-Host "`n初始化项目环境..." -ForegroundColor Green
        
        # 后端环境
        Write-Host "配置后端环境..." -ForegroundColor Yellow
        Set-Location backend
        
        if (!(Test-Path ".env")) {
            Copy-Item ".env.example" ".env"
            Write-Host "✓ 已创建.env配置文件,请根据实际情况修改" -ForegroundColor Green
        }
        
        if (!(Test-Path "venv")) {
            python -m venv venv
            Write-Host "✓ Python虚拟环境已创建" -ForegroundColor Green
        }
        
        # 前端环境
        Set-Location ../frontend
        Write-Host "配置前端环境..." -ForegroundColor Yellow
        
        if (!(Test-Path "node_modules")) {
            npm install
            Write-Host "✓ 前端依赖已安装" -ForegroundColor Green
        }
        
        Set-Location ..
        Write-Host "`n环境初始化完成!" -ForegroundColor Green
        Write-Host "请编辑 backend/.env 配置数据库连接" -ForegroundColor Yellow
    }
    
    default {
        Write-Host "无效选项" -ForegroundColor Red
    }
}
