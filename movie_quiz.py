# Movie Quiz

# Ask for name
name = input("What is your name? ")

# Movies list
movies = ["Babylon", "The Batman", "Everything Everywhere All At Once", "Aftersun"]

# Scores list
scores = [0, 0, 0, 0]

print(f"\nWelcome to the movie quiz, {name}!")
print("Answer the questions by typing the number of your choice.\n")

# Question 1
print("Question 1 - When you're at a party, what are you most likely to do?")
print("1 - Be the center of attention")
print("2 - Stay mysterious in the corner")
print("3 - Jump between groups of friends")
print("4 - Keep to yourself and observe")
answer = input("Your choice: ")

while answer != "1" and answer != "2" and answer != "3" and answer != "4":
    print("Invalid choice, try again.")
    answer = input("Your choice: ")

if answer == "1":
    scores[0] = scores[0] + 1
elif answer == "2":
    scores[1] = scores[1] + 1
elif answer == "3":
    scores[2] = scores[2] + 1
elif answer == "4":
    scores[3] = scores[3] + 1

# Question 2
print("\nQuestion 2 - Which word best describes your vibe?")
print("1 - Bold")
print("2 - Dark")
print("3 - Chaotic")
print("4 - Reflective")
answer = input("Your choice: ")

while answer != "1" and answer != "2" and answer != "3" and answer != "4":
    print("Invalid choice, try again.")
    answer = input("Your choice: ")

if answer == "1":
    scores[0] = scores[0] + 1
elif answer == "2":
    scores[1] = scores[1] + 1
elif answer == "3":
    scores[2] = scores[2] + 1
elif answer == "4":
    scores[3] = scores[3] + 1

# Question 3
print("\nQuestion 3 - What kind of adventure appeals to you most?")
print("1 - A wild night out")
print("2 - A crime-fighting mission")
print("3 - A reality-bending journey")
print("4 - A quiet trip with family")
answer = input("Your choice: ")

while answer != "1" and answer != "2" and answer != "3" and answer != "4":
    print("Invalid choice, try again.")
    answer = input("Your choice: ")

if answer == "1":
    scores[0] = scores[0] + 1
elif answer == "2":
    scores[1] = scores[1] + 1
elif answer == "3":
    scores[2] = scores[2] + 1
elif answer == "4":
    scores[3] = scores[3] + 1

# Question 4
print("\nQuestion 4 - When life gets tough, how do you handle it?")
print("1 - Push through with energy")
print("2 - Keep your guard up")
print("3 - Embrace the chaos")
print("4 - Think deeply about it")
answer = input("Your choice: ")

while answer != "1" and answer != "2" and answer != "3" and answer != "4":
    print("Invalid choice, try again.")
    answer = input("Your choice: ")

if answer == "1":
    scores[0] = scores[0] + 1
elif answer == "2":
    scores[1] = scores[1] + 1
elif answer == "3":
    scores[2] = scores[2] + 1
elif answer == "4":
    scores[3] = scores[3] + 1

# Question 5
print("\nOne last question...")
print("Question 5 - Where do you prefer to watch movies?")
print("1 - In a theater")
print("2 - At home")
answer = input("Your choice: ")

while answer != "1" and answer != "2":
    print("Invalid choice, try again.")
    answer = input("Your choice: ")

if answer == "1":
    scores[0] = scores[0] + 1
elif answer == "2":
    scores[1] = scores[1] + 1

# Find the highest score
max_score = scores[0]
for score in scores:
    if score > max_score:
        max_score = score

# Collect winners
winners = []
i = 0
while i < 4:
    if scores[i] == max_score:
        winners = winners + [movies[i]]
    i = i + 1

# Count winners
count = 0
for winner in winners:
    count = count + 1

# Final choice (loop until valid)
print("\nDo you want a recommendation, or do you want to see if I'd watch a movie with you based on your answers?")
print("1 - Recommendation")
print("2 - See if I'd watch with you")
final_choice = input("Your choice: ")

while final_choice != "1" and final_choice != "2":
    print("Invalid choice, try again.")
    final_choice = input("Your choice: ")

# Output
if final_choice == "1":
    if count == 1:
        print(f"\nBased on your answers, I recommend you watch {winners[0]}, {name}.")
    else:
        # Join the winners into a single string separated by commas
        winners_str = ""
        i = 0
        while i < 4:  # Loop through the winners array
            if i < count - 1:
                winners_str = winners_str + winners[i] + ", "
            else:
                winners_str = winners_str + winners[i]
            i = i + 1
        print(f"\nBased on your answers, I recommend you watch: {winners_str}, {name}.")
else:
    print(f"\nHere's what I think about watching movies with you, {name}:\n")
    i = 0
    while i < 4:
        movie = movies[i]
        if movie in winners:
            print(f" - {movie}: Yes!! I'd watch that with you!")
        else:
            print(f" - {movie}: Sorry, probably not this one.")
        i = i + 1
