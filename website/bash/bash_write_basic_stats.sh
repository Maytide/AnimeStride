#!/bin/bash

export PATH="/maytide/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

python /maytide/stride/AnimeStride/website/manage.py runcrons "home.crons.TaskWriteBasicStats"
if [ $? -eq 0 ]; then
    echo python TaskWriteBasicStats success $(date)
    echo python TaskWriteBasicStats success $(date) >> /maytide/stride/AnimeStride/website/history.txt
else
    echo python TaskWriteBasicStats failed $(date)
    echo python TaskWriteBasicStats failed $(date) >> /maytide/stride/AnimeStride/website/history.txt
fi
