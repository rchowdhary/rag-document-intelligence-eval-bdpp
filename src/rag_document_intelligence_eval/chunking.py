from rag_document_intelligence_eval.models import DocumentChunk, SourceDocument


def chunk_document(document: SourceDocument) -> tuple[DocumentChunk, ...]:
    lines = document.text.splitlines(keepends=True)

    chunks: list[DocumentChunk] = []
    current_lines: list[str] = []
    current_heading: str | None = None

    for line in lines:
        if line.startswith("## "):
            if current_heading is not None:
                chunk_index = len(chunks)
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{document.metadata.document_id}::{chunk_index:03d}",
                        document_metadata=document.metadata,
                        heading=current_heading,
                        text="".join(current_lines),
                        chunk_index=chunk_index,
                    )
                )

                current_lines = []

            current_heading = line[3:].strip()

        current_lines.append(line)

    if current_heading is not None:
        chunk_index = len(chunks)
        chunks.append(
            DocumentChunk(
                chunk_id=f"{document.metadata.document_id}::{chunk_index:03d}",
                document_metadata=document.metadata,
                heading=current_heading,
                text="".join(current_lines),
                chunk_index=chunk_index,
            )
        )

    return tuple(chunks)
