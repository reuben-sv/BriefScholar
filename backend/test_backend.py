from backend.modules.chatbot import PaperChatbot
from backend.modules.simplifier import PaperSimplifier

sample_text = """
This paper proposes a machine learning-based method for detecting plant diseases
from leaf images. The model uses convolutional neural networks and is evaluated
on a dataset of labeled plant leaf images. The proposed system improves accuracy
and reduces manual effort in disease identification.
"""

simplifier = PaperSimplifier()
chatbot = PaperChatbot()

print("SUMMARY:")
print(simplifier.summarize_paper(sample_text))

print("\nCHATBOT:")
print(chatbot.answer_question("What method is used in this paper?", sample_text))
