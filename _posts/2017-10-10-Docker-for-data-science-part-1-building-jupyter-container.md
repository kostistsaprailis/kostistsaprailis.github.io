---
layout: post
title: "Docker for data science, building a simple jupyter container"
date: 2017-10-10 00:00:00 +0300
excerpt: "This is the first post on a series covering my findings while exploring containers for Data Science projects."
categories: [tutorial]
tags: [docker, data science, devops]
comments: true
---

<!--excerpt-->

This is the first in a series of posts where I'll be noting down my findings while exploring Docker and how and if it can help for everything Data Science related. In this post I'll try to build a simple container that will have a jupyter notebook installed.

<h2><strong>Contents</strong></h2>

* TOC
{:toc}

### What is Docker?

From [Wikipedia][docker-wikipedia]:
> Docker is a software technology providing containers, promoted by the company Docker, Inc. Docker provides an additional layer of abstraction and automation of operating-system-level virtualization on Windows and Linux. Docker uses the resource isolation features of the Linux kernel such as cgroups and kernel namespaces, and a union-capable file system such as OverlayFS and others to allow independent "containers" to run within a single Linux instance, avoiding the overhead of starting and maintaining virtual machines (VMs).

So Docker is a program that provides containers, and [containers](https://en.wikipedia.org/wiki/Operating-system-level_virtualization) are one way of performing what is called Operating System Level Virtualization:
> Operating-system-level virtualization, also known as containerization, refers to an operating system feature in which the kernel allows the existence of multiple isolated user-space instances. Such instances, called containers, partitions, virtualization engines (VEs) or jails (FreeBSD jail or chroot jail), may look like real computers from the point of view of programs running in them. A computer program running on an ordinary person's computer's operating system can see all resources (connected devices, files and folders, network shares, CPU power, quantifiable hardware capabilities) of that computer. However, programs running inside a container can only see the container's contents and devices assigned to the container.

This is achieved using the Linux [cgroups](https://en.wikipedia.org/wiki/Cgroups) and [namespaces](https://en.wikipedia.org/wiki/Linux_namespaces) feaures which respectively are described as:
> cgroups (abbreviated from control groups) is a Linux kernel feature that limits, accounts for, and isolates the resource usage (CPU, memory, disk I/O, network, etc.) of a collection of processes.
and
> Namespaces are a feature of the Linux kernel that isolate and virtualize system resources of a collection of processes. Examples of resources that can be virtualized include process IDs, hostnames, user IDs, network access, interprocess communication, and filesystems. Namespaces are a fundamental aspect of containers on Linux.

This means that docker is not the only way to create and use containers. Another similar software is [rkt](https://github.com/rkt/rkt). However since Docker is the dominant container technology I will explore this option for now.

### Getting started with Docker

To use docker it needs to be installed on your system (duh). The official [instructions](https://docs.docker.com/engine/installation/) pretty much cover anything, but there are two main points to notice:

- Docker is provided in the Community Edition and Enterprise Edition. For the majority of use cases the Community Edition is enough as it provides the whole container, orchecstration, networking and security functionality.
- Docker is available for all 3 major OSs however since the container technology is native to Linux, the docker versions for Mac and Windows will use a Virtual Machine on top of which docker will run. This is mostly important when deploying the containers as if they are not deployed on a Linux machine docker, the Virtual Machine that is created to run docker will have a performance cost on the host machine where docker is installed.

Once docker is installed open up a shell to confirm it:
```
$ docker --version
Docker version 17.09.0-ce, build afdb6d4
```

And the typical hello world example is running a hello world container:
```
$ docker run hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://cloud.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/engine/userguide/
```

In the output of the command there's a nice high level explanation of what happened here. So to proceed I need a good tutorial.

Fortunately the official docker [guide](https://docs.docker.com/get-started/) is such a tutorial for getting a feeling for how Docker works. I'll add here the bits that I found interesting while going through it.

First note to keep in mind is the difference between a Docker Image and a Docker Container:
> An image is a lightweight, stand-alone, executable package that includes everything needed to run a piece of software, including the code, a runtime, libraries, environment variables, and config files.

> A container is a runtime instance of an image—what the image becomes in memory when actually executed. It runs completely isolated from the host environment by default, only accessing host files and ports if configured to do so.

> Containers run apps natively on the host machine’s kernel. They have better performance characteristics than virtual machines that only get virtual access to host resources through a hypervisor. Containers can get native access, each one running in a discrete process, taking no more memory than any other executable.

### Docker images

So in order to run a container we need to have an image. But how are images created? This is where the Dockerfiles come in. Dockerfiles describe the way that an image is being build, in layers. Every instruction will build a new layer with the changes of that instruction.

Usually the first command in a dockerfile is a `FROM` command. This defines a base image upon which the current image will be expanded (as mentioned in layers). The command is followed by the image name, a colon and a tag which defines different versions of the image. From that point on the rest of the commands build upon this image, with pretty much every linux command. The available commands can be found [here]](https://docs.docker.com/engine/reference/builder/).

To find available base images the best place is the [Docker store](https://store.docker.com/). Most of the images there are free, however there are also paid ones. You can search and find an image containing pretty much every software package available including images for databases, webservers, messaging systems etc. You can also push your own images to the store for others to use.

For a simple example let's create an image that contains python3 and jupyter. I'll be using the ubuntu image as the base image here. Next we use the `RUN` command to execute the system update and installation of python3 and the pip package manager. The next layer installs jupyter. Then we add another layer which creates a new system user, another layer to change to this user with the `USER` command, and finally using the `ENTRYPOINT` command we will define the command to start jupyter (using the `--ip=*` param to allow incoming traffic to jupyter from any IP). By default the filename of a dockerfile is, well, `Dockerfile`. 

```
# Use the latest ubuntu image as base for the new image
# ubuntu is the image name and latest is a tag that 
# references a particular version of the image.
# In this case latest is always the latest LTS image
# at the time of writing this, it's 16.04.
FROM ubuntu:latest

# Run a system update to get it up to speed
# Then install python3 and pip3
RUN apt-get update && apt-get install -y python3 \
    python3-pip

# Install jupyter
RUN pip3 install jupyter

# Create a new system user
RUN useradd -ms /bin/bash jupyter

# Change to this new user
USER jupyter

# Start the jupyter notebook
ENTRYPOINT ["jupyter", "notebook", "--ip=*"]
```

Now that we have the dockerfile ready let's build the image. Running the command `docker images` lists the available images in the system. The ubuntu base image is not in our local system so when we will build our own image, it will be downloaded.
```
$ docker images
REPOSITORY                   TAG                                       IMAGE ID            CREATED             SIZE
hello-world                  latest                                    1815c82652c0        3 months ago        1.84kB
```

So let's see how we build images. The basic command is `docker build` and the path to the dockerfile. Usually we also provide the `-t` param which defines the new image tag. You can find details regarding the docker build command [here](https://docs.docker.com/engine/reference/commandline/build/). Running the command produces the following output (it has been truncated):

```
$ docker build . -t jupyter
Sending build context to Docker daemon   2.56kB
Step 1/6 : FROM ubuntu:latest
 ---> 2d696327ab2e
Step 2/6 : RUN apt-get update && apt-get install -y python3     python3-pip
 ---> Running in bb404ad1f745
Get:1 http://security.ubuntu.com/ubuntu xenial-security InRelease [102 kB]
Get:2 http://archive.ubuntu.com/ubuntu xenial InRelease [247 kB]
Get:3 http://security.ubuntu.com/ubuntu xenial-security/universe Sources [49.7 kB]
Get:4 http://archive.ubuntu.com/ubuntu xenial-updates InRelease [102 kB]
Get:5 http://security.ubuntu.com/ubuntu xenial-security/main amd64 Packages [456 kB]
...
...
...
Removing intermediate container 4fc4f28aa4a7
Step 4/6 : RUN useradd -ms /bin/bash jupyter
 ---> Running in 1dc139392c0d
 ---> 61a9386d2b4d
Removing intermediate container 1dc139392c0d
Step 5/6 : USER jupyter
 ---> Running in a3d0480587cd
 ---> 2516f84b585d
Removing intermediate container a3d0480587cd
Step 6/6 : ENTRYPOINT jupyter notebook --ip=*
 ---> Running in 0eceeb09bb7d
 ---> ff2f03f5aaea
Removing intermediate container 0eceeb09bb7d
Successfully built ff2f03f5aaea
Successfully tagged jupyter:latest
```

Once it is finished we can run again the `docker images` command to see the newly created image:

```
kostis@kostismbp~/projects/docker-tests/jupyter$ docker images
REPOSITORY                   TAG                                       IMAGE ID            CREATED              SIZE
jupyter                      latest                                    ff2f03f5aaea        About a minute ago   541MB
ubuntu                       latest                                    2d696327ab2e        2 weeks ago          122MB
hello-world                  latest                                    1815c82652c0        3 months ago         1.84kB
```

Now we have our own brand new image to use. As mentioned before we can push this image to the store for others to use. Alternatively we can use a private docker registry (all the major cloud providers have similar services) if the image contains proprietary code, passwords, ssh keys etc. For all commercial applications, all companies use a private registry to privately store the images.

### Docker containers

The main thing we do with an image is run a container. This is done with the `docker run` command. The full details for how to use the command can be found [here](https://docs.docker.com/engine/reference/run/). For the image we have beed building here we can run `docker run -it -p 8888:8888 ff2f03f5aaea /bin/bash` where `ff2f03f5aaea` is the image id that we got from the `docker images` command.

```
$ docker run -it -p 8888:8888 ff2f03f5aaea /bin/bash
[I 20:47:25.881 NotebookApp] Writing notebook server cookie secret to /home/jupyter/.local/share/jupyter/runtime/notebook_cookie_secret
[W 20:47:25.897 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 20:47:25.904 NotebookApp] Serving notebooks from local directory: /bin
[I 20:47:25.904 NotebookApp] 0 active kernels
[I 20:47:25.904 NotebookApp] The Jupyter Notebook is running at:
[I 20:47:25.905 NotebookApp] http://[all ip addresses on your system]:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
[I 20:47:25.905 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 20:47:25.905 NotebookApp] No web browser found: could not locate runnable browser.
[C 20:47:25.906 NotebookApp] 
    
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

If you open a browser window and go to the above url you'll see the notebook live. It's a new clean environment that we can shape as we like and destroy once we are done.

Going to a new terminal and run the `docker ps` command (which lists the running containers) we can see our container! Notice the `-p 8888:8888` parameter. This maps the container's inner port to the host machine's port. This is done so that we can access the jupyter notebook running inside the container from our machine. By default everything is isolated inside the container and we need to manually export any resources that need to be exposed as to be accessed.

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
911acd30ed36        ff2f03f5aaea        "jupyter notebook ..."   18 minutes ago      Up 18 minutes       0.0.0.0:8888->8888/tcp   sleepy_hugle
```

Furthermore the way we ran the container above though we need to keep the terminal open otherwise the container will stop. Typing `ctrl+c` to kill the container we can see that there's no longer any container:

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

To work around this issue we can add the `-d` parameter when we run a container which detaches it from the terminal so that it runs in the background even after the terminal has closed.

```
$ docker run -d -p 8888:8888 ff2f03f5aaea
98890a46a5c2375b8aa3a36111ceee941992391b4c19f2878d9906e4ff5ce699
```
In this case we get the terminal back on the host system which means it has not been attached to the container. However to confirm that the container is running let's run the `docker ps` command again:

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
98890a46a5c2        ff2f03f5aaea        "jupyter notebook ..."   40 seconds ago      Up 38 seconds       0.0.0.0:8888->8888/tcp   hungry_euclid
```
It is indeed running. But how do we get the url from Jupyter? We use another docker command, `docker logs <container>`. Notice that instead of the container id we can also use the container name obtained above.

```
$ docker logs hungry_euclid
[I 19:38:32.023 NotebookApp] Writing notebook server cookie secret to /home/jupyter/.local/share/jupyter/runtime/notebook_cookie_secret
[W 19:38:32.059 NotebookApp] WARNING: The notebook server is listening on all IP addresses and not using encryption. This is not recommended.
[I 19:38:32.075 NotebookApp] Serving notebooks from local directory: /
[I 19:38:32.075 NotebookApp] 0 active kernels
[I 19:38:32.076 NotebookApp] The Jupyter Notebook is running at:
[I 19:38:32.076 NotebookApp] http://[all ip addresses on your system]:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
[I 19:38:32.076 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 19:38:32.076 NotebookApp] No web browser found: could not locate runnable browser.
[C 19:38:32.077 NotebookApp] 
    
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:8888/?token=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Finally to stop the container we need to manually do it by running the command `docker stop <container id>`:

```
$ docker stop hungry_euclid
hungry_euclid
```

And we can see that indeed there are no longer any containers running:

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### Removing containers & images

One last thing that is useful to know is how to remove containers and images. The commands respectively are `docker rm <container>` and `docker rmi <image>`. The way to find containers that are stopped is `docker ps -a`.
```
$ docker ps -a
98890a46a5c2        ff2f03f5aaea                                 "jupyter notebook ..."   10 minutes ago        Exited (0) 12 minutes ago                             hungry_euclid
$ docker rm hungry_euclid
hungry_euclid
```
Now to remove the image we have built:
```
$ docker images
REPOSITORY                   TAG                                       IMAGE ID            CREATED             SIZE
jupyter                      latest                                    ff2f03f5aaea        2 hours ago        541MB
ubuntu                       latest                                    2d696327ab2e        3 weeks ago         122MB
hello-world                  latest                                    1815c82652c0        3 months ago        1.84kB
$ docker rmi ff2f03f5aaea
Untagged: jupyter:latest
Deleted: sha256:ff2f03f5aaea4ce5f2acd36d7ab2fde0337fa34d2921aaac3e51630778f4bba1
Deleted: sha256:2516f84b585d62c71514ce373baa93f6842c50573eb160983793b63b45a16bbe
Deleted: sha256:61a9386d2b4d569787f53b02b93060ee8bb25cf3b21e833e179dda8cfc395a9c
Deleted: sha256:4c69651b94bbbca80e6521cc4576ccf5ff5cfa4a10dc1acae87a047b91d0001a
Deleted: sha256:e5c0bb29999d46880dbe106099f4f1cc265227cf5b16a29a98983ace01db3d97
Deleted: sha256:5fa718810d8afb400449e9967c1f0fc46bbe2f4273b67e4e61a18f159e859dcb
Deleted: sha256:3d5ec8b404c085bc7548a32d8077e5ec58e25e1059e78c88be5effab9414932b
Deleted: sha256:b55b2ae6bd8065f43e39f179773f82e0bb1df302162796bddd48cb606e6e6c1b
```

### Conclusion

This was a small introduction into the docker basics: images and containers. The next post in the series will cover a multi-container system, where containers really shine. In the meantime the official docker [tutorial](https://docs.docker.com/get-started/) is a very good introduction to various concepts that were not covered here, I suggest getting a look at it.

[docker-wikipedia]: https://en.wikipedia.org/wiki/Docker_(software)