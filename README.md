# Welcome on our project
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
This tool is deployed as a docker image so you need to install docker in your computer : 
```
sudo apt-get install docker-engine -y
```

## Installation
To run this project all you need is to pull & run our Docker image.

To run the docker image that contains our project, run the following commands :

```bash
docker login devops.telecomste.fr:5050
```
Enter your login informations. <br>
Then, you can pull the image :

```bash
docker pull devops.telecomste.fr:5050/printerfaceadmin/2022-23/group8/image:latest
```
Now you can run the image :
```bash
docker run -p 8050:8050 devops.telecomste.fr:5050/printerfaceadmin/2022-23/group8/image:latest
```
You can now access to the server in <href>http://localhost:8050/</href>

## Visuals
Here are some screenshots to illustrate how the Server Monitoring tool works.
### The home page : 
Home page of the app, here you can add, delete and choose a machine to monitor
![Alt text](/images/Home.png)
[1] : Here you can add a machine to monitor. <br>
[2] : On this input you can delete a machine from the application by selecting the number of the machine. <br>
[3] : The list of the machine currently save in the application. The machine you can acces are in green, you can monitor them by clickink on them.  

### The monitoring page
 - On this page you can monitor informations about your remote machine such as memory use, biggest files, ongoing processes, access logs or error logs.

![Alt text](/images/Memory.png)
![Alt text](/images/Biggest_files.png)
![Alt text](/images/Processes.png)
![Alt text](/images/access_logs.png)
![Alt text](/images/Error_logs.png)


## Built With
* Python
* Docker
* Alpine

## License
Télécom Saint-Etienne

