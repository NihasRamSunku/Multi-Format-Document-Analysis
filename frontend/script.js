document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const skeleton = document.getElementById('skeleton-loader');
    const dashboard = document.getElementById('results-dashboard');
    const errorBanner = document.getElementById('error-banner');
    
    // Dark Mode Toggle
    const themeBtn = document.getElementById('theme-toggle');
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');
    
    // Check local storage for theme
    if(localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
    }

    themeBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        sunIcon.classList.toggle('hidden');
        moonIcon.classList.toggle('hidden');
        localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    });

    let currentAnalysisData = null; // Store for CSV export
    
    // File Upload Handlers
    browseBtn.addEventListener('click', () => fileInput.click());
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    async function handleFile(file) {
        // Reset UI
        errorBanner.classList.add('hidden');
        dashboard.classList.add('hidden');
        dropZone.classList.add('hidden');
        skeleton.classList.remove('hidden');
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('http://127.0.0.1:8000/api/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok || data.error) {
                throw new Error(data.error || 'Failed to process document');
            }
            
            currentAnalysisData = data;
            populateDashboard(data);
            
            // Artificial delay just to let skeleton animation play for a smooth transition
            setTimeout(() => {
                skeleton.classList.add('hidden');
                dashboard.classList.remove('hidden');
                dropZone.classList.remove('hidden');
            }, 500);
            
        } catch (error) {
            skeleton.classList.add('hidden');
            dropZone.classList.remove('hidden');
            errorBanner.textContent = error.message;
            errorBanner.classList.remove('hidden');
        }
    }

    function populateDashboard(data) {
        // Metrics
        if(data.sentiment) {
            document.getElementById('res-sentiment-type').textContent = data.sentiment.type;
            document.getElementById('res-sentiment-score').textContent = `Pol: ${data.sentiment.polarity} | Subj: ${data.sentiment.subjectivity}`;
        }
        
        document.getElementById('res-readability').textContent = data.readability ? data.readability.toFixed(1) : 'N/A';
        document.getElementById('res-word-count').textContent = data.statistics['Total Content Words'] || 0;
        document.getElementById('res-unique-words').textContent = `${data.statistics['Unique Lemmatized Words'] || 0} unique`;

        // Content
        document.getElementById('res-summary').textContent = data.summary;
        document.getElementById('res-highlight').innerHTML = data.highlighted_text_html;
        
        // POS Lists
        const renderList = (id, items) => {
            const ul = document.getElementById(id);
            ul.innerHTML = '';
            items.forEach(([word, count]) => {
                ul.innerHTML += `<li>${word} <span>${count}</span></li>`;
            });
        };
        
        renderList('res-nouns', data.nouns);
        renderList('res-verbs', data.verbs);
        renderList('res-adjectives', data.adjectives);
        renderList('res-adverbs', data.adverbs);
        renderList('res-keywords', data.keywords);

        // Word Cloud
        const wcImg = document.getElementById('res-wordcloud');
        if(data.wordcloud_img) {
            wcImg.src = data.wordcloud_img;
        }
    }

    // Tab Navigation
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.dataset.tab;
            
            tabBtns.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.add('hidden'));
            
            btn.classList.add('active');
            const pane = document.getElementById(`tab-${target}`);
            pane.classList.remove('hidden');
            
            pane.classList.remove('fade-in');
            void pane.offsetWidth;
            pane.classList.add('fade-in');
        });
    });

    // Export PDF
    document.getElementById('export-pdf').addEventListener('click', () => {
        // Unhide all tabs for printing
        tabPanes.forEach(p => p.classList.remove('hidden'));
        window.print();
        // Restore active tab
        const activeTarget = document.querySelector('.tab-btn.active').dataset.tab;
        tabPanes.forEach(p => {
            if (p.id !== `tab-${activeTarget}`) p.classList.add('hidden');
        });
    });

    // Export CSV
    document.getElementById('export-csv').addEventListener('click', () => {
        if (!currentAnalysisData) return;
        
        const data = currentAnalysisData;
        let csvContent = "data:text/csv;charset=utf-8,";
        
        csvContent += "Category,Word,Count\n";
        
        const addItems = (category, items) => {
            items.forEach(([word, count]) => {
                csvContent += `${category},"${word}",${count}\n`;
            });
        };
        
        addItems("Noun", data.nouns);
        addItems("Verb", data.verbs);
        addItems("Adjective", data.adjectives);
        addItems("Adverb", data.adverbs);
        addItems("Keyword", data.keywords);
        
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "nlp_analysis.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
});
