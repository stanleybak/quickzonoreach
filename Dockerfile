# Dockerfile for QuickZonoReach

FROM python:3.6

# install other (required) dependencies
RUN pip3 install numpy scipy matplotlib

# copy current directory to docker
COPY ./code /code

### As default command: run the tests ###
CMD python3 /code/example_plot.py && python3 /code/example_compare.py && python3 /code/example_profile.py

# USAGE:
# Build container and name it 'quickzono':
# docker build . -t quickzono

# # run example scripts (default command)
# docker run quickzono

# # get a shell:
# docker run -it quickzono bash
# code subfolder is available in /code
# to delete docker container use: docker rm quickzono
