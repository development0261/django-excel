$('.table-carousel').owlCarousel({
    loop: true,
    margin: 30,
    nav: true,
    dots: false,
    navText: ["<i class='fa fa-chevron-left'>", "<i class='fa fa-chevron-right'>"],
    responsive: {
        0: {
            items: 1
        },
        992: {
            items: 2
        }
    }
})

$(".nav-slider-tabs button").click(function () {
    $(".nav-slider-tabs button").removeClass("nav-active");
    $(this).addClass("nav-active");
});

