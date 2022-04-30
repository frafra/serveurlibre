// Codice per la gestione della cassa

// Funzioni di supporto
function str2float(string) {
    return parseFloat(string.replace(',', '.'));
}
function float2str(number) {
    return number.toFixed(2).replace('.', ',');
}

// Inizializzazione
total_without_coupon=0.00;
coupon=0.00;
reusable=false;
done=0;

$(document).ready(function() {
    $('#offer select').select2();
});

// Reset dell'interfaccia
function clean() {
    done=0;
    $('#items > ul').text('');
    total_without_coupon=0;
    coupon=0;
    reusable=false;
    $('#total').text('0,00');
    $('#change').text('0,00');
    $('#price').val('');
    $('#numbersleft > button#symbol-comma').text(',');
    $('#payment_method').val('C');
    $('#topseller > button').css('display', 'inline');
    $('#items * button').removeAttr('disabled'); // NEEDED?
    $('[id^=category-]').css('display', 'none');
    $('[id^=category-]').first().css('display', 'inline');
    $('#buttons > button[id^=button-]').css('display', 'inline');
    $('#numbersright').css('visibility', 'visible');
    $('#waiting').css('display', 'none');
    $('#waiting > button').css('background-color', '');
    $('#waiting > button').first().css('background-color', 'lightblue');
    $('#offer select').val('0');
    $('#offer select').trigger('change');
}

function new_ticket() { // modifica del 6 luglio 2013
    //document.location.reload(true);
    clean();
}

// Gestione dell'evento da tastiera legato alla pressione di un numero (dettaglio prodotto)
function number_pressed(number) {
    item=$('#items > ul > li > div.editor:visible')
    if (item.length) {
        string=item.children('input.quantity').val();
        item.find('input.editor').val(string+number);
        id=item.parent().prop('id');
        element=$('#tabs > div > button.product-'+id);
        reset_value(id, element);
        change_value(id, element, parseInt(string+number));
    } else {
        string=$('#price').val();
        if ((string.indexOf(',')==-1) || (((string.indexOf(',')!=-1) && (string.indexOf(',')>(string.length-3))))) {
            $('#price').val(string+number);
            update_change();
        }
    }
}

// Gestione dell'evento da tastiera legato alla pressione del tasto delete (dettaglio prodotto)
function delete_pressed() {
    item=$('#items > ul > li > div.editor:visible')
    if (item.length) {
        string=item.children('input.quantity').val();
        if (string.length==1 || (string.length==2 && string.substring(0, 1)=='-')) {
            value='0'
        } else {
            value=string.substr(0, string.length-1);
        }
        item.find('input.editor').val(value);
        id=item.parent().prop('id');
        element=$('#tabs > div > button.product-'+id);
        reset_value(id, element);
        change_value(id, element, parseInt(value));
    } else {
        string=$('#price').val();
        $('#price').val(string.substr(0, string.length-1));
        update_change();
    }
}

// Gestione dell'evento da tastiera legato alla pressione del tasto punto o virgola (dettaglio prodotto)
function comma_dot_or_sign() {
    item=$('#items > ul > li > div.editor:visible');
    if (item.length) {
        sign_pressed();
    } else {
        comma_dot_pressed();
    }

}
// Bottone + (dettaglio prodotto)
function plus_pressed() {
    item=$('#items > ul > li > div.editor:visible')
    string=item.children('input.quantity').val();
    if (string.substr(0, 1)=='-') {
        sign_pressed();
    }
}

// Bottone - (dettaglio prodotto)
function minus_pressed() {
    item=$('#items > ul > li > div.editor:visible')
    string=item.children('input.quantity').val();
    if (string.substr(0, 1)!='-') {
        sign_pressed();
    }
}

// Gestione della pressione del tasto ">"
function sign_pressed() {
    item=$('#items > ul > li > div.editor:visible')
    string=item.children('input.quantity').val();
    if (string.substr(0, 1)=='-') {
        value=string.substr(1, string.length);
    } else {
        value='-'+string;
    }
    id=item.parent().prop('id');
    element=$('#tabs > div > button.product-'+id);
    reset_value(id, element);
    change_value(id, element, parseInt(value));
}

// Gestione della pressione del punto e della virgola
function comma_dot_pressed() {
    if ($('#price').val().indexOf(',')==-1) {
        $('#price').val($('#price').val()+',');
    }
}

// Ricalcolo totale
function update_change() {
    if ($('#price').val()=='') {
        $('#change').text('0,00');
    } else if (($('#price').val()!='') && ($('#price').val()!=',')) {
        change=str2float($('#price').val())-str2float($('#total').text());
        $('#change').text(float2str(change));
    }
}

// Cancellazione prodotto e aggiornamento totale
function reset_value(id, element) {
    item=$('#items > ul > li#'+id);
    quantity = parseInt(item.find('span.quantity').text());
    change_value(id, element, -quantity);
}

