
# following along with sentdex pandas (for data manipulatio and analysistutorial:

# Part 4:
import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

# api_key = open('quandleapikey.txt', 'r').read()

api_key = 'Zqg1HGvgWxYKXBnBZyyd'

df = quandl.get('FMAC/HPI_AK', authtoken=api_key)

print(df.head())

fiddy = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")

# # this is a dataframe:
# print(fiddy[0])
#
# # first column:
# print(fiddy[0][0])
#
# for abbv in fiddy_states[0][0][1:]:
#     print()



# Part 5:
df1 = pd.DataFrame({'HPI': [80,85,88,85],
                    'Int_rate': [2,3,2,2],
                    'US_GDP':[50,55,65,55]},
                    index=[2001, 2002, 2003, 2004])

df2 = pd.DataFrame({'HPI': [80,85,88,85],
                    'Int_rate': [2,3,2,2],
                    'US_GDP':[50,55,65,55]},
                    index=[2005, 2006, 2007, 2008])

# df3 = pd.DataFrame({'HPI': [80,85,88,85],
#                     'Int_rate': [2,3,2,2],
#                     'Low_tier_HPI':[50,52, 50, 53]},
#                     index=[2001, 2002, 2003, 2004])

df3 = pd.DataFrame({'HPI': [80,85,88,85],
                    'Unemployment': [7,8,9,6],
                    'Low_tier_HPI':[50,52, 50, 53]},
                    index=[2001, 2002, 2003, 2004])


concat = pd.concat([df1, df2])
# shows the annoying NaNs we get:
# concat= pd.concat([df1, df2, df3])

# print(concat)

# appending not recommended because a dataframe isn't a database:
df4 = df1.append(df2)
# if we try to append df3, we get all these NaNs

# print(df4)

s = pd.Series([80, 2, 50], index=['HPI', 'Int_rate', 'US_GDP'])

df5 = df1.append(s, ignore_index= True)

# print(df5)



# Part 6:

# add Int_rate to reduce data duplication:
# sounds suspiciously like a "join":
merge = pd.merge(df1, df2, on=["HPI", "Int_rate"])

# print(merge)

# To ensure they share an index but no conflicts:
df1.set_index("HPI", inplace=True)
df3.set_index("HPI", inplace=True)
join = df1.join(df3)

# print(join)


## ^ Ducked out halfway through that video, pt. 6


# Part 7 (Pickling -- lets us avoid the need for a CSV, and for supervised machine learning):

main_df = pd.DataFrame()


def state_list():
    fiddy = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
    return fiddy[0][0][1:]

def grab_initial_state_data():
    states = state_list()
    prev_abbv = ''
    main_df = pd.DataFrame()
    for ind, abbv in enumerate(fiddy[0][0][1:]):
        if (ind % 2 == 0):
            prev_abbv = abbv


        query = "FMAC/HPI_"+str(abbv)
        # Wow this is awesome:
        df = quandl.get(query, authtoken=api_key)

        # From part 8:
        # df = df.pct_change()
        # Problem because of my column names:
        name = 'Value' + str(abbv)
        # df[name] = (df[name] - df[name][0]) / df[name][0] * 100

        # This correctly grabs first value in each df (i.e. 1975-1-1):
        # print(df['Value'][0])

        ## Hmm a tough roadblock -- seems to think index is value??
        # ValueError: columns overlap but no suffix specified: Index(['Value'], dtype='object')
        if main_df.empty:
            main_df = df
        else:
            # What do you know, we just had to add the thing it was telling us to add....
            # Hmmm but we're only getting the odd-indexed ones, and we're doubling them....
            main_df = main_df.join(df, lsuffix=str(prev_abbv), rsuffix=str(abbv))

    # print(main_df.head())
    # main_df.to_csv('alabama.csv')

    # pickle_out = open('fiddy.pickle', 'wb')
    pickle_out = open('fiddy3.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()


# grab_initial_state_data()


# Hmmmm more problems due to column names....I have a feeling the API changed subtly.
def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df["United States"] = (df["United States"] - df["United States"][0]) / df["United States"][0] * 100
    return df

fig = plt.figure()
ax1 = plt.subplot2grid((1,1),(0,0))



# Soooo much faster:
# pickle_in = open('fiddy.pickle', 'rb')
# HPI_data = pickle.load(pickle_in)
# print(HPI_data)

# Using Pandas' version of pickling:
# HPI_data.to_pickle('pickletest.pickle')
HPI_data2 = pd.read_pickle('fiddy3.pickle')

# print(HPI_data2)




# Part 8: Correlation tables/percent change:

# Modifying cols:
# HPI_data2['TX2'] = HPI_data2['ValueTX'] * 2
# print(HPI_data2[['ValueTX', 'TX2']])
benchmark = HPI_Benchmark()


HPI_data2.plot(ax = ax1)
benchmark.plot(ax = ax1, color='k', linewidth=10)

plt.legend().remove()
plt.show()




# ahoy
