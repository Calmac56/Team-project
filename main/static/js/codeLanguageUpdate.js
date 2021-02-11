var languageSelector = document.getElementById('languageSelector');

for(var i, j = 0; i = languageSelector.options[j]; j++) {
    if(i.value == Language) {
        languageSelector.selectedIndex = j;
        break;
    }
}

setInterval(updateCookies,5000);

codeArea.onkeyup = function(){
    Code = AceEditor.getValue();
}; 

languageSelector.onchange = function(){
    Language = languageSelector.value;
    editor.getSession().setMode("ace/mode/" + Language.toLowerCase());
    updateCookies();
}; 