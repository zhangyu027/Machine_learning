# Use an official lightweight Python image
FROM python:3.10-slim

# Avoid Python writing .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Install system dependencies (for numpy/pandas/scipy/sklearn, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install common ML / data science libraries
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    scikit-learn \
    matplotlib \
    seaborn \
    jupyter \
    notebook

# Copy the entire repository into the image
COPY . /app

# Default command when container starts
# (You can later change this to run a specific project/script,
#  e.g. ["python", "Customer Churn/train.py"])
CMD ["bash"]
