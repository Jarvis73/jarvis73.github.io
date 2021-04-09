/**
 * some JavaScript code for this blog theme
 */
/* jshint asi:true */

///////////////////////// 头部 ////////////////////////////
/**
 * clickMenu
 */
(function() {
  if (window.innerWidth <= 770) {
    var menuBtn = document.querySelector('#headerMenu')
    var nav = document.querySelector('#headerNav')
    menuBtn.onclick = function(e) {
      e.stopPropagation()
      if (menuBtn.classList.contains('active')) {
        menuBtn.classList.remove('active')
        nav.classList.remove('nav-show')
      } else {
        nav.classList.add('nav-show')
        menuBtn.classList.add('active')
      }
    }
    document.querySelector('body').addEventListener('click', function() {
      nav.classList.remove('nav-show')
      menuBtn.classList.remove('active')
    })
  }
}());

////////////////////////// 返回顶部 ////////////////////////////
(function() {
  var backToTop = document.querySelector('.back-to-top')
  var backToTopA = document.querySelector('.back-to-top a')
  // console.log(backToTop);
  window.addEventListener('scroll', function() {

    // 页面顶部滚进去的距离
    var scrollTop = Math.max(document.documentElement.scrollTop, document.body.scrollTop)

    if (scrollTop > 200) {
      backToTop.classList.add('back-to-top-show')
    } else {
      backToTop.classList.remove('back-to-top-show')
    }
  })

  // backToTopA.addEventListener('click',function (e) {
  //     e.preventDefault()
  //     window.scrollTo(0,0)
  // })
}());

/////////////////////////// 缩短 "Recent Posts" 中的名称 ////////////////////////////
(function() {
  var all_li = document.getElementsByClassName("index-right-recent");
  for (var i = 0; i < all_li.length; i++)
  {
    var before_title = all_li[i].innerHTML;
    var after_title = before_title.replace(/\([a-zA-Z0-9 \-:,;\.\/]*\)$/i, "");
    all_li[i].innerHTML = after_title;
  }
}());

///////////////////////////////// 代码块的复制按钮 ////////////////////////////////////
(function() {
  let codes = document.querySelectorAll('.highlight > pre > code');
  let countID = 0;
  codes.forEach((code) => {
  
    code.querySelector(".rouge-code").setAttribute("id", "code" + countID);
    
    let spanLang = document.createElement('span');
    spanLang.className = 'language';

    let btnDiv = document.createElement('div');
    btnDiv.className = "btnContainer";

    let btn = document.createElement('button');
    btn.innerHTML = "<i class='fa fa-copy'></i> copy";
    btn.className = "btn-copy";
    btn.setAttribute("data-clipboard-action", "copy");
    btn.setAttribute("data-clipboard-target", "#code" + countID);
    
    let spanCopySuccess = document.createElement('button');
    spanCopySuccess.innerHTML = "<i class='fa fa-check'></i>";
    spanCopySuccess.className = "btn-copy-success";

    btnDiv.appendChild(btn);
    btnDiv.appendChild(spanCopySuccess)

    let divCodeHeader = document.createElement('div');
    divCodeHeader.className = 'codeHeader';
    divCodeHeader.appendChild(spanLang);
    divCodeHeader.appendChild(btnDiv);

    // let div = document.createElement('div');
    // div.appendChild(btn);
    
    code.parentElement.before(divCodeHeader);
  
    countID++;
  }); 

  // 复制按钮逻辑
  let clipboard = new ClipboardJS('.btn-copy');
  clipboard.on('success', function (e) {
    e.clearSelection();

    let btnSuccess = e.trigger.nextSibling;
    btnSuccess.className += ' show';
    setTimeout(() => {
      btnSuccess.className += ' hide';
    }, 1000);
    setTimeout(() => {
      btnSuccess.className = btnSuccess.className.slice(0, btnSuccess.className.length - 10);
    }, 1500);
  });
}());


/////////////////////////////// 为代码块填入代码类型属性 //////////////////////////////////
(function() {
  var allCode = document.querySelectorAll("div.highlight");
  for (var i = 0; i < allCode.length; i++) 
  {
    var codeType = allCode[i].parentElement.className;
    // allCode[i].setAttribute("data-content", codeType.split(" ")[0].split("-")[1]);
    var codeLang = allCode[i].querySelector(".codeHeader > .language");
    codeLang.innerHTML = codeType.split(" ")[0].split("-")[1];
  }
}());
