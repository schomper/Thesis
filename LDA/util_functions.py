import math
import global_att


def doc_e_step(document, gamma, phi, model, ss):
    # posterior inference

    likelihood = lda_inference(document, model, gamma, phi)

    # update sufficient statistics

    gamma_sum = 0
    for k in range(0, model.num_topics):
        gamma_sum += gamma[k]
        ss.alpha_suffstats += digamma(gamma[k])

    ss.alpha_suffstats -= model.num_topics * digamma(gamma_sum)

    for n in range(0, document.length):

        for k in range(0, model.num_topics):
            ss.class_word[k][document.words[n]] += document.word_counts[n] * phi[n][k]
            ss.class_total[k] += document.word_counts[n] * phi[n][k]

    ss.num_docs += 1

    return likelihood


def log_sum(log_a, log_b):
    v = None

    if log_a < log_b:
        v = log_b + math.log(1 + math.exp(log_a - log_b))

    else:
        v = log_a + math.log(1 + math.exp(log_b - log_a))

    return v


def digamma(x):
    x += 6
    p = 1 / (x * x)
    p *= (((0.004166666666667 * p - 0.003968253986254) \
           * p + 0.008333333333333) \
          * p - 0.083333333333333)

    p = p + math.log(x) - 0.5 \
                          / x - 1 / (x - 1) - 1 / (x - 2) - 1 \
                                                            / (x - 3) - 1 / (x - 4) - 1 / (x - 5) - 1 / (x - 6)

    return p


def trigamma(x):
    x += 6
    p = 1 / (x * x)
    p = (((((0.075757575757576 * p - 0.033333333333333) \
            * p + 0.0238095238095238) * p - 0.033333333333333) \
          * p + 0.166666666666667) * p + 1) / x + 0.5 * p

    for i in range(0, 6):
        x -= 1
        p += 1 / (x * x)

    return (p)


#
# Variational Inference
#
def lda_inference(document, model, var_gamma, phi):
    converged = 1
    phisum = 0
    likelihood = 0
    likelihood_old = 0.00000001
    oldphi = [0 for x in range(model.num_topics)]
    digamma_gam = [0 for x in range(model.num_topics)]

    # compute posterior dirichlet

    for k in range(0, model.num_topics):

        var_gamma[k] = model.alpha + (document.total_words / model.num_topics)
        digamma_gam[k] = digamma(var_gamma[k])

        for n in range(0, document.length):
            phi[n][k] = 1.0 / model.num_topics

    var_iter = 0

    while ((converged > global_att.VAR_CONVERGED) and (
                (var_iter < global_att.VAR_MAX_ITER) or (global_att.VAR_MAX_ITER == -1))):
        var_iter += 1

        for n in range(0, document.length):

            phisum = 0
            for k in range(0, model.num_topics):

                oldphi[k] = phi[n][k]
                phi[n][k] = digamma_gam[k] + model.log_prob_w[k][document.words[n]]

                if k > 0:
                    phisum = log_sum(phisum, phi[n][k])
                else:
                    phisum = phi[n][k]  # note, phi is in log space

            for k in range(0, model.num_topics):
                phi[n][k] = math.exp(phi[n][k] - phisum)
                var_gamma[k] += document.word_counts[n] \
                                * (phi[n][k] - oldphi[k])
                # !!! a lot of extra di-gamma's here because of how we're computing it
                # !!! but its more automatically updated too.
                digamma_gam[k] = digamma(var_gamma[k])

        likelihood = compute_likelihood(document, model, phi, var_gamma)
        converged = (likelihood_old - likelihood) / likelihood_old
        likelihood_old = likelihood

        # printf("[LDA INF] %8.5f %1.3e\n", likelihood, converged);

    return likelihood


def compute_likelihood(document, model, phi, var_gamma):
    likelihood = 0
    digsum = 0
    var_gamma_sum = 0
    dig = [0 for x in range(model.num_topics)]

    for k in range(0, model.num_topics):
        dig[k] = digamma(var_gamma[k])
        var_gamma_sum = var_gamma[k] + var_gamma_sum

    digsum = digamma(var_gamma_sum)

    likelihood = math.lgamma(model.alpha * model.num_topics) \
                 - model.num_topics * math.lgamma(model.alpha) \
                 - (math.lgamma(var_gamma_sum))

    for k in range(0, model.num_topics):
        likelihood += ((model.alpha - 1) * (dig[k] - digsum)
                       + math.lgamma(var_gamma[k]) - (var_gamma[k] - 1)
                       * (dig[k] - digsum))

        for n in range(0, document.length):
            if phi[n][k] > 0:
                likelihood += document.word_counts[n] * \
                              (phi[n][k] * ((dig[k] - digsum)
                                            - math.log(phi[n][k])
                                            + model.log_prob_w[k][document.words[n]]))

    return likelihood


# newtons method
def opt_alpha(ss, num_docs, num_topics):
    init_a = 100
    iter = 0

    log_a = math.log(init_a)

    iter += 1
    a = math.exp(log_a)
    if math.isnan(a):
        init_a *= 10
        print("warning : alpha is nan; new init = %5.5f" % init_a)
        a = init_a
        log_a = math.log(a)

    f = alhood(a, ss, num_docs, num_topics)
    df = d_alhood(a, ss, num_docs, num_topics)
    d2f = d2_alhood(a, num_docs, num_topics)
    log_a = log_a - df / (d2f * a + df)
    print("alpha maximization : %5.5f   %5.5f" % (f, df))

    while ((math.fabs(df) > global_att.NEWTON_THRESH) and \
                   (iter < global_att.MAX_ALPHA_ITER)):

        iter += 1
        a = math.exp(log_a)
        if math.isnan(a):
            init_a *= 10
            print("warning : alpha is nan; new init = %5.5f" % init_a)
            a = init_a
            log_a = math.log(a)

        f = alhood(a, ss, num_docs, num_topics)
        df = d_alhood(a, ss, num_docs, num_topics)
        d2f = d2_alhood(a, num_docs, num_topics)
        log_a = log_a - df / (d2f * a + df)
        print("alpha maximization : %5.5f   %5.5f" % (f, df))

    return math.exp(log_a)


def alhood(a, ss, num_docs, num_topics):
    return num_docs * (math.lgamma(num_topics * a) - num_topics * math.lgamma(a)) + (a - 1) * ss


def d_alhood(a, ss, num_docs, num_topics):
    return num_docs * (num_topics * digamma(num_topics * a) - num_topics * digamma(a)) + ss


def d2_alhood(a, num_docs, num_topics):
    return num_docs * (num_topics * num_topics * trigamma(num_topics * a) - num_topics * trigamma(a))


def max_value_position(value_list):
    """ Returns the position of the element with the highest value in value_list

    :param value_list(list): the array to be searched through
    :return: the index of the max value in value_list
    """
    max_value = value_list[0]
    max_pos = 0

    for index in range(1, len(value_list)):

        if value_list[index] > max_value:
            max_value = value_list[index]
            max_pos = index

    return max_pos
