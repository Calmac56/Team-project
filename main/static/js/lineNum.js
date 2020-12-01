var codeArea = document.getElementById('codeArea');

codeArea.onkeyup = function(){
    Code = document.getElementById('codeArea').innerText;
    var linesLength =  Code.split(/\r\n|\r|\n/).length
    var lineBuffer = "";
    var lines = "";

    for (i=1;i<linesLength;i++) {
        lineBuffer = lines + i + "\n";
        lines = lineBuffer;
    }

    document.getElementById('lineCount').innerText = lines;
}; 