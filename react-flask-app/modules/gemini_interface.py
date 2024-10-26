import google.generativeai as genai
import os
import requests
import PyPDF2


genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")


def make_summary(text):
    response = model.generate_content(["Given the following story, generate a 6-part summary. I need the six most important parts of the story that are most critical to the plot. If any part is explicit in any way, don't use that. If character names are present, do not include in the summary. However, still describe the character's gender and visual appearance. I want a description of the scene that anyone could understand. Don't use bullet points, just provide me each of the parts on a new line. Don't give system responses or give titles to the sections. The story is as follows: ", text])
    return response.text

def make_script(summary):

     script = model.generate_content("Given the following summary, generate 2 sentences for each part of the summary. The sentences should be purely descriptive and not contain any character names. Describe any character's appearance with very specific details, and make sure the details are the same throughout all summary parts. It should have subject, action (what the subject is doing, adjectives work well here, i.e. walking angrily, dancing happily), setting/mood (the location, include emotional ideas about the overall mood, i.e. a dusty motel, a busy city street, stormy clouds), shot (wide angle, close up, long shot, FPV, snorricam), style (reinforce the mood, i.e. Cinematic film, 80's Action Movie, add color grading ideas) for each part of the summary. Do not include any system responses in your response, and provide a new line between each part. Each part should be able to be interpreted on its own without needing context from other parts. Here is the template you should use: [Camera type/shot], [Main subject], [Subject action], [Camera movement], [Lighting/atmosphere], [Cinematographer/Visual Style], [Mood/emotional tone]. An example would be like: Low-angle tracking shot with a 35mm lens, capturing a hooded figure standing alone in a graffiti-covered tunnel, illuminated by the golden light streaming through the ceiling windows. The camera slowly tracks forward, following the reflections of the tunnel’s bright colors on the wet pavement below. As the figure remains still, the camera moves closer, revealing the moody atmosphere created by the contrast of vivid graffiti and deep shadows. Smoke drifts through the air, adding a sense of mystery and isolation, atmospheric compositions. The scene conveys a feeling of urban solitude and quiet intensity. The summary is as follows: " + summary)
     return script.text

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w') as text_file:
        text_file.write(text)

    return text


def generate_initial_image(prompt_file):
    # read the first line of the prompt file
    with open(prompt_file, "r") as file:
        prompt = file.readline()

    # generate the initial image

    result = imagen.generate_images(
        prompt=prompt,
        number_of_images=1,
        safety_filter_level="block_only_high",
        person_generation="allow_adult",
        aspect_ratio="16:9"
    )





'''
if __name__ == "__main__":

    base_path = "/Users/frankchang/Desktop/code/aiatl/react-flask-app"
    file_path = os.path.join(base_path, "data/books/hatchet/hatchet- summer reading novel.pdf")
    #file_path = os.path.join(base_path, "data/books/great_gatsby/F. Scott Fitzgerald - The Great Gatsby (1925, Scribner) - libgen.li.pdf")


    pdf_to_text(file_path, os.path.join(base_path, "data/text_hatchet.txt"))
    print("Text extracted and saved to data/text_hatchet.txt")

    # generate the summary

    with open(os.path.join(base_path, "data/text_hatchet.txt"), "r") as file:
        text = file.read()

    summary = make_summary(text)

    # write the summary to the summary.txt file in /data/summary.txt
    with open(os.path.join(base_path, "data/summary_hatchet.txt"), "w") as file:
        file.write(summary)

    print("Summary generated and saved to data/summary_hatchet.txt")


    summary = os.path.join(base_path, "data/summary_hatchet.txt")
    with open(summary, "r") as file:
        summary = file.read()
    # generate the script
    script = make_script(summary)

    # write the script to the script.txt file in /data/script.txt
    with open(os.path.join(base_path, "data/script_hatchet.txt"), "w") as file:
        file.write(script)

    print("Script generated and saved to data/script_hatchet.txt")

    #generate_initial_image(os.path.join(base_path, "data/script2.txt"))
'''