def update_score_file(file_name, score_name, score_time):
    with open(file_name, "r+") as file:
        content = file.readlines()
        file.seek(0)
        file.write(f"{score_name}-{score_time}\n")
        file.writelines(content)
        file.truncate()

# Example: Process multiple files efficiently
file_list = ["abc.txt", "xyz.txt"]
score_name = "Player1"
score_time = "10:30"

for file_name in file_list:
    update_score_file(file_name, score_name, score_time)
