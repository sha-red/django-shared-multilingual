
function showLanguages(languages) {
    // Query all input[type=text] and textarea elements which have
    // a lang attribute; hide all but those in the languages parameter

    document.querySelectorAll(
        'input[lang][type="text"]:not([lang=""]), textarea[lang]:not([lang=""])'
    ).forEach( function(widget) {
        var display = 'none';
        if ( languages.includes(widget.attributes['lang'].value) ) {
            display = 'block'
        }
        // Hide direct parent (.field-box) if there are multiple field per row,
        // hide the row if there is only field in it
        if ( widget.parentElement.classList.contains(".field-box") ) {
            widget.parentElement.style.display = display
        } else {
            widget.parentElement.parentElement.style.display = display
        }
    })

    localStorage.admin_languages = languages.join(' ')
    document.querySelectorAll('.language-select').forEach(function(a) {
        if (a.dataset.languages == localStorage.admin_languages) {
            a.classList.add('selected')
        } else {
            a.classList.remove('selected')
        }
    })
}

(function($) {
    $(document).ready(function() {
        $('.language-select').on({
            click: function() {
                showLanguages(this.dataset.languages.split(' '))
            }
        })
        var languages = $('.language-select.selected').data('languages')
        if (localStorage.admin_languages) {
            languages = localStorage.admin_languages
        }
        if (languages) {
            showLanguages(languages.split(' '))
        }
    })
})(django.jQuery);
