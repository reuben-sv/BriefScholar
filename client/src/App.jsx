import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import InsightsTab from "./components/tabs/InsightsTab";
import VivaTab from "./components/tabs/VivaTab";
import ChatTab from "./components/tabs/ChatTab";
import { mockSummary, mockVivaQuestions } from "./data/mockData";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
	const [activeTab, setActiveTab] = useState("insights"); // Tracks 'insights' | 'viva' | 'chat'
	const [uploadedFile, setUploadedFile] = useState(null);
	const [isProcessing, setIsProcessing] = useState(false);
	const [documentId, setDocumentId] = useState(null);
	const [isSending, setIsSending] = useState(false);
	const [summary, setSummary] = useState(mockSummary);
	const [vivaQuestions, setVivaQuestions] = useState(mockVivaQuestions);

	// Chat States for the RAG Frame
	const [chatMessages, setChatMessages] = useState([
		{
			sender: "ai",
			text: "Upload a research paper PDF, then ask me anything about its methodology, datasets, or claims. Grounded RAG guardrails are enabled.",
		},
	]);
	const [inputMessage, setInputMessage] = useState("");

	// Handles client-side PDF metadata layout evaluation (PRD 3.1)
	const handleFileUpload = async (e) => {
		const file = e.target.files[0];
		if (file && file.type === "application/pdf") {
			if (file.size > 50 * 1024 * 1024) {
				alert("File exceeds the 50MB limit specified in requirements.");
				return;
			}
			setIsProcessing(true);
			setUploadedFile(file);
			setDocumentId(null);

			const formData = new FormData();
			formData.append("file", file);

			try {
				const response = await fetch(`${API_BASE_URL}/upload`, {
					method: "POST",
					body: formData,
				});

				const data = await response.json();

				if (!response.ok) {
					throw new Error(data.detail || "PDF upload failed.");
				}

				setDocumentId(data.document_id);

				const insightsResponse = await fetch(`${API_BASE_URL}/insights`, {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						document_id: data.document_id,
					}),
				});

				const insightsData = await insightsResponse.json();

				if (!insightsResponse.ok) {
					throw new Error(insightsData.detail || "Core insights generation failed.");
				}

				setSummary(insightsData);

				const vivaResponse = await fetch(`${API_BASE_URL}/viva`, {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						document_id: data.document_id,
					}),
				});

				const vivaData = await vivaResponse.json();

				if (!vivaResponse.ok) {
					throw new Error(vivaData.detail || "Viva generation failed.");
				}

				setVivaQuestions(vivaData.questions);
				setChatMessages([
					{
						sender: "ai",
						text: `I indexed "${data.filename}" (${data.characters.toLocaleString()} characters). Ask me a question about this paper.`,
					},
				]);
				setActiveTab("insights");
			} catch (error) {
				setUploadedFile(null);
				setChatMessages((prev) => [
					...prev,
					{
						sender: "ai",
						text: error.message,
						isGuardrail: true,
					},
				]);
			} finally {
				setIsProcessing(false);
			}
		} else {
			alert("Please upload a valid PDF document.");
		}
	};

	const handleSendMessage = async (e) => {
		e.preventDefault();
		if (!inputMessage.trim() || isSending) return;

		if (!documentId) {
			setChatMessages((prev) => [
				...prev,
				{
					sender: "ai",
					text: "Please upload a PDF before asking questions.",
					isGuardrail: true,
				},
			]);
			return;
		}

		const userMsg = inputMessage;
		setChatMessages((prev) => [...prev, { sender: "user", text: userMsg }]);
		setInputMessage("");
		setIsSending(true);

		try {
			const response = await fetch(`${API_BASE_URL}/chat`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					document_id: documentId,
					question: userMsg,
				}),
			});

			const data = await response.json();

			if (!response.ok) {
				throw new Error(data.detail || "Chat request failed.");
			}

			setChatMessages((prev) => [
				...prev,
				{
					sender: "ai",
					text: data.answer,
				},
			]);
		} catch (error) {
			setChatMessages((prev) => [
				...prev,
				{
					sender: "ai",
					text: error.message,
					isGuardrail: true,
				},
			]);
		} finally {
			setIsSending(false);
		}
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
					{activeTab === "insights" && <InsightsTab summary={summary} />}

					{activeTab === "viva" && <VivaTab questions={vivaQuestions} />}

					{activeTab === "chat" && (
						<ChatTab
							messages={chatMessages}
							input={inputMessage}
							setInput={setInputMessage}
							onSend={handleSendMessage}
							isSending={isSending}
						/>
					)}
				</div>
			</main>
		</div>
	);
}
