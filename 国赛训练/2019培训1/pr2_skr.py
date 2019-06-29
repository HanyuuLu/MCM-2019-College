from sklearn import linear_model
clf = linear_model.LinearRegression()
# x = [[t.x1,t.x2,t.x3,t.x4,t.x5] for t in self.trainingTexts]
# y = [t.human_rating for t in self.trainingTexts]
x = [[1,2,3,4,5], [2,2,4,4,5], [2,2,4,4,1]] 
x=[[1,2,2],[2,2,2],[3,4,4],[4,4,4],[5,5,1]]
y = [1,2,3,4,5]
aa = clf.fit(x,y)
print(aa)
regress_coefs = clf.coef_
regress_intercept = clf.intercept_    
pass