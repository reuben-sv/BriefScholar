import React from "react";
import { Award, ShieldAlert, Send } from "lucide-react";

export default function ChatTab({ messages, input, setInput, onSend, isSending }) {
	return (
		<div className="content-wrapper">
			<div className="chat-container">
				<div className="chat-header">
					<span
						style={{
							display: "flex",
							alignItems: "center",
							gap: "0.375rem",
							fontWeight: 600,
							color: "var(--text-secondary)",
						}}>
						<Award size={14} color="var(--primary)" />
						Targeted Retrieval Queries
					</span>
					<span
						style={{
							display: "flex",
							alignItems: "center",
							gap: "0.25rem",
							background: "white",
							padding: "0.25rem 0.5rem",
							borderRadius: "0.375rem",
							border: "1px solid var(--border-color)",
						}}>
						<ShieldAlert size={12} color="#f59e0b" />
						Grounded RAG Constraints On
					</span>
				</div>

				<div className="chat-messages">
					{messages.map((msg, idx) => {
						const rowClass = msg.sender === "user" ? "msg-right" : "msg-left";
						const bubbleClass =
							msg.sender === "user"
								? "bubble-user"
								: msg.isGuardrail
									? "bubble-guardrail"
									: "bubble-ai";

						return (
							<div key={idx} className={`message-row ${rowClass}`}>
								<div className={`message-bubble ${bubbleClass}`}>
									{msg.isGuardrail && (
										<div
											style={{
												display: "flex",
												alignItems: "center",
												gap: "0.25rem",
												fontWeight: 600,
												fontSize: "0.75rem",
												marginBottom: "0.25rem",
											}}>
											<ShieldAlert size={14} /> Guardrail System Warning
										</div>
									)}
									<p>{msg.text}</p>
								</div>
							</div>
						);
					})}
				</div>

				<form onSubmit={onSend} className="chat-form">
					<input
						type="text"
						value={input}
						onChange={(e) => setInput(e.target.value)}
						placeholder={isSending ? "Waiting for answer..." : "Ask a question about the uploaded paper..."}
						className="chat-input"
						disabled={isSending}
					/>
					<button type="submit" className="chat-submit" disabled={isSending}>
						<Send size={16} />
					</button>
				</form>
			</div>
		</div>
	);
}
