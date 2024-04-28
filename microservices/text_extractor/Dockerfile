FROM ubuntu:latest
LABEL authors="DELL"

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["top", "-b"]