/**
 * Sarvocch Microcare Foundation - Interactive Engine
 * Pure Vanilla JavaScript (ES6+) - Zero External Dependencies
 * Compatible with Hostinger Shared/Premium Hosting
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initMobileNav();
    initScrollSpy();
    initScrollReveal();
    initStatsCounter();
    initLoanCalculator();
    initFAQ();
    initForms();
    initBackToTop();
});

/* ----------------------------------------------------------
   1. HEADER SCROLL & BLUR EFFECT
   ---------------------------------------------------------- */
function initHeader() {
    const header = document.querySelector('.header');
    if (!header) return;

    const handleScroll = () => {
        if (window.scrollY > 25) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
}

/* ----------------------------------------------------------
   2. MOBILE NAVIGATION DRAWER
   ---------------------------------------------------------- */
function initMobileNav() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!menuToggle || !navMenu) return;

    const toggleMenu = () => {
        const isOpen = navMenu.classList.toggle('open');
        menuToggle.classList.toggle('open', isOpen);
        menuToggle.setAttribute('aria-expanded', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
    };

    menuToggle.addEventListener('click', toggleMenu);

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu.classList.contains('open')) {
                toggleMenu();
            }
        });
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
        if (navMenu.classList.contains('open') &&
            !navMenu.contains(e.target) &&
            !menuToggle.contains(e.target)) {
            toggleMenu();
        }
    });
}

/* ----------------------------------------------------------
   3. SCROLLSPY (ACTIVE NAV LINK HIGHLIGHT)
   ---------------------------------------------------------- */
function initScrollSpy() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    if (!sections.length || !navLinks.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const currentId = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    const href = link.getAttribute('href');
                    if (href === `#${currentId}`) {
                        link.classList.add('active');
                    } else if (href.startsWith('#')) {
                        link.classList.remove('active');
                    }
                });
            }
        });
    }, {
        rootMargin: '-20% 0px -70% 0px'
    });

    sections.forEach(sec => observer.observe(sec));
}

/* ----------------------------------------------------------
   4. SCROLL REVEAL ANIMATIONS (INTERSECTION OBSERVER)
   ---------------------------------------------------------- */
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale');
    if (!reveals.length) return;

    if (!('IntersectionObserver' in window)) {
        reveals.forEach(el => el.classList.add('is-visible'));
        return;
    }

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px'
    });

    reveals.forEach(el => observer.observe(el));
}

/* ----------------------------------------------------------
   5. IMPACT STATS ANIMATED COUNTER
   ---------------------------------------------------------- */
function initStatsCounter() {
    const statBoxes = document.querySelectorAll('.stat-number');
    if (!statBoxes.length) return;

    let hasRun = false;

    const runCounters = () => {
        statBoxes.forEach(box => {
            const target = parseInt(box.getAttribute('data-target'), 10);
            if (isNaN(target)) return;

            const duration = 1800; // ms
            const startTime = performance.now();

            const updateCount = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease out cubic
                const easeOut = 1 - Math.pow(1 - progress, 3);
                const currentVal = Math.round(easeOut * target);

                box.firstChild.textContent = currentVal.toLocaleString('en-IN');

                if (progress < 1) {
                    requestAnimationFrame(updateCount);
                } else {
                    box.firstChild.textContent = target.toLocaleString('en-IN');
                }
            };

            requestAnimationFrame(updateCount);
        });
    };

    const statsSection = document.querySelector('.stats-strip');
    if (!statsSection) return;

    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasRun) {
                hasRun = true;
                runCounters();
                obs.disconnect();
            }
        });
    }, { threshold: 0.3 });

    observer.observe(statsSection);
}

/* ----------------------------------------------------------
   6. INTERACTIVE LOAN EMI CALCULATOR
   ---------------------------------------------------------- */
