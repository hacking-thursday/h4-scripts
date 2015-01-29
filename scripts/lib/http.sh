#!/bin/bash

read_url() {
    url=$1

    content=$(wget $url -q -O -)
    echo $content
}
