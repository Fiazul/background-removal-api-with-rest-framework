import os
import replicate
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_token = os.getenv('REPLICATE_API_TOKEN')
if not api_token:
    api_token = "api token"
client = replicate.Client(api_token=api_token)
def generate_and_save_image(prompt, output_folder):
    input = {
        "prompt": prompt,
        "scheduler": "K_EULER"
    }

    try:
        output = client.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input=input
        )

        image_url = output[0]
        logging.info(f"Generated Image URL: {image_url}")
        filename = prompt.replace(" ", "_") + ".png"
        image_filename = os.path.join(output_folder, filename)
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(image_filename, "wb") as f:
                f.write(image_response.content)
            logging.info(f"Image downloaded and saved as {image_filename}")
            folder_and_file = f"{output_folder}\{filename}"
            print('filename:',folder_and_file)
            return folder_and_file
        else:
            logging.error("Failed to download image")
    except Exception as e:
        logging.error(f"An error occurred: {e}")




