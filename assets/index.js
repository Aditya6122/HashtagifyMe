const imageInput = document.getElementById('formFile');
const imagePreview = document.getElementById('image-preview');
const predict = document.getElementById('submit');
const responseContainer = document.getElementById('response-container');
const generatedHashtagsHeading = document.getElementById('generated-hashtags-heading');

imageInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.addEventListener('load', function() {
            imagePreview.style.display = 'block';
            imagePreview.src = reader.result;
        });
        reader.readAsDataURL(file);
    } else {
        imagePreview.style.display = 'none';
    }
});

window.addEventListener('resize', function() {
    const windowHeight = window.innerHeight;
    const windowWidth = window.innerWidth;
    const containerHeight = windowHeight - 100;
    const containerWidth = windowWidth;
    const imageWidth = containerWidth * 0.4;
    const imageHeight = containerHeight * 0.8;
    
    document.getElementById('container').style.height = containerHeight + 'px';
    document.getElementById('container').style.width = containerWidth + 'px';
    document.getElementById('image-preview').style.maxWidth = imageWidth + 'px';
    document.getElementById('image-preview').style.maxHeight = imageHeight + 'px';
});

window.dispatchEvent(new Event('resize'));

predict.addEventListener('click', e => {
    e.preventDefault();

    const file = imageInput.files[0];
    if (!file) {
        console.log('No image selected');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    $.ajax({
        url:"http://127.0.0.1:8000/",
        type:"POST",
        processData: false,
        contentType: false,
        data: formData,
        success: function(response){
            var captions = response;
            responseContainer.innerHTML = '';

            if (captions.length > 0) {
                generatedHashtagsHeading.style.display = 'block';

                const ul = document.createElement('ul');
                responseContainer.appendChild(ul);

                let currentIndex = 0;

                const printCaption = () => {
                    if (currentIndex < captions.length) {
                        const caption = captions[currentIndex];
                        const li = document.createElement('li');
                        ul.appendChild(li);

                        let currentCharIndex = 0;

                        const printCharacter = () => {
                            if (currentCharIndex < caption.length) {
                                li.textContent += caption[currentCharIndex];
                                currentCharIndex++;
                                setTimeout(printCharacter, 10); // Adjust the interval as needed (in milliseconds)
                            } else {
                                currentIndex++;
                                printCaption(); // Print the next caption
                            }
                        };

                        printCharacter();
                    }
                };

                printCaption();
            } else {
                generatedHashtagsHeading.style.display = 'none';
            }

        }
    });
})