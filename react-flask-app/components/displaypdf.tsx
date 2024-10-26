import React from 'react';


export function DisplayPdf(pdfUrl) {
    return (
        <div>
            {pdfUrl && (
                <iframe
                src={pdfUrl}
                width="1000"
                height="600"
                title="PDF Viewer"
                />
            )}
        </div>
    );
}
