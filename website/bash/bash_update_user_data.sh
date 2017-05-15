#!/bin/bash

export PATH="/maytide/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

python /maytide/stride/AnimeStride/website/manage.py runcrons "home.crons.TaskUpdateUserData"
if [ $? -eq 0 ]; then
    echo python TaskUpdateUserData success $(date)
    echo python TaskUpdateUserData success $(date) >> /maytide/stride/AnimeStride/website/history.txt
else
    echo python TaskUpdateUserData success $(date)
    echo python TaskUpdateUserData failed $(date) >> /maytide/stride/AnimeStride/website/history.txt
fi
