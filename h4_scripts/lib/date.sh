#!/bin/bash

date_to_timestamp() {
    date_string=$1
    echo `date --date="$date_string" +"%s"`
}
