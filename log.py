#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

class LogisticRegression():
    
    def __init__(self, learning_rate, no_of_iterations):

        self.learning_rate = learning_rate

        self.no_of_iterations = no_of_iterations
        
    def fit(self, X, Y):

        self.m, self.n = X.shape
        
        self.w = np.zeros(self.n)

        self.b = 0

        self.X = X

        self.Y = Y
        
        for i in range(self.no_of_iterations):

            self.update_weights()
            
    def update_weights(self):

        
        Y_hat = 1/(1 + np.exp(-((self.X).dot(self.w) + self.b)))

        # L = -(Y log Ŷ + (1-y)
        # log(1 - Ŷ))
        # a = σ(z) = 1 / ((1 + e - z)
        #     z = wx+b
        #     dL / dw = dL / da * da / dw  = dL / da * da / dz * dz / dw
        #     dL / da = -y / a + (1-y) / (1 - a)
        # da / dz = (1 + e - z) - 1
        # = e - z / (1 + e - z)
        # 2
        # → a2 = 1 / (1 + e - z)
        # 2
        # e - z = (1 - a) / a
        # = (1 - a) / a * a2
        # = a(1 - a)
        # dz / dw = d(wx + b) / dw
        # = x + 0
        # = x
        # Therefore, da / dz = a(1 - a)
        # dz / dw = x
        # dL / da = -y / a + (1 - y) / (1 - a)
        # dL / dw = (-y / a + (1 - y) / (1 - a)) * a * (1 - a) * x
        # = (-y + ay a-ay) * a * (1 - a) * x / a(1 - a)
        # dL / dw = x(a - y) → dL / dw = (A - Y).X
        # Therefore, dwst / dW = (A - Y).X
        # So,
        # dL / db = (a - y) / a(1 - a)
        # da / dz = a(1 - a)
        # dz / db = 1
        # Therefore, dwst / db = (A - Y)
        # dw = 1 / m(A - Y) . X
        # db = 1 / m(A - Y)
        # → A = Ŷ
        # → m denotes number of data points in training data.


        dw = (self.X.T).dot(Y_hat-self.Y) / self.m

        db = np.sum(Y_hat - self.Y) / self.m
        
        self.w = self.w - self.learning_rate*dw

        self.b = self.b - self.learning_rate*db
        
        
    def predict(self, X):
        
        Y_pred = 1 / (1 + np.exp( - (X.dot(self.w) + self.b ) ))

        Y_pred = np.where( Y_pred > 0.5, 1, 0)

        return Y_pred


# In[ ]:




