index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body id="kt_body" class="" data-kt-scrolltop="on">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
# on body -> style="--kt-toolbar-height:55px;--kt-toolbar-height-tablet-and-mobile:55px"

external_stylesheets = ['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700',
                        'assets/plugins/global/plugins.bundle.css',
                        'assets/css/style.bundle.css',
                        'assets/css/custom/style.input.css'
                        ]
external_scripts = []
assets_ignore_str = '(css|js)'
template_name = '../metronic'