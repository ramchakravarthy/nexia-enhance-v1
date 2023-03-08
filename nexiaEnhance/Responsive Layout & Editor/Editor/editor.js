var toolbarOptions = [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    ['blockquote', 'code-block'],

    [{ 'header': 1 }, { 'header': 2 }],               // custom button values
    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
    [{ 'script': 'sub' }, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1' }, { 'indent': '+1' }],          // outdent/indent
    [{ 'direction': 'rtl' }],                         // text direction

    [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
    [{ 'font': [] }],
    [{ 'align': [] }],

    ['clean']                                         // remove formatting button
];


var options = {
    // debug: 'info',
    debug: false,
    modules: {
        toolbar: toolbarOptions,
    },
    placeholder: 'Please enter a response...',
    // readOnly: true,
    theme: 'snow'
};
var editor = new Quill('#editor', options);

var justDeltaContent = document.getElementById('justDelta');
var justTextContent = document.getElementById('justText');
var justHtmlContent = document.getElementById('justHtml');


editor.on('text-change', function (delta, oldDelta, source) {
    if (source == 'api') {
        console.log("An API call triggered this change.");
    } else if (source == 'user') {
        console.log("A user action triggered this change.");

      
        // You would have to store this contents variable in the database and use the editor.setContents(contents) method to set the value of the 
        // text editor when being loaded from a database
        var contents = editor.getContents();

        var text = editor.getText();
        var justHtml = editor.root.innerHTML;


        justDeltaContent.innerHTML = JSON.stringify(contents);
        justTextContent.innerHTML = text;
        justHtmlContent.innerHTML = justHtml;

        //   Example for retrieving text and html
        // https://codepen.io/k3no/pen/amwpqZ



    }
});