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
try:
    df = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    st.write(df.collect())   # instead of dataframe
except Exception as e:
    st.write(e)

st.write(session.sql("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()").collect())
# my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
# st.dataframe(my_dataframe.to_pandas(), use_container_width=True)
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
)
if ingredients_list:
    ingredients_string= ''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '
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


