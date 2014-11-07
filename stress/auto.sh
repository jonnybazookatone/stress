#!/bin/bash

/diska/home/jonny/.virtualenvs/stress/bin/python /diska/home/jonny/sw/python/stress/stress/stress_out_gp.py > /diska/home/jonny/sw/python/stress/stress/auto.log 2> /diska/home/jonny/sw/python/stress/stress/auto.log

export PYTHONPATH=$PYTHONPATH:/diska/home/jonny/sw/ && /usr/bin/python /diska/home/jonny/sw/python/stress/stress/stress_out_plot.py > /diska/home/jonny/sw/python/stress/stress/auto.log 2> /diska/home/jonny/sw/python/stress/stress/auto.log

#/usr/bin/python /diska/home/jonny/sw/python/stress/stress/stress_out_plot.py

