export const mockSummary = {
	title: "Attention Is All You Need",
	authors: "Vaswani et al. (2017)",
	abstract:
		"The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
	contributions: [
		"Introduction of the Transformer architecture, the first sequence transduction model relying entirely on self-attention.",
		"Achieved superior translation quality while being significantly more parallelizable, reducing training time from weeks to days.",
		"Established a new state-of-the-art in English-to-German and English-to-French translation tasks.",
	],
};

export const mockVivaQuestions = [
	{
		id: 1,
		type: "Comprehension",
		question:
			"What is the primary operational difference between the Transformer architecture and traditional RNNs?",
		answer:
			"RNNs process tokens sequentially, creating a bottleneck. Transformers use self-attention to process all tokens simultaneously, enabling massive parallelization.",
	},
	{
		id: 2,
		type: "Comprehension",
		question:
			"Explain the purpose of 'Positional Encoding' as described by the authors.",
		answer:
			"Since the model contains no recurrence or convolution, it has no inherent sense of token order. Positional encodings are added to the input embeddings to inject structural sequence order.",
	},
	{
		id: 3,
		type: "Analytical",
		question:
			"What specific datasets were utilized to evaluate the translation performance, and what were the resulting BLEU scores?",
		answer:
			"Evaluated on the WMT 2014 English-to-German dataset (achieving 28.4 BLEU) and WMT 2014 English-to-French (achieving 41.8 BLEU).",
	},
	{
		id: 4,
		type: "Analytical",
		question:
			"How does the computational complexity per layer compare between Self-Attention and Recurrent layers?",
		answer:
			"Self-Attention is O(n² · d), whereas Recurrent is O(n · d²). When n < d, self-attention layers are computationally faster than recurrent layers.",
	},
	{
		id: 5,
		type: "Critical Thinking",
		question:
			"Under what specific data or sequence length conditions would the O(n²) complexity of self-attention fail?",
		answer:
			"For extremely long sequences, the quadratic memory growth of O(n²) becomes a massive physical hardware bottleneck unless sparse attention versions are used.",
	},
];
