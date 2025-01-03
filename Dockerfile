
# Use Python 3.13 base image
FROM python:3.13

# Set working directory in the container
WORKDIR /app

# Install required packages
RUN pip install --no-cache-dir \
    pymupdf==1.25.1 \
    streamlit==1.41.1

# Copy application files and assets
COPY app.py .
COPY bns_pdf_splitter.py .
COPY assets/ ./assets/

# Set environment variable for Streamlit port
ENV STREAMLIT_SERVER_PORT=8523

# Command to run when container starts
CMD ["streamlit", "run", "app.py"]

# Expose the port Streamlit will run on
EXPOSE 8523

# docker build -t asyafiqe/bns-pdf-splitter:0.1 .
# docker run -p 8523:8523 asyafiqe/bns-pdf-splitter:0.1 .