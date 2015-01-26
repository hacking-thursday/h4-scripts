#!/bin/bash

debug_print() {
    message=$1

    if [ "$DEBUG" = "true" ]; then
        echo $message
    fi
}
