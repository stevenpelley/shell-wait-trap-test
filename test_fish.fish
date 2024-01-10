set signal $argv[1]
set is_caught false

function term_handler --on-signal SIGTERM
    # make sure we do not terminate when testing SIGTERM until we observe that
    # signal.
    if [ $signal != "15" ]; or $is_caught
        kill %1 &> /dev/null
        if $is_caught
            exit 0
        else;
            exit 1
        end
    end
end

function handler --on-signal SIGINT
    set -g is_caught true
    echo "signal received"
end

echo "signal handler ready"

if [ $signal = "17" ]
    # force a process to run to test and trigger SIGCHLD
    # bash (or linux?) doesn't let us send this from the outside
    sleep 0
end

# need something to wait on
sleep 1 &
while true
    wait
end