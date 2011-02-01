from pylab import *
import numpy as np
from scipy.stats import scoreatpercentile
import data

def get_data(file):
    data = [x.strip().split('\t') for x in file.readlines()]
    return [row for row in data if len(row) > 4]

def get_col(data, col):
    return [float(row[col]) for row in data]

def get_mul(data, c1, c2):
    return [float(row[c1]) * float(row[c2]) for row in data]


richframe_data = get_data(open('richframe.out'))[:200000]
poorframe_data = get_data(open('poorframe.out'))[:200000]
spanish_data = get_data(open('spanish.out'))[:200000]

def mannerpathtri():
    sizes = [2]*len(richframe_data)
    scatter(get_mul(spanish_data, 0, 1), get_mul(spanish_data, 0, 2),
      s=sizes, c='g', edgecolors='none')
    scatter(get_mul(richframe_data, 0, 1), get_mul(richframe_data, 0, 2),
      s=sizes, c='r', edgecolors='none')
    scatter(get_mul(poorframe_data, 0, 1), get_mul(poorframe_data, 0, 2),
      s=sizes, c='b', edgecolors='none')
    legend(('Spanish', 'English rich frame', 'English poor frame'))
#    plot([0,1], [1,0], 'k')
#    axis([0, 1, 0, 1])
    xlabel('Manner bias')
    ylabel('Path bias')
    show()

def bins2d(xvals, yvals, n=100):
    bins = np.zeros((n,n))
    for (x,y) in zip(xvals, yvals):
        xbin = int(x*n)
        ybin = int(y*n)
        bins[ybin,xbin] += 1
    return bins / np.max(bins)

def contour_plot():
    bins = bins2d(get_col(richframe_data, 1), get_col(richframe_data, 2))
    contour(bins, origin='lower')
    show()

def histogram_plot(col=1, label='', maxbin=1.0):
    bins = np.linspace(0, maxbin, 1000, endpoint=False)
    spanish_col = get_col(spanish_data, col)
    rich_col = get_col(richframe_data, col)
    poor_col = get_col(poorframe_data, col)

    for column, color, nsamples in [(spanish_col, 'g', 18),
                                    (rich_col, 'r', 56),
                                    (poor_col, 'b', 47)]:
        hist(column, histtype='step', bins=bins, ec=color)
    loc = 'upper right'
    if col == 1: loc = 'upper left'
    legend(('Spanish', 'English rich frame', 'English poor frame'), loc=loc)
    
    for column, color, nsamples in [(spanish_col, 'g', 18),
                                    (rich_col, 'r', 56),
                                    (poor_col, 'b', 47)]:
        col_mean = np.mean(column)
        col_stderr = np.std(column)# / np.sqrt(nsamples)
        floorbin = np.floor(col_mean * 1000.0 / maxbin)
        floor = floorbin * maxbin / 1000.0
        ceil = (floorbin+1) * maxbin / 1000.0
        col_max = len([v for v in column if floor <= v < ceil])

        errorbar([col_mean], [col_max*1.25], fmt='.', xerr=[col_stderr],
                 ecolor=color, mec=color, mfc=color)

    #axis([0, 1, 0, 100])
    xlabel(label)
    ylabel('Samples')
    show()

def compare_versions():
    from mannerpath import test_prediction, test_prediction_oldmodel
    rich_params = [np.mean(get_col(richframe_data, i)) for i in xrange(4)]
    poor_params = [np.mean(get_col(poorframe_data, i)) for i in xrange(4)]
    span_params = [np.mean(get_col(spanish_data, i)) for i in xrange(4)]
    
    results = []
    all_diffs = []
    all_old = []
    all_new = []

    new = test_prediction(data.english_richframe, np.array(rich_params[1:]) * rich_params[0])
    old = test_prediction_oldmodel(data.english_richframe)
    diff = old - new
    all_diffs.extend(diff); all_new.extend(new); all_old.extend(old)
    diff_mean = np.mean(diff)
    diff_err = np.std(diff) / np.sqrt(len(diff))
    results.append(('Rich frame', np.mean(new), np.mean(old), diff_mean, diff_err, len(diff)))

    new = test_prediction(data.english_poorframe, np.array(poor_params[1:]) * poor_params[0])
    old = test_prediction_oldmodel(data.english_poorframe)
    diff = old - new
    all_diffs.extend(diff); all_new.extend(new); all_old.extend(old)
    diff_mean = np.mean(diff)
    diff_err = np.std(diff) / np.sqrt(len(diff))
    results.append(('Poor frame', np.mean(new), np.mean(old), diff_mean, diff_err, len(diff)))

    new = test_prediction(data.spanish, np.array(span_params[1:]) * span_params[0])
    old = test_prediction_oldmodel(data.spanish)
    diff = old - new
    all_diffs.extend(diff); all_new.extend(new); all_old.extend(old)
    diff_mean = np.mean(diff)
    diff_err = np.std(diff) / np.sqrt(len(diff))
    results.append(('Spanish', np.mean(new), np.mean(old), diff_mean, diff_err, len(diff)))

    diff_err = np.std(all_diffs) / np.sqrt(len(all_diffs))
    results.append(('All', np.mean(all_new), np.mean(all_old), np.mean(all_diffs), diff_err, len(all_diffs)))

    print results
    return results

def graph_versions():
    results = compare_versions()
    grouped = zip(*results)
    indices = np.arange(4)
    p1 = bar(indices, grouped[2], width=0.25, color='b', ecolor='k', yerr=[x/2 for x in grouped[4]])
    p2 = bar(indices+0.35, grouped[1], width=0.25, color='g', ecolor='k', yerr=[x/2 for x in grouped[4]])
    xticks(indices+0.3, ('Rich frame', 'Poor frame', 'Spanish', 'All'))
    xlim(-0.1, 3.7)
    ylim(0, 0.5)
    xlabel('Condition'); ylabel('Model error')
    text(1.3, 0.4, '**', horizontalalignment='center')
    text(3.3, 0.36, '*', horizontalalignment='center')
    legend((p1[0], p2[0]), ("Havasi (2004) model", "Hierarchical model"))
    show()

def combined_plot():
    subplot(411)
    histogram_plot(0, 'Strength of bias', 10)
    subplot(412)
    histogram_plot(1, 'Proportion of manner bias')
    xlim((0.0, 1.0))
    subplot(413)
    histogram_plot(2, 'Proportion of path bias')
    xlim((0.0, 1.0))
    subplot(414)
    histogram_plot(3, 'Proportion of neither bias')
    xlim((0.0, 1.0))

