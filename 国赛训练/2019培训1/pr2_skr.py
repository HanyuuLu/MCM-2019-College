import csv

from sklearn import linear_model
clf = linear_model.LinearRegression()
# x = [[t.x1,t.x2,t.x3,t.x4,t.x5] for t in self.trainingTexts]
# y = [t.human_rating for t in self.trainingTexts]
x=[[1,2,2],[2,2,2],[3,4,4],[4,4,4],[5,5,1]]
y = [1,2,3,4,5]
aa = clf.fit(x,y)

regress_coefs = clf.coef_
regress_intercept = clf.intercept_   
print(regress_coefs)
print(regress_intercept) 
pass