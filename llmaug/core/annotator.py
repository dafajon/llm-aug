import openai
import tiktoken
import warnings
from collections import Counter

from ..utils import LabeledInstance


class FewShotAnnotator(object):
    def __init__(self, api_key: str,
                 system_prompt: str,
                 example_pairs: list,
                 randomized_prompting: bool = False,
                 prompt_subsample: float = 1.0,
                 model: str = "gpt-3.5-turbo",
                 token_limit: int = None):
        """
        Few Shot Annotation for Single/Multi Label Text Classification Problems
        """
        openai.api_key = api_key

        self.system_prompt = system_prompt
        self.token_limit = token_limit
        self.randomized_prompting = randomized_prompting
        self.prompt_subsample = prompt_subsample
        self.model = model
        self.example_pairs = example_pairs
        self.tokenizer = tiktoken.encoding_for_model(self.model)
        self.logs = []

    def calculate_input_length(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def check_limits(self, messages: list) -> list:
        length = self.token_limit + 1
        while length > self.token_limit:
            full_text = " ".join([msg.get("content") for msg in messages])
            length = self.calculate_input_length(full_text)
            if length > self.token_limit:
                warnings.warn(
                    "Input full prompt is larger that the prompt limit constraint. Eliminating a user, assistant pair from messages.")
                messages = messages[:-2]

        if not messages:
            raise ValueError("Input is truncated to empty list. Please incrase the limit for max token usage.")

        return messages

    @staticmethod
    def check_instance(instance: LabeledInstance) -> LabeledInstance:
        if isinstance(instance, LabeledInstance):
            return instance
        else:
            raise ValueError("Input should be of type LabeledInstance")

    def build_prompt(self) -> list:
        """Build message from provided example pairs.
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        for instance in self.example_pairs:
            messages += [{"role": "user", "content": instance.text}]
            messages += [{"role": "assistant", "content": " - ".join(instance.labels)}]

        if self.token_limit:
            messages = self.check_limits(messages=messages)

        return messages

    @staticmethod
    def vote(labels: list, majority: bool):
        """Perform voting between annotation results.
        Extract majority if set True else take labels that occur in all results.
        """
        if majority:
            threshold = .5
        else:
            threshold = 1.0

        extracted_labels = [label for label, count in dict(Counter(sum(labels, []))).items() if
                            count / len(labels) >= threshold]

        if not extracted_labels:
            warnings.warn(
                "EmptyLabelWarning: Voting did not return any consensus. Switch to majority=True or be more explicit with your prompt for a more robust behavior.")

        return extracted_labels

    def annotate(self, text: str, n: int = 1, majority_vote: bool = True, **kwargs):
        print("annotating...")
        self.input = self.build_prompt() + [{"role": "user", "content": text}]
        response = openai.ChatCompletion.create(messages=self.input, n=n,
                                                model=self.model, **kwargs)

        output = [choice.get("message").get("content").split(" - ") for choice in response.get("choices")]
        _id = response.get("id")
        usage = response.get("usage").get("total_tokens")

        self.logs.append({"_id": _id, "input": self.input, "output": output, "usage": usage})

        # If there are more than one annotators, perform voting for final output.
        if output:
            if n > 1:
                output = self.vote(output, majority=majority_vote)
            else:
                output = output[0]
        else:
            warnings.warn("EmptyLabelWarning: The model did not return any annotations. Check your prompt and retry.")

        return " - ".join(output)
