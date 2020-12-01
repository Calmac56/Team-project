document.getElementById('codeArea').addEventListener('keydown',function(e) {
  if(e.keyCode === 9) { 
      e.preventDefault();

      var target = e.target;

      let _range = document.getSelection().getRangeAt(0);
      let range = _range.cloneRange();
      range.selectNodeContents(target);
      range.setEnd(_range.endContainer, _range.endOffset);
      var caret = range.toString().length;

      var content = this.innerText;


      this.innerText = content.substring(0, caret) + "    " + content.substring(caret);
      document.getSelection().collapse(target, 1);
  }
},false);
