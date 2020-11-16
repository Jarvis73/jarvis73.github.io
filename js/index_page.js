$('#myPager').pager({
    recPerPage: 1,
    lang: 'zh_cn',
    onPageChange: function(state, oldState) {
        if (state.page !== oldState.page) {
            if (state.page == 1) {
                console.log(window.location.pathname);
            }
        }
    },
    linkCreator: function(page, pager) {
        if (page == 1)
            return "/";
        else
            return "/page" + page.toString() + "/";
    }
});
