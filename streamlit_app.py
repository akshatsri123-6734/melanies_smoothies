# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests  
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write(
  """Replace this example with your own code!
  **And if you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your smoothie will be ", name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

# set context
session.sql("USE DATABASE SMOOTHIES").collect()
session.sql("USE SCHEMA PUBLIC").collect()
session.sql("USE WAREHOUSE COMPUTE_WH").collect()

# fetch data
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'),
                                                                     col('SEARCH_ON'))
# display
#st.dataframe(my_dataframe.to_pandas(), use_container_width=True)
#st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
)
if ingredients_list:
    ingredients_string= ''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen+' Nutrition Information')
        smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/watermelon"
        )
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    # st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert=st.button("Submit Order")
    st.write(my_insert_stmt)
    st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered')


