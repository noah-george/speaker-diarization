function saveTextToFile(filename) {
    const text = document.getElementById('output-container').innerText;
    console.log("typeof filename:", typeof filename); // Check the data type of 'filename'
    console.log("typeof text",typeof text);
    const blob = new Blob([text], { type: 'text/plain' });

    // Create a temporary anchor element
    const anchorElement = document.createElement('a');
    anchorElement.href = URL.createObjectURL(blob);
    anchorElement.download = filename;

    // Programmatically click the anchor element to trigger the download
    anchorElement.click();
    axios.post('/save', {
        filename: filename,
        content: text
    })
    .then(response => {
        console.log(response.data);
        alert('Text file saved to the database.');
    })
    .catch(error => {
        console.error(error);
        console.log(error.response.data); // Log the error message from the server    
        outputContainer.innerHTML = "An error occurred: " + error;
    });

    }
async function transcribeAndDiarize(event) {
    event.preventDefault();
    const file = document.getElementById("audio-file").files[0];
    const formData = new FormData();
    formData.append("wav_file", file);
    const outputContainer = document.getElementById("output-container");
    const loader = document.getElementById("loader");
    outputContainer.innerHTML = "";
    loader.style.display = "block";

    try {
        const response = await axios.post("/diarize", formData);
        const data = response.data;
        console.log(data);
        outputContainer.innerHTML = JSON.stringify(data, null, 2);
        const audioPlayer = document.getElementById('audio-player');
        audioPlayer.src = URL.createObjectURL(file);

        // Display the audio player
        audioPlayer.style.display = 'block';
        const saveButton = document.createElement('button');
        saveButton.textContent = 'Save as Text File';
        saveButton.addEventListener('click', () => {
            const filename = file.name.replace(/\.[^/.]+$/, "")+"_transcript.txt"; // Set the desired filename here
            saveTextToFile(filename);}
            );
        outputContainer.appendChild(saveButton);
    }
    catch (error) {
        console.error(error);
        outputContainer.innerHTML = "An error occurred: " + error;
    } finally {
        loader.style.display = "none";
    }
}