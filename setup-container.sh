#!/bin/bash

docker build -t syncer:1.0 .

docker run -d --restart=always -v /var/run/docker.sock:/var/run/docker.sock  syncer:1.0
