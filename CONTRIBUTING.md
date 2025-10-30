# Contributing to NEPSE Smart

First off, thank you for considering contributing to NEPSE Smart! It's people like you that make NEPSE Smart such a great tool.

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## How to Contribute

### Reporting Bugs

Bugs are tracked as [GitHub issues](https://github.com/your-repo/nepse-smart/issues). Before creating a bug report, please check the existing issues to see if the bug has already been reported.

When creating a bug report, please include as many details as possible. Fill out the required template, the information it asks for helps us resolve issues faster.

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://github.com/your-repo/nepse-smart/issues). Before creating an enhancement suggestion, please check the existing issues to see if the enhancement has already been suggested.

### Your First Code Contribution

Unsure where to begin contributing to NEPSE Smart? You can start by looking through these `good-first-issue` and `help-wanted` issues:

- [Good first issues](https://github.com/your-repo/nepse-smart/labels/good%20first%20issue) - issues which should only require a few lines of code, and a test or two.
- [Help wanted issues](https://github.com/your-repo/nepse-smart/labels/help%20wanted) - issues which should be a bit more involved than `good-first-issue` issues.

### Pull Requests

The process described here has several goals:

- Maintain NEPSE Smart's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible NEPSE Smart
- A speedy response to your pull request

Please follow these steps to have your contribution considered by the maintainers:

1.  Follow all instructions in [the template](PULL_REQUEST_TEMPLATE.md)
2.  Follow the [style guides](#style-guides)
3.  After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing

## How to run the project

### Docker Setup (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd nepse-smart

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Start all services (PostgreSQL, backend, frontend)
docker-compose up --build

# 4. Initialize database (first time only)
# In another terminal:
cd backend
python3 init_db.py

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# PostgreSQL: localhost:5432
```

### Local Development

#### 1. Backend Setup

```bash
# Install the NEPSE package
cd api && pip3 install -e .

# Install backend dependencies
cd ../backend
pip3 install -r requirements.txt

# Start the API server
python3 main.py
# Backend runs on http://localhost:8000

# Alternatively, with Uvicorn (hot reload):
# uvicorn backend.main:app --reload
```

#### 2. Frontend Setup

```bash
# In a new terminal
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

## How to run tests

To run the tests, you will need to have the backend and database running.

```bash
# Run backend tests
pytest backend/
```

## Code of Conduct

This project and everyone participating in it is governed by the [NEPSE Smart Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [email@example.com](mailto:email@example.com).

## Style Guides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- When only changing documentation, include `[ci skip]` in the commit title
- Consider starting the commit message with an applicable emoji:
    - 🎨 `:art:` when improving the format/structure of the code
    - 🐎 `:racehorse:` when improving performance
    - 🚱 `:non-potable_water:` when plugging memory leaks
    - 📝 `:memo:` when writing docs
    - 🐧 `:penguin:` when fixing something on Linux
    - 🍎 `:apple:` when fixing something on macOS
    - 🏁 `:checkered_flag:` when fixing something on Windows
    - 🐛 `:bug:` when fixing a bug
    - 🔥 `:fire:` when removing code or files
    - 💚 `:green_heart:` when fixing the CI build
    - ✅ `:white_check_mark:` when adding tests
    - 🔒 `:lock:` when dealing with security
    - ⬆️ `:arrow_up:` when upgrading dependencies
    - ⬇️ `:arrow_down:` when downgrading dependencies
    - 👕 `:shirt:` when removing linter warnings

### Python Styleguide

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) and [PEP 257](https://www.python.org/dev/peps/pep-0257/). We use `black` to format our code.

### TypeScript Styleguide

All TypeScript code must adhere to the [TypeScript Style Guide](https://github.com/basarat/typescript-book/blob/master/docs/style-guide/style-guide.md).

### Vue Styleguide

All Vue code must adhere to the [Vue Style Guide](https://v2.vuejs.org/v2/style-guide/).
