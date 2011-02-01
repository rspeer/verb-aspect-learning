# Data from manner/path experiments.

# First, define some constants.
MANNER, PATH, NEITHER = 0, 1, 2

# A training sequence consists of 12 frames that teach a verb, and in each one
# the correct meaning for that verb is either MANNER or PATH. For example, the
# 50/50 training sequence has 6 path verbs and 6 manner verbs.

fifty_training = [PATH, MANNER, MANNER, PATH, MANNER, MANNER, PATH,
MANNER, MANNER, PATH, PATH, PATH]

# The subject is asked 4 questions, two of them after they see one example (so
# that the only information they have to distinguish manner from path is their
# current bias) and two after they see five more examples (to teach them the
# right answer). We look only at the first two here.
#
# These answers are classified as MANNER (if they answered yes to the
# manner-biased question and no to the path-biased question), PATH (if vice
# versa), or NEITHER (if they answered yes to both or no to both).
#
# This data is expressed here as a list of (manner, path, neither) triples.
# These show the number of subjects who answered MANNER, the number who
# answered PATH, and the number who answered NEITHER, at each step of the
# experiment. The first entry, for example, shows their pre-existing bias when
# they haven't been taught any novel verbs by the experiment.
#
# The data starting from here is for experiments in English.

fifty_data = [(8,0,2), (6,0,4), (10,0,0), (10,0,0), (6,2,2), (9,0,1), (10,0,0),
              (8,1,1), (9,1,0), (7,3,0), (8,2,0), (8,2,0)]

# The "R" sequences are the other sequences in reverse order. This data, for
# example, is for subjects who were shown the 50/50 sequence in reverse order.
# When there are different manner and path verbs, this changes the order that
# they see manner and path taught to them; when the verbs are all manner or all
# path, it simply changes the order of the verbs.

fifty_rtraining = [PATH, PATH, PATH, MANNER, MANNER, PATH, MANNER,
                   MANNER, PATH, MANNER, MANNER, PATH]
fifty_rdata = [(6,0,0), (5,0,1), (3,2,1), (5,0,1), (3,2,1), (6,0,0),
                     (5,0,1), (4,1,1), (6,0,0), (4,0,2), (5,0,1), (6,0,0)]

# Data from the path-only subjects (all correct answers are PATH).

path_training = path_rtraining = [PATH]*12
path_data = [(4,0,1), (3,0,2), (2,3,0), (2,3,0), (0,5,0), (1,1,3),
             (0,3,2), (0,3,2), (0,4,1), (0,5,0), (0,5,0), (0,5,0)]
path_rdata = [(4,1,0), (1,3,1), (0,4,1), (1,2,2), (0,5,0), (1,3,1),
              (1,3,1), (0,5,0), (1,4,0), (1,4,0), (1,3,1), (1,3,1)]

# Data from the manner-only subjects (all correct answers are MANNER).
manner_training = manner_rtraining = [MANNER]*12
manner_data = [(3,1,1), (5,0,0), (5,0,0), (5,0,0), (5,0,0), (5,0,0),
               (5,0,0), (4,0,1), (5,0,0), (4,0,1), (5,0,0), (4,1,0)]
manner_rdata = [(5,0,0), (5,0,0), (5,0,0), (5,0,0), (5,0,0), (4,0,1),
                (5,0,0), (5,0,0), (5,0,0), (5,0,0), (5,0,0), (5,0,0)]


# Data from the 25% path, 75% manner subjects.
qp_training = [MANNER, PATH, MANNER, MANNER, MANNER, MANNER,
               PATH, MANNER, MANNER, PATH, PATH, MANNER]
qp_data = [(4,0,1), (4,0,1), (5,0,0), (5,0,0), (4,0,1), (3,0,2),
           (5,0,0), (3,2,0), (4,0,1), (4,1,0), (4,0,1), (5,0,0)]
# the [::-1] makes the 'rtraining' sequence by reading the 'training' sequence
# in reverse order
qp_rtraining = qp_training[::-1]
qp_rdata = [(3,2,0), (5,0,0), (2,0,3), (5,0,0), (4,1,0), (5,0,0),
            (4,0,1), (2,1,2), (5,0,0), (5,0,0), (4,0,1), (5,0,0)]

# Data from the 75% path, 25% manner subjects.
qm_training = [MANNER, PATH, PATH, PATH, PATH, MANNER,
               PATH, PATH, MANNER, PATH, PATH, PATH]
qm_rtraining = qm_training[::-1]
qm_data = [(4,0,1), (5,0,0), (3,0,2), (4,1,0), (1,4,0), (1,0,4),
           (3,1,1), (1,2,2), (2,2,0), (2,2,1), (2,1,2), (3,2,0)]
qm_rdata = [(3,1,1), (4,1,0), (1,1,3), (2,0,3), (2,3,0), (3,0,2),
            (3,2,0), (2,2,1), (4,1,0), (4,0,1), (2,2,1), (5,0,0)]

# df stands for "different frame", referring to the syntactically poor sentence
# frame that was contrasted with the syntactically rich frame in English,
# because the rich frame may have had an inherent manner bias. They use the
# same training sequences before.

# 50/50, poor frame
df_fifty_training = fifty_training
df_fifty_rtraining = fifty_rtraining
df_fifty_data = [(3,0,1), (0,3,1), (1,1,2), (2,2,0), (1,2,1), (2,1,1),
                 (2,0,2), (0,2,2), (2,0,2), (0,2,2), (0,3,1), (0,1,3)]
