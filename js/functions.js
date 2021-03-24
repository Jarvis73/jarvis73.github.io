//// Functions with jQuery

//////////////////////////////// 可折叠目录的实现 //////////////////////////////////////
(function() {
    // 添加折叠展开的图标
    let $itemHasChild = $("#content-side li:has(ul)");
    $itemHasChild.prepend("<i class='fa fa-caret-down'></i><i class='fa fa-caret-right'></i>");
    let $iconToFold = $("li > .fa-caret-down");
    $iconToFold.addClass("hide");

    // 添加点击事件
    var clickIcon = function(){
        $("#content-side li > i").click(function(){
            $(this).siblings("ul").slideToggle(100);
            $(this).toggleClass("hide");
            $(this).siblings("i").toggleClass("hide");
        })
    }()
}());

  