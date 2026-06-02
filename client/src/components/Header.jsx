import React from "react";
import { FileUp, Loader2, CheckCircle2 } from "lucide-react";

export default function Header({
	uploadedFile,
	isProcessing,
	handleFileUpload,
}) {
	return (
		<header className="header">
			<label className="upload-label">
				<FileUp size={16} />
				<span>
					{uploadedFile
						? uploadedFile.name
						: "Drag & Drop or click to upload context PDF (Max 50MB)"}
				</span>
				<input type="file" accept=".pdf" onChange={handleFileUpload} />
			</label>

			<div style={{ display: "flex", gap: "1rem" }}>
				{isProcessing && (
					<span className="status-badge status-processing">
						<Loader2 size={14} className="spin" />
						Stripping native margins...
					</span>
				)}
				{uploadedFile && !isProcessing && (
					<span className="status-badge status-success">
						<CheckCircle2 size={14} />
						Layout parsed natively
					</span>
				)}
			</div>
		</header>
	);
}
