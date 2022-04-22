# Write the PullRequest number (PR$CHANGE_ID), the title ($CHANGE_TITLE) and the name of the PR author ($CHANGE_AUTHOR) 
# into a text file, validation_webpages.txt, in the directory with histograms 
# python writeToFile.py --dirname $data_dir/PR$CHANGE_ID --prnumber $CHANGE_ID --prtitle "PR$CHANGE_ID : $CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"

import os
import sys

def writeIntoFile(prnumber, prtitle):
    with open('validation_webpages.txt', 'w') as f:
        f.write(prtitle)
    
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
