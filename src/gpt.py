import openai
import os
import sys
import util

openai.api_type = "azure"
openai.api_base = "https://personal-blog-writer.openai.azure.com/"
openai.api_version = "2022-12-01"
max_tokens = 4000


def generate_response(input_file, output_dir):
    # defining the system message
    system_message_template = "<|im_start|>system\n{}\n<|im_end|>"
    system_message = system_message_template.format(
        "You are a William Shakespeare style blog writer")

    # create topic text template
    topic_text_template = "Write an blog post in github flavoured markdown with code examples on {}\n{}"
    extracted_dict = util.read_topic_and_content(input_file)
    topic_title = extracted_dict.get("topic_title")
    topic_content = extracted_dict.get("topic_content")

    print(f'Writing blog post on {topic_title}')

    if (topic_title == ""):
        print("Unable to infer the topic name from the given file path, please provide a valid file path.")
        sys.exit()

    if (topic_content == ""):
        print("Unable to read topic from the given file path, please provide a valid file path.")
        sys.exit()

    # creating a list of messages to track the conversation
    messages = [{
        "sender": "user",
        "text": topic_text_template.format(topic_title, topic_content)
    }]

    # TODO:
    # count prompt tokens - this happens automatically with newer version of gpt models
    # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    # prompt_token_count = len(encoding.encode(input_file_content))
    # system_message += system_message_template.format(
    #     "Max Byte pair encoding token length of generated text should not exceed {} tokens".format(max_tokens - prompt_token_count))

    response = openai.Completion.create(
        engine="test",
        prompt=util.create_prompt(system_message, messages),
        temperature=1,
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["<|im_end|>"])

    out_file = os.path.join(output_dir, input_file)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    f = open(out_file, 'w')

    f.write(response.choices[0].text)
