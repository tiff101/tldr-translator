"""
okay just want you to step out your own goals in your head!!!
input: book title
2x summarised.
output: want it to be summarised.
then, ideally i want you to choose an AUDIENCE
- astrology girl / spiritual
- tech bro
- founder
- domain expert... change the domains??


test criteria and books:
Start With Why
Atomic Habits
How to Influence People
Fundraising


# YEAH OKAY, SO THE FIRST PART THAT I WANT TO TEST!!!
# hey, what do you want to summarise?


# YEAH OKAY! So, the second part!!!
(1) storage!
- I want to improve the actual storage of the "bookshelf"
- bitesized pieces
- also store the image alongside it??

(2) comms and breaking that down
- then conversational guides.

(3) prompt engineering side of things

"""
from api import *



def main():

        choice = input("Enter a book title to summarise: ")
        # choice2 = input("Who is your audience? ")

        # Create and get info about the book.
        call_grok(f"Summarise the book '{choice}' by chapter as directly and firm as possible, focussing on extracting the key points and facts.", temp=0.5)

        # get book + book cover
        current_book = Book(title=choice, summary=message_log[-1])
        current_book.cover = get_book_cover(choice)  # this is a placeholder for the actual image retrieval function
        bookshelf.append(current_book)

        # call_grok(f"Now I'd like you to summarise your previous output yet again into some conversational talking points in a friendly and approachable manner, as if you were talking to a {choice2}. Work with {message_log[-1]}", temp=1)

        # # SHOW THE FINAL OUTPUT
        # print(message_log[-1])


if __name__ == "__main__":
    main()


