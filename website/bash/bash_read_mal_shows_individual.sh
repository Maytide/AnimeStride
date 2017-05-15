#!/bin/bash

export PATH="/maytide/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

python /maytide/stride/AnimeStride/website/manage.py runcrons "home.crons.TaskReadMALShowsIndividual"
if [ $? -eq 0 ]; then
    echo python TaskReadMALShowsIndividual success $(date)
    echo python TaskReadMALShowsIndividual success $(date) >> /maytide/stride/AnimeStride/website/history.txt
else
    echo python TaskReadMALShowsIndividual failed $(date)
    echo python TaskReadMALShowsIndividual failed $(date) >> /maytide/stride/AnimeStride/website/history.txt
fi
