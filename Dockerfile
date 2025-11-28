FROM python:3.12-slim

# 1. Install system tools needed for Playwright & building
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip git \
    && rm -rf /var/lib/apt/lists/*

# 2. Install uv
RUN pip install uv

WORKDIR /app

# 3. Copy dependency files FIRST (for better caching)
COPY pyproject.toml uv.lock ./

# 4. Install dependencies into the system python (no venv needed for docker)
RUN uv sync --frozen --system

# 5. NOW install the browsers using the installed package
# We use 'uv run' to ensure it uses the correct environment
RUN uv run playwright install chromium --with-deps

# 6. Copy the rest of the code
COPY . .

# 7. Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# 8. Run the app
# Note: We use 'python' directly because we installed to system
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]