function contact(event) {
    event.preventDefault()
    // const loading = document.querySelector('.modal__overlay--loading')
    // const success = document.querySelector('.modal__overlay--success')
    // loading.classList += " modal__overlay--visible"
    
    emailjs
        .sendForm(
            'service_wp048se',
            'template_si8f8fp',
            event.target,
            'IoiwiKiSBN_lWY9MM'
        ).then(() => {
            // loading.classList.remove("modal__overlay--visible")
            setTimeout(function(){}, 3000)
        }).catch(() => {
            // loading.classList.remove("modal__overlay--visible")
            alert(
                "The email service is temporatily unavailable. Please contact me directly on malidzulfiqar@gmail.com"
            )
        }) 
}