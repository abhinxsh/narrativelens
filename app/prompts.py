def get_bias_prompt(article):
    with open("prompts/bias_prompt.txt", "r") as f:
        template = f.read()
    return template.replace("{article}", article)

def get_reframe_prompt(article):
    with open("prompts/reframe_prompt.txt","r") as f:
        template = f.read()
    return template.replace("{article}", article)
