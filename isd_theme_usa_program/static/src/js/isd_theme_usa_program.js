/** @odoo-module **/

// USA Program Theme Interactive Scripts for Odoo 18

const usaProgramData = [
    {
        name: 'High School Dual Diploma',
        icon: '♧',
        desc: 'Explore a U.S.-aligned high school curriculum and dual-diploma pathway.',
        meta: 'Online courses · Requirements apply',
        details: 'The High School Courses / Dual Diploma Program prepares international students for U.S. university placement. Course selection, graduation requirements, and eligibility can be customized to individual student pathways.'
    },
    {
        name: 'Academic English',
        icon: 'A',
        desc: 'Build academic English skills while learning about American culture and customs.',
        meta: 'Digital course · Levels described in brochure',
        details: 'Academic English builds language confidence through recorded and interactive lessons on U.S. academic standards, college essay writing, and cultural adaptation.'
    },
    {
        name: 'Pathway Program',
        icon: '⌂',
        desc: 'Prepare for academic study, career exploration, and university applications.',
        meta: 'Six-month program stated in brochure',
        details: 'A focused six-month preparatory pathway covering academic readiness, college admission prep, and career orientation before entering a U.S. college campus.'
    },
    {
        name: 'CTE Courses',
        icon: '▣',
        desc: 'Explore Career & Technical Education courses related to U.S. industry certification.',
        meta: 'Course and certification details vary',
        details: 'Industry-aligned Career & Technical Education courses providing recognized foundation credits and practical career skills in high-demand fields.'
    },
    {
        name: 'American University Placement',
        icon: '✈',
        desc: 'Explore university options and support for application and enrollment.',
        meta: 'U.S. post-secondary education',
        details: 'End-to-end guidance from school matching across 100+ institutions, application filing, timeline management, F-1 visa interview coaching, to pre-departure orientation.'
    }
];