// Cambio quantità prodotto e aggiornamento totale
function change_value(id, element, diff) {
    item=$('#items > ul > li#'+id);
    quantity = item.find('span.quantity');
    quantity_value = parseInt(quantity.text())+diff;
    quantity.text(quantity_value);
    item.find('div.editor > input.quantity').val(quantity_value);
    price = item.find('span.price');
    old_price = str2float(price.text());
    new_price = quantity_value*str2float(element.children('span.price').text())
    price.text(float2str(new_price));
    adjust_total(total_without_coupon-old_price+new_price);
}

// Scrolling automatico verso l'alto per l'anteprima dello scontrino
function scrolltop() {
    $('#items').scrollTop($('#items')[0].scrollHeight);
}

// Gestione dei bottoni (dettaglio ordine)
function button_pressed(element) {
    id=element.prop('class').substr(8, element.prop('class').length-1);
    if (!$('#items > ul > li#'+id).length) {
        $('#items > ul').append('<li id="'+id+'"><button class="edit">&gt;</button>&nbsp;&nbsp;&nbsp;<span class="quantity">0</span>x '+element.children('span.name').text()+' = <span class="price">0,00</span> €<div class="editor" style="display: none;"><br /\>Quantità: <input class="quantity" type="number" name="quantity" readonly="readonly" /\>&nbsp;&nbsp;&nbsp;<button class="add">+</button><button class="reduce">-</button><button class="delete">X</button></div></li>');
        item=$('#items > ul > li#'+id);
        item.find('button.edit').click(function() {
            edit_item($(this));
            // is it visible?
        });
        item.find('button.add').click(function() {change_value(id, element, 1);});
        item.find('button.reduce').click(function() {change_value(id, element, -1);});
        item.find('button.delete').click(function() {
            reset_value(id, element);
            item.remove();
            if (!$('#items > ul > li').length) clean();
        });
        scrolltop();
    }
    change_value(id, element, 1);
}

// Apertura della linea per la modifica del dettaglio prodotto
function edit_item(element) {
    id=element.parent().prop('id');
    $('#items > ul > li[id!='+id+'] > div.editor').css('display', 'none');
    item=$('#items > ul > li#'+id+' > div.editor');
    if (item.css('display')=='none') {
        item.css('display', 'inline');
        $('#numbersleft > button#symbol-comma').text('-/+');
    } else {
        item.css('display', 'none');
        $('#numbersleft > button#symbol-comma').text(',');
    }
}

// Aggiornamento totale in seguito all'applicazione di uno sconto
function adjust_total(value) {
    total_without_coupon=value;
    if (reusable && coupon != 0.00) {
        $('#total').text('0,00');
    } else {
        total=total_without_coupon-coupon;
        if (total>0) $('#total').text(float2str(total_without_coupon-coupon));
        else $('#total').text('0,00');
    }
    update_change();
}

// Stampa
last_order=0;
function print() {
    window.location.href='/print/'+last_order+'/';
}

// Salvataggio
function save() {
    $('#send').prop('disabled', 'disabled');
    if (done==1) {
        print();
    } else {
        info={}
        if ($('#items > ul > li').length) {
            $('#items > ul > li').each(function() {
                id=$(this).prop('id');
                parts=id.split('-');
                if (parts[0]=='offer') {
                    offer=parts[1];
                    uid=parts[2];
                    quantity=$('#items > ul > li#'+id+' > span.quantity').text();
                    $(this).find('div.offer-products > span').each(function() {
                        product=$(this).prop('id').split('-')[3];
                        info['offer-'+offer+'-'+uid+'-'+product]=quantity;
                    });
                } else {
                    quantity=$('#items > ul > li#'+id+' > span.quantity').text()
                    info[id]=quantity;
                }
            });
            if ($('#contributors').length) contributor=$('#contributors').val();
            else contributor=0;
            payment_method='C';
            if (contributor==0) {
                url='./'+payment_method+'/save/';
            } else {
                url='./'+payment_method+'/'+contributor+'/save/';
            }
            $.post(url, info)
            .done(function(response) {
                if (contributor!=0) {
                    onceaday=$('#contributors option[value=\''+contributor+'\']').prop('class').split('-')[1];
                    if (onceaday=='True') $('#contributors option[value=\''+contributor+'\']').remove();
                }
                done=1;
                last_order=response;
                $('#topseller > button').css('display', 'none');
                $('#items * button').prop('disabled', 'disabled');
                $('#buttons > button[id^=button-]').css('display', 'none');
                $('#numbersright').css('visibility', 'hidden');
                $('[id^=category-]').css('display', 'none');
                $('#waiting').css('display', 'inline');
                print();
            })
            .fail(function(response) {
                alert(response.responseText);
            });
        }
    }
    $('#send').removeAttr('disabled');
}
function compare(arr1, arr2) {
    return $(arr1).not(arr2).length == 0 && $(arr2).not(arr1).length == 0
}

