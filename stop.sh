#!/bin/bash
screen -ls | grep pingthis | cut -d"." -f1 | xargs kill
screen -w
screen -ls
