#!/bin/bash

#### config ####
logdir='/home/yan/.irssi/irclogs/freenode/#h4'  # 此資料夾也必須要是個 git repo
message_full=15  # 訊息變動的行數
check_time=15  # 檢查檔案變動的頻率 (分鐘)
#### config ####

jobs=()
trap 'echo kill ${jobs[*]} ; ((${#jobs[@]} == 0)) || kill ${jobs[*]} ; exit' EXIT HUP TERM INT

check_message_full() {
    while read res
    do
        event=`echo $res | awk '{print $2'}`
        file=`echo $res | awk '{print $3'}`

        echo $res

        case "$event" in
        CREATE)
            # Traitement sur création d'un fichier
            echo "new file: $file"

            cd $logdir; \
            git add $file; \
            git commit -m "new file: $file"; \
            git push origin master
            ;;
        MODIFY)
            changes=`cd $logdir; git diff --numstat | awk '{print $1}'`

            if [ $((changes)) -ge $((message_full)) ]; then
                cd $logdir; \
                git add $file; \
                git commit -m "`tail -n 1 $file`"; \
                git push origin master
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
        git push origin master
    done
}

main() {
    ## argument parse start ##
    while [ $# != 0 ]
        do
        case "$1" in
        -h)
            echo -e "Usage:"
            echo -e "$0 [arguments] dir|file\n"
            exit 0
            ;;
        esac
        shift
    done
    ## argument parse end ##

    # inotify monitor
    (echo "$BASHPID" > pid-file; inotifywait -m -r -e create -e modify -e close_write --exclude "\.git/*" $logdir) | check_message_full &
    jobs+=(`cat pid-file`)

    # time monitor
    while true; do
        echo `date +%s`
        sleep $(($((check_time)) * 60))
        check_file_change
    done
}

if [[ "$BASH_SOURCE" == "$0" ]]
then
    main
fi
