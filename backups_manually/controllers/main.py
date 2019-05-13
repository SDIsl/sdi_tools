import logging
import werkzeug
import datetime
import odoo
from odoo import http
from odoo.http import content_disposition, dispatch_rpc, request, \
    serialize_exception as _serialize_exception, Response

_logger = logging.getLogger(__name__)

from odoo import api, fields, models


class Main(http.Controller):
    
    @http.route('/web/binary/download_db', type='http', auth="user")
    def backup(self, name, backup_format, **kw):
        try:
            # name == nombre de la BBDD a descargar
            # backup_format == formato de compresion, por defecto zip
            
            ts = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
            filename = "%s_%s.%s" % (name, ts, backup_format)
            headers = [
                ('Content-Type', 'application/octet-stream; charset=binary'),
                ('Content-Disposition', content_disposition(filename)),
            ]
            dump_stream = odoo.service.db.dump_db(name, None, backup_format)
            response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
            return response
        except Exception as e:
            _logger.exception('Database.backup')
            error = "Database backup error: %s" % (str(e) or repr(e))
            return self._render_template(error=error)
