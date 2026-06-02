import React from "react";

export default function VivaTab({ questions }) {
	const tiers = ["Comprehension", "Analytical", "Critical Thinking"];

	return (
		<div className="content-wrapper">
			<div
				style={{
					borderBottom: "1px solid var(--border-color)",
					paddingBottom: "1rem",
				}}>
				<h2 className="card-title">Tiered Viva Examination Blueprint</h2>
				<p className="card-subtitle">
					Contextual evaluation matrices tailored across dynamically loaded
					difficulty vectors.
				</p>
			</div>

			{tiers.map((tier) => {
				const filteredQuestions = questions.filter((q) => q.type === tier);
				if (filteredQuestions.length === 0) return null;

				const badgeClass =
					tier === "Comprehension"
						? "badge-comprehension"
						: tier === "Analytical"
							? "badge-analytical"
							: "badge-critical";

				return (
					<div
						key={tier}
						style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
						<div>
							<span className={`badge ${badgeClass}`}>{tier} Tier</span>
						</div>

						{filteredQuestions.map((q) => (
							<div key={q.id} className="viva-q-card">
								<h4 className="viva-q-title">
									<span style={{ color: "var(--text-muted)" }}>Q:</span>
									{q.question}
								</h4>
								<div className="viva-answer-box">
									<p className="viva-answer-label">Suggested Defense Pivot:</p>
									<p className="paragraph" style={{ marginTop: "0.25rem" }}>
										{q.answer}
									</p>
								</div>
							</div>
						))}
					</div>
				);
			})}
		</div>
	);
}
