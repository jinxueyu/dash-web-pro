import dash

from core import layout

app = dash.Dash(__name__,
                index_string=layout.index_string,
                assets_folder=layout.template_name+"/assets",
                assets_url_path="assets",
                assets_ignore=layout.assets_ignore_str,
                external_stylesheets=layout.external_stylesheets,
                external_scripts=layout.external_scripts,
                suppress_callback_exceptions=True,
                prevent_initial_callbacks=True)
server = app.server