function initUsaProgramInteractions() {
    const backdrop = document.getElementById('usaModalBackdrop');
    const content = document.getElementById('usaModalContent');
    if (!backdrop || !content) return;

    function closeModal() {
        backdrop.classList.remove('show');
        document.body.style.overflow = '';
    }

    function openModal(type, extra) {
        backdrop.classList.add('show');
        document.body.style.overflow = 'hidden';

        if (type === 'program') {
            const p = usaProgramData[extra] || usaProgramData[0];
            content.innerHTML = `
                <div class="usa-eyebrow">Explore a Program</div>
                <h2>${p.name}</h2>
                <p class="modal-lead">${p.details}</p>
                <div style="background:#f4f7fb; border-radius:10px; padding:15px; margin-bottom:20px; font-size:13px; color:#556987">
                    <b>Program Status:</b> Currently accepting candidate consultations for upcoming academic intakes.
                </div>
                <button class="btn-usa-primary" data-usa-open="guidance" data-usa-interest="${p.name}">Ask About This Program →</button>
            `;
            return;
        }

        if (type === 'partners') {
            content.innerHTML = `
                <div class="usa-eyebrow">Global Partner Network</div>
                <h2>Find Support in Your Region</h2>
                <p class="modal-lead">Search by country or region to connect with authorized coordinators and partner offices.</p>
                <div class="partner-filter-box">
                    <input id="partnerSearchInput" placeholder="Enter your country or city…">
                    <select id="partnerRegionSelect">
                        <option value="">All Regions</option>
                        <option>Americas</option>
                        <option>Europe</option>
                        <option>Asia-Pacific</option>
                        <option>Middle East & Africa</option>
                    </select>
                </div>
                <div id="partnerListContainer" style="display:grid; gap:12px; margin-bottom:20px">
                    <div class="partner-result-card">
                        <div class="partner-logo-box">USA</div>
                        <div>
                            <h3 id="partnerPromptTitle">Central Admission Office</h3>
                            <p id="partnerPromptDesc">Tell us where you are based and our regional counselor will assist you.</p>
                        </div>
                    </div>
                </div>
                <button class="btn-usa-primary" data-usa-open="guidance" data-usa-interest="Regional Partner Inquiry">Request Help in My Region →</button>
            `;
            return;
        }

        if (type === 'partner') {
            content.innerHTML = `
                <div class="usa-eyebrow">Partner With Us</div>
                <h2>Discuss an Institutional Partnership</h2>
                <p class="modal-lead">Share your agency or school profile to explore student referral and dual program collaboration.</p>
                <form id="usaPartnerForm">
                    <div class="form-grid-layout">
                        <div class="field-group">
                            <label>Organization name *</label>
                            <input required name="org" placeholder="Your agency or school">
                        </div>
                        <div class="field-group">
                            <label>Official Email *</label>
                            <input required type="email" name="email" placeholder="contact@organization.com">
                        </div>
                        <div class="field-group">
                            <label>Country / Territory *</label>
                            <input required name="country" placeholder="e.g. Vietnam, Japan, Korea...">
                        </div>
                        <div class="field-group">
                            <label>Organization Type</label>
                            <select name="type">
                                <option>Education Agency</option>
                                <option>High School / K-12</option>
                                <option>College / University</option>
                                <option>Government / NGO</option>
                            </select>
                        </div>
                        <div class="field-group field-full">
                            <label>Programs or markets of interest</label>
                            <textarea name="details" placeholder="Briefly introduce your organization and student profile..."></textarea>
                        </div>
                    </div>
                    <button class="btn-usa-primary" style="margin-top:20px" type="submit">Submit Partnership Interest →</button>
                    <div class="demo-result-box" id="partnerFormResult">
                        ✓ Cảm ơn bạn! Thông tin đăng ký đối tác đã được ghi nhận thành công trên giao diện mẫu.
                    </div>
                </form>
            `;
            return;
        }

        // Default: Guidance modal
        const selectedInterest = extra || '';
        content.innerHTML = `
            <div class="usa-eyebrow">Personalized Guidance</div>
            <h2>Tell Us About Your Goals</h2>
            <p class="modal-lead">Get connected with an academic counselor to plan your U.S. study pathway.</p>
            <form id="usaGuidanceForm">
                <div class="form-grid-layout">
                    <div class="field-group">
                        <label>Full name *</label>
                        <input required name="name" placeholder="Nguyễn Văn A">
                    </div>
                    <div class="field-group">
                        <label>Email address *</label>
                        <input required type="email" name="email" placeholder="you@example.com">
                    </div>
                    <div class="field-group">
                        <label>Country where you live *</label>
                        <input required name="country" placeholder="Vietnam">
                    </div>
                    <div class="field-group">
                        <label>Preferred Consultation</label>
                        <select name="support">
                            <option>Online consultation (Zoom / Meet)</option>
                            <option>In-person consultation</option>
                            <option>Email & WhatsApp / Zalo</option>
                        </select>
                    </div>
                    <div class="field-group field-full">
                        <label>Program of interest</label>
                        <select name="program" id="usaInterestSelect">
                            <option value="">I'm exploring multiple options</option>
                            ${usaProgramData.map(p => `<option value="${p.name}">${p.name}</option>`).join('')}
                            <option value="University Placement">American University Placement</option>
                            <option value="Find a local partner">Find a local partner</option>
                        </select>
                    </div>
                    <div class="field-group field-full">
                        <label>Your questions or academic background</label>
                        <textarea name="message" placeholder="Current grade, GPA, target intake, or specific questions..."></textarea>
                    </div>
                </div>
                <button class="btn-usa-primary" style="margin-top:20px" type="submit">Request Guidance →</button>
                <div class="demo-result-box" id="guidanceFormResult">
                    ✓ Cảm ơn bạn! Yêu cầu tư vấn của bạn đã được tiếp nhận thành công. Chuyên viên tư vấn sẽ liên hệ lại sớm nhất.
                </div>
            </form>
        `;

        if (selectedInterest) {
            setTimeout(() => {
                const sel = document.getElementById('usaInterestSelect');
                if (sel) sel.value = selectedInterest;
            }, 0);
        }
    }

    // Global click listener
    document.addEventListener('click', (e) => {
        const opener = e.target.closest('[data-usa-open]');
        if (opener) {
            e.preventDefault();
            const type = opener.getAttribute('data-usa-open');
            const interest = opener.getAttribute('data-usa-interest');
            openModal(type, interest);
            return;
        }

        const progBtn = e.target.closest('[data-usa-program]');
        if (progBtn) {
            e.preventDefault();
            const idx = parseInt(progBtn.getAttribute('data-usa-program'), 10);
            openModal('program', idx);
            return;
        }

        if (e.target.id === 'usaCloseModal' || e.target === backdrop) {
            closeModal();
        }
    });

    // Forms handling
    document.addEventListener('submit', (e) => {
        if (e.target.id === 'usaGuidanceForm' || e.target.id === 'usaPartnerForm') {
            e.preventDefault();
            const resultBox = e.target.querySelector('.demo-result-box');
            if (resultBox) resultBox.classList.add('show');
            const submitBtn = e.target.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Submitted ✓';
            }
        }
    });

    // Partner search filter
    function updatePartnerFilter() {
        const searchInput = document.getElementById('partnerSearchInput');
        const regionSelect = document.getElementById('partnerRegionSelect');
        const desc = document.getElementById('partnerPromptDesc');
        if (desc && (searchInput || regionSelect)) {
            const q = searchInput ? searchInput.value.trim() : '';
            const r = regionSelect ? regionSelect.value : '';
            if (q || r) {
                desc.textContent = `Showing support options for: ${[q, r].filter(Boolean).join(' · ')}. Click below to connect with a regional coordinator.`;
            } else {
                desc.textContent = 'Tell us where you are based and our regional counselor will assist you.';
            }
        }
    }

    document.addEventListener('input', (e) => {
        if (e.target.id === 'partnerSearchInput' || e.target.id === 'partnerRegionSelect') {
            updatePartnerFilter();
        }
    });
    document.addEventListener('change', (e) => {
        if (e.target.id === 'partnerRegionSelect') {
            updatePartnerFilter();
        }
    });

    // Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
}

// Auto init on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUsaProgramInteractions);
} else {
    initUsaProgramInteractions();
}
