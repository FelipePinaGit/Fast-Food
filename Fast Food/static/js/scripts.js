document.addEventListener("DOMContentLoaded", function() {
    const navLinks = document.querySelectorAll('nav ul li a');

    for (const link of navLinks) {
        link.addEventListener('click', function(event) {
            const href = event.currentTarget.getAttribute("href");
            if (href.startsWith("#")) {
                event.preventDefault();
                smoothScroll(href.substring(1));
            }
        });
    }

    function smoothScroll(targetId) {
        const targetElement = document.getElementById(targetId);

        window.scrollTo({
            top: targetElement.offsetTop,
            behavior: "smooth"
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
