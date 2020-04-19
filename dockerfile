FROM python:3.8.2-buster

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /server

# Set the working directory to /server
WORKDIR /server

# Copy the backend directory contents into the container at /server
ADD backend/scrumtool /server/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000
CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]
