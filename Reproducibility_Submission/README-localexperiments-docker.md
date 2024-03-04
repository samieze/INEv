The provided container image bundles code and data for the local experiments.

# How to obtain the image and run a container 

```
docker run -it ghcr.io/samieze/repro23
```

This will run a shell inside the container. From this shell, execute 

```
./all_figures.sh
```

to start the experiments. They will take 2-3 days to finish.
Outputs will appear in the Figures subfolder inside the container.

# How to get results out of the container
Obtain the ID of the container with "docker ps -a". Then run 

```
docker cp CONTAINER_ID:/root/local_experiments/Figures ./
```

to copy the figures out.
