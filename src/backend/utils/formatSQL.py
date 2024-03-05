import re
# import streamlit as st

# takes a dictionary of queries and formats them with some explanation to the user
def formatSQL(queries):
    # display a formatted sql query

    if not any(queries.values()):
        return "No SQL generated."

    explained = "##### These are the following queries that Copilot for Business used to fetch the data...\n\n"
    
    for query in queries:
        # split query by words
        splitByWord = re.split('\s', queries[query])
        # splitByComma = re.split(', |[A-Z]+\s', sql)
        
        if query[0].isupper():
            explained += f'**{query}** was created using the following query: \n\n'
        else:
            explained += f'**{query.capitalize()}** was created using the following query: \n\n'
        
        explained += f'```sql\n{queries[query]}\n```'

        # if a string is a command then show it orange
        # for string in splitByWord:
        #     if string.isupper():
        #         explained += f':orange[{string}] '
        #     else:
        #         explained += string
        #         explained += " "

        # if there is an AS show this to the user
        for i, word in enumerate(splitByWord):
            # if there is an AS phrase
            if word == "AS":
                name = re.match('^[a-zA-Z0-9_.-]*', splitByWord[i + 1])
                
                columns = ""
                for j in range (i - 1, 0, -1):
                    # if there's no comma in the preceding word add it to the column
                    if ',' not in splitByWord[j]:
                        columns = splitByWord[j] + " " + columns
                    else:
                        break

                # columns = re.match('(.*), ^[a-zA-Z0-9_.-]*', sql)

                if name and columns:
                    explained += f'\n\nThe :orange[{name.group(0)}] values are generated from :blue[{columns}]'
        
        explained += "\n\n"
    
    # if placeholder is None:
    #     st.write(explained)
    # else:
    #     placeholder.write(explained)
    
    return explained