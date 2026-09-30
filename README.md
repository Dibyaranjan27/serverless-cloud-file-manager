# Serverless Cloud File Manager

A modern, event-driven Cloud File Manager built for a 4th-year Cloud Computing course project. 

This project fully simulates an enterprise AWS serverless architecture (S3, Lambda, DynamoDB) **entirely locally and for free** using LocalStack and Docker. It features a responsive, glassmorphism UI built with Python Flask.

## Architecture Diagram

1. **Frontend (Flask)**: User uploads a file.
2. **Storage (Amazon S3)**: File is stored securely in an S3 bucket.
3. **Event-Driven Compute (AWS Lambda)**: S3 triggers an asynchronous Lambda function to extract file metadata.
4. **Database (Amazon DynamoDB)**: Lambda writes the metadata (filename, size, timestamp) to a NoSQL DynamoDB table.
5. **Retrieval**: The Flask frontend queries DynamoDB to display the files.

## Features
- ☁️ **Full Local AWS Simulation**: Zero cloud costs.
- 📁 **Multiple File Upload**: Upload dozens of files simultaneously.
- 🔍 **Instant Search**: Real-time client-side search filtering.
- 📱 **Mobile Responsive**: Custom stacked-card layout for small screens.
- ⬇️ **Direct Downloads**: Stream files back directly from S3.
- 🎨 **Glassmorphism UI**: Beautiful, modern frontend design.

## Prerequisites
- Docker Desktop
- Docker Compose

## Getting Started

1. **Start the environment:**
   \\\ash
   docker-compose up -d
   \\\`n
2. **Access the application:**
   Open your browser and navigate to \http://localhost:5000\`n
3. **Stopping the environment:**
   \\\ash
   docker-compose down
   \\\`n
## Tech Stack
- **Backend**: Python 3.9, Flask, Boto3 (AWS SDK)
- **Frontend**: HTML5, CSS3, Vanilla JS, Jinja2
- **Infrastructure**: LocalStack, Docker, Docker Compose
- **Simulated Cloud Services**: AWS S3, AWS Lambda, AWS DynamoDB

