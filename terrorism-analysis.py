import pandas as pd

# We use only few columns
df = pd.read_excel('globalterrorismdb.xlsx', usecols=[1,2,3,7,8,9,10,11,12,13,14,28,29,34,35,40,41,58,81,82,98,105,106])

df.shape

df.ndim
df.columns

df.head()

df.isnull().sum()

df.info()

df.to_csv('global_terror.csv',header=True,index=False)

df[df['country_txt']=="India"].to_csv('india_terror.csv',header=True,index=False)

# Reading global_terror file
df = pd.read_csv('global_terror.csv')

df['region_txt'].nunique()

df['country_txt'].unique()

df['country_txt'].nunique()

# Year which has maximum attacks
df['iyear'].value_counts()

# region which has maximum attacks
df['region_txt'].value_counts(normalize=True) # get in terms of percentage

# different type of attacks
df['attacktype1_txt'].value_counts()

# country that is most affected 
df['natlty1_txt'].value_counts()




