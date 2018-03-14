
# following along with sentdex pandas (for data manipulatio and analysistutorial:

# Part 4:
import quandl
import pandas as pd

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


# Part 7 (Pickling -- lets us avoid the need for a CSV):

main_df = pd.DataFrame()

for abbv in fiddy[0][0][1:]:
    # print(abbv)
    query = "FMAC/HPI_"+str(abbv)
    # Wow this is awesome:
    df = quandl.get(query, authtoken=api_key)

    # df.set_index("Date")

    # print(main_df.empty)
    # print(df.head())

    ## Hmm a tough roadblock -- seems to think index is value??
    # ValueError: columns overlap but no suffix specified: Index(['Value'], dtype='object')
    if main_df.empty:
        main_df = df
    else:
        print('else')
        main_df = main_df.join(df)
#
# print(main_df.head())









# ahoy
