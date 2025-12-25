# Formbricks Data Seeder 🚀

A Python-based CLI tool to programmatically run, populate, and interact with a local Formbricks instance using APIs and realistic data generated via **Cerebras AI**.

This project demonstrates the ability to quickly understand a new application, generate realistic data, and fill it programmatically using API calls only.

---

## 📝 Project Aim

* Quickly spin up a local Formbricks instance.
* Generate realistic survey, user, and response data using an LLM.
* Seed the Formbricks instance entirely via API.
* Showcase good judgment in creating realistic, actively used system data.

---

## ⚡ Features

* **Up Command**: Run Formbricks locally using Docker/Docker Compose.
* **Down Command**: Gracefully stop and clean up the local Formbricks instance.
* **Generate Command**: Produce realistic data (users, surveys, responses) via **Cerebras AI**.
* **Seed Command**: Programmatically fill Formbricks using **Management API** (users, surveys) and **Client API** (survey responses).

---

## 📦 Installation & Setup

1. Clone the repository:

```bash
git clone https://github.com/coderRaj07/nuerona-challenge
cd nuerona-challenge
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your environment variables (Cerebras API keys) in a `.env` file (use .env.example as a template):

```
CEREBRAS_API_KEY=
FORMBRICKS_API_KEY=
FORMBRICKS_API_URL=
FORMBRICKS_ENV_ID=
FORMBRICKS_ORG_ID=
```

 **Note:** How to obtain and fill the Formbricks environment variables (`FORMBRICKS_API_KEY`, `FORMBRICKS_ENV_ID`, `FORMBRICKS_ORG_ID`) is explained in the official demo video: [Formbricks Demo Video](https://youtu.be/124P5GyCgxc)

---

## 🚀 Usage

The project provides a simple CLI via `main.py` to perform all tasks:

| Command                              | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| `python main.py formbricks up`       | Start the Formbricks instance locally              |
| `python main.py formbricks down`     | Stop and clean up the instance                     |
| `python main.py formbricks generate` | Generate realistic survey, user, and response data |
| `python main.py formbricks seed`     | Seed the Formbricks instance via APIs              |

---

## 📊 Seeding Details

* **Surveys**: 5 unique surveys with realistic questions and configurations.
* **Responses**: At least 1 realistic response per survey.
* **Users**: 10 unique users with `Manager` or `Owner` access levels.

All seeding is done **only via APIs**; no direct database manipulation is performed.

---

## 🛠 Technology Stack

* **Python 3.11+**
* **Cerebras AI** for generating realistic survey and user data
* **Formbricks** (self-hosted)
* **Docker & Docker Compose** for local environment management
* **Requests** for API interactions

---

## 📚 References

* [Formbricks API Documentation](https://formbricks.com/docs/overview/introduction)
* [Cerebras AI](https://www.cerebras.ai/)

---

## ✅ Notes

* Designed to be modular and maintainable.
* Focused on realistic, human-like data to showcase active system usage.
* Demonstrates ability to quickly understand and interact with new API systems programmatically.

---

## 🧑‍💻 Author

**Rajendra Bisoi**

* GitHub: [github.com/coderRaj07](https://github.com/coderRaj07)

---