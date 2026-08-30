import os

path = 'js/app.js'
auth_logic = """

/* ── Auth State Management (Nav Update) ────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('auth_token');
    const userName = localStorage.getItem('user_name');
    
    if (token && userName) {
        // Find all Sign In buttons and replace them with Account dropdown/link
        const signinBtns = document.querySelectorAll('a[href="login.html"]');
        
        signinBtns.forEach(btn => {
            if (btn.classList.contains('hide-sm') || btn.classList.contains('btn-ghost')) {
                const isFooter = !btn.classList.contains('hide-sm');
                if (isFooter) {
                    btn.textContent = 'My Account';
                    btn.href = 'account.html';
                } else {
                    const accountHtml = `
                        <div class="account-dropdown" style="position: relative; display: inline-block;">
                            <a href="account.html" class="btn btn-ghost hide-sm" style="display: inline-flex; align-items: center; gap: 8px; text-decoration: none; padding: 6px 12px;">
                                <div style="width:24px; height:24px; background:var(--primary); color:#000; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px;">
                                    ${userName.charAt(0).toUpperCase()}
                                </div>
                                <span>${userName.split(' ')[0]}</span>
                            </a>
                        </div>
                    `;
                    btn.outerHTML = accountHtml;
                }
            }
        });
    }
});
"""

with open(path, 'a', encoding='utf-8') as f:
    f.write(auth_logic)

print("app.js updated.")
