#!/bin/bash

IRC_SERVER='irc.freenode.net'
IRC_PORT=6667
IRC_USERNAME='h4bot'
IRC_FULLNAME='h4bot'
IRC_NICK='h4bot'
IRC_CHANNEL='#h4'

send_irc_message() {
    message=$1

    cat << _EOF_ | nc $IRC_SERVER $IRC_PORT
USER $IRC_USERNAME 8 \* : $IRC_FULLNAME
NICK $IRC_NICK
JOIN $IRC_CHANNEL
PRIVMSG $IRC_CHANNEL :$message
QUIT
_EOF_
}
