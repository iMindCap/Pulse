# Contributing to Pulse

First off, thank you for considering contributing to Pulse! Every contribution helps make this project better for the entire homelab community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check if the issue already exists. When creating a bug report, include as many details as possible using the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

### Suggesting Features

Feature requests are welcome! Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and describe what problem it solves, how it should work, and any alternatives you've considered.

### Your First Contribution

Look for issues labeled **`good first issue`** — these are specifically designed for newcomers:

- Adding a new notification channel (Discord, Slack, email)
- Adding a new system metric collector
- Improving documentation
- Writing tests
- Fixing typos

### Adding a Widget

Widgets are self-contained Vue components in `frontend/src/components/widgets/`. To add one:

1. Create a new `.vue` file in the widgets directory
2. Register it in the widget registry
3. Add any backend collectors needed in `backend/collectors/`
4. Submit a PR with screenshots

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker (for testing)
- Git

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run the development server
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

# Run the development server
npm run dev
```

### Running Both

```bash
# Terminal 1 — Backend
cd backend && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev
```

The frontend dev server proxies API requests to the backend automatically.

## Project Structure

```
pulse/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── api/                 # API route handlers
│   │   └── routes.py
│   ├── collectors/          # Data collection modules
│   │   ├── docker_collector.py
│   │   ├── system_collector.py
│   │   └── ping_collector.py
│   ├── db/                  # Database models and migrations
│   │   └── models.py
│   └── config/              # Configuration management
│       └── settings.py
├── frontend/
│   └── src/
│       ├── components/      # Reusable Vue components
│       │   └── widgets/     # Dashboard widgets
│       ├── views/           # Page-level components
│       └── assets/          # Static assets
├── docs/                    # Documentation
└── docker-compose.yml       # Production deployment
```

## Pull Request Process

1. **Fork** the repository and create your branch from `main`
2. **Install** dependencies and make sure existing tests pass
3. **Add tests** for any new functionality
4. **Update documentation** if you changed APIs or added features
5. **Write a clear PR description** explaining what and why
6. **Link the related issue** if one exists

### PR Title Convention

```
feat: add Discord notification channel
fix: correct CPU usage calculation on ARM
docs: add Raspberry Pi setup guide
refactor: simplify Docker collector logic
test: add unit tests for ping collector
chore: update dependencies
```

## Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use type hints for all function parameters and return values
- Write docstrings for public functions
- Format with `black` and lint with `ruff`

```python
async def get_container_stats(container_id: str) -> ContainerStats:
    """Fetch resource usage stats for a specific Docker container."""
    ...
```

### TypeScript/Vue (Frontend)

- Use Vue 3 Composition API with `<script setup>`
- Use TypeScript for all components
- Follow the existing Tailwind CSS patterns
- Format with Prettier and lint with ESLint

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const cpuUsage = ref<number>(0)
</script>
```

### Commits

- Write clear, concise commit messages
- Use the present tense: "Add feature" not "Added feature"
- Reference issues when applicable: "Fix #42"

---

Questions? Feel free to open an issue with the `question` label. We're happy to help!
