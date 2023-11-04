class ChatGPTClient:
    def __init__(self,
                 model: str,
                 system_prompt: str,
                 **kwargs):
        self.model = model
        self.system_prompt = system_prompt

    def generate(self):
        pass
