FROM rasa/rasa-sdk:2.8.2

# Use subdirectory as working directory

# Copy any additional custom requirements, if necessary (uncomment next line)
# COPY actions/requirements-actions.txt ./

# Change back to root user to install dependencies
#USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
# RUN pip install -r requirements-actions.txt

# Copy actions folder to working directory
USER root

RUN /opt/venv/bin/python -m pip install --upgrade pip
RUN pip install ipdb
RUN pip install sendgrid==6.3.1
RUN pip install redis==3.5.3


COPY ./actions  /app/actions

WORKDIR /app
