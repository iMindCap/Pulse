<div align="center">

# ⚡ Pulse

**One dashboard. Full visibility. Zero config.**

Your entire homelab — containers, system metrics, services — in a single, beautiful dashboard.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/iMindCap/pulse)](https://github.com/iMindCap/pulse/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Quick Start](#-quick-start) · [Features](#-features) · [Screenshots](#-screenshots) · [Contributing](#-contributing) · [Roadmap](#-roadmap)

</div>

---

## 🤔 Why Pulse?

Running a homelab usually means juggling multiple tools just to know what's going on — one for bookmarks, another for uptime, others for system metrics and containers. Before you know it, you're managing more dashboards than services.

**Pulse brings everything into a single, self-hosted dashboard** that installs in 30 seconds and works out of the box.

No complex configuration. No databases to set up. No dashboards to build manually.

Just run it and see everything.

---

## ✨ Features

- 🐳 **Docker Monitoring** — Live status, resource usage, and health of every container
- 📊 **System Metrics** — CPU, RAM, disk usage, and temperature at a glance
- 🌐 **Service Uptime** — Monitor any HTTP/TCP endpoint with latency tracking
- 📈 **Historical Data** — Metrics stored locally, visualized with interactive charts
- 🔗 **Quick Links** — One-click access to all your self-hosted apps
- 🔔 **Alerts** — Get notified via Discord, Telegram, or email when something goes wrong
- 🌙 **Dark Mode** — Beautiful dark-first UI, with light mode available
- 📱 **Responsive** — Looks great on desktop, tablet, and mobile
- 🪶 **Lightweight** — Minimal footprint, runs on a Raspberry Pi

---

## 🚀 Quick Start

```bash
docker run -d \
  --name pulse \
  -p 3000:3000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v pulse_data:/app/data \
  pulse/pulse:latest
```

Open `http://your-server-ip:3000` — that's it. No accounts, no setup wizard, no config files.

### Docker Compose

```yaml
version: "3.8"
services:
  pulse:
    image: pulse/pulse:latest
    container_name: pulse
    ports:
      - "3000:3000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - pulse_data:/app/data
    restart: unless-stopped

volumes:
  pulse_data:
```

```bash
docker-compose up -d
```

---

## 📸 Screenshots

> 🚧 Coming soon — the project is in active development.

<!--
![Dashboard](docs/screenshots/dashboard.png)
![Containers](docs/screenshots/containers.png)
![Metrics](docs/screenshots/metrics.png)
-->

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, FastAPI |
| **Frontend** | Vue 3, TypeScript, Tailwind CSS |
| **Charts** | Chart.js |
| **Database** | SQLite |
| **Container** | Docker |

---

## 🗺️ Roadmap

- [x] Project setup and documentation
- [ ] Docker container monitoring (status, stats, logs)
- [ ] System metrics collection (CPU, RAM, disk, temperature)
- [ ] REST API with Swagger documentation
- [ ] Dashboard UI with real-time updates
- [ ] Service uptime monitoring (HTTP/TCP)
- [ ] Historical metrics with interactive charts
- [ ] Alert system (Discord, Telegram, email)
- [ ] Widget/plugin system for extensibility
- [ ] Integrations (Pi-hole, Plex, Proxmox, TrueNAS)

---

## 🤝 Contributing

Contributions are what make open source amazing. Whether it's a bug fix, a new feature, a widget, or a typo — **every contribution matters**.

Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

### Good First Issues

Look for issues labeled [`good first issue`](https://github.com/YOUR_USERNAME/pulse/labels/good%20first%20issue) — they're designed to help you get familiar with the codebase.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/pulse.git
cd pulse

# Start the backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Start the frontend (in another terminal)
cd frontend
npm install
npm run dev
```

---

## 📄 License

Pulse is open source software licensed under the [MIT License](LICENSE).

---

<div align="center">

**If Pulse helps you, consider giving it a ⭐ — it helps others find the project.**

</div>
