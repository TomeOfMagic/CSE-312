#!/bin/bash -l

wget https://github.com/facebookresearch/detectron2/archive/refs/tags/v0.4.zip

unzip 'v0.4.zip'

cd detectron2-0.4

pip install -e .

cd ..

pip install -r requirements.txt

#Remeber to download Git LFS For Model

