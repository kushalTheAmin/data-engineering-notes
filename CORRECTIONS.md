# corrections

every fix made to a note after it was published, newest first. if you learned from an older version of a note, this is what changed and why.

- 005, 2026-10-16: the checks file compared the binary column of the table with itself, so it proved nothing. it now compares against the written out patterns, the note text is unchanged. evidence: python, checks/005.py
- 004, 2026-10-16: said colors on screen stop at 255. deep color displays use 10 or more bits per channel, so it now says usually. evidence: https://en.wikipedia.org/wiki/Color_depth
- 001, 2026-10-15: said phones, macs and most web servers all count time from the start of 1970. the iphone API defaults to 2001, so it now says linux, macs and javascript. evidence: https://en.wikipedia.org/wiki/Unix_time
- 005, 2026-10-15: said sixteen is two doubled four times, which is really 32. it now says 2 times 2 times 2 times 2. the hex loop now uses the same place value shape as 003, and git is glossed. evidence: python, 2 * 2 ** 4 == 32
- 004, 2026-10-15: said 003 showed that 8 bits count from 0 to 255, which 003 never says; the ip address claim now covers only the dotted IPv4 kind; kaju katli is glossed; quiz 2 now names the real trap, storing 1000 as text takes 4 bytes. evidence: the text of 003, https://www.computerhope.com/jargon/d/dotted-quad-notation.htm

## audit log
audit runs that could not finish, newest first. format: YYYY-MM-DD HH:MM: what happened