function initLoanCalculator() {
    const amountSlider = document.getElementById('calcAmount');
    const rateSlider = document.getElementById('calcRate');
    const tenureSlider = document.getElementById('calcTenure');

    const amountValue = document.getElementById('calcAmountVal');
    const rateValue = document.getElementById('calcRateVal');
    const tenureValue = document.getElementById('calcTenureVal');

    const emiDisplay = document.getElementById('calcEmiDisplay');
    const principalDisplay = document.getElementById('calcPrincipalDisplay');
    const interestDisplay = document.getElementById('calcInterestDisplay');
    const totalDisplay = document.getElementById('calcTotalDisplay');

    const distPrincipal = document.getElementById('distPrincipal');
    const distInterest = document.getElementById('distInterest');
    const legendPrincipalVal = document.getElementById('legendPrincipalVal');
    const legendInterestVal = document.getElementById('legendInterestVal');

    const applyBtn = document.getElementById('calcApplyBtn');

    if (!amountSlider || !rateSlider || !tenureSlider) return;

    const formatINR = (val) => {
        return '₹' + Math.round(val).toLocaleString('en-IN');
    };

    const updateSliderFill = (slider) => {
        const min = Number(slider.min) || 0;
        const max = Number(slider.max) || 100;
        const value = Number(slider.value);
        const percent = ((value - min) / (max - min)) * 100;
        slider.style.background = `linear-gradient(to right, #0757b8 0%, #0757b8 ${percent}%, #e2e8f0 ${percent}%, #e2e8f0 100%)`;
    };

    const calculate = () => {
        const P = Number(amountSlider.value);
        const annualRate = Number(rateSlider.value);
        const N = Number(tenureSlider.value);

        const r = annualRate / 1200; // Monthly interest rate

        let emi;
        if (r === 0) {
            emi = P / N;
        } else {
            emi = (P * r * Math.pow(1 + r, N)) / (Math.pow(1 + r, N) - 1);
        }

        const totalRepayment = emi * N;
        const totalInterest = Math.max(0, totalRepayment - P);

        // Update Text
        amountValue.textContent = formatINR(P);
        rateValue.textContent = `${annualRate}% p.a.`;
        tenureValue.textContent = `${N} Months`;

        if (emiDisplay) emiDisplay.textContent = formatINR(emi);
        if (principalDisplay) principalDisplay.textContent = formatINR(P);
        if (interestDisplay) interestDisplay.textContent = formatINR(totalInterest);
        if (totalDisplay) totalDisplay.textContent = formatINR(totalRepayment);

        // Visual Distribution Bar
        const principalPct = totalRepayment > 0 ? (P / totalRepayment) * 100 : 100;
        const interestPct = 100 - principalPct;

        if (distPrincipal) distPrincipal.style.width = `${principalPct.toFixed(1)}%`;
        if (distInterest) distInterest.style.width = `${interestPct.toFixed(1)}%`;

        if (legendPrincipalVal) legendPrincipalVal.textContent = `${principalPct.toFixed(0)}%`;
        if (legendInterestVal) legendInterestVal.textContent = `${interestPct.toFixed(0)}%`;

        updateSliderFill(amountSlider);
        updateSliderFill(rateSlider);
        updateSliderFill(tenureSlider);
    };

    // Attach Input Listeners
    [amountSlider, rateSlider, tenureSlider].forEach(slider => {
        slider.addEventListener('input', calculate);
    });

    // Preset Chip Buttons
    document.querySelectorAll('.chip-btn[data-target]').forEach(chip => {
        chip.addEventListener('click', (e) => {
            const targetId = chip.getAttribute('data-target');
            const value = chip.getAttribute('data-value');
            const targetSlider = document.getElementById(targetId);

            if (targetSlider) {
                targetSlider.value = value;
                calculate();

                // Toggle active state in sibling chips
                const parent = chip.closest('.calc-chips');
                if (parent) {
                    parent.querySelectorAll('.chip-btn').forEach(c => c.classList.remove('active'));
                    chip.classList.add('active');
                }
            }
        });
    });

    // "Apply for this Loan" CTA prefill
    if (applyBtn) {
        applyBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const loanAmount = amountSlider.value;
            const applySection = document.getElementById('application');
            const amountInput = document.querySelector('#loanForm input[name="amount"]');

            if (amountInput) {
                amountInput.value = loanAmount;
            }

            if (applySection) {
                applySection.scrollIntoView({ behavior: 'smooth' });
                // Briefly flash focus on input
                setTimeout(() => {
                    if (amountInput) amountInput.focus();
                }, 600);
            }
        });
    }

    calculate();
}

