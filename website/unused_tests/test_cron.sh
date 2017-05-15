#!/bin/bash

export PATH="/maytide/anaconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"

echo Hello World!!! >> script_one_output.txt
if [ $? -eq 0 ]; then
    echo Hello World!!! command success >> script_one_output.txt
else
    echo Hello World!!! command failed >> script_one_output.txt
fi

python /maytide/stride/AnimeStride/website/manage.py runcrons "home.crons.RunCronJob" >> pythonlog.txt
if [ $? -eq 0 ]; then
    echo python .../website/manage.py success >> script_one_output.txt
else
    echo python .../website/manage.py failed >> script_one_output.txt
fi

python /maytide/stride/AnimeStride/website/test_bash_output.py >> pythonlog.txt
if [ $? -eq 0 ]; then
    echo python .../website/test_bash_output success >> script_one_output.txt
else
    echo python .../website/test_bash_output failed >> script_one_output.txt
    echo $? >> script_one_output.txt
fi

source /maytide/stride/AnimeStride/website/test_cron_2.sh
if [ $? -eq 0 ]; then
    echo test_cron_2 command success >> script_one_output.txt
else
    echo test_cron_2 command failed >> script_one_output.txt
fi

