# Write the PullRequest ($CHANGE_TITLE) name into a text file
# python writeToFile.py --dirname PR$CHANGE_ID --prnumber $CHANGE_ID --prtitle "$CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"

# File structure
# PR$CHANGE_ID : $CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)
# PR$CHANGE_IDconfig1 : $CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)
# Ex : PR3 : Testing multiconfig (from user_name, https.....)
#      PR3config1 : Testing multiconfig (from user_name, https.....)

import os
import sys

def writeIntoFile(prnumber, prtitle):
    with open('validation_webpages.txt', 'w') as f:
        prnb  = "PR" + prnumber
        title = prnb + " : " + prtitle + "\n"
        title_config1 = prnb + "config1" + " : Config1"
        f.write(title + title_config1) 

def main(dirname, prnumber, prtitle):
    print('dirname = ', dirname)
    print('prtitle = ', prtitle)
    print('prnumber= ', prnumber)
    os.chdir(dirname)
    writeIntoFile(prnumber, prtitle)


if __name__== "__main__":
    import optparse
    import importlib
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('--dirname', dest='dirname', help=' ', default='')
    parser.add_option('--prnumber', dest='prnumber', help=' ', default='')
    parser.add_option('--prtitle', dest='prtitle', help=' ', default='', type="string")
    (opt, args) = parser.parse_args()

    main(opt.dirname, opt.prnumber, opt.prtitle)
