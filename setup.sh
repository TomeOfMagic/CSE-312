#!/bin/bash -l
pip install torch

pip install torchvision

pip install -r requirements.txt

wget https://github.com/facebookresearch/detectron2/archive/refs/tags/v0.4.zip

unzip 'v0.4.zip'

cd detectron2-0.4

pip install -e .

cd ..



#Remeber to download Git LFS For Model

