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

# Install pystan, has to be done first?
RUN pip install --trusted-host pypi.python.org pystan

# Install requirements
RUN pip install --ignore-installed --trusted-host pypi.python.org -r requirements.txt

# Install FBProphet
RUN conda install -c conda-forge fbprophet

# Download zillow data
RUN wget http://files.zillowstatic.com/research/public/Zip/Zip_Zhvi_AllHomes.csv

# Expose port 80 for web browser
EXPOSE 80

# Run gunicorn server
CMD ["gunicorn --bind 0.0.0.0:80", "index:server"]