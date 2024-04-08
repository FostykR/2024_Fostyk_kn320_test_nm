#!/bin/bash 
echo "Start"
name="2_project"
cd $name
python -m venv ./venv_$name
source venv_$name/Scripts/activate
pip install -r requirements.txt
deactivate
echo "Finish"
