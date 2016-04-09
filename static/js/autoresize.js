// Codice speciale per il dimensionamento ottimale della pulsantiera

function _autoresize(selector, ratio, ratioWidth) {
    for (i=1; i<=$(selector).children().size(); i++) {
        element = $(selector+':nth-child('+i+')');
        boxes   = element.children().size(); 
        rows    = Math.ceil(Math.sqrt(boxes/ratio));
        columns = Math.ceil(boxes/rows);
        if (!ratioWidth) {
            tmp     = rows;
            rows    = columns;
            columns = tmp;
        }
        element.children().css('width',  100/rows+'%');
        element.children().css('height', 100/columns+'%');
    }
}
function autoresize(id, selector, ratio, ratioWidth) {
    $(selector).children().css('float', 'left');
    $(selector).children().first().css('display', 'inline');  
    $(id).css('bottom', '0');
    $(id).css('right', '0');
    $(id).css('left', '0');
    $(id).css('top', '0');
    $(window).bind('resize', _autoresize(selector, ratio, ratioWidth));
}
