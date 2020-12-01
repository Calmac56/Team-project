var codeArea = document.getElementById('codeArea');

codeArea.onkeyup = function(){
    Code = codeArea.innerText;
    var linesLength = Code.split(/\r\n|\r|\n/).length;
    var dLine = Code.split(/\r\n\n|\r|\n\n/).length;
    linesLength = linesLength - dLine + 2;
    var lineBuffer = "";
    var lines = "";

    for (i=1;i<linesLength;i++) {
        lineBuffer = lines + i + "\n";
        lines = lineBuffer;
    }

    document.getElementById('lineCount').innerText = lines;
}; 