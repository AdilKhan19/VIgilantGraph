# VigilantGraph 🛡️🕸️

An advanced, risk-aware cyber security analytics platform designed to model corporate laboratory environments, map potential vulnerabilities, simulate complex multi-stage attack vectors, and determine high-impact defensive remediations using mathematical optimization and game-theoretic agents.

---

## 🏗️ System Architecture & Components

VigilantGraph is broken down into highly specialized modular systems, each handling a distinct layer of the security simulation pipeline:

| Component | Responsibility |
| :--- | :--- |
| **Network Discovery** | Identify authorized lab devices and active running services. |
| **Asset Intelligence** | Maintain structured device, software version, and network service profiles. |
| **Vulnerability Intelligence** | Map known test vulnerabilities (CVEs) directly onto active inventory assets. |
| **Attack Graph Engine** | Build directed attack relationship models mapping interconnected exploit possibilities. |
| **Bayesian Risk Engine** | Compute operational compromise probabilities across the network nodes. |
| **HMM Prediction Engine** | Model probable attacker lateral movement progression using Hidden Markov Models. |
| **Pathfinding Engine** | Calculate least-resistance, risk-weighted attack paths across network topologies. |
| **Centrality Engine** | Pinpoint high-impact corporate assets through systemic structural analysis. |
| **Patch Optimization** | Select cost-effective and structurally impactful security patch interventions. |
| **Anomaly Detection** | Monitor and flag unusual or malicious network activity. |
| **Game Theory Engine** | Simulate adversarial strategic decision conflicts between attackers and defenders. |
| **Dashboard** | Provide interactive visual reports, graphs, and defensive metrics recommendations. |

---

## 🛠️ Software Requirements & Development Stack

### Core Lab Prerequisites
The network virtualization and local infrastructure utilize the following system engines:
* **Python 3.13+** – Main programming language platform
* **Visual Studio Code** – Primary IDE and local execution environment
* **Oracle VirtualBox** – Multi-node system hosting virtual corporate lab servers
* **Ubuntu Server 24.04 LTS** – Server operating system layer deployed inside lab nodes
* **Docker Engine / Docker Compose** – Containerized container layers isolating database and app services
* **Nmap** – Network auditing tool providing authorized lab asset and service discovery scans

### Python Tech Stack & Libraries
* **FastAPI** – High-performance backend REST API infrastructure
* **NetworkX** – Complex network structures and structural graph operations
* **NumPy / SciPy** – Linear algebra computations and sparse matrix manipulations
* **Pandas** – Data wrangling, ingestion framing, and asset dataset parsing
* **Scikit-learn** – Core anomaly detection algorithms (K-Means and Isolation Forests)
* **PostgreSQL / SQLAlchemy** – Reliable relational storage engine paired with object-relational mapping
* **OR-Tools** – Combinatorial optimization solver driving mathematical patching models
* **Pydantic** – Declarative data payload validation and schema parsing
* **Pytest** – Unit testing, integration automation framework, and algorithmic diagnostics
* **Plotly / Cytoscape.js** – Interactive analytical data plots and client-side canvas network topologies

### Recommended VS Code Extensions
To maintain code formatting parity and infrastructure access, ensure these tools are installed inside your workspace:
* `ms-python.python` (Python core support)
* `ms-python.vscode-pylance` (Static type checker)
* `ms-python.debugpy` (Python debugger)
* `ms-azuretools.vscode-docker` (Container management engine)
* `eamodio.gitlens` (Interactive version controls)
* `ckearneg.postgresql` (Database inspector browser)
* `charliermarsh.ruff` (Linter and code style formatter)

---

## 📊 Dashboard Modules & Features

The web presentation console compiles data out of the backend analytics services into clear tabs:

