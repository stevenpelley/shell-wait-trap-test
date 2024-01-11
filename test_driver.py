import subprocess
import signal
import sys
import threading
import time


class FailedTestException(Exception):
    def __init__(self, message):
        super().__init__(message)


def assert_test(condition, message):
    if not condition:
        raise FailedTestException(message)

        
def get_test_configs(command_args, sig_set):
    for sig in sig_set:
        yield (command_args, sig)

        
def test_signal(command_args, sig):
    args = command_args + ["{}".format(sig)]
    with subprocess.Popen(
        args,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
        ) as p:
        
        def timeout_thread_target():
            time.sleep(0.5)
            p.terminate()
            time.sleep(0.2)
            p.kill()
            # resume so that it receives the kill
            if sig == signal.SIGSTOP:
                p.send_signal(signal.SIGCONT)


        ex = None
        try:
            t = threading.Thread(target=timeout_thread_target)
            t.daemon = True # thread dies with the program
            t.start()

            line = p.stdout.readline()
            assert_test(line == b"signal handler ready\n", 
                        "expected \"signal handler ready\\n\".  Found: {}".format(line))
            # bash (or linux?) will not let us signal SIGCHLD when not a child.
            # we test trapping sigchld by running a quick process after setting up the handler
            if sig != signal.SIGCHLD:
                p.send_signal(sig)
            line = p.stdout.readline()
            assert_test(line == b"signal received\n", 
                        "expected \"signal received\\n\".  Found: {}".format(line))
        except FailedTestException as e:
            ex = e
        p.terminate()
        retcode = p.wait()
        if retcode == 0 and ex is None:
            sys.stdout.write("{}: success\n".format(sig))
        else:
            sys.stdout.write("{}: fail. return code: {}. exception: {}\n".format(sig, retcode, ex))


def main():
    command_args = {
        "bash": ["bash", "test_bash.sh"],
        "zsh": ["zsh", "test_bash.sh"],
        "fish": ["fish", "test_fish.fish"],
    }.get(sys.argv[1])
    if command_args is None:
        sys.stderr.write("expecting 'bash' or 'fish'.  Found: {}".format(sys.argv[1]))
        sys.exit(1)
    for tup in get_test_configs(command_args, signal.valid_signals()):
        test_signal(*tup)
        

if __name__ == "__main__":
    main()