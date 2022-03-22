document.ready(function() {
    $tabs = document.getElementByClassName("tabbable");

    document.querySelectorAll(".nav-tabs a").click(function(e) {
        e.preventDefault();
        this.tab('show');
    })
    
    $( "tbody.connectedSortable" )
        .sortable({
            connectWith: ".connectedSortable",
            items: "> tr:not(:first)",
            appendTo: $tabs,
            helper:"clone",
            zIndex: 999990,
            start: function(){ $tabs.classList.add("dragging") },
            stop: function(){ $tabs.classList.remove("dragging") }
        })
        .disableSelection()
    ;
    
    let $tab_items = $( ".nav-tabs > li", $tabs ).droppable({
      accept: ".connectedSortable tr",
      hoverClass: "ui-state-hover",
      over: function( event, ui ) {
        let $item = $( this );
        $item.find("a").tab("show");
        
      },
      drop: function( event, ui ) {
        return false;
      }
    });
    
});