# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 12:27:38 2014

@author: ben
"""

def run_demo_with_bootstrapped_and_exemplar(vmPFC_intact,player_to_use=None):
    global verbosity
    #now run a single trial of IGT to see what it's like.
    print "Running set of 6 IGT Blocks"
    verbosity=5
    sup=GT_supervisor()
    #trial_num=len(deck_to_use["A"])
    if player_to_use==None:
        player=GT_player()
    else:
        player=player_to_use
    player.vmPFC_intact=vmPFC_intact
    sup.run_block_set(sup.deck_dist_igt,player_to_use=player)
    
    #and now run a single trial of SGT
    print "Running set of 6 SGT Blocks"
    verbosity=2
    #deck_to_use=deck_dist_sgt
    #trial_num=len(deck_to_use["A"])
    sup.run_block_set(sup.deck_dist_sgt,player_to_use=player)
    
    
    verbosity=0
    #Run 100 whole blocks of IGT trials
    #deck_to_use=deck_dist_igt
    #trial_num=len(deck_to_use["A"])
    iterations=500
    print "Running "+ str(iterations) + " iterations of 6 IGT Blocks"
    rt_val=0
    for bs in range(0,iterations):
        val=sup.run_block_set(sup.deck_dist_igt,player_to_use=player)
        rt_val=rt_val+val['value']
    print "mean val = " +str(rt_val/iterations)
    
    iterations=500
    print "Running "+ str(iterations) + " iterations of 6 SGT Blocks"
    rt_val=0
    for bs in range(0,iterations):
        val=sup.run_block_set(sup.deck_dist_sgt,player_to_use=player)
        rt_val=rt_val+val['value']
    print "mean val = " +str(rt_val/iterations)

#pvlv_weight=0.05
#random_noise_multiplier=0.5
print ("Running demo with vmPFC intact.")
run_demo_with_bootstrapped_and_exemplar(True)
print ("Running demo with vmPFC lesioned.")
run_demo_with_bootstrapped_and_exemplar(False)