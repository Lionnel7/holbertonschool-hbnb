async function login(email, password) {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    })
    if (!response) {
      throw new Error("serverError")
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.log(error)
  }
}

document.addEventListener('DOMContentLoaded', () => {
  console.log("loaded");
  
 
  const placeData = {
    host: "John Doe",
    price: "$150",
    description: "A beautiful beach house with amazing views...",
    amenities: ["WiFi", "Pool", "Air Conditioning"]
  };

  const placeInfo = document.getElementById('place-info');
  if (placeInfo) {
    placeInfo.innerHTML = `
      <p><span class="bold">Host:</span> ${placeData.host}</p>
      <p><span class="bold">Price per night:</span> ${placeData.price}</p>
      <p><span class="bold">Description:</span> ${placeData.description}</p>
      <p><span class="bold">Amenities:</span> ${placeData.amenities.join(", ")}</p>
    `;
  }

 const loginForm = document.getElementById("login-form")
if (loginForm) {
  console.log("loginForm");
  
  loginForm.addEventListener("submit", async(event) => {
    event.preventDefault()
    console.log("yes");
    
    const email = loginForm.email.value
    const password = loginForm.password.value
    const data = await login(email, password)
    if (data.access_token) {
      document.cookie = `token=${data.access_token}; path=/`
      window.location.href = "index.html"
    }
  })
}

  
  document.querySelectorAll('.stars').forEach(container => {
    const currentScore = parseInt(container.dataset.score, 10) || 0;
    let selectedRating = currentScore;

    function renderStars(rating) {
      container.innerHTML = '';
      for (let i = 1; i <= 5; i++) {
        const star = document.createElement('span');
        star.textContent = '★';
        if (i <= rating) star.classList.add('selected');
        container.appendChild(star);
      }
    }

    function highlightStars(index) {
      const stars = container.querySelectorAll('span');
      stars.forEach((star, i) => {
        star.classList.toggle('hover', i <= index);
      });
    }

    renderStars(currentScore);

    container.addEventListener('mouseover', e => {
      if (e.target.tagName === 'SPAN') {
        const index = Array.from(container.children).indexOf(e.target);
        highlightStars(index);
      }
    });

    container.addEventListener('mouseout', () => {
      const stars = container.querySelectorAll('span');
      stars.forEach(star => star.classList.remove('hover'));
    });

    container.addEventListener('click', e => {
      if (e.target.tagName === 'SPAN') {
        selectedRating = Array.from(container.children).indexOf(e.target) + 1;
        container.dataset.score = selectedRating;
        renderStars(selectedRating);
        console.log(`New rating: ${selectedRating}`);
      }
    });
  });
});
