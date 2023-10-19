# Secure Gate

Secure Gate is a complete access management solution, combining a user-friendly web app, a robust backend system, and ESP32 integration.
It enables users to manage gate access by RFID cards, providing better security and convenience.

## Requirements

- Python 3.10
- Pip 21.3
- Virtualenv
- Pre-commit
- Docker
- Docker Compose

## Installation

1. Create a virtual environment

   ```bash
   python3 -m venv .venv
   ```

2. Activate the virtual environment

   ```bash
   source .venv/bin/activate
   ```

3. Install the dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Install the pre-commit hooks

   ```bash
   pre-commit install
   ```

5. Make husky pre-commit hook executable

```bash
chmod +x .husky/pre-commit
```

## Running

1. Run docker-compose

   ```bash
   docker-compose up
   ```

## Authors

- [@pymarcus](https://github.com/PyMarcus)
- [@eoisaac](https://github.com/eoisaac)
