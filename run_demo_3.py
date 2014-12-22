
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 12:27:38 2014

@author: ben
"""

def run_demo_with_bootstrapped_and_exemplar(vmPFC_intact):
    global verbosity
    
    supervisor=GT_supervisor()
    #now run a single trial of IGT to see what it's like.
    print "Running set of 6 IGT Blocks"
    verbosity=4
    #trial_num=len(deck_to_use["A"])
    res= supervisor.run_block_set(vmPFC_intact,supervisor.deck_dist_igt)
    print res 
    
    #and now run a single trial of SGT
    print "Running set of 6 SGT Blocks"
    verbosity=2
    #deck_to_use=deck_dist_sgt
    #trial_num=len(deck_to_use["A"])
    res = supervisor.run_block_set(vmPFC_intact,supervisor.deck_dist_sgt)
    print res
    
    
    verbosity=0
    #Run 100 whole blocks of IGT trials
    run_demo_bootstrap(supervisor.deck_dist_igt,"IGT")
    
    #Run 100 whole blocks of SGT trials
    run_demo_bootstrap(supervisor.deck_dist_sgt,"SGT")

def run_demo_bootstrap(deck_set,deck_set_name,vmPFC_intact=True):
    iterations=100
    print "Running "+ str(iterations) + " iterations of 6 " + deck_set_name + " Blocks"
    rt_val=0
    for bs in range(0,iterations):
        val=supervisor.run_block_set(vmPFC_intact,deck_set)
        rt_val=rt_val+val
    print "mean val = " +str(rt_val/iterations)
    

print ("Running demo with vmPFC intact.")
run_demo_with_bootstrapped_and_exemplar(True)
#print "with lesion"
#run_demo_with_bootstrapped_and_exemplar(False)