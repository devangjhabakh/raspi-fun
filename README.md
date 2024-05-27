# Devang's Raspeberry Pi Projects

This is a side project I'm going to be undertaking. It is going to run on a dedicated, always-on raspberry pi server. Just want to make my life easier.

## Intial Setup

Creating a setup shell script that allows me to run all of the projects that I've created.
The setup script should be able to consume a .yml file that contains the commands that a project needs to run.
The setup script will only need to run once, when the device boots up.

## Project 1: An always-on lambda function-esque server

I will host a web server with a UI that allows me to:

- Upload files to any directory of my rapspberry pi
- Run any python script on my raspberry pi on a set schedule (e.g. every 15 minutes)

Files this project requires:

- A python server that handles these requests.