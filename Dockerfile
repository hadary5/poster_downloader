# Step 1 select default OS image
FROM alpine
# Step 2 Setting up environment
RUN apk add --no-cache python3-dev && apk add py3-pip
RUN pip3 install --upgrade pip
# Step 3 Configure a software
# Defining working directory
WORKDIR /app
# Installing dependencies.
COPY /requirements.txt /app
RUN pip3 install -r requirements.txt
# Copying project files.
COPY app.py /app
COPY MongoDBDAL.py /app
COPY TMDBDownLoader.py /app
COPY config.py /app
RUN mkdir -p /app/templates
RUN mkdir -p /app/temp_content
COPY ./Templates/* /app/templates
# Exposing an internal port
EXPOSE 5001
# Step 4 set default commands
 # Default command
ENTRYPOINT [ "python3" ]
# These commands will be replaced if user provides any command by himself
CMD ["app.py"]