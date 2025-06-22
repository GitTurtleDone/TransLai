#!/bin/bash
# Navigate to the backend directory and run it
eval "$(/home/giang/miniforge3/bin/conda shell.bash hook)"
conda activate /home/giang/Programming/AI/TransLai/TransLaiPyEnv
cd ~/Programming/AI/TransLai/
nohup uvicorn PythonBE.combined_app:app > backend.log 2>&1 &

# Navigate to the frontend directory and run it
eval "$(/home/giang/miniforge3/bin/conda shell.bash hook)"
conda activate /home/giang/Programming/AI/TransLai/TransLaiPyEnv
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"
nvm use node
cd ~/Programming/AI/TransLai/ReactTSFE
export PATH=$PATH:/usr/bin:/usr/local/bin

nohup npm run dev > frontend.log 2>&1 &

# Wait a bit and open the browser to the frontend
sleep 20
xdg-open http://localhost:5173