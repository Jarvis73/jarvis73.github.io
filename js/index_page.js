$('#myPager').pager({
    recPerPage: 1,
    lang: 'zh_cn',
    linkCreator: function(page, pager) {
        if (page == 1)
            return "/";
        else
            return "/page" + page.toString() + "/";
    }
});
