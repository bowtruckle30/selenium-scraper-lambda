FROM public.ecr.aws/lambda/python:3.8

RUN yum install -y \
    Xvfb \
    wget \
    unzip

# Install google-chrome-stable
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm && \
    yum localinstall -y google-chrome-stable_current_x86_64.rpm

# Install chromedriver
RUN wget https://chromedriver.storage.googleapis.com/2.40/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod 775 chromedriver

# Install selenium
RUN pip3 install -U pip selenium

# Install beautifulsoup
RUN pip3 install -U pip beautifulsoup4

# Copy lambda's main script
COPY app.py .

CMD ["app.lambda_handler"]