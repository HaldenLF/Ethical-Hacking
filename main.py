import string

def password_Strength_Checker():
    password = input("What password do you want to check: \n"
                    "> ")

    upper_case = any([1 if c in string.ascii_uppercase else 0 for c in password])
    lower_case = any([1 if c in string.ascii_lowercase else 0 for c in password])
    special = any([1 if c in string.punctuation else 0 for c in password])
    digits = any([1 if c in string.digits else 0 for c in password])

    char = [ upper_case, lower_case, special, digits]
    length = len(password)

    score = 0

    with open('pswd.txt', 'r') as f:
        common = f.read().splitlines()

    if password in common:
        print("Password found in common list. Score: 0/7")
        exit()

    if length >= 8:
        score += 1
    if length >= 10:
        score += 1
    if length >= 12:
        score += 1
    if length >= 14:
        score += 1

    print(f"Password length is {str(length)}, adding {str(score)} points!")

    if sum(char) > 1:
        score += 1
    if sum(char) > 2:
        score += 1
    if sum(char) > 3:
        score += 1

    print(f"Password has {str(sum(char))} different characters, adding {str(sum(char) -1 )} points!")

    if score < 4:
        print(f"This password is weak! Score: {str(score)} / 7")
    elif score == 4:
        print(f"This password is below average strength! Score: {str(score)} / 7")
    elif 4 < score < 6:
        print (f"This password is average strength! Score: {str(score)} / 7")
    elif score > 6:
        print (f"The password is strong! Score: {str(score)} / 7")

def check_another_password():
    pass

def main():
    print("Welcome to the password checker!")
    userInput = input("Do you want to check if your password is valid?")

    if userInput.lower() == "y" or choice.lower() == "yes":
        password_Strength_Checker()

        