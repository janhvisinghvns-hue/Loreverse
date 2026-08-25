const themeToggle = document.getElementById("theme-toggle");
    const savedTheme = localStorage.getItem("loreverse-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
        themeToggle.textContent = "☀️";
    }

    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("loreverse-theme", "dark");
            themeToggle.textContent = "☀️";
        } else {
            localStorage.setItem("loreverse-theme", "light");
            themeToggle.textContent = "🌙";
        }
    });
    window.addEventListener("load", function () {
        const loader = document.getElementById("page-loader");
        setTimeout(function () {
            loader.classList.add("loader-hidden");
        }, 250);
    });


const chapterContent = document.getElementById("chapter-content");
const decreaseFont = document.getElementById("decrease-font");
const resetFont = document.getElementById("reset-font");
const increaseFont = document.getElementById("increase-font");

if (chapterContent && decreaseFont && resetFont && increaseFont) {

    let fontSize = 18;

    decreaseFont.addEventListener("click", function () {
        if (fontSize > 14) {
            fontSize -= 2;
            chapterContent.style.fontSize = fontSize + "px";
        }
    });

    resetFont.addEventListener("click", function () {
        fontSize = 18;
        chapterContent.style.fontSize = fontSize + "px";
    });

    increaseFont.addEventListener("click", function () {
        if (fontSize < 26) {
            fontSize += 2;
            chapterContent.style.fontSize = fontSize + "px";
        }
    });
}



const worldImages = document.querySelectorAll(".world-explorer-image");

worldImages.forEach(function (image) {
    image.addEventListener("click", function () {

        const overlay = document.createElement("div");
        overlay.className = "image-overlay";

        const enlargedImage = document.createElement("img");
        enlargedImage.src = image.src;
        enlargedImage.alt = image.alt;

        const closeButton = document.createElement("button");
        closeButton.className = "image-overlay-close";
        closeButton.textContent = "×";
        closeButton.setAttribute("aria-label", "Close image");

        overlay.appendChild(enlargedImage);
        overlay.appendChild(closeButton);

        document.body.appendChild(overlay);

        closeButton.addEventListener("click", function () {
            overlay.remove();
        });

        overlay.addEventListener("click", function (event) {
            if (event.target === overlay) {
                overlay.remove();
            }
        });
    });
});

const deleteStoryForms = document.querySelectorAll(".delete-story-form");

deleteStoryForms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
        const confirmed = confirm(
            "Are you sure you want to delete this story?"
        );

        if (!confirmed) {
            event.preventDefault();
        }
    });
});

const likeForm = document.getElementById("chapter-like-form");

if (likeForm) {
    likeForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const button = likeForm.querySelector("button");
        const likesCount = likeForm.querySelector(".likes-count");

        const csrfToken = likeForm.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

        fetch(likeForm.action, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.user_liked) {
                button.innerHTML = "❤️ Unlike";
                button.classList.remove("btn-outline-danger");
                button.classList.add("btn-danger");
            } else {
                button.innerHTML = "🤍 Like";
                button.classList.remove("btn-danger");
                button.classList.add("btn-outline-danger");
            }

            likesCount.textContent = `${data.likes_count} likes`;
        })
        .catch(error => {
            console.error("Error toggling chapter like:", error);
        });
    });
}

const commentForm = document.getElementById("chapter-comment-form");

if (commentForm) {
    commentForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(commentForm);
        const commentsList = document.getElementById("comments-list");
        const csrfToken = commentForm.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

        fetch(window.location.href, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const emptyState = commentsList.querySelector(".empty-state");

            if (emptyState) {
                emptyState.remove();
            }

            const commentItem = document.createElement("div");
            commentItem.className = "comment-item";

            const username = document.createElement("strong");
            username.textContent = data.username;

            const content = document.createElement("p");
            content.textContent = data.content;

            commentItem.appendChild(username);
            commentItem.appendChild(content);

            commentsList.appendChild(commentItem);

            commentForm.reset();
        })
        .catch(error => {
            console.error("Error posting comment:", error);
        });
    });
}