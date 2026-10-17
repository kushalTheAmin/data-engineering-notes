# checks for notes/049-the-terminal.md
import shlex
import subprocess

assert "echo masala chai".split() == ["echo", "masala", "chai"]
assert shlex.split('echo "masala chai"') == ["echo", "masala chai"]
# a real shell agrees: unquoted gives two arguments, quoted gives one
two = subprocess.run(["bash", "-c", 'printf "%s\\n" masala chai'], capture_output=True, text=True).stdout.split("\n")[:-1]
one = subprocess.run(["bash", "-c", 'printf "%s\\n" "masala chai"'], capture_output=True, text=True).stdout.split("\n")[:-1]
assert two == ["masala", "chai"] and one == ["masala chai"]
# echo prints its arguments back
assert subprocess.run(["bash", "-c", "echo dhokla khandvi"], capture_output=True, text=True).stdout == "dhokla khandvi\n"
# bash has echo built in, so the first word is not always a file on disk
assert subprocess.run(["bash", "-c", "type echo"], capture_output=True, text=True).stdout.startswith("echo is a shell builtin")
# source: https://docs.python.org/3/library/shlex.html
#   confirmed: shlex.split "Split the string s using shell-like syntax"
# source: https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html
#   confirmed: echo is listed as a bash builtin, "Output the args, separated by spaces"
print("049 ok")
