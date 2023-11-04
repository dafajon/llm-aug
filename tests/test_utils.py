from .context import LabeledInstance


def test_labeled_instance():
    txt1 = LabeledInstance("hello world", ["greeting", "benevolent"])
    txt2 = LabeledInstance("we will kill you", ["threat", "evil"])

    assert txt1.text == "hello world"
    assert txt1.labels[0] == "greeting"
    assert txt2.text == "we will kill you"
    assert txt2.labels[1] == "evil"
