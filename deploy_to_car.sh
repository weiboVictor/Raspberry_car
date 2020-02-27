#!/bin/bash
: '
read -p "Deploy Server folder? (y/n)" varserver
read -p "Deploy Client folder? (y/n)" varclient

if [ $varserver == "y" ]; then
    rsync -rvzI -e ssh ~/Desktop/01-Work/05-Projects/Raspberry\ car/Raspberry_car/Server/ pi@192.168.1.17:~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/
fi

if [ $varclient == "y" ]; then
    rsync -rvzI -e ssh ~/Desktop/01-Work/05-Projects/Raspberry\ car/Raspberry_car/Client/ pi@192.168.1.17:~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Client/
fi
'

rsync -rvzI -e ssh ~/Desktop/01-Work/05-Projects/Raspberry\ car/Raspberry_car/lambda_car_core/ pi@192.168.1.17:~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/lambda_car_core/