CREATE A VIRTUAL ENVIRONMENT
    #--> python -m venv venv


ACTIVATE THE VIRTUAL ENVIRONMENT
    #--> venv\Scripts\activate


INSTALL FASTAPI AND UVIORN AND PYDANTIC
    #--> pip install fastapi uvicorn pydantic


RUN THE APPLICATION    
    # --> uvicorn main:app --reload
    # main is the name of the file, app is the FastAPI instance 
    # --reload enables auto-reload on code changes


OPEN THE BROWSER    
    # reload http://127.0.0.1:8000
    # to check the auto generated documentation
    # http://127.0.0.1:8000/docs

TO CREATE REQUIREMENT.TXT FILE 
    #--> pip freeze > requirements.txt

To create docker image
    # docker build -t ansh2043/fastapi_tutorial .
    # docker push ansh2043/fastapi_tutorial
    # docker run -p 8000:8000 ansh2043/fastapi_tutorial


AWS Deployment
    1. create an EC2 instance
    2. Connect to the EC2 instance
    3. Run the following commands
        a. sudo apt-get update
        b. sudo apt-get install -y docker.io
        c. sudo systemctl start docker
        d. sudo systemctl enable docker
        e. sudo usermod -aG docker $USER
        f. exit
 
    4. Restart a new connection to EC2 instance
    5. Run the following commands
        a. docker push ansh2043/fastapi_tutorial:latest
        b. docker run -p 8000:8000 ansh2043/fastapi_tutorial

    6. change security group settings
    7. Check the API 
    