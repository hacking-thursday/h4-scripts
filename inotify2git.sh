#!/bin/bash

#### config ####
logdir='/home/yan/.irssi/irclogs/freenode/#h4'  # 此資料夾也必須要是個 git repo
message_full=15  # 訊息變動的行數
check_time=30  # 檢查檔案變動的頻率 (分鐘)
#### config ####

DEBUG="false"
DRYRUN="false"
jobs=()

add_new_file() {
    file=$1

    if [ "$DEBUG" = "true" ]; then
        echo "new file: $file"
    fi

    cd $logdir; \
    git add $file; \
    git commit -m "new file: $file"; \
    if [ "$DRYRUN" = "false" ]; then \
        git push origin master; \
    fi
}

check_message_full() {
    file=$1

    if [ "$DEBUG" = "true" ]; then
        echo "file change: $file"
    fi

    changes=`cd $logdir; git diff --numstat | awk '{print $1}'`

    if [ "$DEBUG" = "true" ]; then
        echo "change line: $changes"
        echo "message full: $message_full"
        echo "change - full: $((changes - message_full))"
    fi

    if [ $((changes)) -ge $((message_full)) ]; then
        cd $logdir; \
        git add $file; \
        git commit -m "`tail -n 1 $file`"; \
        if [ "$DRYRUN" = "false" ]; then \
            git push origin master; \
        fi
    fi
}

inotify_file_create_handler="add_new_file"
inotify_file_modify_handler="check_message_full"

inotify_handler() {
    while read res
    do
        event=`echo $res | awk '{print $2'}`
        file=`echo $res | awk '{print $3'}`

        if [ "$DEBUG" = "true" ]; then
            echo $res
        fi

        case "$event" in
        CREATE)
            if [ \"$inotify_file_create_handler\" ]; then
                eval $inotify_file_create_handler $file
            fi
            ;;
        MODIFY)
            if [ \"$inotify_file_modify_handler\" ]; then
                eval $inotify_file_modify_handler $file
            fi
            ;;
        esac
    done
}

check_file_change() {
    changes=`cd $logdir; git diff`

    for file in $(cd $logdir; git diff --name-only)
    do
        cd $logdir; \
        git add $file; \
        git commit -m "`tail -n 1 $file`"; \
        if [ "$DRYRUN" = "false" ]; then \
            git push origin master; \
        fi
    done
}

display_usage() {
    echo -e "Usage:"
    echo -e "$0 [arguments] file|dir\n"
    echo -e "Arguments:"
    echo -e "   -d | --debug    print debug message"
    echo -e "   --dryrun        dryrun"
}

main() {
    ## argument parse start ##
    if [ $# == 0 ]; then
        display_usage
        exit
    fi

    while [ $# != 0 ]
        do
        case "$1" in
        -h)
            display_usage
            exit 0
            ;;
        -d | --debug)
            DEBUG="true"
            ;;
        --dryrun)
            DRYRUN="true"
            ;;
        *)
            logdir="$1"
            ;;
        esac
        shift
    done
    ## argument parse end ##

    # kill subprocess when exit
    # trap 'echo kill ${jobs[*]} ; ((${#jobs[@]} == 0)) || kill ${jobs[*]} ; exit' EXIT HUP TERM INT
    trap 'echo kill ${jobs[*]} ; ((${#jobs[@]} == 0)) || pkill -P ${jobs[*]} ; exit' EXIT HUP TERM INT

    # inotify monitor
    (echo "$BASHPID" > pid-file; inotifywait -m -r -e create -e modify -e close_write --exclude "\.git/*" $logdir | inotify_handler) &
    jobs+=(`cat pid-file`)

    # time monitor
    while true; do
        if [ "$DEBUG" = "true" ]; then
            echo `date +%s`
        fi
        sleep $(($((check_time)) * 60))
        check_file_change
    done
}

if [[ "$BASH_SOURCE" == "$0" ]]
then
    main $@
fi
