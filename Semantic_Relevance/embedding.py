from transformers import BertTokenizer, BertModel
import numpy as np
import torch

model_checkpoint = 'D:/bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_checkpoint)
model = BertModel.from_pretrained(model_checkpoint)

def get_sentence_embeddings(sentences):
    # 一次性分词并返回张量
    inputs = tokenizer(sentences, return_tensors='pt', padding=True, truncation=True, max_length=512)

    with torch.no_grad():  # 不计算梯度，节省显存
        outputs = model(**inputs)

    # Mean Pooling（带 attention mask 避免 padding 干扰）
    attention_mask = inputs['attention_mask']
    masked_embeddings = outputs.last_hidden_state * attention_mask.unsqueeze(-1)
    sum_embeddings = masked_embeddings.sum(dim=1)
    mean_embeddings = sum_embeddings / attention_mask.sum(dim=1, keepdim=True)

    return mean_embeddings

sentences = [
    "I love machine learning.",
    "I enjoy studying artificial intelligence."
]

# 一次性获取两个句子的 embedding
embeddings = get_sentence_embeddings(sentences).numpy()

def cosine_similarity(vec1, vec2):
    vec1 = vec1.flatten()
    vec2 = vec2.flatten()
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

sim = cosine_similarity(embeddings[0], embeddings[1])
print(f"Cosine similarity: {sim:.4f}")

def sentence_similarity(sentence1, sentence2):
    vec1 = get_sentence_embeddings(sentence1).numpy()
    vec2 = get_sentence_embeddings(sentence2).numpy()
    similarity = cosine_similarity(vec1, vec2)
    return similarity

sentence1 = sentences[0]
sentence2 = sentences[1]
print(sentence_similarity(sentence1, sentence2))