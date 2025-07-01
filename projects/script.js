// DOM Elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const startCameraBtn = document.getElementById('start-camera');
const captureBtn = document.getElementById('capture-btn');
const recordBtn = document.getElementById('record-btn');
const stopRecordBtn = document.getElementById('stop-record-btn');
const photoPreview = document.getElementById('photo-preview');
const videoPreview = document.getElementById('video-preview');
const locationData = document.getElementById('location-data');
const saveBtn = document.getElementById('save-btn');
const emailBtn = document.getElementById('email-btn');
const whatsappBtn = document.getElementById('whatsapp-btn');
const smsBtn = document.getElementById('sms-btn');
const instagramBtn = document.getElementById('instagram-btn');
const facebookBtn = document.getElementById('facebook-btn');

// Global variables
let stream = null;
let mediaRecorder = null;
let recordedChunks = [];
let currentPhoto = null;
let currentVideo = null;
let userLocation = null;

// Start Camera
startCameraBtn.addEventListener('click', async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: 'user'
            },
            audio: false
        });
        video.srcObject = stream;
        captureBtn.disabled = false;
        recordBtn.disabled = false;
        startCameraBtn.disabled = true;
        
        // Get location when camera starts
        getLocation();
    } catch (err) {
        console.error("Error accessing camera:", err);
        alert("Could not access the camera. Please check permissions.");
    }
});

// Capture Photo
captureBtn.addEventListener('click', () => {
    if (!stream) return;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const imageDataUrl = canvas.toDataURL('image/jpeg');
    currentPhoto = imageDataUrl;
    currentVideo = null;
    
    photoPreview.innerHTML = `<img src="${imageDataUrl}" alt="Captured Photo">`;
    videoPreview.style.display = 'none';
    photoPreview.style.display = 'block';
    
    // Enable share buttons
    enableShareButtons();
});

// Record Video
recordBtn.addEventListener('click', () => {
    if (!stream) return;
    
    recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    
    mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
            recordedChunks.push(event.data);
        }
    };
    
    mediaRecorder.onstop = () => {
        const videoBlob = new Blob(recordedChunks, { type: 'video/webm' });
        const videoUrl = URL.createObjectURL(videoBlob);
        currentVideo = videoUrl;
        currentPhoto = null;
        
        videoPreview.src = videoUrl;
        videoPreview.style.display = 'block';
        photoPreview.style.display = 'none';
        
        // Enable share buttons
        enableShareButtons();
    };
    
    mediaRecorder.start();
    recordBtn.disabled = true;
    stopRecordBtn.disabled = false;
});

// Stop Recording
stopRecordBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        recordBtn.disabled = false;
        stopRecordBtn.disabled = true;
    }
});

// Get Location
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy
                };
                
                // Reverse geocoding to get address (using Nominatim API)
                fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${userLocation.latitude}&lon=${userLocation.longitude}`)
                    .then(response => response.json())
                    .then(data => {
                        const address = data.display_name || 'Address not available';
                        locationData.innerHTML = `
                            <strong>Coordinates:</strong> ${userLocation.latitude.toFixed(6)}, ${userLocation.longitude.toFixed(6)}<br>
                            <strong>Accuracy:</strong> ${userLocation.accuracy} meters<br>
                            <strong>Address:</strong> ${address}
                        `;
                    })
                    .catch(err => {
                        console.error("Geocoding error:", err);
                        locationData.innerHTML = `
                            <strong>Coordinates:</strong> ${userLocation.latitude.toFixed(6)}, ${userLocation.longitude.toFixed(6)}<br>
                            <strong>Accuracy:</strong> ${userLocation.accuracy} meters
                        `;
                    });
            },
            (error) => {
                console.error("Geolocation error:", error);
                locationData.textContent = "Location access denied or not available.";
            }
        );
    } else {
        locationData.textContent = "Geolocation is not supported by this browser.";
    }
}

// Enable share buttons when media is available
function enableShareButtons() {
    saveBtn.disabled = false;
    emailBtn.disabled = false;
    whatsappBtn.disabled = false;
    smsBtn.disabled = false;
    instagramBtn.disabled = false;
    facebookBtn.disabled = false;
}

// Save Media Locally
saveBtn.addEventListener('click', () => {
    if (currentPhoto) {
        const link = document.createElement('a');
        link.href = currentPhoto;
        link.download = `photo_${new Date().toISOString().slice(0, 10)}.jpg`;
        link.click();
    } else if (currentVideo) {
        const link = document.createElement('a');
        link.href = currentVideo;
        link.download = `video_${new Date().toISOString().slice(0, 10)}.webm`;
        link.click();
    }
});

// Share via Email
emailBtn.addEventListener('click', () => {
    let subject = "Check out my media!";
    let body = "I captured this using the Media Capture app.";
    
    if (userLocation) {
        body += `\n\nLocation: ${userLocation.latitude}, ${userLocation.longitude}`;
        body += `\nhttps://www.google.com/maps?q=${userLocation.latitude},${userLocation.longitude}`;
    }
    
    if (currentPhoto) {
        // For photos, we can't directly attach in mailto link
        // So we'll just share the text and location
        window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    } else if (currentVideo) {
        // For videos, same limitation
        window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    }
});

// Share via WhatsApp
whatsappBtn.addEventListener('click', () => {
    let text = "Check out my media!";
    
    if (userLocation) {
        text += `\n\nLocation: ${userLocation.latitude}, ${userLocation.longitude}`;
        text += `\nhttps://www.google.com/maps?q=${userLocation.latitude},${userLocation.longitude}`;
    }
    
    if (currentPhoto) {
        // For WhatsApp Web, we can only share text
        window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
    } else if (currentVideo) {
        window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
    }
});

// Share via SMS
smsBtn.addEventListener('click', () => {
    let text = "Check out my media!";
    
    if (userLocation) {
        text += `\n\nLocation: ${userLocation.latitude}, ${userLocation.longitude}`;
        text += `\nhttps://www.google.com/maps?q=${userLocation.latitude},${userLocation.longitude}`;
    }
    
    window.location.href = `sms:?body=${encodeURIComponent(text)}`;
});

// Share to Instagram
instagramBtn.addEventListener('click', () => {
    alert("To post to Instagram:\n1. Save the media first\n2. Open Instagram app\n3. Upload the saved file\n\nDirect sharing to Instagram isn't possible from web browsers due to API restrictions.");
});

// Share to Facebook
facebookBtn.addEventListener('click', () => {
    alert("To post to Facebook:\n1. Save the media first\n2. Open Facebook in a new tab\n3. Upload the saved file\n\nDirect sharing to Facebook would require Facebook SDK integration.");
});

// Clean up when leaving the page
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
});