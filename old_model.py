# -*- coding: utf-8 -*-
import string 
#from Numeric import * 
#import LinearAlgebra 
from copy import deepcopy
from numpy import zeros, array

# Here, the possible hypotheses and events are assigned to indices. 
# Although the same index corresponds to the hypothesis and the event, 
# they are given different names so that the code that references them 
# can clarify which one it’s using. 
HManner = 0 
HPath = 1 
HNeither = 2 
EManner = 0 
EPath = 1 
ENeither = 2

# How strong are the initial priors in the memory effect? 
priorEffect = 6.0


# Define the set of stimuli for each condition.
manner = [EManner, EManner, EManner, EManner, EManner, EManner, EManner, EManner, EManner, EManner, EManner, EManner]
path = [EPath, EPath, EPath, EPath, EPath, EPath, EPath, EPath, EPath, EPath, EPath, EPath]
fiftyFifty = [EPath, EManner, EManner, EPath, EManner, EManner, EPath, EManner, EManner, EPath, EPath, EPath]
fiftyFiftyR = [EPath, EPath, EPath, EManner, EManner, EPath, EManner, EManner, EPath, EManner, EManner, EPath]
qm = [EManner, EPath, EPath, EPath, EPath, EManner, EPath, EPath, EManner, EPath, EPath, EPath]
qmr = [EPath, EPath, EPath, EManner, EPath, EPath, EManner, EPath, EPath, EPath, EPath, EManner]
qp = [EManner, EPath, EManner, EManner, EManner, EManner, EPath, EManner, EManner, EPath, EManner, EManner]
qpr = [EManner, EManner, EPath, EManner, EManner, EPath, EManner, EManner, EManner, EManner, EPath, EManner]

allConditions = {'manner': manner, 'path': path, 'fiftyfifty': fiftyFifty, 'fiftyfiftyr':fiftyFiftyR, 'qm': qm, 'qmr': qmr, 'qp': qp, 'qpr': qpr}

def run_old_model(condition):
        # Calculate the divisor (P(E_i)) for a given type of event. 
        def makeDivisor(type): 
             return likelihood[type][HManner]*prior[HManner] + likelihood[type][HPath] *prior[HPath] + likelihood[type][HNeither]*prior[HNeither]

        if isinstance(condition, basestring):
            condition = allConditions[condition]
        # Set the initial priors. 
        # For the poor frame, these should be set 
        # to [0.56, 0.17, 0.27] instead.
        prior = array([0.77, 0.05, 0.18])
        # Set the likelihood values (P(H_i|E_j)). 
        likelihood = array([[0.72, 0.07, 0.21], [0.06, 0.71, 0.23],[0.22, 0.22, 0.56]])
        # Initialize the event memory to the initial priors. 
        mcount = priorEffect*prior[HManner] 
        pcount = priorEffect*prior[HPath] 
        ncount = priorEffect*prior[HNeither]
        count = priorEffect 
        #print "Condition: %s" % condition
        # Set the relative weight of the Bayesian component. 
        bayesweight = 1.0
        # Iterate over 11 blocks. (After the 12th block, there are no more
        # questions for the subject, so # determined.)
        biases_for_output = []
        biases_for_output.append([prior[HManner], prior[HPath], prior[HNeither]])
        for block in range(0,11):
                bayesBias = zeros(3) 
                case = condition[block] 
                if case == EManner: mcount += 1
                elif case == EPath: pcount += 1
                elif case == ENeither: ncount += 1
                count += 1
                # Calculate new priors with Bayes’ rule 
                for hypothesis in [HManner, HPath, HNeither]: 
                        bayesBias[hypothesis] = likelihood[case][hypothesis] *prior[hypothesis]/ makeDivisor(case)
                # Weighting factor 
                bayesweight *= .95

                # Calculate the values for the memory effect 
                memoryBias = zeros(3) 
                memoryBias[EManner] = mcount/count 
                memoryBias[EPath] = pcount/count 
                memoryBias[ENeither] = ncount/count
                # Set the new bias to the weighted average of bayesBias 
                # and memoryBias 
                newBias = (bayesweight)*bayesBias + (1-bayesweight)*memoryBias 
                prior = newBias
                biases_for_output.append([prior[HManner], prior[HPath], prior[HNeither]])
                #print "%s: %s, bias value: %s" % (block+1, newBias, prior[HPath]-prior[HManner])
        return biases_for_output
