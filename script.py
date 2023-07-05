import json

def add_skills_to_json(input_file, json_file):
    # Read existing skills from the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
        existing_skills = data['skill_patterns']

    # Read new skills from the input text file
    new_skills = []
    with open(input_file, 'r') as file:
        for line in file:
            skill = line.strip()
            if skill:
                words = skill.split()
                skill_dict = [{"LOWER": word.lower()} for word in words]
                new_skills.append(skill_dict)

    # Add new skills to the existing skills
    updated_skills = existing_skills + new_skills

    # Update the data with the new skills
    data['skill_patterns'] = updated_skills

    # Write the updated JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print("Skills added successfully!")

def main():
    input_file = 'skill.txt'  # Replace with the path to your input file
    json_file = 'skill.json'  # Replace with the path to your existing JSON file

    add_skills_to_json(input_file, json_file)

if __name__ == '__main__':
    main()
