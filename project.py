import numpy
import random
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 23:34:55 2014
Copyright (C) 2014 Ben J. Smith
This file and the related project is distributed under the terms of the GNU General Public License v3.0 available in the accompanying license file.
By using this work your agree to the terms of the license.
@author: ben
"""
verbosity=0

def printv(v,str_to_print):
    verbosity=0
    if verbosity>v:
        print str_to_print
#least verbose

class GT_player(object):
    
    
    #constants
    PVLV_MODE_PROSPECT=1
    PVLV_MODE_EXPECTANCY=0
    
    #sim parameters
    vmPFC_intact=True
    working_memory_confidence=1
    random_noise_multiplier=0.5
    habit_strength=0.5
    pvlv_weight=0.2
    pvlv_mode=PVLV_MODE_EXPECTANCY
    
        
    #state variables
    game_in_play=False
    
    dlPFC_working_memory_last_card=""
    dlPFC_working_memory_last_card_val=0
    
    #http://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide#Handling-assignment
    pvlv_val=None
    #decks=None
    
    verbosity=0
    
    def __init__(self):
        #global verbosity
        #self.pvlv_val=[0,0,0,0]
        if self.verbosity>1: print "Initializing new player."
        
    def start_game(self,decks):
        self.game_in_play=True
        self.pvlv_val=[0]*len(decks)
        self.reset_state()
        #self.decks=decks
        
    def get_parameter_dictionary(self):
        params={}
        params['vmPFC_intact']=self.vmPFC_intact
        params['working_memory_confidence']=self.working_memory_confidence
        params['random_noise_multiplier']=self.random_noise_multiplier
        params['habit_strength']=self.habit_strength
        params['pvlv_weight']=self.pvlv_weight
        params['pvlv_mode']=self.pvlv_mode
        return params
        
    #should actually implement params as dictionary
    #instead of this pseudo-dictionary
    #but we'll see
    def set_parameter_by_key(self,key,value):
        if 'vmPFC_intact' ==key:
            self.vmPFC_intact=value
        if 'working_memory_confidence'==key:
            self.working_memory_confidence=value
        if 'random_noise_multiplier'==key:
            self.random_noise_multiplier=value
        if 'habit_strength'==key:
            self.habit_strength=value
        if 'pvlv_weight'==key:
            self.pvlv_weight=value
        if 'pvlv_mode'==key:
            self.pvlv_mode=value
    
    def pvlv_learn(self,chosen_deck,val):
        #global verbosity
        if self.verbosity>5:print("learning; PVLV learning mode is " + self.pvlv_mode)
        #adjust weights for the PVLV system.
        discrepancy=val-self.pvlv_val[chosen_deck]
        if self.pvlv_mode==self.PVLV_MODE_EXPECTANCY:
            self.pvlv_val[chosen_deck]=self.pvlv_val[chosen_deck]+self.pvlv_weight*discrepancy
            if self.verbosity>5:
                print("setting learning with weight*discrepancy of " + str(self.pvlv_weight*discrepancy))
                print chosen_deck
                print self.pvlv_val
        elif self.pvlv_mode==self.PVLV_MODE_PROSPECT:
            printv(5,"using prospect: " + str(discrepancy))
            self.pvlv_val[chosen_deck]=self.pvlv_val[chosen_deck]+self.pvlv_weight*pow(abs(discrepancy),0.5)*sign(discrepancy)
    
    def reset_state(self):
        #return all state variables to their initialized states.
        self.reset_working_memory()
    
        #reset PVLV as well...should start from the beginning in each block set.
        self.reset_pvlv()
        
    def reset_pvlv(self):
        #global verbosity
        #global pvlv_val
        if self.verbosity>0:print "Reset PVLVs"
        self.pvlv_val=[0]*len(self.pvlv_val)
        
    def reset_working_memory(self):
        #global verbosity
        self.dlPFC_working_memory_last_card=""
        self.dlPFC_working_memory_last_card_val=0
        if self.verbosity>0:print "Reset working memory"
    
        
    def reflective_u(self,prev_val):
        return self.working_memory_confidence*prev_val
    def impulsive_u(self,prev_val):
        return(prev_val)
        
    def get_pvlv_signal(self,deck):
        return self.pvlv_val[deck]
        
    def choose_deck(self,decks):
        #global verbosity
        #decks=self.decks
        #loop through the decks 10 times then choose one with the most positive affect
        #assumes decks are always presented in the same order.
        if ((len(decks)==4)==False):
            raise Exception ("This player can only play a game with exactly 4 decks.")
        if (self.game_in_play==False):
            raise Exception("Can't choose deck; haven't started playing yet!")
            
        accumulator=[0,0,0,0]
        wm_vals=[0,0,0,0]    
        acc_rand_noise=None
        deck_count=len(decks)
        for n in range(0,1):#cycles #this is obsole
            #accumulator random noise; calculate all deck_count at once
            acc_rand_noise=numpy.random.normal(0,0.5,deck_count)*self.random_noise_multiplier
            #and add the random noise to the accumulator
            accumulator+=acc_rand_noise
            
            for d in range(0,deck_count):#for each deck.
                #affect arising from working memory
                if (self.vmPFC_intact):
                    if self.dlPFC_working_memory_last_card==d:#if this is the last deck we picked
                        #and if was good rather than bad!
                        wm_val=self.reflective_u(self.dlPFC_working_memory_last_card_val)
                        wm_vals[d]=wm_vals[d]+wm_val

                        accumulator[d]+=wm_val
                        
                #otherwise...what is the PVLV system telling us about this deck?
                accumulator[d]+=(accumulator[d]+
                            self.get_pvlv_signal(d)*self.habit_strength
                            )
                            
                #accumulator random noise
                #acc_rand_noise[d]=numpy.random.normal(0,0.5)*self.random_noise_multiplier
              
                #add random noise
                #accumulator[d]=accumulator[d]+acc_rand_noise[d]
        #print(accumulator)
        #having accumulated, we now return our decision
    
        
        if self.verbosity>3:
            #this summary is incompatible with having more htan one cycle above since some value are only stored for the last cycle.
            print("Deck:\t" + '\t'.join(decks))
            print("PVLV:\t" + '\t'.join([str(round(v,3)) for v in self.pvlv_val]))
            print("WM:\t" + '\t'.join([str(round(x,3)) for x in wm_vals]))
            print("aRAND:\t" + '\t'.join([str(round(x,3)) for x in acc_rand_noise]))
            print "Total:\t" + '\t'.join([str(round(n,3)) for idx,n in enumerate(accumulator)])
        
        #http://stackoverflow.com/questions/3989016/how-to-find-positions-of-the-list-maximum
        #return [idx for idx,n in enumerate(accumulator) if n==max(accumulator)][0]
        #return accumulator.index(max(accumulator))
        return numpy.argmax(accumulator)
    
    #subject observes choice result and learns from it.
    def observe_choice_result(self,net_gain,chosen_deck):
        self.dlPFC_working_memory_last_card=chosen_deck
        self.dlPFC_working_memory_last_card_val=net_gain
            
        self.pvlv_learn(chosen_deck,net_gain)


        
class GT_supervisor(object):
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
    deck_set_current=deck_dist_igt
    
    value_in_hand=0
    
    player=None
    
    verbosity=0
    
    def __init__(self):
        
        print "Initializing new game supervisor."
        print "current verbosity:" + str(self.verbosity)
    
    # http://stackoverflow.com/q/3844931/
    def check_equal(self,lst):
        return not lst or [lst[0]]*len(lst) == lst
    
    def get_trial_num(self):
        #get the number of cards in each deck in the current set.
        #deck_lengths = [len(value) for key,value in self.deck_set_current.iteritems() ]
        deck_lengths = [len(value) for value in self.deck_set_current.itervalues() ]
        #if len(set(deck_lengths))>1:#deck lengths are different
        if self.check_equal(deck_lengths)==False:
            raise Exception("One deck has more cards than other decks. This is against the rules.")
        #OK, the lengths of all decks are equal. Number of trials is == to number of cards in each deck so...
        return deck_lengths[0]
        
    def run_block_set(self,deck_set_to_use=None,player_to_use=None):
        #global verbosity
        #global value_in_hand, vmPFC_intact,dlPFC_working_memory_last_card,dlPFC_working_memory_last_card_val,verbosity, pvlv_val,deck_set_current,trial_num
        
        self.deck_set_current=deck_set_to_use
        #trial_num=self.get_trial_num()
        self.value_in_hand=0
    
        #vmPFC_intact=use_intact_vmPFC
        if player_to_use==None:
            self.player=GT_player()#start with a new player to play with us.
        else:
            self.player=player_to_use
        
        self.player.start_game(self.decks)
    
        if (self.verbosity>0):
            print("Deck Set in Use:")
            print '\n'.join([key + ": " + str(value) for key, value in self.deck_set_current.iteritems()])
            print "deck expected values:"
            print [d + ": " + str(numpy.mean(self.deck_set_current[d])) for d in self.decks]
            print ("vmPFC status: " + ("intact" if player_to_use.vmPFC_intact else "lesioned"))
            
        deck_choice_by_block=[]
        for b in range(0,6):
            if (self.verbosity>0): print ("Block " + str(b+1))
            bdt=self.execute_block()
            deck_choice_by_block.append(bdt)
            if (self.verbosity>0): print "Block (times deck chosen):" + str(bdt)
        if (self.verbosity>0): print "Subject finished with $" + str(self.value_in_hand)
            
        results={}
        results["value"]=self.value_in_hand
        results["deck_choice"]=deck_choice_by_block
        
        return results

    
    def execute_block(self):
        #global verbosity
        block_deck_tally=[0,0,0,0]
        
        
        round_num=20/self.get_trial_num()
        for r in range(0,round_num):
            if self.verbosity>1: print "Running round " + str(r) + " of " + str(round_num)
            round_deck_tally = self.execute_round()
            for i, dt in enumerate(round_deck_tally):
                block_deck_tally[i]=block_deck_tally[i]+dt
            #print value_in_hand
        #print "deck learned weights:"
        #print pvlv_val
        return block_deck_tally
            
    def execute_round(self):
        #global verbosity
        #print "beginning round"
        #global value_in_hand, dlPFC_working_memory_last_card, dlPFC_working_memory_last_card_val,deck_set_current
        #working memory tends to fade after each round.
        trial_num=self.get_trial_num()
        round_deck_order=range(0,trial_num)
        random.shuffle(round_deck_order)
        round_deck_tally=[0,0,0,0]
        
        for t in round_deck_order:
            if self.verbosity>2:print "Running trial " + str(t+1) + " of " + str(trial_num)
            chosen_deck=self.player.choose_deck(self.decks)
            if self.verbosity>2:print "Chosen Deck " + self.decks[chosen_deck]
            #player has chosen a deck, now we find out what we get for it for this trial
            val=self.deck_set_current[self.decks[chosen_deck]][t]
            
            #show the player what they got, so they can learn from it.
            self.player.observe_choice_result(val,chosen_deck)

            #value is awarded to value in hand
            self.value_in_hand+=val
            if self.verbosity>2:print "You won $" + str(val) + " (total: " + str(self.value_in_hand) +")"
            #record deck chosen at this point in time
            
            round_deck_tally[chosen_deck]+=1
        
        #print value_in_hand
        return round_deck_tally

    def reset_sim(self):
            #initialize memory stripes for task.
        self.player.reset_state()
        
        
