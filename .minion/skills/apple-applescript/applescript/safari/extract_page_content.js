// Extract page content
function extractPageContent() {
    const title = document.title;
    const bodyText = document.body.textContent;
    
    return {
        title: title,
        content: bodyText
    };
}
	extractPageContent();