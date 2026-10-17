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
print("049 ok")
