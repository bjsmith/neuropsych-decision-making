import numpy
import random
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 23:34:55 2014

@author: ben
"""

decks=["A","B","C","D"]
deck_dist_sgt={"A":[1,1,1,1,-5.25],
"B":[0.5,0.5,0.5,0.5,-3.25],
"C":[-1,-1,-1,-1,5.25],
"D":[-0.5,-0.5,-0.5,-0.5,3.25]}

deck_dist_igt={
"A":[1,1,-0.5,1,-2,1,-1,1,-1.5,-2.5],
"B":[1,1,1,1,1,1,1,1,1-12.50,1],
"C":[.5,.5,0,.5,.5-.75,.5,.5-.25,.5,.5-.5,.5-.5],
"D":[.5,.5,.5,.5,.5,.5,.5,.5,.5-2.5,.5]}

verbosity=0
#least verbose

value_in_hand=0

vmPFC_intact=True

random_noise_multiplier=1
#initialize memory stripes for task.
dlPFC_working_memory_last_card=""
dlPFC_working_memory_last_card_val=0

pvlv_val=[0,0,0,0]
pvlv_weight=0.1

deck_to_use=deck_dist_igt


def execute_block():
    global vmPFC_intact
    block_deck_tally=[0,0,0,0]
    
    for r in range(0,20/trial_num):
        if verbosity>1: print "Running round " + str(r) + " of " + str(20/trial_num)
        round_deck_tally = execute_round()
        for i, dt in enumerate(round_deck_tally):
            block_deck_tally[i]=block_deck_tally[i]+dt
        #print value_in_hand
    #print "deck learned weights:"
    #print pvlv_val
    if verbosity>1: print vmPFC_intact
    return block_deck_tally
        
def execute_round():
    #print "beginning round"
    global value_in_hand, dlPFC_working_memory_last_card, dlPFC_working_memory_last_card_val,deck_to_use
    #working memory tends to fade after each round.
    trial_num=len(deck_to_use["A"])
    round_deck_order=range(0,trial_num)
    random.shuffle(round_deck_order)
    round_deck_tally=[0,0,0,0]
    
    for t in round_deck_order:
        if verbosity>2:print "Running trial " + str(t+1) + " of " + str(trial_num)
        chosen_deck=choose_deck()
        if verbosity>2:print "Chosen Deck " + decks[chosen_deck]
        #we've chosen a deck, now we find out what we get for it for this trial
        val=deck_to_use[decks[chosen_deck]][t]
        if verbosity>2:print "You won $" + str(val)
        #print t
        #print "options: " + str([key + ": "  + str(value[t]) for key,value in deck_to_use.iteritems()])
        #print "chosen deck " + decks[chosen_deck] + "; value earned was " + str(val)
        #deck and associated value is recorded in working memory
        dlPFC_working_memory_last_card=chosen_deck
        dlPFC_working_memory_last_card_val=val
        
        #print val
        #value is awarded to value in hand
        value_in_hand=value_in_hand+val
        #record deck chosen at this point in time
        pvlv_learn(chosen_deck,val)
        
        round_deck_tally[chosen_deck]=round_deck_tally[chosen_deck]+1
    
    #print value_in_hand
    return round_deck_tally

def pvlv_learn(chosen_deck,val):
    global pvlv_val
    #adjust weights for the PVLV system.
    discrepancy=val-pvlv_val[chosen_deck]
    pvlv_val[chosen_deck]=pvlv_weight*discrepancy
    #print pvlv_val[chosen_deck]

def reset_pvlv():
    global pvlv_val
    if verbosity>0:print "Reset PVLVs"
    pvlv_val=[0,0,0,0]
    
def reset_working_memory():
    global dlPFC_working_memory_last_card,dlPFC_working_memory_last_card_val
    dlPFC_working_memory_last_card=""
    dlPFC_working_memory_last_card_val=0
    if verbosity>0:print "Reset working memory"

    
def pick_card_from_chosen_deck(deck):
    if all(deck_chosen):
        return None#all the cards from this deck have been chosen!
def reflective_u(prev_val):
    return prev_val
def impulsive_u(prev_val):
    return(prev_val)
    
def get_pvlv_signal(deck):
    global pvlv_val
    return pvlv_val[deck]
def choose_deck():
    #loop through the decks 10 times then choose one with the most positive affect
    accumulator=[0,0,0,0]
    
    for n in range(0,1):#cycles
        for d in range(0,len(decks)):
            #affect arising from working memory
            if (vmPFC_intact):
                if dlPFC_working_memory_last_card==d:#if this is the last deck we picked
                    #and if was good rather than bad!
                    accumulator[d]=(
                        accumulator[d]+
                        reflective_u(dlPFC_working_memory_last_card_val)
                        )
            #otherwise...what is the PVLV system telling us about this deck?
            accumulator[d]=(accumulator[d]+
                        get_pvlv_signal(d)
                        )
            
            #random noise
            accumulator[d]=accumulator[d]+numpy.random.uniform(low=-1, high=1,size=1)*random_noise_multiplier
    #print(accumulator)
    #having accumulated, we now return our decision
    if verbosity>3:
        print("PVLV: " + str(pvlv_val))
        print "This round's accumulation: " + str([ str([idx,n])  for idx,n in enumerate(accumulator)])
    return [idx for idx,n in enumerate(accumulator) if n==max(accumulator)][0]

def reset_sim():
    global value_in_hand, vmPFC_intact,dlPFC_working_memory_last_card,dlPFC_working_memory_last_card_val,verbosity, pvlv_val
        #initialize memory stripes for task.
    dlPFC_working_memory_last_card=""
    dlPFC_working_memory_last_card_val=0

    #reset PVLV as well...should start from the beginning in each block set.
    reset_pvlv()

def run_block_set(use_intact_vmPFC=True):
    global value_in_hand, vmPFC_intact,dlPFC_working_memory_last_card,dlPFC_working_memory_last_card_val,verbosity, pvlv_val
    value_in_hand=0

    vmPFC_intact=use_intact_vmPFC
    reset_sim()    

    if (verbosity>0):
        print("Deck Set in Use:")
        print '\n'.join([key + ": " + str(value) for key, value in deck_to_use.iteritems()])
        print "deck expected values:"
        print [d + ": " + str(numpy.mean(deck_to_use[d])) for d in decks]
        print ("vmPFC status: " + ("intact" if vmPFC_intact else "lesioned"))
        
    
    for b in range(0,6):
        if (verbosity>0): print ("Block " + str(b+1))
        bdt=execute_block()
        if (verbosity>0): print "Block (times deck chosen):" + str(bdt)
    if (verbosity>0): print "Subject finished with $" + str(value_in_hand)
    return value_in_hand



