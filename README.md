# Article fetcher
This is a python script running in docker that fecthes articles from https://jsonmock.hackerrank.com/api/articles.

## Getting started

Execute `make build` to build the docker image.

Execute `make run` to run the docker container.

Execute `make save` to save the docker image as a TAR file *(Optional)*.

To download a csv file instead of printing to terminal execute `make run ARGS="--csv"`.