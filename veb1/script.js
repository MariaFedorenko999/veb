document.addEventListener('DOMContentLoaded', () => {
    const cakeLinks = document.querySelectorAll('.cake-link');
    const cakeInfos = document.querySelectorAll('.cake-info');

    cakeLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            cakeInfos.forEach(info => {
                info.style.display = 'none';
            });
            const linkId = link.getAttribute('href');
            const infoBlock = document.querySelector(linkId);
            infoBlock.style.display = 'block';
        });
    });
});
