# shell-wait-trap-test
demonstration and test bash and fish trap and wait.  I believe fish is broken and I want to compare it to bash and also provide an eventual regression test for fish

This repository may be opened and run within a devcontainer.  See .devcontainer for configuration

run test via `python3 test_driver.py [bash | fish]`.  The output will display one signal per line by signal number and a either a success or error message.  The printed result is intended to be used to diff bash against fish and each against some stored reference output as a regression test.

currently runs a bash test showing that signals 9 (kill) and 19 (stop) fail.  These signals cannot be caught so this is a correct result.

TODO: consider testing interactive mode and non, as well as with job control enabled and disabled.  These properties of a shell change signal handling, although there's no indication that they should impact trap behavior.



Notes: