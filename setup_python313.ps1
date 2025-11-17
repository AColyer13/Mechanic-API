# Setup script for Python 3.13
Write-Host "🔍 Checking Python version..."
python --version

Write-Host "`n📦 Creating virtual environment..."
python -m venv .venv

Write-Host "`n🔧 Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

Write-Host "`n📥 Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "`n✅ Setup complete! Python version:"
python --version

Write-Host "`n🚀 You can now run:"
Write-Host "   python app.py"
