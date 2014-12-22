# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 12:27:38 2014

@author: ben
"""




#now run a single trial of IGT to see what it's like.
print "Running set of 6 IGT Blocks"
verbosity=2
deck_to_use=deck_dist_igt
trial_num=len(deck_to_use["A"])
run_block_set(True)

#and now run a single trial of SGT
print "Running set of 6 SGT Blocks"
verbosity=2
deck_to_use=deck_dist_sgt
trial_num=len(deck_to_use["A"])
run_block_set(True)


verbosity=0
#Run 100 whole blocks of IGT trials
deck_to_use=deck_dist_igt
trial_num=len(deck_to_use["A"])
iterations=400
print "Running "+ str(iterations) + " iterations of 6 IGT Blocks"
rt_val=0
for bs in range(0,iterations):
    val=run_block_set(True)
    rt_val=rt_val+val
print "mean val = " +str(rt_val/iterations)

#Run 100 whole blocks of SGT trials
deck_to_use=deck_dist_sgt
trial_num=len(deck_to_use["A"])
iterations=400
print "Running "+ str(iterations) + " iterations of 6 SGT Blocks"
rt_val=0
for bs in range(0,iterations):
    val=run_block_set(True)
    rt_val=rt_val+val
print "mean val = " +str(rt_val/iterations)


# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 12:27:38 2014

@author: ben
"""


###########################################################################3

#now run a single trial of IGT to see what it's like.
print "Running set of 6 IGT Blocks"
verbosity=2
deck_to_use=deck_dist_igt
trial_num=len(deck_to_use["A"])
run_block_set(False)

#and now run a single trial of SGT
print "Running set of 6 SGT Blocks"
verbosity=2
deck_to_use=deck_dist_sgt
trial_num=len(deck_to_use["A"])
run_block_set(False)


verbosity=0
#Run 100 whole blocks of IGT trials
deck_to_use=deck_dist_igt
trial_num=len(deck_to_use["A"])
iterations=400
print "Running "+ str(iterations) + " iterations of 6 IGT Blocks"
rt_val=0
for bs in range(0,iterations):
    val=run_block_set(False)
    rt_val=rt_val+val
print "mean val = " +str(rt_val/iterations)

#Run 100 whole blocks of SGT trials
deck_to_use=deck_dist_sgt
trial_num=len(deck_to_use["A"])
iterations=400
print "Running "+ str(iterations) + " iterations of 6 SGT Blocks"
rt_val=0
for bs in range(0,iterations):
    val=run_block_set(False)
    rt_val=rt_val+val
print "mean val = " +str(rt_val/iterations)

