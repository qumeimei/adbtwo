#!/bin/bash

num_vars=$#
KEY=AIzaSyD-DxMBEDLEzKmCW5yWoyJ8gbMUO0_bXuY

if [ $num_vars -eq 0 ]; then
	python adbtwo.py -key $KEY 

else
	python adbtwo.py $@

fi
