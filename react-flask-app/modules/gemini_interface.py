import google.generativeai as genai
import os
import requests
import PyPDF2
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip




genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

# converts book pdf to text
def pdf_to_text(pdf_path, output_txt):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    with open(output_txt, 'w') as text_file:
        text_file.write(text)

    return text

# makes a summary of the text given a .txt of the book
def make_summary(text):
    response = model.generate_content(["Given the following story, generate a 6-part summary. I need the six most important parts of the story that are most critical to the plot. If any part is explicit in any way, don't use that. If character names are present, do not include in the summary. However, still describe the character's gender and visual appearance. I want a description of the scene that anyone could understand. Don't use bullet points, just provide me each of the parts on a new line. Don't give system responses or give titles to the sections. The story is as follows: ", text])
    
    return response.text

# makes a script for runway based on the summary
def make_script(summary):
    script = model.generate_content("Given the following summary, generate 2 sentences for each part of the summary. The sentences should be purely descriptive and not contain any character names. Describe any character's appearance with very specific details, and make sure the details are the same throughout all summary parts. It should have subject, action (what the subject is doing, adjectives work well here, i.e. walking angrily, dancing happily), setting/mood (the location, include emotional ideas about the overall mood, i.e. a dusty motel, a busy city street, stormy clouds), shot (wide angle, close up, long shot, FPV, snorricam), style (reinforce the mood, i.e. Cinematic film, 80's Action Movie, add color grading ideas) for each part of the summary. Do not include any system responses in your response, and provide a new line between each part. Each part should be able to be interpreted on its own without needing context from other parts. Here is the template you should use: [Camera type/shot], [Main subject], [Subject action], [Camera movement], [Lighting/atmosphere], [Cinematographer/Visual Style], [Mood/emotional tone]. An example would be like: Low-angle tracking shot with a 35mm lens, capturing a hooded figure standing alone in a graffiti-covered tunnel, illuminated by the golden light streaming through the ceiling windows. The camera slowly tracks forward, following the reflections of the tunnel’s bright colors on the wet pavement below. As the figure remains still, the camera moves closer, revealing the moody atmosphere created by the contrast of vivid graffiti and deep shadows. Smoke drifts through the air, adding a sense of mystery and isolation, atmospheric compositions. The scene conveys a feeling of urban solitude and quiet intensity. The summary is as follows: " + summary)
    
    return script.text

# generates an image for runway based on the script line
def generate_image(prompt_file, line):
    with open(prompt_file, "r") as file:
        prompt = file.readlines()[line]

    result = imagen.generate_images(
        prompt=prompt,
        number_of_images=1,
        safety_filter_level="block_only_high",
        person_generation="allow_adult",
        aspect_ratio="16:9"
    )

    # save to /react-flask-app/data/images/image_{line}.png
    image_path = os.path.join(os.path.dirname(prompt_file), f"image_{line}.png")
    result.images[0].save(image_path)

    return image_path

# generates captions for the movie trailer based on the summary
def generate_captions(summary_file):
    with open(summary_file, "r") as file:
        summary = file.read()

    captions = model.generate_content(["I am going to give you the summary of a book, which has been used to create a movie trailer. Generate about movie-trailer like captions for each part of the summary. The captions should be exciting and engaging, and should make the viewer want to watch the movie. Do not include any system responses in your response, and provide a new line between each part. There should be 6 parts.  Here is the summary: ", summary], safety_settings="block_none")

    return captions.text


# generates a .srt file for the captions
def create_srt(txt_file, output_path = "/react-flask-app/data/captions/", output_srt="captions.srt"):
    from datetime import datetime, timedelta

    # Settings based on 30-second video with each caption lasting 5 seconds
    start_time = "00:00:00,000"
    duration = 5  # Each caption lasts 5 seconds

    # Read captions from the text file
    with open(txt_file, "r") as file:
        captions = [line.strip() for line in file if line.strip()]

    # Initialize variables for generating .srt content
    time_format = "%H:%M:%S,%f"
    current_time = datetime.strptime(start_time, time_format)
    srt_entries = []

    for index, caption in enumerate(captions, start=1):
        # Start and end timestamps for each caption
        start_timestamp = current_time.strftime(time_format)[:-3]
        end_time = current_time + timedelta(seconds=duration)
        end_timestamp = end_time.strftime(time_format)[:-3]

        # Append formatted .srt entry
        entry = f"{index}\n{start_timestamp} --> {end_timestamp}\n{caption}\n\n"
        srt_entries.append(entry)

        # Update current time for the next caption
        current_time = end_time

    # Write the .srt content to a file
    with open(os.path.join(output_path, output_srt), "w") as file:
        file.writelines(srt_entries)
    
    return os.path.join(output_path, output_srt)


# burns subtitles onto the trailer
def burn_subtitles(video_path, subtitle_path, output_path):
    video_clip = VideoFileClip(video_path)

    def generator(txt):
        return TextClip(txt, font="Helvetica", fontsize=50, color="white", stroke_color = "black", method='label', size=video_clip.size)

    sub_clip = SubtitlesClip(subtitle_path, generator)

    result = CompositeVideoClip([video_clip, sub_clip])

    result.write_videofile(output_path, fps=video_clip.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    return output_path
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

if __name__ == "__main__":

    # test the generate_captions function
    base_path = "/Users/frankchang/Desktop/code/aiatl/react-flask-app"
    summary = os.path.join(base_path, "data/summary2.txt")

    captions = generate_captions(summary)

    # save captions to a file
    #with open(os.path.join(base_path, "data/captions/captions.txt"), "w") as file:
        #file.write(captions)

    create_srt(os.path.join(base_path, "data/captions/captions.txt"), os.path.join(base_path, "data/captions/captions.srt"))

    print("Subtitles created at data/captions/captions.srt")

    burn_subtitles("/Users/frankchang/Desktop/code/aiatl/OUT/gatsby/gatsby_trailer.mp4", os.path.join(base_path, "data/captions/captions.srt"), os.path.join(base_path, "data/videos/video_with_captions.mp4"))

    print("Video with subtitles created at data/videos/video_with_captions.mp4")


