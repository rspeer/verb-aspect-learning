"""
mannerpath.py: Implements a hierarchical Bayesian model for analyzing verb
lexicalization biases.
"""

from scipy.special import gamma, gammaln
from numpy import *
from numpy.random.mtrand import *
from data import english_richframe, english_poorframe, spanish,\
                 MANNER, PATH, NEITHER

def multivariate_polya(avec, nvec):
    """
    Returns a posterior probability from a Dirichlet-multinomial distribution.
    avec is the vector of parameters on the Dirichlet distribution, and
    nvec is the vector of observed counts.

    More simply: avec is what you started out believing, and nvec is what
    you actually observed.
    """
    sumvec = avec + nvec
    log1 = gammaln(sum(avec)) - gammaln(sum(sumvec))
    log2 = sum(gammaln(sumvec))-sum(gammaln(avec))
    return log1 + log2

def betaln(avec):
    """
    Returns the log of the Beta function of a vector.
    """
    return sum(gammaln(avec)) - gammaln(sum(avec))

def dirichlet_logprob(avec, xvec):
    """
    Returns the probability density for a particular vector (xvec) in a
    Dirichlet distribution parameterized by avec.
    """
    logtotal = -betaln(avec)
    for (a, x) in zip(avec, xvec):
        logtotal += (a-1)*log(x)
    return logtotal

def hastings_value(new, old):
    """
    Calculate the log of the Hastings factor (P(a|b) / P(b|a)) for two points
    in a Dirichlet-distributed proposal.
    """
    return dirichlet_logprob(new, old) - dirichlet_logprob(old, new)

def test_likelihood(input, avec):
    """
    Given the parameter vector of a Dirichlet distribution, evaluate the
    likelihood of the experimental data given the model.
    """
    logpost = 0.0
    for training, data in input:
        nvec = zeros(3)
        for t in range(12):
            # Account for the previously-taught verb meanings.
            if t > 0: nvec[training[t-1]] += 1
            for resp in (MANNER, PATH, NEITHER):
                # Calculate the log probability of the possible meanings of the
                # next verb, given the previous verbs.
                incvec = zeros((3,))
                incvec[resp] += 1
                logpost += (data[t][resp] *
                  (multivariate_polya(avec, nvec+incvec) -
                   multivariate_polya(avec, nvec)))
    return logpost

def test_prediction(input, avec):
    """
    Given the parameter vector of a Dirichlet distribution, determine what
    the model predicts and calculate its difference from people's actual
    responses for this experimental condition.
    """
    print "Parameters:", avec
    rmse_list = []
    for training, data in input:
        nvec = zeros(3)
        print
        for t in range(12):
            if t > 0:
                nvec[training[t-1]] += 1
            probs = []
            for resp in (MANNER, PATH, NEITHER):
                incvec = zeros((3,))
                incvec[resp] += 1
                probs.append(
                  (multivariate_polya(avec, nvec+incvec) -
                   multivariate_polya(avec, nvec)))
            theprobs = probs
            probs = np.exp(np.array(probs))
            probs /= np.sum(probs)
            actual = np.array(data[t], 'f')
            actual /= np.sum(actual)

            print nvec, probs, actual
            rmse_list.append(np.sqrt(np.sum((probs - actual)**2)))
    return np.array(rmse_list)

def test_prediction_oldmodel(input):
    """
    Determine what the Havasi 2004 model predicts given the stimuli in an
    experimental condition, and calculate its difference from what people
    actually exist
    """
    from old_model import run_old_model
    rmse_list = []
    for training, data in input:
        steps = [[0.77, 0.05, 0.18]] + run_old_model(training)
        print
        for step, actual in zip(steps, data):
            probs = np.array(step, 'f') / sum(step)
            actual = np.array(actual, 'f') / np.sum(actual)
            
            print probs, actual
            rmse_list.append(np.sqrt(np.sum((probs - actual)**2)))
    return np.array(rmse_list)

def metropolis_hastings(input, alpha, beta, out):
    """
    Implement the Metropolis-Hastings algorithm for this model, writing the
    results to a file.
    """
    best = -1e300
    accepted = 0
    total = 0
    while True:
        # Sample alpha from a log-normal proposal
        newalpha = lognormal(log(alpha), 0.25)
        # Sample beta from a Dirichlet proposal. Don't let any of the values
        # get so small that we get NaN for probabilities.
        newbeta = maximum(dirichlet(beta*100), 1e-6)
        newbeta /= sum(newbeta)

        prop_goodness = test_likelihood(input, newalpha*newbeta)-(newalpha)
        prev_goodness = test_likelihood(input, alpha*beta)-(alpha)
        metropolis_value = (prop_goodness - prev_goodness +
        hastings_value(newbeta, beta))
        total += 1
        
        # Decide whether to accept the proposal
        if (not isnan(prop_goodness) and metropolis_value >
        log(random.random())):
            alpha = newalpha
            beta = newbeta
            accepted += 1
            print alpha, beta, prop_goodness, best
            print >> out, ("%6.6f\t%6.6f\t%6.6f\t%6.6f\t%6.6f" %
                           (alpha, beta[0], beta[1], beta[2], prop_goodness))
            # If this is the best point so far, show it in the debugging
            # output, as well as the acceptance rate so far
            if prop_goodness > best:
                print "***", alpha, beta, prop_goodness
                best = prop_goodness

CONDITIONS = {
    'richframe': (english_richframe, 'richframe.out'),
    'poorframe': (english_poorframe, 'poorframe.out'),
    'spanish': (spanish, 'spanish.out')
}

def run(dataset, filename):
    out = open(filename, 'w+')
    try:
        # change english_richframe to english_poorframe or spanish, or
        # whatever data set we want to use on this run
        metropolis_hastings(dataset, 3,
            array([1.0, 1.0, 1.0])/3, out)
    finally:
        out.close()

if __name__ == '__main__':
    import sys
    try:
        condition = sys.argv[1]
        dataset, filename = CONDITIONS[condition]
        run(dataset, filename)
    except (IndexError, KeyError):
        print "No conditions specified."

