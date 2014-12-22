  # -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 11:52:10 2014
Copyright (C) 2014 Ben J. Smith
This file and the related project is distributed under the terms of the GNU General Public License v3.0 available in the accompanying license file.
By using this work your agree to the terms of the license.

@author: ben
"""
import numpy
import scipy as sp
from scipy import stats
import random
from project import GT_supervisor
from project import GT_player


verbosity=1

class GT_manager(object):
    supervisor=None
    #constants used in several functions in this class.
    vmPFC_range={'vmPFC_intact':True,'vmPFC_lesioned':False}
    def __init__(self):
        self.verbosity=1
        if verbosity>1: print "Initializing new player."
        
    def get_deck_set_range(self):
        return {'igt':self.supervisor.deck_dist_igt,'sgt':self.supervisor.deck_dist_sgt}
        
    def run_bootstrap_get_match_score(self,test_player, iterations=100):
        vmPFC_range=self.vmPFC_range
        deck_set_range=self.get_deck_set_range()
        bs_aggregate_result=self.run_bootstrap(test_player,iterations)
        
                #if self.verbosity>1:print "mean val = " +str(numpy.mean(rt_val)):
        targets={}
        for vmPFC_name,vmPFC_status in vmPFC_range.iteritems():
            targets[vmPFC_name]={}
            for deck_set_name in deck_set_range.iterkeys():#.iteritems():
                targets[vmPFC_name][deck_set_name]={}
        #target 1: deck choices in Round 6:
        targets['vmPFC_intact']['igt']['deck_choice_round_6']=[p*20 for p in [0.1,0.18,0.44,0.28]]
        targets['vmPFC_intact']['sgt']['deck_choice_round_6']=[p*20 for p in [0.33,0.24,0.15,0.28]]
        targets['vmPFC_lesioned']['igt']['deck_choice_round_6']=[p*20 for p in [0.33,0.24,0.15,0.28]]
        targets['vmPFC_lesioned']['sgt']['deck_choice_round_6']=[p*20 for p in [0.33,0.24,0.15,0.28]]
        
        targets['vmPFC_intact']['igt']['deck_choice_round_5']=[p*20 for p in [0.1,0.18,0.44,0.28]]
        targets['vmPFC_intact']['sgt']['deck_choice_round_5']=[p*20 for p in [0.30,0.27,0.15,0.28]]
        targets['vmPFC_lesioned']['igt']['deck_choice_round_5']=[p*20 for p in [0.33,0.24,0.15,0.28]]
        targets['vmPFC_lesioned']['sgt']['deck_choice_round_5']=[p*20 for p in [0.30,0.27,0.15,0.28]]
        #target 1: deck choices in Round 6:
        targets['vmPFC_intact']['igt']['deck_choice_round_1']=[p*20 for p in [0.25,0.25,0.25,0.25]]
        targets['vmPFC_intact']['sgt']['deck_choice_round_1']=[p*20 for p in [0.3,0.3,0.2,0.2]]
        targets['vmPFC_lesioned']['igt']['deck_choice_round_1']=[p*20 for p in [0.25,0.25,0.25,0.25]]
        targets['vmPFC_lesioned']['sgt']['deck_choice_round_1']=[p*20 for p in [0.3,0.3,0.2,0.2]]
        #targets['vmPFC_intact']['igt']['deck_choice_round_6']=[p*20 for p in [0,0,0.5,0.5]]
        #targets['vmPFC_intact']['sgt']['deck_choice_round_6']=[p*20 for p in [0.25,0.25,0.25,0.25]]
        #targets['vmPFC_lesioned']['igt']['deck_choice_round_6']=[p*20 for p in [0.25,0.25,0.25,0.25]]
        #targets['vmPFC_lesioned']['sgt']['deck_choice_round_6']=[p*20 for p in [0.25,0.25,0.25,0.25]]
        
        bs_target_match=targets

        
        #calculate the match to the target values.
        for vmPFC_status in vmPFC_range.iterkeys():                    
            for condition in deck_set_range.iterkeys():
                #iterate each deck in the last block
                for d in range(0,len(bs_aggregate_result[vmPFC_status][condition]['deck_choice'][6-1])):
                    bs_target_match[vmPFC_status][condition]['deck_choice_round_6'][d]=(
                    (
                    -pow(
                        (targets[vmPFC_status][condition]['deck_choice_round_6'][d]
                        -bs_aggregate_result[vmPFC_status][condition]['deck_choice'][6-1][d]
                        )
                        ,2)))
                    bs_target_match[vmPFC_status][condition]['deck_choice_round_5'][d]=(
                    (
                    -pow(
                        (targets[vmPFC_status][condition]['deck_choice_round_5'][d]
                        -bs_aggregate_result[vmPFC_status][condition]['deck_choice'][3-1][d]
                        )
                        ,2)))
                    bs_target_match[vmPFC_status][condition]['deck_choice_round_1'][d]=(
                    (
                    -pow(
                        (targets[vmPFC_status][condition]['deck_choice_round_1'][d]
                        -bs_aggregate_result[vmPFC_status][condition]['deck_choice'][3-1][d]
                        )
                        ,2)))
                
       
        #now combine the target values into a single value.
        #score = sum([sum(ss.values()) for ss in  bs_target_match.values()])
        score = sum([sum([sum(ss2.values()) for ss2 in ss1.values()]) for ss1 in  bs_target_match.values()])
        #print "stdev val = " +str(numpy.std(rt_val))
        return score
        
    def run_bootstrap_representative_sample(self,iterations=500):
        player=GT_player()
        self.supervisor=GT_supervisor()
        res = self.run_bootstrap(player,iterations=iterations)
        print res
        return res
        
    def print_res_rec(self,val):
        if type(val)==type({}):#we have a dictionary, decode to string or string array
            dicstr=[]
            for name, subvalue in val.iteritems():
                subval_as_str=self.print_res_rec(subvalue)
                if type(subval_as_str)==type(dicstr):
                    dicstr.append(name + ':\n' + '\t'.join(subval_as_str))
                else:
                    dicstr.append(name + ':\n\t' + subval_as_str)
            return "\n\t".join(dicstr)
        elif type(val)==type([]):
            if type([]) in set([type(li) for li in val]):#if this is a list of lists
                return "" + "\n".join([self.print_res_rec(li) for li in val]) + ""
            else:
                return "" + ",".join([self.print_res_rec(li) for li in val]) + ""
        elif type(val)==type(""):
            return val
        elif type(val)==type(0.0):
            return str(round(val,2))
        else:
            return (str(val))
            
        

    def run_bootstrap(self,test_player, iterations=100):
        if self.verbosity>1: print "Running "+ str(iterations) + " iterations of a block set"
        vmPFC_range=self.vmPFC_range
        deck_set_range=self.get_deck_set_range()
        rt_val=[]
        bs_res=[]
        for bs in range(0,iterations):
            res_set_2={}
            for vmPFC_stat_label, vmPFC_status in vmPFC_range.iteritems():
                res_set_1={}
                for deck_set_name, deck_set in deck_set_range.iteritems():
                    test_player.vmPFC_intact=vmPFC_status
                    res=self.supervisor.run_block_set(deck_set,player_to_use=test_player)
                    res_set_1[deck_set_name]=res
                res_set_2[vmPFC_stat_label]=(
                    res_set_1
                    )
            bs_res.append(res_set_2)


        #calculate mean result.
        #copy the first result as a template.
        bs_aggregate_result=bs_res[0]
        
        for vmPFC_status in vmPFC_range.iterkeys():
            for condition in deck_set_range.iterkeys():
                for block in range(0,len(bs_aggregate_result[vmPFC_status][condition]['deck_choice'])):
                    for deck in range(0,len(bs_aggregate_result[vmPFC_status][condition]['deck_choice'][block])):
                        #we've stored an aggregate value
                        bs_aggregate_result[vmPFC_status][condition]['deck_choice'][block][deck]=(
                            numpy.mean([test_iteration[vmPFC_status][condition]['deck_choice'][block][deck] for test_iteration in bs_res]))
                        #what about a comparing this aggregate with the target values?
        if self.verbosity>1:
            print bs_aggregate_result
            
        return bs_aggregate_result

        
    def set_new_player_parameters(self,p_working_memory_confidence,p_random_noise_multiplier,p_habit_strength,p_pvlv_weight,p_pvlv_mode):
        player = GT_player()
        player.working_memory_confidence=p_working_memory_confidence
        player.random_noise_multiplier=p_random_noise_multiplier
        player.habit_strength=p_habit_strength
        player.pvlv_weight=p_pvlv_weight
        player.pvlv_mode=p_pvlv_mode
        return player
    def optimize_parameters(self):
        #set parameters
        self.supervisor=GT_supervisor()
        player = GT_player()
        #set player parameters
        
        
        #bootstrap the bootstrap to test its standard deviation
        #so we can decide on how many iterations torun.
        #find out how many iterations we need to run to get an estimate that's stable
        
        #bootstrap_res=[]
        #for n in range(0,10):
        #    bootstrap_res.append(Param_Optimize.run_bootstrap(supervisor.deck_dist_igt,"IGT",True,100))
        #for the default parameters, it seems to be around about 70 needed to get SD~=1.
        #let's round up to 100.
        
        #test to see how good the player does.
        player_result=self.run_bootstrap_get_match_score(player,100)
        new_player_result=None
        new_player=None
        
        for n in range(0,500):
            if (self.verbosity>1):print("Trying new player " + str(n) + "...")
            player_params=player.get_parameter_dictionary()
            new_player = GT_player()
            #copy the parameters from the old player.
            [new_player.set_parameter_by_key(k,v) for k,v in player_params.iteritems()]

            #we don't want to 'optimize' vmPFC intact
            del player_params['vmPFC_intact']
            #decide on number of parameters to change.            
            #n_to_modify = int(ceil(randint(1,len(player_params)+1)/2))
            n_to_modify = randint(1,len(player_params)+1)
            if n_to_modify==0: raise Exception ("n to modify is 0, somehow. player params length was:" + str(len(player_params)))
            keys=[k for k in player_params.iterkeys()]
            
            #now randomize the order the keys come in
            random.shuffle(keys)
            
            #and adjust the first n keys
            keys_to_modify=keys[0:n_to_modify]
            if (self.verbosity>2):print "keys to modify: " + str(keys_to_modify) + "; " + str(n_to_modify)
            
            #80% chance of an incremental modification; 20% chance of a major modification
            if (rand()<0.6):
                modify_amount=0.2
            else:
                modify_amount=2
            for key in keys_to_modify:
                if (self.verbosity>1):print key + " to modify; current val:" + str(player_params[key])
                old_val=player_params[key]
                new_val=None
                #if it's PVLV mode
                if key=='pvlv_mode':
                    #flip it
                    if old_val==GT_player.PVLV_MODE_PROSPECT:
                       new_val=GT_player.PVLV_MODE_EXPECTANCY
                    else:
                        new_val=GT_player.PVLV_MODE_PROSPECT
                else:#all the others are floats
                    #by a small amount
                    new_val=old_val*(1+numpy.random.uniform(-0.4,1)*modify_amount)
                    #else:#or by a large amount
                    #    new_val=old_val*(1+numpy.random.normal(0,2))
                #announce what we're changing.
                old_val_str = old_val if type(old_val)==str else str(round(old_val,3))
                new_val_str = new_val if type(new_val)==str else str(round(new_val,3))
                if (self.verbosity>1):print "...with " + key + " changed from " + old_val_str + " to " + new_val_str
                #set the key
                new_player.set_parameter_by_key(key,new_val)
                
            
           
            #test the new player
            new_player_result=self.run_bootstrap_get_match_score(new_player,100)
            np_params=new_player.get_parameter_dictionary()
            
            print (str(player_result) + " to beat; " + "Player " + str(n) + " had a match score of " + str(new_player_result) + ".")
            if(new_player_result>player_result*1.01):
                print ("Changes:"
                + ','.join([k + "(" + str(player_params[k])+"->"+str(np_params[k])+")" for k in keys_to_modify]))
                player=new_player
                player_result=new_player_result
                
                print("Player " + str(n) + " Parameters: " + str(np_params))
                print("Player " + str(n) + " was an improvement. Working with the new player.")
                
            #else:
            #    print("Player " + str(n) + " was not an improvement. Staying with the old player.")
        
        return player
        
    def run_demo_with_bootstrapped_and_exemplar(self):
        #now run a single trial of IGT to see what it's like.
        print "Running set of 6 IGT Blocks"
        
        sup=GT_supervisor()
        self.supervisor=sup
        sup.verbosity=5
        #trial_num=len(deck_to_use["A"])
        player=GT_player()

        player.vmPFC_intact=True
        sup.run_block_set(sup.deck_dist_igt,player_to_use=player)
        
        #and now run a single trial of SGT
        print "---------------------------"
        print "Running set of 6 SGT Blocks"
        sup.verbosity=1
        #deck_to_use=deck_dist_sgt
        #trial_num=len(deck_to_use["A"])
        sup.run_block_set(sup.deck_dist_sgt,player_to_use=player)
        
        player.vmPFC_intact=False
        sup.verbosity=1
        print "---------------------------"
        print "Running set of 6 IGT Blocks with vmPFC lesion"
        sup.run_block_set(sup.deck_dist_igt,player_to_use=player)
        print "---------------------------"
        print "Running set of 6 SGT Blocks with vmPFC lesion"
        sup.run_block_set(sup.deck_dist_igt,player_to_use=player)
        
        print "Please wait; running bootstrapped iterations..."
        sup.verbosity=0
        iterations=500
        res=self.run_bootstrap(player,iterations=iterations)
        for vmPFC_status, vmPFC_data in res.iteritems():
            for task_name, task_data in vmPFC_data.iteritems():
                print "Ran " + str(iterations) + " iterations of task " + task_name + " with status " + vmPFC_status + ";\naverage counts of cards chosen from each deck as follows:"
                print '\t' + '\t'.join(["Deck " + str(d) for d in ["A","B","C","D"]])
                for b, block in enumerate(task_data['deck_choice']):
                    print ("Block " + str(b+1) + "\t" + 
                        '\t'.join([str(round(deck,2)) for deck in block]))
                print "Total value: " + str(task_data['value'])
                print "\n"
                

        
gt=GT_manager()
