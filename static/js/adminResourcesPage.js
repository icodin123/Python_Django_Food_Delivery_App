// API for uploading new files to the website

let fileUploadButton;
let uploadedFile;
let saveButton;
let fileManager;
let fileUIManager;

function FileUIManager(){

  this.addNewFile = function(){

    let fileTable = document.querySelector('#fileTable');

    let newTr = document.createElement('tr');
    let newTd1 = document.createElement('td');
    let newTd2 = document.createElement('td');
    let newTd3 = document.createElement('td');
    let newTd4 = document.createElement('td');
    let newTd5 = document.createElement('td');

    newTd1.textContent = 'filename';
    newTd2.textContent = '0B';
    newTd3.textContent = '2019/11/04';

    let button1 = document.createElement('button');
    let button2 = document.createElement('button');

    button1.className = 'reviewButton';
    button2.className = 'reviewButton';
    button1.textContent = 'Delete';
    button2.textContent = 'Update';

    newTd4.appendChild(button1);
    newTd5.appendChild(button2);

    newTr.appendChild(newTd1);
    newTr.appendChild(newTd2);
    newTr.appendChild(newTd3);
    newTr.appendChild(newTd4);
    newTr.appendChild(newTd5);

    fileTable.appendChild(newTr);

  }

}

function FileManager(){

  this.saveFile = function(){
    console.log('saving file');
    fileUIManager.addNewFile();
  }

}

function onFileUpload(e){
  console.log(e);
  console.log(e.target.result); // log text contents of the file
}

function extractImage(e) {
    let file = fileUploadButton.files[0];
    let fileReader = new FileReader();
    fileReader.onload = onFileUpload;
    fileReader.readAsText(file);
    uploadedFile = fileReader;
}

fileManager = new FileManager();
fileUIManager = new FileUIManager();
window.onload = function () {

  saveButton = document.querySelector('#saveButton');
  saveButton.addEventListener('click', fileManager.saveFile);

  fileUploadButton = document.querySelector('#fileUploadButton');
  fileUploadButton.addEventListener('change', extractImage);

};
