Write-Host "🚀 Installing Smart Cyber Guard..."

$APP_DIR = "C:\Program Files\SmartCyberGuard"
$PYTHON = "python"

# Create folder
if (!(Test-Path $APP_DIR)) {
    New-Item -ItemType Directory -Path $APP_DIR
}

# Copy files
Copy-Item "..\*" $APP_DIR -Recurse -Force

Set-Location $APP_DIR

# Create venv
& $PYTHON -m venv venv
& .\venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create startup shortcut
$startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$shortcut = "$startup\SmartCyberGuard.lnk"

$WshShell = New-Object -ComObject WScript.Shell
$sc = $WshShell.CreateShortcut($shortcut)
$sc.TargetPath = "$APP_DIR\venv\Scripts\pythonw.exe"
$sc.Arguments = "$APP_DIR\tray\tray_app.py"
$sc.Save()

Write-Host "✅ Installation completed"
Write-Host "🔔 Smart Cyber Guard will start automatically on login"

$exePath = "C:\Program Files\SmartCyberGuard\background_monitor.exe"

New-ItemProperty `
 -Path "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run" `
 -Name "SmartCyberGuard" `
 -Value $exePath `
 -PropertyType String `
 -Force
