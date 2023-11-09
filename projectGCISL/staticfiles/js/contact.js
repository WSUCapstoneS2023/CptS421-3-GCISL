function contact(event) {
  event.preventDefault();
  const loading = document.querySelector(".contact__overlay--loading");
  const success = document.querySelector(".contact__overlay--success");
  loading.classList += " contact__overlay--visible";

  emailjs
    .sendForm(
      "service_wp048se",
      "template_si8f8fp",
      event.target,
      "IoiwiKiSBN_lWY9MM"
    )
    .then(() => {
      loading.classList.remove("contact__overlay--visible");
      setTimeout((success.classList += " contact__overlay--visible"), 3000);
    })
    .catch(() => {
      loading.classList.remove("contact__overlay--visible");
      alert(
        "The email service is temporatily unavailable. Please contact me directly on malidzulfiqar@gmail.com"
      );
    });
}
