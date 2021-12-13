# Write the PulRequest ($CHANGE_TITLE) name into a text file
# python writeToFile.py --dirname PR$CHANGE_ID --prnumber $CHANGE_ID --prtitle "$CHANGE_TITLE"

import os
import sys

def writeIntoFile(prnumber, prtitle):
    with open('validation_webpages.txt', 'w') as f:
        f.write(prtitle)
    
def main(dirname, prnumber, prtitle):
    print('dirname = ', dirname)
    print('prtitle = ', prtitle)
    print('prnumber= ', prnumber)
    os.mkdir(dirname)
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