FROM python:3.10.14-alpine

WORKDIR /workspace

# COPY source dest
COPY  ./requirements.txt /workspace/requirements.txt

#installing package
RUN  pip install  -r /workspace/requirements.txt 
RUN pip install python-dotenv
# COPY source dest
COPY ./src /workspace/src 

EXPOSE 5000
#cmd to run the app
CMD ["flask","--app","./src/main", "run", "--host", "0.0.0.0", "--port", "5000"]
