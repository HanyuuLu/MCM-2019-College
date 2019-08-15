import pandas as pd
import pandas_profiling
data = pd.read_csv(u"data (1).csv")
res = data.describe()
profile = data.profile_report(title='Titanic Dataset')
profile.to_file(output_file='result/titanic_report.html')
print(res)
