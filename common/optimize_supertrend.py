from common.backtestingsuper import *
a=test()
open('optimized_supertrend_for_nifty.txt','w').write(f'{a[0]}\n{a[1]}')