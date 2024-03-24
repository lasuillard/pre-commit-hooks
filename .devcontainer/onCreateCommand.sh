#!/usr/bin/env bash

apt-get update && apt-get install -y bash-completion

echo '
if [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
fi
' >>~/.bashrc
