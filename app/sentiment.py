from skllm import ZeroShotGPTClassifier
from skllm.datasets import get_classification_dataset
from skllm.config import SKLLMConfig
SKLLMConfig.set_openai_key("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")
SKLLMConfig.set_openai_org("Personal")


def sentiment_analysis(text,labels):
    clf = ZeroShotGPTClassifier()
    clf.fit(None, labels)
    print(text)
    label = clf.predict(text)
    print(label)
    print(len(label))
    return label