#!/bin/bash

export PATH="/maytide/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

python /maytide/stride/AnimeStride/website/manage.py runcrons "home.crons.RunCronJob"
if [ $? -eq 0 ]; then
    echo python RunCronJob success $(date)
    echo python RunCronJob success $(date) >> /maytide/stride/AnimeStride/website/history.txt
else
    echo python RunCronJob failed $(date)
    echo python RunCronJob failed $(date) >> /maytide/stride/AnimeStride/website/history.txt
fi
