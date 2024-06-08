console.log('Script loaded');

document.addEventListener('DOMContentLoaded', function () {
    fetchVideos();
});

function fetchVideos() {
    fetch('/api/video/')
        .then((response) => response.json())
        .then((videos) => {
            console.log('Videos Refreshed:', videos);
            const list = document.getElementById('video-list');
            list.innerHTML = '';
            videos.forEach((video) => {
                const item = document.createElement('li');
                const container = document.createElement('div');
                container.style.display = 'flex';
                container.style.justifyContent = 'space-between';
                container.style.alignItems = 'center';
                container.style.width = '100%';

                const textNode = document.createTextNode(video.name);
                const textSpan = document.createElement('span');
                textSpan.appendChild(textNode);

                const buttonGroup = document.createElement('div');
                buttonGroup.style.marginLeft = 'auto';

                const playButton = document.createElement('button');
                playButton.textContent = 'Play';
                playButton.style.marginRight = '12px';
                playButton.onclick = () => playVideo(video.name);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.style.backgroundColor = '#eb4034';
                deleteButton.onclick = () => deleteVideo(video.name);

                buttonGroup.appendChild(playButton);
                buttonGroup.appendChild(deleteButton);

                container.appendChild(textSpan);
                container.appendChild(buttonGroup);
                item.appendChild(container);
                list.appendChild(item);
            });
        })
        .catch((error) => console.error('Error:', error));
}
function uploadVideo(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    fetch('/api/video/', {
        method: 'POST',
        body: formData,
        headers: {
            Accept: 'application/json',
        },
    })
        .then(() => {
            setTimeout(() => {
                fetchVideos();
            }, 100);
        })
        .catch((error) => console.error(error));
}

function playVideo(videoName) {
    const videoPlayer = document.getElementById('video-player');
    videoPlayer.src = `/api/video/${videoName}`;
    videoPlayer.load();
    videoPlayer.play();
}

function deleteVideo(videoName) {
    fetch(`/api/video/delete/${videoName}`, {
        method: 'DELETE',
    })
        .then((response) => {
            if (response.ok) {
                fetchVideos();
            } else {
                console.error('Error in deletion');
            }
        })
        .catch((error) => console.error(error));
}

function handleSubmit(event) {
    event.preventDefault();
    // Add here your form processing logic
    uploadVideo(event);
}
