# HackIt

HackIt Entry

Design: https://drive.google.com/open?id=1epobOGU_xQWEQW658HH9IYjrLYbyvkzb

Use Tensorflow 2.0

Dont use Tensorflow-gpu if we dont intent to have GPU on server.
  If we have a GPU, it must be CUDA Compute 6.1 or higher

The official Network is Networks\RoutingEngine1Mrecords25epoch96percent.NN


Tensorboard
  tensorboard --logdir=.\HackIt\HackItSolution\Logs


use "GenerateCallVolume.py" to gennerate new call volume

use "TrainNetwork.py" to train on that new volume

update "\Inferencing\__init__.py" to use the new .NN

use "Main.py" to Inference the New Network


## Docker

This project contains a `Dockerfile` for running the API in a container.

From the root of the project tree, run the following:

```bash
$ docker build -t hackit .
$ docker run -p 5000:5000 hackit
```

If you need to get to a local shell, run the container with `docker run --interactive --tty hackit bash`.