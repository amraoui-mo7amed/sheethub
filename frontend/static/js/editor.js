const htlm = document.querySelector('html');
const htmlLanguage = htlm.getAttribute('lang');


const form = document.querySelector('form');
form.addEventListener('submit', function (e) {
  tinymce.triggerSave(); // Sync TinyMCE content to textarea

  const description = document.querySelector('[name="description"]').value;
  if (!description.trim()) {
    e.preventDefault(); // Stop form submission
    alert("Description is required!"); // Or show a nicer error
    tinymce.get('description').focus(); // Focus TinyMCE editor
  }
});

tinymce.init({
  selector: 'textarea.tiny',
  height: 500,
  plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons accordion',
  // menubar: 'file edit view insert format tools table help',
  toolbar: "undo redo | accordion accordionremove | blocks fontfamily fontsize | bold italic underline strikethrough | align numlist bullist | link | table media | lineheight outdent indent| forecolor backcolor removeformat | charmap emoticons | code fullscreen preview | save print | pagebreak anchor codesample | ltr rtl",
  file_picker_callback: (callback, value, meta) => {
    /* Provide file and text for the link dialog */
    if (meta.filetype === 'file') {
      callback('https://www.google.com/logos/google.jpg', { text: 'My text' });
    }

    /* Provide image and alt text for the image dialog */
    if (meta.filetype === 'image') {
      callback('https://www.google.com/logos/google.jpg', { alt: 'My alt text' });
    }

    /* Provide alternative source and posted for the media dialog */
    if (meta.filetype === 'media') {
      callback('movie.mp4', { source2: 'alt.ogg', poster: 'https://www.google.com/logos/google.jpg' });
    }
  },
  plugins: [
    'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
    'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
    'insertdatetime', 'media', 'table', 'help', 'wordcount'
  ],
  content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }',
  language: htmlLanguage,
  license_key: 'gpl'

});