* **Overview:** Summarizes global asset health counters, net risk indexes, and top critical system nodes.
* **Network Topology:** An interactive structural rendering tracking live active network infrastructure layouts.
* **Attack Graph:** A directed dependency canvas tracing accessible exploit links and lateral pivot risks.
* **Path Prediction:** Real-time comparative tracking pitting Dijkstra against A* routing configurations.
* **Risk Propagation:** Explores Bayesian blast radius calculations and cascading compromise distributions.
* **Threat Analytics:** Evaluates Hidden Markov Model predictions alongside anomalies caught inside tracking sequences.
* **Patch Optimizer:** Compares cost-optimal security remediation algorithms across Greedy, DP, and ILP models.
* **Game Simulation:** Evaluates matrix payouts from defensive interactions between competing threat agents.
* **Vulnerability Intelligence:** Provides indexed views matching software packages against CVE mappings and strict CVSS severities.
* **Audit & Reports:** A compliance engine generating metrics overviews and raw exportable summaries.

---

## 🗺️ Project Development Roadmap

VigilantGraph's complete deployment architecture spans 12 structured development horizons:

[Phase 1: Environment Setup] ──> [Phase 2: Corporate Lab Build] ──> [Phase 3: Network Discovery]
│
[Phase 6: Pathfinding Engines] <── [Phase 5: Graph Structure]  <── [Phase 4: Vulnerabilities]
│
[Phase 7: Probability Models]  ──> [Phase 8: Criticality Metrics] ──> [Phase 9: Optimization]
│
[Phase 12: Final Integration]  <── [Phase 11: Game Theory]     <── [Phase 10: Machine Learning]

### 🟩 Foundation Tasks
1. **Phase 1 — Development Environment:** Install local software applications, configure Python virtual runtimes, connect Git components, and build the initial codebase repositories.
2. **Phase 2 — Corporate Laboratory:** Configure independent hardware nodes, map isolated local networks, mount virtualized Ubuntu servers, and verify baseline environment connectivity.
3. **Phase 3 — Network Discovery:** Implement background asset collection services, perform port identification sweeps, build active asset inventories, and establish ingestion queues.
4. **Phase 4 — Vulnerability Intelligence:** Construct the structured CVE dictionary caches, implement software fingerprint matching, calculate threat severities, and generate baseline asset risk rows.
5. **Phase 5 — Graph Engine:** Build central network data structures, establish active adjacency listing schemas, define directed dependency relations, and connect underlying graph persistence layers.
6. **Phase 6 — Pathfinding:** Integrate Dijkstra and A* shortest path search variations, construct weighted cost functions, and evaluate multivariable network attack avenues.

### 🟦 Advanced Analytics Systems
7. **Phase 7 — Probability Engine:** Build comprehensive Bayesian threat graphs, model Noisy-OR node distributions, and construct automated lateral movement trackers using Hidden Markov Models.
8. **Phase 8 — Criticality Analysis:** Deploy PageRank scoring arrays, apply centrality parameters, and evaluate systemic node failure metrics across varying compromise scenarios.
9. **Phase 9 — Optimization:** Construct multi-objective Knapsack solvers, design greedy resource allocation logic, and compare dynamic programming alongside Integer Linear Programming patch models.
10. **Phase 10 — Machine Learning:** Train custom K-Means clusters and Isolation Forest anomaly models, construct behavioral data pipelines, and validate telemetry data splits.
11. **Phase 11 — Game Theory:** Define distinct attacking and defending software agents, manage conditional utility pay-off matrices, and evaluate equilibrium choices under resource stress.
12. **Phase 12 — Integration & Demonstration:** Finalize frontend web panels, couple analytical pipelines across the localized testing node structures, run active platform experiments, generate audit paperwork, and present system defenses.

---

## 🚀 Setup & Execution Guide

### 1. Project Initialization
Cloning and preparing isolated environment bindings locally:
```bash
# Clone the repository
git clone https://github.com
cd VIgilantGraph

# Initialize Python virtual environment
python -m venv .venv
source .venv/Scripts/activate  # On Windows use: .venv\Scripts\activate
```

### 2. Dependency Management
Install the foundational testing framework requirements:
```bash
pip install pytest pydantic fastapi uvicorn
```

### 3. Running Diagnostic Tests
Validate your current graph builder operations and routing engine instances before writing extensions:
```bash
pytest tests/ -v
```