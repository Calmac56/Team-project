languageSelector.onchange = function(){
    Language = languageSelector.value;
    editor.getSession().setMode("ace/mode/" + Language.toLowerCase());

}; 