// TODO Add lang attribute to form fields, use lang attribute to query fields
function showLanguages(languages) {
    document.querySelectorAll('.form-row, .field-box').forEach(function(row) {
        var lang = [];
        row.classList.forEach(function(cls) {
            if (cls) {
                var l = cls.split('_').pop();
                if (l.length == 2 || l.length == 3) {
                    // TODO Quick fix; better use "lang" attribute
                    if (['id', 'url'].indexOf(l) == -1) {
                        lang.push(l);
                    }
                }
            }
        });
        if (lang.length) {
            var display = 'none';
            if (lang.filter(function(l) { return languages.includes(l); }).length > 0) {
                display = 'block'
            }
            row.style.display = display;
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