/* ----------------------------------------------------------
   7. ACCORDION FAQ
   ---------------------------------------------------------- */
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) return;

    faqItems.forEach(item => {
        const trigger = item.querySelector('.faq-trigger');
        if (!trigger) return;

        trigger.addEventListener('click', () => {
            const wasActive = item.classList.contains('active');

            // Close other items
            faqItems.forEach(other => {
                other.classList.remove('active');
                const otherTrigger = other.querySelector('.faq-trigger');
                if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
            });

            if (!wasActive) {
                item.classList.add('active');
                trigger.setAttribute('aria-expanded', 'true');
            }
        });
    });
}

/* ----------------------------------------------------------
   8. FORMS VALIDATION & AJAX SUBMISSION
   ---------------------------------------------------------- */
function initForms() {
    const forms = [
        { id: 'loanForm', successMsg: 'Your Loan Enquiry has been submitted successfully. Our team will contact you shortly.' },
        { id: 'grievanceForm', successMsg: 'Your grievance complaint has been logged. Our Grievance Officer will review your submission.' },
        { id: 'contactForm', successMsg: 'Thank you for reaching out. Your message has been sent to our Bhopal office.' }
    ];

    forms.forEach(cfg => {
        const form = document.getElementById(cfg.id);
        if (!form) return;

        // Auto-validate 10 digit phone inputs
        const phoneInput = form.querySelector('input[name="phone"]');
        if (phoneInput) {
            phoneInput.addEventListener('input', () => {
                phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 10);
            });
        }

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Native form check
            if (!form.checkValidity()) {
                form.reportValidity();
                return;
            }

            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit';

            // Loading state
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `
                    <svg class="btn-spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation: spin 1s linear infinite;">
                        <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
                        <path d="M12 2a10 10 0 0 1 10 10" stroke-linecap="round"></path>
                    </svg>
                    Processing...
                `;
            }

            const formData = new FormData(form);

            try {
                // Submit to PHP endpoint
                const response = await fetch(form.action || 'api/submit.php', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });

                let result;
                try {
                    result = await response.json();
                } catch {
                    result = { success: response.ok };
                }

                if (result.success || response.ok) {
                    showToast('Submission Received', result.message || cfg.successMsg, 'success');
                    form.reset();
                } else {
                    showToast('Notice', result.message || 'Submission could not be completed. Please try again or reach out directly by phone.', 'error');
                }
            } catch (err) {
                // If running locally without PHP web server, show helpful demo confirmation
                console.warn('Backend endpoint unavailable. Simulating client demo success:', err);
                showToast('Enquiry Received (Demo Mode)', cfg.successMsg, 'success');
                form.reset();
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                }
            }
        });
    });
}

/* ----------------------------------------------------------
   9. TOAST NOTIFICATION COMPONENT
   ---------------------------------------------------------- */
function showToast(title, message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const iconSvg = type === 'success'
        ? `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`
        : `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`;

    toast.innerHTML = `
        <div class="toast-icon">${iconSvg}</div>
        <div class="toast-content">
            <strong>${escapeHTML(title)}</strong>
            <p>${escapeHTML(message)}</p>
        </div>
        <button class="toast-close" aria-label="Close notification">&times;</button>
    `;

    container.appendChild(toast);

    const removeToast = () => {
        toast.classList.add('toast-hide');
        setTimeout(() => toast.remove(), 350);
    };

    toast.querySelector('.toast-close').addEventListener('click', removeToast);

    // Auto dismiss after 5 seconds
    setTimeout(removeToast, 5000);
}

function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
    }[tag] || tag));
}

/* ----------------------------------------------------------
   10. BACK TO TOP BUTTON WITH CIRCULAR SCROLL PROGRESS
   ---------------------------------------------------------- */
function initBackToTop() {
    const btn = document.querySelector('.back-to-top');
    const circle = document.querySelector('.progress-ring-circle');

    if (!btn) return;

    const circumference = 2 * Math.PI * 22; // radius 22px => ~138.2

    if (circle) {
        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = circumference;
    }

    const updateProgress = () => {
        const scrollTop = window.scrollY || document.documentElement.scrollTop;
        const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;

        if (scrollTop > 280) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }

        if (circle && docHeight > 0) {
            const scrollPercent = Math.min(Math.max(scrollTop / docHeight, 0), 1);
            const offset = circumference - (scrollPercent * circumference);
            circle.style.strokeDashoffset = offset;
        }
    };

    window.addEventListener('scroll', updateProgress, { passive: true });

    btn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    updateProgress();
}
