# Python bytecode and caches
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
coverage.xml
htmlcov/

# Virtual environments
.venv/
venv/
env/
ENV/
.conda/

# Environment and secrets
.env
.env.*
!.env.example
*.pem
*.key
secrets/

# Jupyter
.ipynb_checkpoints/

# macOS and archive metadata
.DS_Store
.AppleDouble
.LSOverride
__MACOSX/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Generated pipeline artifacts
outputs/
models/
artifacts/
mlruns/
*.joblib
*.pkl
*.pt
*.pth
*.ckpt
*.onnx

# Logs and temporary files
*.log
tmp/
temp/
.cache/

# Distribution and packaging
build/
dist/
*.egg-info/
*.zip
*.tar.gz

# Terraform local state
.terraform/
*.tfstate
*.tfstate.*
terraform.tfvars
crash.log

# Local database and feedback artifacts
*.db
*.sqlite
*.sqlite3
clinician_feedback.jsonl