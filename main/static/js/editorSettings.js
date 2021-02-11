var editor = ace.edit("codeArea");
editor.setTheme("ace/theme/tomorrow_night");
editor.getSession().setMode("ace/mode/java");

onLoadFunction = editor => {
    editor.renderer.setPadding(8)
}

editor.getSession().on('change', function () {
     Code = editor.getSession().getValue();
});