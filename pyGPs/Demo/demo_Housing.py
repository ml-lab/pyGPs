#================================================================================
#    Marion Neumann [marion dot neumann at uni-bonn dot de]
#    Daniel Marthaler [marthaler at ge dot com]
#    Shan Huang [shan dot huang at iais dot fraunhofer dot de]
#    Kristian Kersting [kristian dot kersting at cs dot tu-dortmund dot de]
#
#    This file is part of pyGP_PR.
#    The software package is released under the BSD 2-Clause (FreeBSD) License.
#
#    Copyright (c) by
#    Marion Neumann, Daniel Marthaler, Shan Huang & Kristian Kersting, 30/09/2013
#================================================================================

from pyGPs.Core import *
import numpy as np
import matplotlib.pyplot as plt

def HousingPlotter(x,y,xm,ym,ys2,xt,yt):
    _convertData = lambda z: np.reshape(z,(z.shape[0],))
    plt.plot(x,y, 'r.', linewidth = 3.0)
    plt.plot(xm,ym,'g-', linewidth = 3.0)
    plt.fill_between(xm, _convertData(ym + 2.*np.sqrt(ys2)), _convertData(ym - 2.*np.sqrt(ys2)), facecolor=[0.,1.0,0.0,0.7],linewidths=0.0)    
    plt.plot(xt,yt, 'bx', linewidth = 3.0, markersize = 5.0)
    plt.grid()
    plt.xlabel('Index')
    plt.ylabel('Median Home Values (normalized)')
    plt.show()    

if __name__ == '__main__':

    infile = 'data_for_demo/housing.txt'
    data = np.genfromtxt(infile)

    DN, DD = data.shape
    N = 25
    # Get all data (exclude the 4th column which is binary) except the last 50 points for training
    x  = np.concatenate((data[:-N,:4],data[:-N,5:-1]),axis=1)
    x = (x - np.mean(x,axis=0))/(np.std(x,axis=0)+1.e-16)
    # The function we will perform regression on:  Median Value of owner occupied homes
    y  = np.reshape(data[:-N,-1],(len(data[:-N,-1]),1))
    y = (y-np.mean(y))/(np.std(y)+1.e-16)
    # Test on the last 50 points
    xs  = np.concatenate((data[-N:,:4],data[-N:,5:-1]),axis=1)
    xs = (xs - np.mean(xs,axis=0))/(np.std(xs,axis=0)+1.e-16)
    ys = np.reshape(data[-N:,-1],(N,1))
    ys = (ys-np.mean(ys))/(np.std(ys)+1.e-16)
    N,D = x.shape
    
    model = gp.GPR()
    model.fit(x, y)
    print 'Initial negative log marginal likelihood = ', round(model._neg_log_marginal_likelihood_,3)
    
    # train and predict
    from time import clock
    t0 = clock()
    model.train(x,y)
    t1 = clock()
    ym, ys2, fm, fs2, lp = model.predict(xs)

    print 'Time to optimize = ', t1-t0
    print 'Optimized mean = ', model.meanfunc.hyp
    print 'Optimized covariance = ', model.covfunc.hyp
    print 'Optimized liklihood = ', model.likfunc.hyp
    print 'Final negative log marginal likelihood = ', round(model._neg_log_marginal_likelihood_,3)

    HousingPlotter(range(len(y)),y,range(len(ym)),ym,ys2,range(len(y),len(y)+len(ys)),ys)