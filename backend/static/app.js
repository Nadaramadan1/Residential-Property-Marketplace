document.addEventListener('DOMContentLoaded', () => {
    // التعامل مع مفاتيح التبديل (Toggles)
    const toggles = document.querySelectorAll('.toggle-input');
    
    toggles.forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            const settingName = e.target.closest('.setting-item').querySelector('.name').innerText;
            const status = e.target.checked ? 'Enabled' : 'Disabled';
            
            console.log(`${settingName} has been ${status}`);
            
            // يمكنك هنا إضافة طلب Fetch لإرسال التحديث للسيرفر مستقبلاً
        });
    });

    // زر تعديل الملف الشخصي (مثال بسيط)
    const editBtn = document.querySelector('.btn-outline');
    editBtn.addEventListener('click', () => {
        alert('Edit Profile mode activated!');
    });

    // زر المشاركة
    const shareBtn = document.querySelector('.btn-primary');
    shareBtn.addEventListener('click', () => {
        if (navigator.share) {
            navigator.share({
                title: 'Julian Sterling Portfolio',
                url: window.location.href
            }).catch(console.error);
        } else {
            alert('Portfolio link copied to clipboard!');
        }
    });
});