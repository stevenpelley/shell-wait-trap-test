signal=$1

is_caught=false

term_handler() {
    kill %1 &> /dev/null
    if $is_caught ;
    then
        exit 0
    else
        exit 1
    fi
}
# this might get overwritten below if we are testing SIGTERM!
trap term_handler SIGTERM; 

handler () {
    is_caught=true
    # overwrite SIGTERM handler in case we are testing SIGTERM
    if [ "$signal" == "15" ]; then
        trap term_handler SIGTERM; 
    fi
    echo "signal received"
}
trap handler $signal


echo "signal handler ready"

if [ "$signal" == "17" ]; then
    # force a process to run to test and trigger SIGCHLD
    # bash (or linux?) doesn't let us send this from the outside
    sleep 0
fi

# need something to wait on
sleep 1 &
for (( ; ; ))
do
    wait
done