#!/bin/bash

for X in nginx:alpine httpd:alpine alpine busybox python:alpine debian:buster-slim pengbai/docker-supermario; do
	docker run -dti $X
done
