# quick setup for a Snapdragon X (Windows on ARM) HP laptop
# run this from a PowerShell prompt in the project folder

Write-Host "setting up ShikshaMitra..."

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

Write-Host "core deps installed."
Write-Host "now grab a model export from aihub.qualcomm.com and drop it in models\llm"
Write-Host "then: pip install onnxruntime-genai-qnn"
Write-Host ""
Write-Host "run with: python main.py          (opens the desktop chat window)"
Write-Host "      or: python main.py --cli    (terminal mode)"
