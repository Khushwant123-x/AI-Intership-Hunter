document.addEventListener('DOMContentLoaded', () => {
    // State
    let userSkills = [];
    let isUploading = false;
    let isSearching = false;

    // Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const fileStatus = document.getElementById('fileStatus');
    const fileName = document.getElementById('fileName');
    const progressBar = document.getElementById('progressBar');
    const removeFileBtn = document.getElementById('removeFileBtn');

    const skillsSection = document.getElementById('skillsSection');
    const skillsContainer = document.getElementById('skillsContainer');
    const newSkillInput = document.getElementById('newSkillInput');
    const addSkillBtn = document.getElementById('addSkillBtn');
    const searchBtn = document.getElementById('searchBtn');
    const searchLoader = document.getElementById('searchLoader');

    const welcomeView = document.getElementById('welcomeView');
    const loadingView = document.getElementById('loadingView');
    const loadingText = document.getElementById('loadingText');
    const loadingSubtext = document.getElementById('loadingSubtext');
    const resultsView = document.getElementById('resultsView');
    const resultsCount = document.getElementById('resultsCount');
    const queriesTags = document.getElementById('queriesTags');
    const cardsGrid = document.getElementById('cardsGrid');

    // --------------------------------------------------------------------------
    // DRAG AND DROP EVENTS
    // --------------------------------------------------------------------------
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'dragend', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-over');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const dt = e.dataTransfer;
        const file = dt.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });



    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileSelection(file);
        }
    });

    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUpload();
    });

    // --------------------------------------------------------------------------
    // RESUME PARSING / SKILL EXTRACTION
    // --------------------------------------------------------------------------
    function handleFileSelection(file) {
        const isPDF = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
        if (!isPDF) {
            alert('Please upload a valid PDF file.');
            return;
        }

        isUploading = true;
        fileName.textContent = file.name;
        dropZone.classList.add('hidden');
        fileStatus.classList.remove('hidden');
        progressBar.style.width = '0%';

        // Transition main view to loading
        showLoadingState("Parsing Resume & Skills...", "Reading text contents and extracting technical concepts.");

        // Simulate upload animation, then trigger fetch
        let progress = 0;
        const interval = setInterval(() => {
            progress += 10;
            progressBar.style.width = `${progress}%`;
            if (progress >= 90) {
                clearInterval(interval);
                uploadFileToServer(file);
            }
        }, 80);
    }

    function uploadFileToServer(file) {
        const formData = new FormData();
        formData.append('resume', file);

        fetch('/api/extract', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to parse file.');
            }
            return response.json();
        })
        .then(data => {
            progressBar.style.width = '100%';
            userSkills = data.skills || [];
            
            setTimeout(() => {
                showWelcomeState();
                renderSkills();
                skillsSection.classList.remove('hidden');
                isUploading = false;
            }, 300);
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred while extracting skills. Please try again.');
            resetUpload();
            showWelcomeState();
            isUploading = false;
        });
    }

    function resetUpload() {
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        fileStatus.classList.add('hidden');
        skillsSection.classList.add('hidden');
        userSkills = [];
        showWelcomeState();
    }

    // --------------------------------------------------------------------------
    // SKILLS TAGS CONTROLLER
    // --------------------------------------------------------------------------
    function renderSkills() {
        skillsContainer.innerHTML = '';
        userSkills.forEach((skill, index) => {
            const tag = document.createElement('div');
            tag.className = 'skill-tag';
            tag.innerHTML = `
                <span>${skill}</span>
                <span class="remove-tag" data-index="${index}">&times;</span>
            `;
            skillsContainer.appendChild(tag);
        });

        // Add event listeners to delete buttons
        document.querySelectorAll('.remove-tag').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const idx = parseInt(e.target.getAttribute('data-index'));
                userSkills.splice(idx, 1);
                renderSkills();
            });
        });
    }

    // Add new skill
    function addNewSkill() {
        const value = newSkillInput.value.trim();
        if (value && !userSkills.some(s => s.toLowerCase() === value.toLowerCase())) {
            userSkills.push(value);
            renderSkills();
            newSkillInput.value = '';
        }
    }

    addSkillBtn.addEventListener('click', addNewSkill);
    newSkillInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addNewSkill();
        }
    });

    // --------------------------------------------------------------------------
    // INTERNSHIP SEARCH
    // --------------------------------------------------------------------------
    searchBtn.addEventListener('click', () => {
        if (userSkills.length === 0) {
            alert('Please add at least one skill to match internships.');
            return;
        }

        isSearching = true;
        searchLoader.classList.remove('hidden');
        searchBtn.disabled = true;

        showLoadingState(
            "Crawling Internship Listings...",
            "Searching top remote & Indian job platforms via real-time search queries."
        );

        fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ skills: userSkills })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Search failed.');
            }
            return response.json();
        })
        .then(data => {
            renderResults(data);
        })
        .catch(err => {
            console.error(err);
            alert('An error occurred during search. Please try again.');
            showWelcomeState();
        })
        .finally(() => {
            isSearching = false;
            searchLoader.classList.add('hidden');
            searchBtn.disabled = false;
        });
    });

    // --------------------------------------------------------------------------
    // RENDERING SEARCH RESULTS
    // --------------------------------------------------------------------------
    function renderResults(data) {
        const jobs = data.jobs || [];
        const queries = data.queries || [];

        // Hide loader
        loadingView.classList.add('hidden');
        resultsView.classList.remove('hidden');

        // Set counts
        resultsCount.textContent = `We found ${jobs.length} remote and tech internship matches based on your skills`;

        // Render search queries
        queriesTags.innerHTML = '';
        queries.forEach(q => {
            const item = document.createElement('span');
            item.className = 'query-item';
            item.textContent = q;
            queriesTags.appendChild(item);
        });

        // Render job cards
        cardsGrid.innerHTML = '';
        if (jobs.length === 0) {
            cardsGrid.innerHTML = `
                <div class="glass-card" style="text-align: center; padding: 40px; color: var(--text-secondary);">
                    <h3>No internships match your current skills.</h3>
                    <p style="margin-top: 8px; font-size: 13.5px;">Try adding more generic skill terms (like "Python", "React", or "Frontend") to expand the search.</p>
                </div>
            `;
            return;
        }

        jobs.forEach((job, i) => {
            const score = job.score || 0;
            let status = "Low Match";
            let statusClass = "danger";
            
            if (score >= 60) {
                status = "High Match";
                statusClass = "success";
            } else if (score >= 30) {
                status = "Medium Match";
                statusClass = "warning";
            }

            const r = 30; // circle radius
            const circumference = 2 * Math.PI * r;
            const strokeOffset = circumference - (score / 100) * circumference;

            // Group matched and missing tags
            const matchedSkills = job.matched_skills || [];
            // Guess what other skills this job could need
            const allJobSkills = job.skills || [];
            const missingSkills = allJobSkills.filter(s => !matchedSkills.some(ms => ms.toLowerCase() === s.toLowerCase()));

            const card = document.createElement('div');
            card.className = 'glass-card job-card';
            card.style.animationDelay = `${i * 0.1}s`;

            card.innerHTML = `
                <div class="score-gauge">
                    <svg>
                        <circle class="bg-ring" cx="32" cy="32" r="${r}"></circle>
                        <circle class="fill-ring" cx="32" cy="32" r="${r}" style="stroke-dashoffset: ${strokeOffset}; stroke: var(--${statusClass === 'success' ? 'success' : statusClass === 'warning' ? 'warning' : 'danger'})"></circle>
                    </svg>
                    <div class="score-text">
                        <span class="score-num">${Math.round(score)}</span>
                        <span class="score-symbol">%</span>
                    </div>
                </div>

                <div class="job-main-info">
                    <h3>${job.title}</h3>
                    <div class="job-meta-row">
                        <div class="meta-item">
                            <span class="icon">🎯</span>
                            <span>${status}</span>
                        </div>
                        <div class="meta-item">
                            <span class="icon">🌐</span>
                            <span>Remote / Web Listing</span>
                        </div>
                    </div>
                    
                    <div class="skills-comparison">
                        <div class="comparison-row">
                            <div class="row-label">Matched:</div>
                            <div class="comparison-tags">
                                ${matchedSkills.map(s => `<span class="match-skill-tag common">${s}</span>`).join('') || '<span class="match-skill-tag missing">None</span>'}
                            </div>
                        </div>
                        ${missingSkills.length > 0 ? `
                        <div class="comparison-row">
                            <div class="row-label">Desired:</div>
                            <div class="comparison-tags">
                                ${missingSkills.map(s => `<span class="match-skill-tag missing">${s}</span>`).join('')}
                            </div>
                        </div>
                        ` : ''}
                    </div>
                </div>

                <div class="job-action">
                    <a href="${job.link}" target="_blank" rel="noopener noreferrer" class="btn-apply">
                        <span>Apply Now</span>
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="7" y1="17" x2="17" y2="7"></line>
                            <polyline points="7 7 17 7 17 17"></polyline>
                        </svg>
                    </a>
                </div>
            `;
            cardsGrid.appendChild(card);
        });
    }

    // --------------------------------------------------------------------------
    // MAIN STATE ROUTERS
    // --------------------------------------------------------------------------
    function showLoadingState(headerText, subtext) {
        welcomeView.classList.add('hidden');
        resultsView.classList.add('hidden');
        loadingView.classList.remove('hidden');

        loadingText.textContent = headerText;
        loadingSubtext.textContent = subtext;
    }

    function showWelcomeState() {
        loadingView.classList.add('hidden');
        resultsView.classList.add('hidden');
        welcomeView.classList.remove('hidden');
    }
});
