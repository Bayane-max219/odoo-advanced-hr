FROM odoo:17.0

COPY . /mnt/extra-addons/odoo_advanced_hr/

USER root
RUN pip3 install --no-cache-dir requests
USER odoo
