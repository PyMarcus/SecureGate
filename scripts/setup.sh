#!/bin/bash

# Define colors
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Create a virtual environment
echo -e "${CYAN}Creating virtual environment${NC}"
python3 -m venv .venv

# Step 2: Activate the virtual environment
echo -e "${CYAN}Activating the virtual environment${NC}"
source .venv/bin/activate

# Step 3: Install the Python dependencies
echo -e "${CYAN}Installing Python dependencies${NC}"
pip install -r requirements.txt

# Step 4: Install the pre-commit hooks
echo -e "${CYAN}Installing pre-commit hooks${NC}"
pre-commit install

# Step 5: Install node dependencies
echo -e "${CYAN}Installing node dependencies${NC}"
npm install

# Step 6: Make husky pre-commit hook executable
echo -e "${CYAN}Making husky pre-commit hook executable${NC}"
chmod +x .husky/pre-commit

echo -e "${GREEN}Setup completed. Virtual environment activated.${NC}"
