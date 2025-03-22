"""
Helper functions for lecture 12, sections on classifiers.
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def f(x1, x2):
    """
    True relationship for classification examples.

    Implements the trigonometric function f(x1, x2) = sin(2*pi*x1) * cos(pi*x2).

    Parameters
    ----------
    x1 : array-like
        First feature.
    x2 : array-like
        Second feature.

    Returns
    -------
    array-like
        Value of the function f(x1, x2) at the given points.
    """
    return np.sin(2*np.pi*x1) * np.cos(np.pi*x2)



def create_class_data(N=100, sigma=0.2, rng=None):
    """
    Create synthetic data for binary classification examples.

    Parameters
    ----------
    N : int
        Number of observations to generate.
    sigma : float
        Standard deviation of the error term.
    rng : numpy.random.Generator, optional
        Random number generator to use.

    Returns
    -------
    X : array-like
        Feature matrix.
    y : array-like
        Binary response variable.

    """

    if rng is None:
        rng = np.random.default_rng(seed=1234)

    # Draw features from uniform distribution
    x1 = rng.uniform(0, 1, size=N)
    x2 = rng.uniform(0, 1, size=N)

    z = f(x1, x2)

    # Add noise to latent variable if noise variance is positive
    if sigma > 0:
        # Draw errors from normal distribution
        epsilon = rng.normal(0, sigma, size=N)
        z += epsilon

    # Create binary response variable
    y = (z >= 0).astype(int)

    # Stack features into matrix
    X = np.column_stack((x1, x2))

    return X, y



def plot_classes(X, y, X_test=None, y_test=None):
    """
    Plot classes in y for given features X. Optionally visualize 
    training and test data separately, if test data is provided.

    Parameters
    ----------
    X : array-like of shape (n_samples, 2)
        Features x1 and x2
    y : array-like of shape (n_samples,)
        Response variable
    X_test : array-like of shape (n_samples, 2), optional
        Test features x1 and x2
    y_test : array-like of shape (n_samples,), optional
        Test response variable
    """
    fig, ax = plt.subplots(figsize=(4, 4))

    # Indicator whether test data is provided
    has_test = X_test is not None

    colors = ['steelblue', 'darkred']
    markers = ['o', '*']

    classes = np.unique(y)

    for i in classes:
        mask = y == i
        label = f'Class {i} (training)' if has_test else f'Class {i}'
        ax.scatter(
            X[mask, 0], X[mask, 1], s=50, marker=markers[i], c=colors[i],
            alpha=0.7, lw=0.75, label=label
        )

        if has_test:
            mask = y_test == i
            label = f'Class {i} (test)'
            ax.scatter(
                X_test[mask, 0], X_test[mask, 1], s=60, marker=markers[i], 
                c='none', edgecolors=colors[i],
                alpha=1.0, lw=1.1, label=label
            )

    ax.set_xlabel('$x_1$')
    ax.set_ylabel('$x_2$')
    fig.legend(loc='upper left', ncols=1, bbox_to_anchor=(0.92, 0.89))

    return ax


def plot_decision_boundary(ax, x, classifier):
    """
    Plot decision boundary of a classifier on a given axes object.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis to plot on.
    x : array-like
        Grid points for x1 and x2.
    classifier : object
        Classifier object used to predict decision boundary.

    """

    xx1, xx2 = np.meshgrid(x, x)

    X = np.column_stack((xx1.ravel(), xx2.ravel()))
    y_pred = classifier.predict(X)
    y_pred = y_pred.reshape(xx1.shape)

    colors = ['steelblue', 'darkred']
    cmap = ListedColormap(colors)

    ax.contourf(xx1, xx2, y_pred, cmap=cmap, alpha=0.2, zorder=-10)
    ax.contour(xx1, xx2, y_pred, colors='black', linewidths=0.5, zorder=-5)
    

def plot_accuracy_validation_curve(param_range, train_scores, test_scores,
                                   xlabel='Parameter C',
                                   log_scale=True):
    """
    Plot validation curve with training and test scores

    Parameters
    ----------
    param_range : array-like
        Values of the hyperparameter.
    train_scores : array-like of shape (n_params, n_folds)
        Training scores for each parameter value.
    test_scores : array-like of shape (n_params, n_folds)
        Test scores for each parameter value.
    """

    # Compute average and standard deviation of scores across folds
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    plt.figure(figsize=(6, 4))
    plt.plot(
        param_range,
        train_mean,
        c='black',
        ls='--',
        label='Training accuracy',
    )
    plt.fill_between(
        param_range,
        train_mean + train_std,
        train_mean - train_std,
        alpha=0.15,
        color='black',
        lw=0
    )
    plt.plot(
        param_range,
        test_mean,
        color='steelblue',
        lw=1.5,
        marker='o',
        markersize=4,
        zorder=10,
        label='Validation accuracy',
    )
    plt.fill_between(
        param_range,
        test_mean + test_std,
        test_mean - test_std,
        alpha=0.15,
        color='steelblue',
        lw=0
    )
    plt.grid(ls=':', alpha=0.25, color='black', zorder=-10)
    if log_scale:
        plt.xscale('log')
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel('Accuracy')
    plt.title('Validation curve')

    ymin = min(np.amin(test_mean - test_std), np.amin(train_mean - train_std))
    ymin = np.floor(ymin * 10) / 10
    plt.ylim((ymin, 1.0))