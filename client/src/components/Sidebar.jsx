import React from "react";
import { FileText, HelpCircle, MessageSquare, Layers } from "lucide-react";

export default function Sidebar({ activeTab, setActiveTab }) {
	const navItems = [
		{ id: "insights", label: "Core Insights Brief", icon: FileText },
		{ id: "viva", label: "Viva Prep Panel", icon: HelpCircle },
		{ id: "chat", label: "Conversational Frame", icon: MessageSquare },
	];

	return (
		<aside className="sidebar">
			<div>
				<div className="brand">
					<div className="brand-icon">
						<Layers size={20} />
					</div>
					<div>
						<h1 className="brand-title">BriefScholar</h1>
						<p className="brand-subtitle">Research Simplifier</p>
					</div>
				</div>

				<nav className="nav-menu">
					{navItems.map((item) => {
						const Icon = item.icon;
						return (
							<button
								key={item.id}
								onClick={() => setActiveTab(item.id)}
								className={`nav-btn ${activeTab === item.id ? "active" : ""}`}>
								<Icon size={18} />
								{item.label}
							</button>
						);
					})}
				</nav>
			</div>

			<div className="user-profile">
				<div className="avatar">sX</div>
				<div>
					<p style={{ fontSize: "0.875rem", fontWeight: 600 }}>Synapse-X</p>
					<p style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>
						Thesis Mode Active
					</p>
				</div>
			</div>
		</aside>
	);
}
