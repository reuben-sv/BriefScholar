import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import InsightsTab from "./components/tabs/InsightsTab";
import VivaTab from "./components/tabs/VivaTab";
import ChatTab from "./components/tabs/ChatTab";
import { mockSummary, mockVivaQuestions } from "./data/mockData";

export default function App() {
	const [activeTab, setActiveTab] = useState("insights"); // Tracks 'insights' | 'viva' | 'chat'
	const [uploadedFile, setUploadedFile] = useState(null);
	const [isProcessing, setIsProcessing] = useState(false);

	// Chat States for the RAG Frame
	const [chatMessages, setChatMessages] = useState([
		{
			sender: "ai",
			text: "Hello Sarah. I have indexed 'Attention Is All You Need'. Ask me anything about its methodology, datasets, or claims. (Grounded RAG guardrails enabled).",
		},
	]);
	const [inputMessage, setInputMessage] = useState("");

	// Handles client-side PDF metadata layout evaluation (PRD 3.1)
	const handleFileUpload = (e) => {
		const file = e.target.files[0];
		if (file && file.type === "application/pdf") {
			if (file.size > 50 * 1024 * 1024) {
				alert("File exceeds the 50MB limit specified in requirements.");
				return;
			}
			setIsProcessing(true);
			setUploadedFile(file);
			//
			// backend logic would go here to send the file to the server and receive processing status updates (PRD 3.1.3)
			//
			setTimeout(() => {
				setIsProcessing(false);
			}, 1500);
		} else {
			alert("Please upload a valid PDF document.");
		}
	};

	const handleSendMessage = (e) => {
		e.preventDefault();
		if (!inputMessage.trim()) return;

		const userMsg = inputMessage;
		setChatMessages((prev) => [...prev, { sender: "user", text: userMsg }]);
		setInputMessage("");

		setTimeout(() => {
			//
			// this is where the message would be sent to the backend for processing, and the response would be handled accordingly.
			//
			const lowerQuery = userMsg.toLowerCase();
			setChatMessages((prev) => [
				...prev,
				{
					sender: "ai",
					text: "I am unable to answer this query. The requested information regarding software code implementations or project budget metrics is missing from the underlying PDF document framework.",
					isGuardrail: true,
				},
			]);
		}, 800);
	};

	return (
		<div className="app-container">
			{/* Structural Navigation Column */}
			<Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

			{/* Main Analytical Space */}
			<main className="main-area">
				{/* Persistent Ingestion Header */}
				<Header
					uploadedFile={uploadedFile}
					isProcessing={isProcessing}
					handleFileUpload={handleFileUpload}
				/>

				{/* Dynamic Context Viewport */}
				<div className="workspace">
					{activeTab === "insights" && <InsightsTab summary={mockSummary} />}

					{activeTab === "viva" && <VivaTab questions={mockVivaQuestions} />}

					{activeTab === "chat" && (
						<ChatTab
							messages={chatMessages}
							input={inputMessage}
							setInput={setInputMessage}
							onSend={handleSendMessage}
						/>
					)}
				</div>
			</main>
		</div>
	);
}