// Inizializzazione
$(document).ready(function() {
    /* Setup categories */
    $('#buttons').children().css('width', 100/$('#buttons').children().size()+'%');

    $('#buttons > button[id^=button-]').click(function() {
        id=$(this).prop('id').split('-')[1];
        $('#tabs').children().css('display', 'none');
        $('#category-'+id).css('display', 'inline');
    });

    /* Setup button table */
    $('#tabs').children().css('display', 'none');
    $('#tabs').children().first().css('display', 'inline');

    /* Setup autoresize */
    autoresize('#tabs', '#tabs > div', 2, true);

    $('#contributors').change(function() {
        val=$('#contributors').val();
        if (val!=0) {
            selected=$('#contributors > option[value=\''+val+'\']');
            attrs=selected.prop('class').split('-');
            coupon=str2float(attrs[2]);
        } else {
            coupon=0;
        }
        if (attrs[1]=='True') reusable=false;
        else reusable=true;
        adjust_total(total_without_coupon);
    });

    /* Setup numbers events */
    $('#numbersleft > button[id^=number-]').click(function() {number_pressed($(this).text());});
    $('#numbersleft > button#operator-del').click(function() {delete_pressed();});
    $('#numbersleft > button#symbol-comma').click(function() {comma_dot_or_sign();});
    $(document).keydown(function(event){
        if (!event.ctrlKey && !event.altKey && !event.metaKey && !event.shiftKey) {
            if ((48 <= event.which) && (event.which <= 57)) {
                event.preventDefault();
                number_pressed((event.which-48).toString());
            } else if (event.which==8) {
                event.preventDefault();
                delete_pressed();
            } else if ((event.which==188) || (event.which==190)) {
                item=$('#items > ul > li > div.editor:visible')
                if (!item.length) {
                    event.preventDefault();
                    comma_dot_pressed();
                }
            } else if (event.which==109) {
                item=$('#items > ul > li > div.editor:visible')
                if (item.length) {
                    event.preventDefault();
                    minus_pressed();
                }
            } else if (event.which==61) {
                item=$('#items > ul > li > div.editor:visible')
                if (item.length) {
                    event.preventDefault();
                    plus_pressed();
                }
            } else if (event.which==38) {
                item=$('#items > ul > li > div.editor:visible')
                if (item.length) {
                    event.preventDefault();
                    id=item.parent().prop('id');
                    element=$('#tabs > div > button.product-'+id);
                    change_value(id, element, 1);
                }
            } else if (event.which==40) {
                item=$('#items > ul > li > div.editor:visible')
                if (item.length) {
                    event.preventDefault();
                    id=item.parent().prop('id');
                    element=$('#tabs > div > button.product-'+id);
                    change_value(id, element, -1);
                }
            } else if (event.which==46) {
                event.preventDefault();
                item=$('#items > ul > li > div.editor:visible')
                if (item.length) {
                    id=item.parent().prop('id');
                    element=$('#tabs > div > button.product-'+id);
                    reset_value(id, element);
                    item.remove();
                    if (!$('#items > ul > li').length) clean();
                } else {
                    clean();
                }
            } else if (event.which==13) {
                    event.preventDefault();
                    save();
            }
        }
    });
    $('input#price').click(function() {
        $('#items > ul > li > div.editor').css('display', 'none');
        $('#numbersleft > button#symbol-comma').text(',');
    });

    /* Setup buttons events */
    $('#tabs > div > button').click(function() {button_pressed($(this));});
    $('#topseller > button').click(function() {button_pressed($(this));});

    $('#numbersright > button').click(function() {
        id=$(this).prop('id').split('-')[2];
        element=$('#offer-'+id);
        id='pack-'+id
        if (!$('#items > ul > li#'+id).length) {
            product_list=[];
            element.find('div').each(function() {
                product_list.push('<span id="'+id+'-'+$(this).prop('id')+'">'+$(this).text()+'</span>');
            });
            $('#items > ul').append('<li id="'+id+'"><button class="edit">&gt;</button>&nbsp;&nbsp;&nbsp;<span class="quantity">0</span>x '+element.children('h3').text()+' = <span class="price">0,00</span> €<div class="offer-products" style="text-align: right; margin-right: 15px;">'+product_list.join(', ')+'</div><div class="editor" style="display: none;">Quantità: <input class="quantity" type="number" name="quantity" readonly="readonly" /\>&nbsp;&nbsp;&nbsp;<button class="add">+</button><button class="reduce">-</button><button class="delete">X</button></div></li>');
                item=$('#items > ul > li#'+id);
                item.find('button.edit').click(function() {
                    edit_item($(this));
                    // is it visible?
                });
                item.find('button.add').click(function() {change_value(id, element, 1);});
                item.find('button.reduce').click(function() {change_value(id, element, -1);});
                item.find('button.delete').click(function() {
                    reset_value(id, element);
                    item.remove();
                    if (!$('#items > ul > li').length) clean();
            });
            scrolltop();
        }
        change_value(id, element, 1);
    });

    $('#waiting > button').click(function(event) {
        url='../../change/'+last_order+'/payment_method/'+event.target.value+'/';
        event.target.style.backgroundColor='yellow';
        $.get(url, function(response) {
            $('#waiting > button').css('background-color', '');
            event.target.style.backgroundColor='lightblue';
        });
    });

    /* Setup send button */
    $('#send').click(function() {save();});

    /* Setup reset button */
    $('#reset').click(function() {new_ticket();});

    /* Clean */
    clean();
});