df_fifty_rdata = [(1,2,2), (0,3,2), (1,4,0), (1,3,1), (2,2,1), (2,2,1),
                  (3,2,0), (2,3,0), (5,0,0), (2,2,1), (2,2,1), (4,1,0)]

# All path, poor frame
df_path_training = df_path_rtraining = [PATH]*12
df_path_data = [(3,0,2), (0,3,2), (0,3,2), (2,3,0), (0,5,0), (0,3,2),
                (0,3,2), (1,3,1), (0,3,2), (0,5,0), (0,5,0), (0,5,0)]
df_path_rdata = [(1,1,3), (1,4,0), (0,4,1), (2,2,1), (1,4,0), (1,4,0),
                 (0,3,2), (0,5,0), (0,5,0), (0,5,0), (0,3,2), (0,4,1)]

# All manner, poor frame
df_manner_training = df_manner_rtraining = [MANNER]*12
df_manner_data = [(2,1,2), (4,1,0), (5,0,0), (5,0,0), (4,0,1), (4,0,1),
                  (5,0,0), (4,0,1), (5,0,0), (5,0,0), (5,0,0), (5,0,0)]
df_manner_rdata = [(3,1,1), (4,0,1), (2,3,0), (5,0,0), (4,1,0), (5,0,0),
                   (4,0,1), (3,1,1), (5,0,0), (4,0,1), (4,1,0), (5,0,0)]

# 75% path, poor frame
df_qm_training = [MANNER, PATH, PATH, PATH, PATH, MANNER,
                  PATH, PATH, MANNER, PATH, PATH, PATH]
df_qm_rtraining = df_qm_training[::-1]
df_qm_data = [(4,1,0), (2,1,2), (1,2,2), (3,2,0), (0,5,0), (0,3,2),
              (2,2,1), (1,3,1), (3,1,1), (0,5,0), (1,3,1), (0,3,2)]
df_qm_rdata = [(1,1,1), (1,1,1), (0,2,1), (1,1,1), (2,1,0), (0,2,1),
               (0,3,0), (0,2,1), (1,2,0), (1,2,0), (0,2,1), (0,2,1)]

# 25% path, poor frame
df_qp_training = [MANNER, PATH, MANNER, MANNER, MANNER, MANNER,
                  PATH, MANNER, MANNER, PATH, PATH, MANNER]
df_qp_rtraining = df_qp_training[::-1]
df_qp_data = [(5,0,0), (4,0,1), (1,4,0), (5,0,0), (4,0,1), (5,0,0),
              (5,0,0), (1,3,1), (5,0,0), (4,1,0), (3,1,1), (4,1,0)]
df_qp_rdata = [(3,1,1), (2,0,3), (3,1,1), (5,0,0), (5,0,0), (5,0,0),
               (5,0,0), (4,1,0), (5,0,0), (5,0,0), (5,0,0), (4,1,0)]

# From here on, the data is from experiments that were held in Spanish.
#
# Spanish, 50/50
sp_fifty_training = [PATH, MANNER, MANNER, PATH, MANNER, PATH,
                     PATH, MANNER, MANNER, PATH, PATH, PATH]
sp_fifty_data = [(4,0,1), (2,0,3), (5,0,0), (3,1,1), (5,0,0), (5,0,0),
                 (5,0,0), (5,0,0), (5,0,0), (3,2,0), (4,1,0), (4,1,0)]

# Spanish, all path
sp_path_training = sp_path_rtraining = [PATH]*12
sp_path_data = [(2,1,2), (0,4,1), (1,4,0), (1,3,1), (0,5,0), (0,4,1),
                (1,4,0), (1,3,1), (1,3,1), (0,5,0), (1,4,0), (2,3,0)]
sp_path_rdata = [(1,0,1), (0,2,0), (1,1,0), (1,1,0), (0,2,0), (0,2,0),
                 (0,1,1), (0,2,0), (0,1,1), (0,2,0), (0,2,0), (0,1,1)]

# Spanish, all manner (was never run in reverse)
sp_manner_training = [MANNER]*12
sp_manner_data = [(6,0,0), (6,0,0), (5,0,1), (6,0,0), (4,1,1), (6,0,0),
                  (6,0,0), (6,0,0), (6,0,0), (6,0,0), (5,0,1), (5,0,1)]

# Pair up the training sequences with the appropriate data for the three kinds
# of experiments: English rich frame, English poor frame, and Spanish.
english_richframe = [(fifty_training, fifty_data),
                     (fifty_rtraining, fifty_rdata),
                     (path_training, path_data),
                     (path_rtraining, path_rdata),
                     (manner_training, manner_data),
                     (manner_rtraining, manner_rdata),
                     (qp_training, qp_data),
                     (qp_rtraining, qp_rdata),
                     (qm_training, qm_data),
                     (qm_rtraining, qm_rdata)]
english_poorframe = [(df_fifty_training, df_fifty_data),
                     (df_fifty_rtraining, df_fifty_rdata),
                     (df_path_training, df_path_data),
                     (df_path_rtraining, df_path_rdata),
                     (df_manner_training, df_manner_data),
                     (df_manner_rtraining, df_manner_rdata),
                     (df_qm_training, df_qm_data),
                     (df_qm_rtraining, df_qm_rdata),
                     (df_qp_training, df_qp_data),
                     (df_qp_rtraining, df_qp_rdata)]
spanish = [(sp_fifty_training, sp_fifty_data),
           (sp_path_training, sp_path_data),
           (sp_path_rtraining, sp_path_rdata),
           (sp_manner_training, sp_manner_data)]

