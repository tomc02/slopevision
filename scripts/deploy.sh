#!/bin/bash
source ../.env
export $(cat ../.env | xargs)
cd ../deploy
./inventory.py
ansible-playbook -i inventory.ini playbook.yml
