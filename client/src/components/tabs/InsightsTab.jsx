import React from "react";

export default function InsightsTab({ summary }) {
	console.log("InsightsTab received summary:", summary);
	return (
		<div className="content-wrapper">
			<div className="card">
				<span className="badge badge-primary">Abstractive Brief</span>
				<h2 className="card-title">{summary.title}</h2>
				<p className="card-subtitle">{summary.authors}</p>
				<hr className="divider" />
				<p className="paragraph">{summary.abstract}</p>
			</div>

			<div className="card">
				<h3
					style={{
						fontSize: "0.875rem",
						color: "var(--text-muted)",
						marginBottom: "1rem",
						textTransform: "uppercase",
					}}>
					Key Technical Contributions
				</h3>
				<ul className="list">
					{summary.contributions.map((contribution, index) => (
						<li key={index} className="list-item">
							<div className="list-number">{index + 1}</div>
							<span className="paragraph">{contribution}</span>
						</li>
					))}
				</ul>
			</div>
		</div>
	);
}
