#!/bin/bash 
# $1 - це така зміннв, яка відповідає першому аргументу який буде переданий у скрипт
name=$1
echo "Start creating $name"


cd $name
python -m venv ./venv_$name
source venv_$name/Scripts/activate
pip install -r requirements.txt
deactivate
echo "Finish"
