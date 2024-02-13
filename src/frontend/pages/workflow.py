from src.backend.utils.database import SQLiteDatabase
from src.backend.actioner import Actioner
import json

def workflow(userQuery):
    # get the database
    db = SQLiteDatabase('databases/crm_refined.sqlite3')
    # create an actioner object    
    actioner = Actioner(db)

    # get requirements from the actioner
    requirements = actioner.get_requirements(userQuery)

    # for each of the requirements get the required action
    for requirement in requirements:
        action = actioner.get_action(requirement, userQuery)
        
        # can only use them for the sql generator if its a success
        if json.loads(action)['status'] == 'success':
            # pass the right things to the sql generator
            pass

        # pass actions to the sql generator

        # pass data, query, and actioner parameters to the visualisation

        # go to new page to show plot? allow a keep and delete
        # show code
        # show sql
            
    # button to allow the user to accept or remove --> a button 

    # show the answer
    # st.pyplot(plot)






def createVisualisation(action):
    graph_type = action['graph_type']
    if graph_type == PieChart.getChartName():
        # pie chart object
        # get stuff from actioner
        pass
    elif graph_type == BarChart.getChartName():
        # bar chart object
        pass
    elif graph_type == LineChart.getChartName():
        # line chart object
        pass
    else:
        # other
        pass