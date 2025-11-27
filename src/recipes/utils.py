#Imports for QuerySet/DataFrame
from django.urls import reverse #For building links in DataFrame
from .models import Recipe  #Access to Recipe model
from .forms import IngredientSearchForm
import pandas as pd

#Chart/Graph imports
from io import BytesIO 
import base64
import matplotlib.pyplot as plt



#Formats a recipe QuerySet into pandas DataFrame html
def recipe_queryset_to_html(qs):

    #Create DataFrame with selected columns
    recipes_df = pd.DataFrame(qs.values('id','name','ingredients'))
            
    # - - - Format values in DataFrame - - - #

    #Capitalize each word in recipe name
    recipes_df['name'] = recipes_df['name'].str.title() 
    #Create link to recipe detail page
    recipes_df['name'] = recipes_df.apply(
        lambda row: f'<a href="{ reverse("recipes:detail", args=[row["id"]]) }">{row["name"]}</a>',
        axis=1 #This sets the link to each row, 0 sets to column (woldn't work)
    )
    #Format ingredients list
    recipes_df['ingredients'] = (recipes_df['ingredients']
        .str.split(',')
        .apply(lambda items: sorted([i.strip().title() for i in items]))
        .str.join(', ')                
    )

    #Format column names in DataFrame
    recipes_df.rename(columns = {
        'name': 'Recipe Name',
        'ingredients': 'Ingredients'
    }, inplace=True)

    #Create HTML but drop recipe id column (not useful info to user)
    recipes_df_html = recipes_df.drop(columns=['id']).to_html(
        escape=False,
        index=False,
        classes="table table-striped"
    )

    return recipes_df_html





#========== Charting functions for recipes app: ==========

#Generates the chart at the file/byte level
def get_graph():
    #Create BytesIO buffer for image
    buffer = BytesIO()

    #Create a plot with a bytesIO object as a file-like object. Set format to png
    plt.savefig(buffer, format='png')

    #Set cursor to beginning of the stream
    buffer.seek(0)

    #Retrieve content of the file
    image_png = buffer.getvalue()

    #Encode bytes-like object
    graph = base64.b64encode(image_png)

    #Decode to get the string as output
    graph = graph.decode('utf-8')

    #Free up the memory of buffer
    buffer.close()

    return graph


#Determines type of graph/chart to display and sends data to get_graph()
# chart_type: type of chart 
# data: pandas dataframe
def get_chart(chart_type, data, **kwargs):
   #Switch plot backend to AGG (Anti-Grain Geometry) - to write to file
   #AGG is preferred solution to write PNG files
   plt.switch_backend('AGG')

   #Specify figure size
   fig = plt.figure(figsize=(6,3))

   #Generate chart for recipes/views.py based on type:
   if chart_type == 'bar':
       #📊Plot bar chart between user/creator on x-axis and recipe count on y-axis
       plt.bar(data['created_by__username'], data['count'])

   elif chart_type == 'pie':
       #🥧Generate pie chart base on recipes that do/don't include search ingredient
       #Labels show do & don't include, values show number of recipes in each
       plt.pie(data['value'], labels=data['label']) #⬅️Numerical values must be first param!

   elif chart_type == 'line':
       #📉Plot line chart based on difficulty on x-axis and number of recipes for the difficulty on y-axis
       plt.plot(data['difficulty'], data['count'], marker='o')
   
   else:
       print (f'⚠️Unknown chart type : {chart_type}')

   #Specify layout details
   plt.tight_layout()

   #Render the graph to file
   chart = get_graph() 
   return chart