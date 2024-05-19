# Devang's Raspeberry Pi Projects

This is a side project I'm going to be undertaking. It is going to run on a dedicated, always-on raspberry pi server. Just want to make my life easier.

## Project 1: An always-on lambda function-esque server

I will host a web server with a UI that allows me to:

- Upload files to any directory of my rapspberry pi
- Run any python script on my raspberry pi on a set schedule (e.g. every 15 minutes)

Files this project requires:

- A python server start script (start.sh)
- A python script to run on a schedule (lambda_runner.py)
- A UI to upload files and run scripts 
- A UI to view logs
- A UI to view the status of the server