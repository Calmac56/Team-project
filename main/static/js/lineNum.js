var codeArea = document.getElementById('codeArea');

codeArea.onkeyup = function(){
    Code = AceEditor.getValue();

    document.getElementById('output').innerText = "Code";
}; 