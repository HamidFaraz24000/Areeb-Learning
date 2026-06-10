import re
from collections import Counter

file_name = input("Enter the full file name that will be analysed(including the .txt): ")

try:
    with open (file_name, "r") as file:
        text = file.read().lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)

    words = text.split()

    total_lines = len(text.splitlines())
    total_words = len(text.split())
    total_characters = len(text)
    word_count = Counter(text.lower().split())
    unique_words = len(set(words))

    while True:
          print("\n1: Total Lines")
          print("2: Total Words")
          print("3: Total Characters")
          print("4: Most Frequent Words")
          print("5: Count of Unique Words")
          print("6: Search for a word")
          print("7: Exit")

          choice = input("Choose an option by indicating the number allocacted to it: ")
          if choice == "1":
             print("Total Lines: ", total_lines)
          elif choice == "2":
             print("Total Words: ", total_words)
          elif choice == "3":
             print("Total Characters: ", total_characters)
          elif choice == "4":
             print("Top 10 Most Frequent Words")
             for word, count in word_count.most_common(10):
                 print(word, "-", count)
          elif choice == "5":
             print("Unique Words: ", unique_words)
          elif choice == "6":
              search_word = input("Enter the word you would like to search for: ").lower()
              print(search_word, " appeared - ", word_count[search_word], " times")
          elif choice == "7":
           break
          else:
                print("Invalid Option")

except FileNotFoundError:
    print("The file was not found")