/**
 * VIT-ChainVote Frontend Application Logic
 * Handles authentication, API communication, and UI interactions
 */

const API_URL = window.CONFIG?.API_URL || 'http://localhost:5000/api';

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

function showModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
}

// ============================================================================
// ELECTION STATE MONITORING
// ============================================================================

async function updateElectionStatus() {
    try {
        const response = await fetch(`${API_URL}/election/state`);
        const data = await response.json();

        if (data.success) {
            const statusBadge = document.getElementById('electionStatus');
            const state = data.state.toUpperCase();

            statusBadge.className = `status-badge status-${data.state}`;

            const icons = {
                'waiting': '⏸️',
                'live': '🔴',
                'closed': '🔒'
            };

            statusBadge.textContent = `${icons[data.state] || ''} ${state}`;
        }
    } catch (error) {
        console.error('Error fetching election state:', error);
    }
}

// Update status every 3 seconds
setInterval(updateElectionStatus, 3000);
updateElectionStatus();

// ============================================================================
// ADMIN LOGIN
// ============================================================================

function showAdminLogin() {
    showModal('adminLoginModal');
}

document.getElementById('adminLoginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('adminEmail').value.trim();

    try {
        const response = await fetch(`${API_URL}/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();

        if (data.success) {
            // Store admin session
            localStorage.setItem('adminEmail', email);

            // Redirect to admin dashboard
            window.location.href = 'admin.html';
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        alert('❌ Error: ' + error.message);
    }
});

// ============================================================================
// VOTER LOGIN
// ============================================================================

function showVoterLogin() {
    showModal('voterLoginModal');
}

document.getElementById('voterLoginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = document.getElementById('voterEmail').value.trim().toLowerCase();
    const department = document.getElementById('voterDepartment').value;

    if (!email || !department) {
        alert('❌ Please fill in all fields');
        return;
    }

    // Validate VIT email format
    const vitEmailPattern = /^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@vit\.edu$/;
    if (!vitEmailPattern.test(email)) {
        alert('❌ Invalid VIT email format. Use: name.prn@vit.edu');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/voter/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, department })
        });

        const data = await response.json();

        if (data.success) {
            // Store voter session
            localStorage.setItem('voterEmail', email);
            localStorage.setItem('voterDepartment', department);

            // Close login modal and show OTP modal
            closeModal('voterLoginModal');
            showModal('otpModal');

            alert('✅ OTP sent to your email! Check your inbox.');
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        alert('❌ Error: ' + error.message);
    }
});

// ============================================================================
// OTP VERIFICATION
// ============================================================================

document.getElementById('otpForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = localStorage.getItem('voterEmail');
    const otp = document.getElementById('otpCode').value.trim();

    if (!email || !otp) {
        alert('❌ Invalid session or OTP');
        return;
    }

    if (otp.length !== 6 || !/^\d{6}$/.test(otp)) {
        alert('❌ OTP must be exactly 6 digits');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/voter/verify-otp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, otp })
        });

        const data = await response.json();

        if (data.success) {
            // OTP verified - redirect to voting page
            window.location.href = 'voter.html';
        } else {
            alert('❌ ' + data.message);
        }
    } catch (error) {
        alert('❌ Error: ' + error.message);
    }
});

// ============================================================================
// AUTO-FOCUS OTP INPUT
// ============================================================================

document.getElementById('otpCode')?.addEventListener('input', (e) => {
    // Only allow digits
    e.target.value = e.target.value.replace(/\D/g, '');
});

// ============================================================================
// KEYBOARD SHORTCUTS
// ============================================================================

document.addEventListener('keydown', (e) => {
    // Escape key closes modals
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay').forEach(modal => {
            modal.classList.add('hidden');
        });
    }
});

// ============================================================================
// CLICK OUTSIDE TO CLOSE MODAL
// ============================================================================

document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.add('hidden');
        }
    });
});

// ============================================================================
// CONSOLE BRANDING
// ============================================================================

console.log('%c🗳️ VIT-ChainVote', 'font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;');
console.log('%cSecure Blockchain Voting System', 'font-size: 14px; color: #667eea;');
console.log('%cPowered by Proof-of-Work Consensus & Google Gemini AI', 'font-size: 12px; color: #999;');
