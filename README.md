# 🚀 FastAPI Pro Starter Template

A production-ready, high-performance architectural foundation for FastAPI applications. 

This isn't just a "Hello World" example. It is a deeply thought-out structure incorporating **Clean Architecture**, **RBAC (Role-Based Access Control)**, **Redis-backed Session Management**, and **Async SQLAlchemy**.

## 📖 The Story
I started building this template when I was **14 years old** to solve a recurring problem: setting up a secure, scalable backend from scratch is repetitive and error-prone. Over the course of about **30 hours** of focused development—finishing just after my **15th birthday**—I built this to serve as a "Gold Standard" for my future projects.

It focuses on **Security-First** principles, using Argon2 for hashing, JWT rotation, and strict context management.

---

## ✨ Key Features
- **Modern Auth:** JWT-based authentication with Refresh Token rotation.
- **RBAC System:** Fine-grained Role-Based Access Control (Users -> Roles -> Permissions).
- **Redis Integration:** Fast session storage and response caching using `fastapi-cache2`.
- **State Management:** Uses Python `ContextVars` to access User/Request state globally without "Prop Drilling."
- **Rate Limiting:** Built-in protection via `slowapi`.
- **Database:** Async PostgreSQL integration with `SQLAlchemy 2.0` and `Alembic` migrations.
- **Developer Experience:** Fully typed with Pydantic V2 and basic logging.

---

## 🛠️ Getting Started

This project uses [**uv**](https://github.com/astral-sh/uv), the ultra-fast Python package manager.

### 1. Installation
First, install `uv` if you haven't already, then set up the environment:

```bash
# Clone the repository
git clone https://github.com/Jas-creator-31/fastapi-starter-template
cd fastapi-starter-template

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
