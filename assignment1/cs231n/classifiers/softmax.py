from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    num_class = W.shape[1]
    for i in range(num_train):
        score = X[i].dot(W)
        score -= np.max(score)  # 进行归一化，实现数值稳定
        correct_class_score = score[y[i]]
        loss += -np.log(np.exp(correct_class_score) / np.sum(np.exp(score)))  # softmax计算公式
        for j in range(num_class):
            if j == y[i]:
                dW[:, y[i]] += (-1 + np.exp(correct_class_score) / np.sum(np.exp(score))) * X[i]
            else:
                dW[:, j] += (np.exp(score[j]) / np.sum(np.exp(score))) * X[i]
    pass
    loss /= num_train
    loss += reg * np.sum(W * W)
    dW /= num_train
    dW += reg * W
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    num_train = X.shape[0]
    scores = X.dot(W)
    scores -= np.max(scores, axis=1, keepdims=True)  # 进行归一化，实现数值稳定
    # 需要知道每张图片正确分类的的得分
    correct_class_score = scores[np.arange(num_train), y].reshape(num_train, 1)
    exp_sum = np.sum(np.exp(scores), axis=1).reshape(num_train, 1)
    loss += np.sum(-correct_class_score + np.log(exp_sum))
    loss /= num_train
    loss += reg * np.sum(W * W)

    margins = np.exp(scores) / exp_sum
    margins[np.arange(num_train), y] += -1
    dW = X.T.dot(margins)
    dW /= num_train
    dW += reg * W
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
