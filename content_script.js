// Function to send an image URL to the Flask server and update the alt attribute
async function processImage(image) {
    const imageUrl = image.src;
    console.log('Processing image:', imageUrl);

    // Function to check if the server is available
    async function isServerAvailable() {
        try {
            const response = await fetch('http://localhost:5000/health_check', {
                method: 'GET',
            });
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    // Retry with a delay until the server becomes available
    const maxRetries = 10; // Adjust the maximum number of retries as needed
    let retries = 0;
    while (retries < maxRetries) {
        if (await isServerAvailable()) {
            // Server is available, send the image URL to the Flask server
            const response = await fetch('http://localhost:5000/process_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image_url: imageUrl }),
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Received text:', result.text);

                // Update the alt attribute of the image with the processed text
                image.alt = result.text;
                console.log('Alt attribute updated.');
            } else {
                console.error('Failed to process image:', response.status);
            }

            break; // Exit the retry loop if successful
        } else {
            // Server is not available, wait for a moment before retrying
            console.log('server not available. Attempt',retries);
            await new Promise(resolve => setTimeout(resolve, 5000)); // 5 seconds delay
            retries++;
        }
    }

    if (retries >= maxRetries) {
        console.error('Server did not become available after max retries.');
    }
}

// Find all image elements on the page
const images = document.querySelectorAll('img');

// Process each image one by one
images.forEach(processImage);

console.log("Content script finished!");
