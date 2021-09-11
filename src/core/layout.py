index_string = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body id="kt_body" class="" style="--kt-toolbar-height:55px;--kt-toolbar-height-tablet-and-mobile:55px" data-kt-scrolltop="on">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <!--begin::Javascript-->
        <!--begin::Global Javascript Bundle(used by all pages)-->

        <!--end::Global Javascript Bundle-->
        <!--begin::Page Custom Javascript(used by this page)-->

        <!--end::Page Custom Javascript-->
        <!--end::Javascript-->
    </body>
</html>"""


external_stylesheets = ['https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700',
                        'assets/plugins/global/plugins.bundle.css',
                        'assets/css/style.bundle.css',
                        'assets/css/custom/style.input.css'
                        ]
external_scripts = None
assets_ignore_str = '(css|js)'
template_name = '../metronic'