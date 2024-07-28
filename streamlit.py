#!/usr/bin/env python3
import os
import streamlit as st
from api import *
from streamlit_card import card


## Session state (multi-page)
show_expander = False
if 'library' not in st.session_state:
    st.session_state.library = []
if 'current_book_title' not in st.session_state:
    st.session_state.current_book_title = ''
if 'current_book' not in st.session_state:
    st.session_state.current_book = None
if 'summary' not in st.session_state:
    st.session_state.summary = ''

# st.session_state.library = [
#     Book("To Kill a Mockingbird", "A tale of racial injustice and the indomitable spirit of the human spirit.", cover="https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1630483761i/16071764.jpg"),
#     Book("1984", "George Orwell's dystopian novel about totalitarianism."),
#     Book("Animal Farm", "Frank Herbert's masterpiece about the exploitation of animals for food and profit."),
#     Book("The Great Gatsby", "F. Scott Fitzgerald's classic novel about the American Dream."),
#     Book("Pride and Prejudice", "Jane Austen's romantic novel about societal expectations and prejudice."),
#     Book("The Catcher in the Rye", "J.D. Salinger's classic novel about the American Dream."),
#     Book("The Help", "Katherine Arden's romantic novel about the power of love and the importance of community."),
# ]

def add_to_library():
    # add it as a book???
    img_url = get_book_cover(st.session_state.current_book_title)
    book = Book(st.session_state.current_book_title, st.session_state.summary, cover=img_url, headline=headline)
    print('33', book)

    st.session_state.current_book = book
    #library = st.session_state.library.append(book)
    st.session_state.library.append(book)
    print('36', st.session_state.library)
    print('38', len(st.session_state.library))


st.title('TL;DR')

with st.popover("Summarise a book"):
    # st.markdown("Too long, don't wanna read? 👀")
    c11, c12 = st.columns([4,1])
    with c11:
        book_title = st.text_input("Enter a book title to summarise:")
        st.session_state.current_book_title = book_title
    with c12:
        st.text('')
        st.text('')
        if st.button("Go"):
            show_expander = True
            # Get data
            summary = call_grok(f"Summarise the book '{book_title}' by chapter as directly and firm as possible, focussing on extracting the key points and facts.", temp=0.5)
            headline = call_grok(f"Summarise the book '{book_title}' into a single sentence.", temp=0.5)
            print('headline', headline)
            st.session_state.summary = summary

# TEST OUTPUT SECTION
if show_expander:
    with st.expander('See Summary'):
        st.header(st.session_state.current_book_title)
        st.markdown(st.session_state.summary)
        st.button("Add to my library", on_click=add_to_library)


# LIBRARY VIEW    
with st.container():
    st.header("📚 Your Library")
    # populate data
    for i, book in enumerate(st.session_state.library):
        # st.write(book.title)
        # st.write(book.headline)
        # st.image(book.cover)
        card_ = card(
            title=book.title,
            text=book.headline,
            image=book.cover,
            #on_click=lambda: show_details(book)
        )
        
    


    # c1.header("Lean In")
    # c1.image("https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1630483761i/16071764.jpg", use_column_width=True)


