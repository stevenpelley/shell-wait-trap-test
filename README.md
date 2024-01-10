# shell-wait-trap-test
demonstration and test bash and fish trap and wait.  I believe fish is broken and I want to compare it to bash and also provide an eventual regression test for fish

This repository may be opened and run within a devcontainer.  See .devcontainer for configuration

run test via `python3 test_driver.py`

currently runs a bash test showing that signals 9 (kill) and 19 (stop) fail.  These signals cannot be caught so this is a correct result.