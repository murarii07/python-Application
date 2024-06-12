FROM python:3.10.14-alpine

WORKDIR /workspace

# COPY source dest
COPY  ./requirements.txt /workspace/requirements.txt

#installing package
RUN  pip install --no-cache-dir --upgrade -r /workspace/requirements.txt 

# COPY source dest
COPY ./src /workspace/src 

#cmd to run the app
CMD ["flask","--app","./src/main", "run", "--host", "0.0.0.0", "--port", "5000"]
