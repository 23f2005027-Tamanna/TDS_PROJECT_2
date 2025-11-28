FROM python:3.12-slim

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy requirements first
COPY requirements.txt .

# 3. Install Python libraries using standard PIP (Safe Mode)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Install Playwright Browsers
RUN playwright install chromium --with-deps

# 5. Copy the rest of the code
COPY . .

# 6. Expose the port
EXPOSE 7860

# 7. Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]