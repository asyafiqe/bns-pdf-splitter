# BNS PDF Splitter App

A simple Streamlit application that allows users to split PDF files into multiple documents. This tool provides an easy-to-use interface for dividing large PDF files into smaller segments.

## Features

- Upload PDF files through a web interface
- Auto-detect page ranges for splitting
- Download split PDF files as a zip file
- Simple and intuitive user interface

## Getting Started

### Prerequisites

- Docker
- Docker Compose (optional)

### Installation & Running

There are several ways to run this application:

#### 1. Using Docker (Direct Build)

```bash
# Clone the repository
git clone https://github.com/asyafiqe/bns-pdf-splitter.git
cd bns-pdf-splitter

# Build the Docker image
docker build -t asyafiqe/bns-pdf-splitter .

# Run the container
docker run -p 8523:8523 asyafiqe/bns-pdf-splitter
```

#### 2. Using Docker Compose

```bash
# Clone the repository
git clone https://github.com/asyafiqe/bns-pdf-splitter.git
cd bns-pdf-splitter

# Start the application
docker compose up -d
```

The application will be available at `http://localhost:8523`

### Usage

1. Open your web browser and navigate to `http://localhost:8523`
2. Upload your PDF file using the file uploader
3. Download your split PDF files

## Development

To run the application locally for development:

1. Clone the repository
```bash
git clone https://github.com/asyafiqe/bns-pdf-splitter.git
cd pdf-splitter
```

2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
streamlit run app.py
```
