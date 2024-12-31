#!/bin/bash
source ../.env
export $(cat ../.env | xargs)
./inventory.py
ansible-playbook -i inventory.ini playbook.yml
