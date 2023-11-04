from collections import namedtuple

LabeledInstance = namedtuple("LabeledInstance", ["text", "labels"])


class PromptBuilder:
    def __init__(self, system_prompt: str, model: str, problem_type: str):
        self.system_prompt = system_prompt
        self.model = model
        self.builder = self._get_builder(problem_type=problem_type)

    def few_shot_prompt_builder(self, example_pairs, categories=None):
        if categories is None:
            categories = []
        if categories:
            self.system_prompt = self.system_prompt + "\n" + "\n".join(categories)

        if "gpt" in self.model:
            messages = [{"role": "system", "content": self.system_prompt}]
            for instance in example_pairs:
                messages += [{"role": "user", "content": instance.text}]
                messages += [{"role": "assistant", "content": " - ".join(instance.labels)}]

        # TODO: Implement Checks for Token limits based on the specified closed model

    def doc_summarization_prompt_builder(self, doc):
        pass

    def comment_summarization_prompt_builder(self):
        pass

    def augmentation_prompt_builder(self, examples: list, categories: list):
        pass

    def _get_builder(self, problem_type):
        __builders = {"few-shot-annotation": self.few_shot_prompt_builder,
                      "doc-summarization": self.doc_summarization_prompt_builder,
                      "comment-summarization": self.comment_summarization_prompt_builder,
                      "data-augmentation": self.augmentation_prompt_builder}

        builder_fn = __builders.get(problem_type)
        if builder_fn is None:
            raise ValueError("Only valid task types are 'few-shot-annotation', 'doc-summarization',"
                             "'comment-summarization, 'data-augmentation'")
        else:
            return builder_fn
