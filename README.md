# Group8
## Welcome on our project
## Description
This application is a Server Monitoring tool :
* Connecting to the machine "to be monitored" through SSH.
* Get CPU & RAM info from these distant machines.
* Extract info from LOGs on the machines.
* Continuous delivery of the project in a Docker image.

This application was developed in a ***DevOps*** context, so that includes tests and deployments : 
* Writing tests and running them on each push.
* Continuous integration.
* Using a linter.
* Computing code coverage statistics.

## Dependencies
You need to install a dependency : 
```
sudo apt-get install docker-engine -y
```

## Installation
To run this project all you need is to pull & run our Docker image.

To run the docker image that contains our project, run the following commands :

```bash
docker login
```
The username is: group8

The password is: group8mdp

```bash
docker pull devops.telecomste.fr:5050/printerfaceadmin/2022-23/group8/image:latest
```
```bash
docker run -p 8080:8080 devops.telecomste.fr:5050/printerfaceadmin/2022-23/group8/image:latest
```

## Built With
* Python
* Docker
* Alpine

## Badges
We added badges in our project description to get the status of a stage and to show its progress, for instance if the pipeline passed and the coverage percentage.

## Visuals
Here are some screenshots to illustrate how the Server Monitoring tool works :

<!-- [monitor]: <png file>
[monitor]: <png file>
[monitor]: <png file> -->

## License
Télécom Saint-Etienne

## Authors
- Mathis Thuel-Chassaigne
- Cyril Bier
- Grégoire Naz
- Cédric Thong
- Omar El Gribes
