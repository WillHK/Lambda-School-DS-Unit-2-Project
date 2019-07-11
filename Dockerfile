#Use Anaconda base image
FROM continuumio/anaconda3

# I made this, me.
LABEL maintainer="Will Haeck"

# Set working directory
WORKDIR /app

# Copy from base machine to docker container
COPY . /app

# Install GCC from apt-get repository
RUN apt-get install -y gcc

# Install requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port 80 for web browser
EXPOSE 80

# Run gunicorn server
CMD ["gunicorn", "index:server"]