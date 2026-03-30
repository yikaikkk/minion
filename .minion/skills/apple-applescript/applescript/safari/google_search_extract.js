// Extract Google search results
function extractGoogleSearchResults() {
    const results = [];
    const searchResults = document.querySelectorAll('.g');
    
    searchResults.forEach((result, index) => {
        const titleElement = result.querySelector('h3');
        const linkElement = result.querySelector('a');
        const snippetElement = result.querySelector('.VwiC3b');
        
        if (titleElement && linkElement) {
            results.push({
                title: titleElement.textContent,
                url: linkElement.href,
                snippet: snippetElement ? snippetElement.textContent : ''
            });
        }
    });
    
    return results;
}

extractGoogleSearchResults();