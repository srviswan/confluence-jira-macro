/**
 * JIRA Macro JavaScript Implementation
 */

class JiraMacro {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            jql: options.jql || JIRA_CONFIG.defaultJql,
            fields: options.fields || JIRA_CONFIG.defaultFields,
            maxResults: options.maxResults || JIRA_CONFIG.defaultMaxResults,
            title: options.title || 'JIRA Issues',
            sortBy: options.sortBy || null,
            ...options
        };
        
        this.issues = [];
        this.filteredIssues = [];
        this.currentSort = { field: null, direction: 'asc' };
        this.currentPage = 1;
        this.pageSize = 25;
        
        this.init();
    }
    
    init() {
        this.render();
        this.loadIssues();
    }
    
    render() {
        this.container.innerHTML = `
            <div class="jira-grid-container">
                <div class="jira-grid-header">
                    <h3 class="jira-grid-title">${this.options.title}</h3>
                    <div class="jira-grid-count" id="jira-count">Loading...</div>
                </div>
                <div class="jira-grid-controls">
                    <input type="text" class="jira-search-input" placeholder="Search issues..." id="jira-search">
                    <button class="jira-refresh-btn" id="jira-refresh">↻ Refresh</button>
                </div>
                <div id="jira-content">
                    <div class="jira-loading">
                        <div class="jira-loading-spinner"></div>
                        Loading JIRA issues...
                    </div>
                </div>
            </div>
        `;
        
        this.attachEventListeners();
    }
    
    attachEventListeners() {
        const searchInput = document.getElementById('jira-search');
        const refreshBtn = document.getElementById('jira-refresh');
        
        searchInput.addEventListener('input', (e) => {
            this.filterIssues(e.target.value);
        });
        
        refreshBtn.addEventListener('click', () => {
            this.loadIssues();
        });
    }
    
    async loadIssues() {
        try {
            this.showLoading();
            
            const response = await this.fetchJiraData();
            this.issues = response.issues || [];
            this.filteredIssues = [...this.issues];
            
            this.updateCount();
            this.renderTable();
            
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    async fetchJiraData() {
        const url = `${JIRA_CONFIG.baseUrl}${JIRA_CONFIG.searchEndpoint}`;
        const params = new URLSearchParams({
            jql: this.options.jql,
            fields: this.options.fields.join(','),
            maxResults: this.options.maxResults
        });
        
        // Create basic auth header
        const credentials = btoa(`${JIRA_CONFIG.username}:${JIRA_CONFIG.apiToken}`);
        
        const response = await fetch(`${url}?${params}`, {
            method: 'GET',
            headers: {
                'Authorization': `Basic ${credentials}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: 'cors'
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error(JIRA_CONFIG.errorMessages.authentication);
            } else if (response.status === 400) {
                throw new Error(JIRA_CONFIG.errorMessages.jql);
            } else {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        }
        
        return await response.json();
    }
    
    renderTable() {
        const content = document.getElementById('jira-content');
        
        if (this.filteredIssues.length === 0) {
            content.innerHTML = '<div class="jira-empty">No issues found matching your criteria.</div>';
            return;
        }
        
        const paginatedIssues = this.getPaginatedIssues();
        
        content.innerHTML = `
            <table class="jira-grid-table">
                <thead>
                    <tr>
                        ${this.options.fields.map(field => `
                            <th class="sortable" data-field="${field}">
                                ${FIELD_DISPLAY_NAMES[field] || field}
                            </th>
                        `).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${paginatedIssues.map(issue => this.renderIssueRow(issue)).join('')}
                </tbody>
            </table>
            ${this.renderPagination()}
        `;
        
        this.attachTableEventListeners();
    }
    
    renderIssueRow(issue) {
        return `
            <tr>
                ${this.options.fields.map(field => `
                    <td>${this.renderFieldValue(issue, field)}</td>
                `).join('')}
            </tr>
        `;
    }
    
    renderFieldValue(issue, field) {
        const fieldValue = this.getFieldValue(issue, field);
        
        switch (field) {
            case 'key':
                return `<a href="${JIRA_CONFIG.baseUrl}/browse/${fieldValue}" target="_blank" class="jira-issue-key">${fieldValue}</a>`;
            
            case 'summary':
                return `<div class="jira-issue-summary">${this.truncateText(fieldValue, JIRA_CONFIG.truncateLength)}</div>`;
            
            case 'status':
                const statusColor = STATUS_COLORS[fieldValue] || '#42526E';
                return `<span class="jira-status-badge" style="background-color: ${statusColor}">${fieldValue}</span>`;
            
            case 'priority':
                const priorityColor = PRIORITY_COLORS[fieldValue] || '#8993A4';
                return `
                    <div class="jira-priority-badge">
                        <div class="jira-priority-icon" style="background-color: ${priorityColor}"></div>
                        ${fieldValue}
                    </div>
                `;
            
            case 'assignee':
                if (!fieldValue || fieldValue === 'Unassigned') {
                    return '<span style="color: #6B778C;">Unassigned</span>';
                }
                return `
                    <div class="jira-assignee">
                        <div class="jira-avatar" style="background-color: #0052CC; color: white; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold;">
                            ${fieldValue.charAt(0).toUpperCase()}
                        </div>
                        ${fieldValue}
                    </div>
                `;
            
            case 'updated':
            case 'created':
                return `<div class="jira-date">${this.formatDate(fieldValue)}</div>`;
            
            default:
                return this.truncateText(fieldValue, 50);
        }
    }
    
    getFieldValue(issue, field) {
        const fields = issue.fields;
        
        switch (field) {
            case 'key':
                return issue.key;
            case 'assignee':
                return fields.assignee ? fields.assignee.displayName : 'Unassigned';
            case 'reporter':
                return fields.reporter ? fields.reporter.displayName : 'Unknown';
            case 'status':
                return fields.status ? fields.status.name : '';
            case 'priority':
                return fields.priority ? fields.priority.name : '';
            case 'issuetype':
                return fields.issuetype ? fields.issuetype.name : '';
            case 'project':
                return fields.project ? fields.project.name : '';
            case 'fixVersions':
                return fields.fixVersions ? fields.fixVersions.map(v => v.name).join(', ') : '';
            case 'labels':
                return fields.labels ? fields.labels.join(', ') : '';
            case 'components':
                return fields.components ? fields.components.map(c => c.name).join(', ') : '';
            default:
                return fields[field] || '';
        }
    }
    
    attachTableEventListeners() {
        const headers = document.querySelectorAll('.jira-grid-table th.sortable');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const field = header.dataset.field;
                this.sortIssues(field);
            });
        });
        
        const pageButtons = document.querySelectorAll('.jira-page-btn[data-page]');
        pageButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const page = parseInt(btn.dataset.page);
                this.goToPage(page);
            });
        });
    }
    
    sortIssues(field) {
        const direction = this.currentSort.field === field && this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        
        this.filteredIssues.sort((a, b) => {
            const aValue = this.getFieldValue(a, field);
            const bValue = this.getFieldValue(b, field);
            
            let comparison = 0;
            if (aValue < bValue) comparison = -1;
            else if (aValue > bValue) comparison = 1;
            
            return direction === 'asc' ? comparison : -comparison;
        });
        
        this.currentSort = { field, direction };
        this.currentPage = 1;
        this.renderTable();
        this.updateSortHeaders();
    }
    
    updateSortHeaders() {
        const headers = document.querySelectorAll('.jira-grid-table th');
        headers.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
            if (header.dataset.field === this.currentSort.field) {
                header.classList.add(`sort-${this.currentSort.direction}`);
            }
        });
    }
    
    filterIssues(searchTerm) {
        if (!searchTerm.trim()) {
            this.filteredIssues = [...this.issues];
        } else {
            const term = searchTerm.toLowerCase();
            this.filteredIssues = this.issues.filter(issue => {
                return this.options.fields.some(field => {
                    const value = this.getFieldValue(issue, field).toString().toLowerCase();
                    return value.includes(term);
                });
            });
        }
        
        this.currentPage = 1;
        this.updateCount();
        this.renderTable();
    }
    
    getPaginatedIssues() {
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        return this.filteredIssues.slice(startIndex, endIndex);
    }
    
    renderPagination() {
        const totalPages = Math.ceil(this.filteredIssues.length / this.pageSize);
        
        if (totalPages <= 1) return '';
        
        const startItem = (this.currentPage - 1) * this.pageSize + 1;
        const endItem = Math.min(this.currentPage * this.pageSize, this.filteredIssues.length);
        
        return `
            <div class="jira-pagination">
                <div class="jira-pagination-info">
                    Showing ${startItem}-${endItem} of ${this.filteredIssues.length} issues
                </div>
                <div class="jira-pagination-controls">
                    <button class="jira-page-btn" data-page="${this.currentPage - 1}" ${this.currentPage === 1 ? 'disabled' : ''}>← Previous</button>
                    ${this.renderPageNumbers(totalPages)}
                    <button class="jira-page-btn" data-page="${this.currentPage + 1}" ${this.currentPage === totalPages ? 'disabled' : ''}>Next →</button>
                </div>
            </div>
        `;
    }
    
    renderPageNumbers(totalPages) {
        const pages = [];
        const maxVisible = 5;
        
        let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
        let end = Math.min(totalPages, start + maxVisible - 1);
        
        if (end - start < maxVisible - 1) {
            start = Math.max(1, end - maxVisible + 1);
        }
        
        for (let i = start; i <= end; i++) {
            pages.push(`
                <button class="jira-page-btn ${i === this.currentPage ? 'active' : ''}" data-page="${i}">
                    ${i}
                </button>
            `);
        }
        
        return pages.join('');
    }
    
    goToPage(page) {
        this.currentPage = page;
        this.renderTable();
    }
    
    updateCount() {
        const countElement = document.getElementById('jira-count');
        if (countElement) {
            countElement.textContent = `${this.filteredIssues.length} issues`;
        }
    }
    
    showLoading() {
        const content = document.getElementById('jira-content');
        content.innerHTML = `
            <div class="jira-loading">
                <div class="jira-loading-spinner"></div>
                Loading JIRA issues...
            </div>
        `;
    }
    
    showError(message) {
        const content = document.getElementById('jira-content');
        content.innerHTML = `
            <div class="jira-error">
                <strong>Error:</strong> ${message}
            </div>
        `;
    }
    
    truncateText(text, maxLength) {
        if (!text) return '';
        text = text.toString();
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    }
    
    formatDate(dateString) {
        if (!dateString) return '';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        } catch (e) {
            return dateString;
        }
    }
}

// Utility function to initialize the macro
function initJiraMacro(containerId, options) {
    return new JiraMacro(containerId, options);
}
