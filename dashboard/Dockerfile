# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for pigpio build, rpi.gpio, and your libs
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    unzip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libzbar0 \
    python3-rpi.gpio \
    python3-pigpio \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download, build, and install pigpio daemon from source
RUN wget http://abyz.me.uk/rpi/pigpio/pigpio.zip && \
    unzip pigpio.zip && \
    cd PIGPIO && \
    make && make install && \
    cd .. && rm -rf pigpio.zip PIGPIO

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Start pigpio daemon and then run your Streamlit app
CMD pigpiod && streamlit run streamlit.py --server.port=8501 --server.address=0.0.0.0
