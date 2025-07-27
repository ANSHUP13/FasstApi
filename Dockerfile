# choose base image
FROM python:3.13.1-slim

# set working directory
WORKDIR /app

# copy requirements file
COPY . /app/

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# expose port
EXPOSE 8000 

# run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
