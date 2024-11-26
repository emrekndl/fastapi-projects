#!/bin/bash

ips=("172.18.0.2" "172.18.0.3" "172.18.0.4" "172.18.0.5" "172.18.0.6" "172.18.0.7")

if ! command -v parallel &> /dev/null
then
    echo "parallel tool is not installed"
    exit
fi

parallel -j 6 podman run -d --name ssh_server_{1} --net my_custom_network --ip {1} ssh_server ::: "${ips[@]}"
# parallel -j 8 podman run -d --name ssh_server_{1} --net my_custom_network --ip {1} -p {1}:300{#}:22 ssh_server ::: "${ips[@]}"
# parallel -j 9 podman run -dit --name ssh_server_{1} --net my_custom_network --ip {1} -p {1}:300{#}:22 ssh_server ::: "${ips[@]}"

