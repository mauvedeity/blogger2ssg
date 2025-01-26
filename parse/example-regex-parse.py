# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"<.*"

test_str = ("  <table align=\"center\" cellpadding=\"0\" cellspacing=\"0\" class=\"tr-caption-container\" style=\"margin-left: auto; margin-right: auto;\">\n"
	"    <tbody>\n"
	"      <tr>\n"
	"        <td style=\"text-align: center;\">\n"
	"          <a href=\"./images/opening-screen.png\" style=\"margin-left: auto; margin-right: auto;\">\n"
	"            <img border=\"0\" src=\"./images/opening-screen.png\" width=\"320\">\n"
	"          </a>\n"
	"        </td>\n"
	"      </tr>\n"
	"      <tr>\n"
	"        <td class=\"tr-caption\" style=\"text-align: center;\">Opening game screen featuring title and first choice point</td> <!-- duplicate as alt text -->\n"
	"      </tr>\n"
	"    </tbody>\n"
	"  </table>")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
