import random

first_name = {
    1: "Thomas",
    2: "John",
    3: "Matthew"
}

middle_name = {
    1: "Maria",
    2: "Ruprecht",
    3: "Jan"
}

last_name = {
    1: "Schmidt",
    2: "Meier",
    3: "Schreiber"
}

def generate_name():
    choose_first_name = random.choice(list(first_name.values()))
    choose_middle_name = random.choice(list(middle_name.values()))
    choose_last_name = random.choice(list(last_name.values()))
    print(f"{choose_first_name} {choose_middle_name} {choose_last_name}")