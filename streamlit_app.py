# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


name_on_order=st.text_input("Name on Smoothie:")
st.write('Name on your Smoothie will be :', name_on_order)
cnx=st.connection("snowflake")
session= cnx.session()
MY_DATAFRAME=session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.stop()
#st.dataframe(data=MY_DATAFRAME,use_container_width=True)

Ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
     MY_DATAFRAME,
     max_selections=5
     )
if Ingredients_list:
       
  st.write(Ingredients_list)
  st.text(Ingredients_list)

Ingredients_string =''
for fruit_chosen in Ingredients_list:
    Ingredients_string += fruit_chosen + ' '
    st.subheader(fruit_chosen + ' Nutrition Information')
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
    fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
st.write(Ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + Ingredients_string + """','""" + name_on_order + """')"""

#st.write(my_insert_stmt)
time_to_insert=st.button('Submit_order')

if time_to_insert:
        session.sql(my_insert_stmt).collect()
st.success('Your Smoothie is ordered,'+ ' ' + name_on_order + '!', icon="✅")



