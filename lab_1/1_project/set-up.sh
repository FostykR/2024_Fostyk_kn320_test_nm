#!/bin/bash 
echo "Start"
# Наступна команда буде створювати віртуальне середовище
python -m venv ./project_requests
# Далі нам потрібно встановити всі необхідні бібліотеки, всередині нашого віртуального середовища 
source project_requests/Scripts/activate
pip install requests
deactivate
echo "Finish"