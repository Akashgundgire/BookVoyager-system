import pandas as pd
import numpy as np


import seaborn as sns
import streamlit as st
tab1, tab2 = st.tabs(["Recommendation","Trending Books"])
with tab1:
    final_rating = pd.read_csv("final_rating.csv")
    st.title("Discover Your Next Favorite Book")
    x=final_rating['User-ID'].value_counts()>200

    final_rating.drop_duplicates(['User-ID','Book-Title'],inplace=True)
    book_pivot=final_rating.pivot_table(columns='User-ID',index='Book-Title',values='num_rating')
    book_pivot.fillna(0,inplace=True)
    from sklearn.metrics.pairwise import cosine_similarity
    score=cosine_similarity(book_pivot)
    final_rating.drop_duplicates(['Book-Title'],inplace=True)
    


    def recommend(book_name):
        recommended_books = []

        try:
            index = np.where(book_pivot.index == book_name)[0][0]
            similar_items = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:6]
            for i in similar_items:
                recommended_books.append(book_pivot.index[i[0]])

            filtered_data = final_rating[final_rating['Book-Title'].isin(recommended_books)]

            for index, row in filtered_data.iterrows():


            # Display small image
                st.markdown(f'<img src="{row["Image-URL-M"]}" alt="Book Cover" style="width:100px; height:150px;">', unsafe_allow_html=True)
                st.write("Book Title:", row['Book-Title'])
                st.write("Book Author:", row['Book-Author'])
                st.write("Year of Publication:", row['Year-Of-Publication'])
                st.write("Publisher:", row['Publisher'])
                st.write("Number of Ratings:", row['num_rating'])
                st.write("-------------------------------")

        except IndexError:
            st.success("That book is not Available .")

# Sidebar with button
    if st.sidebar.button("INFO"):
        st.write(
            "Welcome to the Book Discovery App! 📚✨\n\n"
            "Discovering your favorite book can be an exciting journey. Whether you're into "
            "mysteries, fantasies, or heartwarming stories, this app is designed to help you "
            "find the perfect read. Simply enter a book name in the input box and click 'Recommend'. "
            "Explore the recommendations and who knows, your next favorite book might be just a click away!"
    )
# User input for book name
    book_name_input = st.text_input("Enter Book Name:")
    if st.button("Recommend"):
        recommend(book_name_input)

with tab2:
    st.title("Trending Books")
    x = final_rating[final_rating['num_rating'] > 100].head(50)
    for index, row in x.iterrows():
        st.markdown(f'<img src="{row["Image-URL-M"]}" alt="Book Cover" style="width:100px; height:150px;">',unsafe_allow_html=True)
        st.write("Book Title:", row['Book-Title'])
        st.write("Book Author:", row['Book-Author'])
        st.write("Year of Publication:", row['Year-Of-Publication'])
        st.write("Publisher:", row['Publisher'])
        st.write("Number of Ratings:", row['num_rating'])
        st.write("-------------------------------")
