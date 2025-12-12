FROM python:3.11-slim

# 1. Install system dependencies required for Playwright and building tools
RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copy requirements first to leverage caching
COPY requirements.txt .

# 3. Install Python libraries
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# 4. Install Playwright Browsers (Critical for scraping tasks)
RUN playwright install chromium --with-deps

# 5. Copy the rest of the application code
COPY . .

# 6. Expose the port Hugging Face expects
EXPOSE 7860

# 7. Start the application
# We use 'uvicorn' to run the 'app' object from 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
