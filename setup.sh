#!/bin/bash -l
pip install torch

pip install torchvision

pip install -r requirements.txt


wget -v -O Model/output/model.zip -L https://ucmerced.app.box.com/shared/static/5cbui0nirr8t83gn1f6lvv8a7umn79tt

unzip Model/output/model.zip -d Model/output

wget https://github.com/facebookresearch/detectron2/archive/refs/tags/v0.4.zip

unzip 'v0.4.zip'

cd detectron2-0.4

pip install -e .

cd ..


#Remeber to download Git LFS For Model

