#Use Python 3.13-slim base image
FROM python:3.13-slim

#Set the working directory in the container
WORKDIR /app/basketball_proj

#Copy requirements.txt first (for dependency caching)
COPY requirements.txt .

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy other files in directory into container
COPY . ./