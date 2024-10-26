import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")


# generates a 6-line summary of the text
def make_summary(text):
    response = model.generate_content("Given the following story, I need you to generate a summary of the story. I need the 6 most important parts of the story that contain the most action. If character names are present, do not include in the summary. I want a description of the scene that anyone could understand. Just provide me the 6 parts, each on a new line; don't use bullet points. There should be 6 lines total. Don't give system responses or give titles to the sections. Make sure to not give away the end of the story. The story is as follows: " + text)
    return response.text

# generates a script 
def make_script(summary):


if __name__ == "__main__":
    # read the raw text from the book.txt file

    base_path = "/Users/frankchang/Desktop/code/aiatl"
    file_path = os.path.join(base_path, "data/books/book.txt")
    with open(file_path, "r") as file:
        text = file.read()

    # generate the summary
    summary = make_summary(text)

    # write the summary to the summary.txt file in /data/summary.txt
    with open(os.path.join(base_path, "data/summary.txt"), "w") as file:
        file.write(summary)

    print("Summary generated and saved to data/summary.txt")
