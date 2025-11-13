// foundation_cms/campaigns/static/campaigns/js/camo-petition-form.js
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('petitionForm');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            // Disable button during submission
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
            
            try {
                const response = await fetch(window.campaignData.camoEndpoint, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Hide form and show thank you (like FormAssembly)
                    form.style.display = 'none';
                    
                    // Show thank you message with ShareProgress integration
                    showThankYouMessage(data);
                    
                } else {
                    alert(data.message || 'There was an error. Please try again.');
                }
            } catch (error) {
                console.error('Petition submission error:', error);
                alert('There was an error. Please try again.');
            } finally {
                // Re-enable button
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    }
});

function showThankYouMessage(responseData) {
    const thankYouDiv = document.querySelector('.formassembly-petition-thank-you');
    
    if (thankYouDiv) {
        // Create thank you content (similar to petition-thank-you.jsx)
        thankYouDiv.innerHTML = `
            <div class="petition-success">
                <h4>${responseData.message}</h4>
                <p>Your signature has been added to the petition.</p>
                
                <!-- ShareProgress buttons (like legacy) -->
                <div class="share-buttons">
                    ${responseData.share_data.bluesky ? `<div class="${responseData.share_data.bluesky} sp_tw_small"></div>` : ''}
                    ${responseData.share_data.facebook ? `<div class="${responseData.share_data.facebook} sp_fb_small"></div>` : ''}
                    ${responseData.share_data.email ? `<div class="${responseData.share_data.email} sp_em_small"></div>` : ''}
                </div>
                
                <!-- Continue to donation/next steps -->
                <div class="next-actions">
                    <button onclick="showDonationModal()" class="btn btn-primary">
                        Support this campaign
                    </button>
                    <a href="?state=end" class="btn btn-secondary">
                        Skip to end
                    </a>
                </div>
            </div>
        `;
        
        thankYouDiv.style.display = 'block';
        
        // Initialize ShareProgress buttons (like legacy)
        if (window.ShareProgress) {
            window.ShareProgress.init();
        }
    }
}

function showDonationModal() {
    // Trigger donation modal or redirect to donation state
    // This integrates with your existing DonateBanner system
    window.location.href = '?state=signed&donate=true';
}
