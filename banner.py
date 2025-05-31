'''
MAJOR PROJECT
'''

import sys
sys.dont_write_bytecode = True

class Banner(object):
    def LoadWebSpyBanner(self):
        try:
            from termcolor import cprint, colored
            banner = '''

__        __   _    ____
\ \      / /__| |__/ ___| _ __  _   _
 \ \ /\ / / _ \ '_ \___ \| '_ \| | | |
  \ V  V /  __/ |_) |__) | |_) | |_| |
   \_/\_/ \___|_.__/____/| .__/ \__, |
                         |_|    |___/
                                        By Req999
              '''

            cprint(banner, 'magenta', attrs=['bold'])

        except ImportError as ie:
            print(banner)
